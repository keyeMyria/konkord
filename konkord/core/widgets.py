from django.forms.widgets import ClearableFileInput


class ClearableImageInputWithThumb(ClearableFileInput):
    template_with_initial = (
        '%(initial_text)s: '
        '<a href="%(initial_url)s"><img width="100px" src="%(initial_url)s"></a> '
        '%(clear_template)s<br />%(input_text)s: %(input)s'
    )