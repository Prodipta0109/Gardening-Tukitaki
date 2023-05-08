from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.db.models import Q;
from django.http import JsonResponse
from django.contrib import messages
from django.utils.text import slugify
from user_profile.models import User


from .models import(
    Sell_Post_Category,
    Sell_post
)


# @login_required(login_url='login')
# def add_sell_post(request):
#     form = AddBlogForm()

#     if request.method == "POST":
#         form = AddBlogForm(request.POST, request.FILES)
#         if form.is_valid():
#             tags = request.POST['tags'].split(',')
#             user = get_object_or_404(User, pk=request.user.pk)
#             category = get_object_or_404(Category, pk=request.POST['category'])
#             blog = form.save(commit=False)
#             blog.user = user
#             blog.category = category
#             blog.save()

#             for tag in tags:
#                 tag_input = Tag.objects.filter(
#                     title__iexact=tag.strip(),
#                     slug= slugify(tag.strip())
#                 )
#                 if tag_input.exists():
#                     t = tag_input.first()
#                     blog.tags.add(t)

#                 else:
#                     if tag != '':
#                         new_tag = Tag.objects.create(
#                             title=tag.strip(),
#                             slug=slugify(tag.strip())
#                         )
#                         blog.tags.add(new_tag)

#             messages.success(request, "Blog added successfully")
#             return redirect('blog_details', slug=blog.slug)
#         else:
#             print(form.errors)

#     context = {
#         "form": form
#     }
#     return render(request, 'add_blog.html',context)
# Create your views here.

@login_required(login_url='login')
def sell_post(request):
    return render(request,'sell_post.html')