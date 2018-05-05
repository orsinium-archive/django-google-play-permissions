# built-in
from urllib.parse import parse_qs

# django
from django import forms
from django.conf import settings
from django.utils.translation import ugettext, ugettext_lazy


class PermissionForm(forms.Form):
    url = forms.URLField(label=ugettext_lazy('Aplication URL'))

    def clean_url(self):
        """Extract from url dict of params and set default values.
        """
        url = self.cleaned_data['url']
        if '?' not in url:
            raise forms.ValidationError(ugettext('Invalid URL'))
        url = url.split('?', 1)[-1]
        data = dict(parse_qs(url))
        if 'id' not in data:
            raise forms.ValidationError(ugettext('URL must contain application ID'))
        else:
            data['id'] = data['id'][0]
        if 'hl' not in data:
            data['hl'] = settings.LANGUAGE_CODE
        else:
            data['hl'] = data['hl'][0]
        return data
