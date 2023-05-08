from django import forms

from .models import Blog

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class TextForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, required=True)


class AddBlogForm(forms.ModelForm):
    description = RichTextUploadingField()
    
    class Meta:
        model = Blog
        fields = (
            "title",
            "category",
            "banner",
            "description"
        ) 