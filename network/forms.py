from django import forms

from .models import Post


class NewPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewPostForm, self).__init__(*args, **kwargs)
        self.fields['post'].widget.attrs = {'class': 'form-control'}
        self.fields['post'].label = ''
        
    class Meta:
        model = Post
        fields = ["post"]