from django import forms
import datetime
from django.core.exceptions import ValidationError

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Entre com uma data entre agora e 4 semanas (default 3).")

    def clean_renewal_date(self):

        data = self.cleaned_data['renewal_date']

        if data < datetime.date.today():
            raise ValidationError('Data inválida - renovação no passado.')

        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError('Data inválida - renovação com mais de 4 semanas.')

        return data