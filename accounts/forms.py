from django.contrib.auth.forms import UserCreationForm

from accounts.models import User
from typing import Any


class SignInForm(UserCreationForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Enter Username'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Enter Email'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Enter Password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Repeat Password'})
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']