from django import forms
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Article

class ArticleForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = reverse_lazy('articles:home')
        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = Article
        fields = ['name', 'description', 'content', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class':'mt-3 mb-3'}),
            'description': forms.TextInput(attrs={'class':'mt-3 mb-3'}),
            'content': forms.Textarea(attrs={'class':'mt-3 mb-3'}),
            'category': forms.RadioSelect()
        }
