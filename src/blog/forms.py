from django import forms

from .models import Blog,Sell_post

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
        
class AddSellPostForm(forms.ModelForm):
    description = RichTextUploadingField()
    
    class Meta:
        model = Sell_post
        fields = (
            "title",
            "category",
            "banner",
            "description",
            "number"
        ) 
        