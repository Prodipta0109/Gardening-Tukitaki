from django.db import models
from django.utils.text import slugify

from user_profile.models import User
from .slugs import generate_unique_slug
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

class Sell_Post_Category(models.Model):
    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
# Create your models here.


class Sell_post(models.Model):
    user = models.ForeignKey(
        User,
        related_name='user_sellPost',
        on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        Sell_Post_Category,
        related_name='category_sellPost',
        on_delete=models.CASCADE
    )
    title = models.CharField(
        max_length=250
    )
    slug = models.SlugField(null=True, blank=True)
    banner = models.ImageField(upload_to='sellPost_banners')
    description = RichTextUploadingField()
    created_date = models.DateField(auto_now_add=True)

    #from Video here
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        updating = self.pk is not None
        
        if updating:
            self.slug = generate_unique_slug(self, self.title, update=True)
            super().save(*args, **kwargs)
        else:
            self.slug = generate_unique_slug(self, self.title)
            super().save(*args, **kwargs)