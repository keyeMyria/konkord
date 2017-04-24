# -*- coding: utf-8 -*-
import pdfkit.pdfkit


def _command(self, path=None):
    """
    Generator of all command parts
    """
    if self.css:
        self._prepend_css(self.css)

    # yield self.wkhtmltopdf
    from tempfile import NamedTemporaryFile
    tmp = NamedTemporaryFile(mode="w+b", suffix='.pdf')
    self.tmp_file = tmp
    yield 'xvfb-run /usr/bin/wkhtmltopdf - %s' % tmp.name

    for argpart in self._genargs(self.options):
        if argpart:
            yield argpart

    if self.cover and self.cover_first:
        yield 'cover'
        yield self.cover

    if self.toc:
        yield 'toc'
        for argpart in self._genargs(self.toc):
            if argpart:
                yield argpart

    if self.cover and not self.cover_first:
        yield 'cover'
        yield self.cover

    # If the source is a string then we will pipe it into wkhtmltopdf
    # If the source is file-like then we will read from it and pipe it in
    if self.source.isString() or self.source.isFileObj():
        yield '-'
    else:
        if isinstance(self.source.source, basestring):
            yield self.source.to_s()
        else:
            for s in self.source.source:
                yield s

    # If output_path evaluates to False append '-' to end of args
    # and wkhtmltopdf will pass generated PDF to stdout
    if path:
        yield path
    else:
        yield '-'


def to_pdf(self, path=None):
    import subprocess
    import sys
    args = self.command(path)

    result = subprocess.Popen(
        args, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, shell=True)

    # If the source is a string then we will pipe it into wkhtmltopdf.
    # If we want to add custom CSS to file then we read input file to
    # string and prepend css to it and then pass it to stdin.
    # This is a workaround for a bug in wkhtmltopdf (look closely in README)
    if self.source.isString() or (self.source.isFile() and self.css):
        input = self.source.to_s().encode('utf-8')
    elif self.source.isFileObj():
        input = self.source.source.read().encode('utf-8')
    else:
        input = None
    stdout, stderr = result.communicate(input=input)
    stderr = stderr or stdout
    if self.tmp_file is not None:
        read = self.tmp_file.read()
        self.tmp_file.close()
        return read
    try:
        stderr = stderr.decode('utf-8')
    except UnicodeDecodeError:
        stderr = ''
    exit_code = result.returncode

    if 'cannot connect to X server' in stderr:
        raise IOError('%s\n'
                      'You will need to run wkhtmltopdf within a "virtual" X server.\n'
                      'Go to the link below for more information\n'
                      'https://github.com/JazzCore/python-pdfkit/wiki/Using-wkhtmltopdf-without-X-server' % stderr)

    if 'Error' in stderr:
        raise IOError('wkhtmltopdf reported an error:\n' + stderr)

    if exit_code != 0:
        raise IOError(
            "wkhtmltopdf exited with non-zero code {0}. error:\n{1}".format(
                exit_code, stderr))

    # Since wkhtmltopdf sends its output to stderr we will capture it
    # and properly send to stdout
    if '--quiet' not in args:
        sys.stdout.write(stderr)

    if not path:
        return stdout
    else:
        try:
            with codecs.open(path, encoding='utf-8') as f:
                # read 4 bytes to get PDF signature '%PDF'
                text = f.read(4)
                if text == '':
                    raise IOError('Command failed: %s\n'
                                  'Check whhtmltopdf output without \'quiet\' '
                                  'option' % ' '.join(args))
                return True
        except IOError as e:
            raise IOError('Command failed: %s\n'
                          'Check whhtmltopdf output without \'quiet\' option\n'
                          '%s ' %(' '.join(args)), e)


pdfkit.pdfkit.PDFKit._command = _command
pdfkit.pdfkit.PDFKit.to_pdf = to_pdf
