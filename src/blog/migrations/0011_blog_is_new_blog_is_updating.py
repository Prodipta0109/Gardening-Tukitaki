# Generated by Django 4.2 on 2023-05-14 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_alter_blog_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='is_new',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='blog',
            name='is_updating',
            field=models.BooleanField(default=False),
        ),
    ]
