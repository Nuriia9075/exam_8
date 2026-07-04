from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Author, Topic


class AuthorCreationForm(UserCreationForm):
    username = forms.CharField(label="Имя", required=True)

    class Meta(UserCreationForm.Meta):
        model = Author
        fields = ( 'username', 'email', 'avatar' )


class TopicForm(forms.ModelForm):
   class Meta:
       model = Topic
       fields =['title','description']
       widgets = {
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control','rows': 5}),
       }

#
# class SimpleSearchForm(forms.Form):
#     search = forms.CharField(max_length=100, required=False, label="")