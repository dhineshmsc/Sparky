
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'groups']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['id'] = 'id_username'
        self.fields['email'].widget.attrs['id'] = 'id_email'
        self.fields['password1'].widget.attrs['id'] = 'id_password1'
        self.fields['password2'].widget.attrs['id'] = 'id_password2'
        self.fields['groups'].widget.attrs['id'] = 'id_groups'

