from django import forms
from pagedown.widgets import PagedownWidget
from taggit.forms import TagField

from .models import Post, Reply


class PostForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'size': 50}))
    content = forms.CharField(widget=forms.Textarea())
    tags = TagField(required=False)

    class Meta:
        model = Post
        fields = [
            "title",
            "tags",
            "category",
            "content",
            "public",
            "anonymous",
        ]
