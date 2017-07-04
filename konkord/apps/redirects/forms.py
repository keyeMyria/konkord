from django import forms
from django.utils.translation import ugettext_lazy as _
import xlrd
from django.contrib.sites.models import Site
from collections import defaultdict
from redirects.models import Redirect


class RedirectsImportForm(forms.Form):
    file = forms.FileField(label=_('File'))

    def clean_file(self):
        file_name = self.cleaned_data.get('file')
        file = self.files.get('file')
        if file.content_type not in (
            'application/vnd.ms-excel',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        ):
            raise forms.ValidationError(_('Wrong file type'))
        book = xlrd.open_workbook(file_contents=file.read())
        sheet = book.sheet_by_index(0)
        self.sheet = sheet
        from_redirects = defaultdict(lambda: 0)
        empty_rows = []
        for rownum in range(sheet.nrows):
            row = sheet.row_values(rownum)
            if not row[0] or not row[1]:
                empty_rows.append(str(rownum + 1))
            from_redirects[row[0]] += 1
        if empty_rows:
            raise forms.ValidationError(
                _('Old or new url not filled in lines: %s') % ', '.join(
                    empty_rows))
        error_urls = []
        for redirect_url, redirect_count in from_redirects.items():
            if redirect_count > 1:
                error_urls.append(redirect_url)
        if error_urls:
            raise forms.ValidationError(
                _('Duplicated old urls: %s') % ', '.join(error_urls))

        exists_redirects = Redirect.objects.filter(
            old_path__in=from_redirects.keys()
        ).values_list('old_path', flat=True)
        if exists_redirects:
            raise forms.ValidationError(
                _('Some of redirects already exists: %s') % ', '.join(
                    exists_redirects)
            )
        return file_name

    def save(self):
        sheet = self.sheet
        site = Site.objects.get_current()
        redirects = []
        for rownum in range(sheet.nrows):
            row = sheet.row_values(rownum)
            redirects.append(Redirect(site=site, old_path=row[0], new_path=row[1]))
        Redirect.objects.bulk_create(redirects)
