# Generated by Django 4.2 on 2023-05-15 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_blog_is_new_blog_is_updating'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sell_post',
            options={'ordering': ['-created_date']},
        ),
        migrations.AddField(
            model_name='sell_post',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='sell_post',
            name='is_featured',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='sell_post',
            name='is_new',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='sell_post',
            name='is_updating',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='sell_post',
            name='number',
            field=models.CharField(default='Not Given', max_length=11),
        ),
    ]
