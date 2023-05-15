from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, m2m_changed

from django.shortcuts import reverse
from django.utils.html import strip_tags

from .models import Blog, Comment, Reply
from user_profile.models import User
from notification.models import Notification


@receiver(post_save, sender=Comment)
def send_notification(sender, instance, *args, **kwargs):
    blog_owner = instance.blog.user
    if instance.user != blog_owner:
        verb = 'commented on'
        description = f'{strip_tags(instance.text)[:50]}...'
        #url = reverse('blog_detail', args=[instance.blog.id])

        notification = Notification(
            content_object = instance,
            user=blog_owner,
            notification_types="Comment",
            text=f'{instance.user.username} {verb} your blog: {description}',
            #target=instance.blog,
           # url=url
        )
        notification.save()


@receiver(post_save, sender=Reply)
def send_notification(sender, instance, *args, **kwargs):
    comment_owner = instance.comment.user
    if instance.user != comment_owner:
        verb = 'replied to'
        description = f'{strip_tags(instance.text)[:50]}...'
        #url = reverse('blog_detail', args=[instance.blog.id])

        notification = Notification(
            content_object = instance,
            user=comment_owner,
            notification_types="Blog",
            text=f'{instance.user.username} {verb} your comment: {description}',
            #target=instance.blog,
           # url=url
        )
        notification.save()

@receiver(m2m_changed, sender=Blog.likes.through)
def send_notification_when_someone_likes_blog(instance, pk_set, action, *args, **kwargs):
    pk = list(pk_set)[0]
    user = User.objects.get(pk=pk)

    if action == "post_add":
        Notification.objects.create(
            content_object=instance,
            user=instance.user,
            text=f"{user.username} liked your blog",
            notification_types="Like"
        )