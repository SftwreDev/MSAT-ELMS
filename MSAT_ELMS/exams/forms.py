from django import forms
from django.forms.widgets import RadioSelect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

class ExamForm(forms.Form):
    def __init__(self, question, *args, **kwargs):
        super(ExamForm, self).__init__(*args, **kwargs)
        choice_list = [x for x in question.get_answers_list()]
        self.fields["answers"] = forms.ChoiceField(choices=choice_list, widget=RadioSelect)




class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
