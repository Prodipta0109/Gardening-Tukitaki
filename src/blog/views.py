from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.db.models import Q;
from django.http import JsonResponse
from django.contrib import messages
from django.utils.text import slugify
from user_profile.models import User
from django.db.models import Count



from .models import (
    Blog,
    Tag,
    Category,
    Comment,
    Reply,
    Sell_post,
    Sell_Post_Category
)

from .forms import TextForm, AddBlogForm, AddSellPostForm
# Create your views here.


def home(request):
    blogs = Blog.objects.filter(is_approved=True).order_by('-created_date')
    tags = Tag.objects.filter(is_approved=True).order_by('-created_date')
    featured_blogs = Blog.objects.filter(is_featured=True, is_approved=True).order_by('-created_date')
    popular_blogs = Blog.objects.annotate(num_likes=Count('likes')).order_by('-num_likes','-created_date')

    context = {
        "blogs": blogs,
        "featured_blogs" : featured_blogs,
        "tags" : tags,
        "popular_blogs" : popular_blogs
        
    }
    return render(request, 'home.html', context)

def blogs(request):
    blogs = Blog.objects.filter(is_approved=True).order_by('-created_date')
    queryset = Blog.objects.filter(is_approved=True).order_by('-created_date')
    tags = Tag.objects.filter(is_approved=True).order_by('-created_date')
    page = request.GET.get('page', 1)
    paginator = Paginator(blogs, 4)
    featured_blogs = Blog.objects.filter(is_featured=True).order_by('-created_date')
    popular_blogs = Blog.objects.annotate(num_likes=Count('likes')).order_by('-num_likes','-created_date')
    
    try:
        blogs = paginator.page(page)
    except EmptyPage:
        blogs = paginator.page(1)
    except PageNotAnInteger:
        blogs = paginator.page(1)
        return redirect('blogs')
    
    context = {
        "blogs": blogs,
        "tags": tags,
        "paginator": paginator,
        "queryset" : queryset,
        "featured_blogs" : featured_blogs,
        "popular_blogs" : popular_blogs
    }
    return render(request, 'blogs.html', context)

def category_blogs(request, slug):
    category = get_object_or_404(Category, slug=slug)
    blogs = category.category_blogs.all().filter(is_approved=True)
    tags = Tag.objects.filter(is_approved=True).order_by('-created_date')[:5]
    page = request.GET.get('page', 1)
    paginator = Paginator(blogs, 2)
    all_blogs = Blog.objects.filter(is_approved=True).order_by('-created_date')[:5]
    
    try:
        blogs = paginator.page(page)
    except EmptyPage:
        blogs = paginator.page(1)
    except PageNotAnInteger:
        blogs = paginator.page(1)
        return redirect('blogs')

    context = {
        "blogs": blogs,
        "tags": tags,
        "all_blogs": all_blogs
        
    }
    return render(request, 'category_blogs.html', context)


def tag_blogs(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    queryset = tag.tag_blogs.all().filter(is_approved=True)
    tags = Tag.objects.filter(is_approved=True).order_by('-created_date')[:5]
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 2)
    all_blogs = Blog.objects.filter(is_approved=True).order_by('-created_date')[:5]
    
    try:
        blogs = paginator.page(page)
    except EmptyPage:
        blogs = paginator.page(1)
    except PageNotAnInteger:
        blogs = paginator.page(1)
        return redirect('blogs')

    context = {
        "blogs": blogs,
        "tags": tags,
        "all_blogs": all_blogs
    }
    return render(request, 'category_blogs.html', context)

def blog_details(request, slug):
    form = TextForm()
    blog = get_object_or_404(Blog, slug=slug)
    category = Category.objects.get(id=blog.category.id)
    related_blogs = category.category_blogs.all().filter(is_approved=True)
    tags = Tag.objects.order_by('-created_date')[:5]
    # liked_by = request.user in blog.likes.all()

    if request.method == "POST" and request.user.is_authenticated:
        form = TextForm(request.POST)
        if form.is_valid():
            Comment.objects.create(
                user=request.user,
                blog=blog,
                text=form.cleaned_data.get('text')
            )
            return redirect('blog_details', slug=slug)

    context = {
        "blog": blog,
        "related_blogs": related_blogs,
        "tags": tags,
        "form": form,
        # "liked_by": liked_by
    }
    return render(request, 'blog_details.html', context)

def pending_blog_details(request, slug):
    form = TextForm()
    blog = get_object_or_404(Blog, slug=slug)
    category = Category.objects.get(id=blog.category.id)
    related_blogs = category.category_blogs.all().filter(is_approved=True)
    tags = Tag.objects.filter(is_approved=True).order_by('-created_date')[:5]
    # liked_by = request.user in blog.likes.all()

    if request.method == "POST" and request.user.is_authenticated:
        form = TextForm(request.POST)
        if form.is_valid():
            Comment.objects.create(
                user=request.user,
                blog=blog,
                text=form.cleaned_data.get('text')
            )
            return redirect('pending_blog_details', slug=slug)

    context = {
        "blog": blog,
        "related_blogs": related_blogs,
        "tags": tags,
        "form": form,
        # "liked_by": liked_by
    }
    return render(request, 'pending_blog_details.html', context)

@login_required(login_url='login')
def add_reply(request, blog_id, comment_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == "POST":
        form = TextForm(request.POST)
        if form.is_valid():
            comment = get_object_or_404(Comment, id=comment_id)
            Reply.objects.create(
                user=request.user,
                comment=comment,
                text=form.cleaned_data.get('text')
            )
    return redirect('blog_details', slug=blog.slug)


@login_required(login_url='login')
def my_blogs(request):
    queryset = request.user.user_blogs.all().filter(is_approved=True)
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 6)
    delete = request.GET.get('delete', None)

    if delete:
        blog = get_object_or_404(Blog, pk=delete)
        
        if request.user.pk != blog.user.pk:
            return redirect('home')

        blog.delete()
        messages.success(request, "Your blog has been deleted!")
        return redirect('my_blogs')

    try:
        blogs = paginator.page(page)
    except EmptyPage:
        blogs = paginator.page(1)
    except PageNotAnInteger:
        blogs = paginator.page(1)
        return redirect('blogs')

    context = {
        "blogs": blogs,
        "paginator": paginator
    }
    
    return render(request, 'my_blogs.html', context)

@login_required(login_url='login')
def pending_blogs(request):
    queryset = request.user.user_blogs.all().filter(is_approved=False)
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 6)
    delete = request.GET.get('delete', None)

    if delete:
        blog = get_object_or_404(Blog, pk=delete)
        
        if request.user.pk != blog.user.pk:
            return redirect('home')

        blog.delete()
        messages.success(request, "Your blog has been deleted!")
        return redirect('pending_blogs')

    try:
        blogs = paginator.page(page)
    except EmptyPage:
        blogs = paginator.page(1)
    except PageNotAnInteger:
        blogs = paginator.page(1)
        return redirect('blogs')

    context = {
        "blogs": blogs,
        "paginator": paginator,
        "queryset" : queryset
    }
    
    return render(request, 'pending_blogs.html', context)

#to check branches
@login_required(login_url='login')
def like_blog(request, pk):
    context = {}
    blog = get_object_or_404(Blog, pk=pk)
    
    if request.user in blog.likes.all():
        blog.likes.remove(request.user)
        context['liked'] = False
        context['like_count'] = blog.likes.all().count()
        
    else:
        blog.likes.add(request.user)
        context['liked'] = True
        context['like_count'] = blog.likes.all().count()

    return JsonResponse(context, safe=False)

def search_blogs(request):
    search_key = request.GET.get('search', None)
    recent_blogs = Blog.objects.filter(is_approved=True).order_by('-created_date')
    tags = Tag.objects.filter(is_approved=True).order_by('-created_date')
    
    if search_key:
        blogs = Blog.objects.filter(
            Q(title__icontains=search_key, is_approved=True) |
            Q(category__title__icontains=search_key,is_approved=True) |
            Q(user__username__icontains=search_key,is_approved=True) |
            Q(tags__title__icontains=search_key,is_approved=True) 
        ).distinct()

        context = {
            "blogs": blogs,
            "recent_blogs": recent_blogs,
            "tags": tags,
            "search_key": search_key
        }

        return render(request, 'search.html', context)

    else:
        return redirect('home')
    
    
@login_required(login_url='login')
def add_blog(request):
    form = AddBlogForm()

    if request.method == "POST":
        form = AddBlogForm(request.POST, request.FILES)
        if form.is_valid():
            tags = request.POST['tags'].split(',')
            user = get_object_or_404(User, pk=request.user.pk)
            category = get_object_or_404(Category, pk=request.POST['category'])
            blog = form.save(commit=False)
            blog.user = user
            blog.category = category
            blog.is_new = True
            blog.save()

            for tag in tags:
                tag_input = Tag.objects.filter(
                    title__iexact=tag.strip(),
                    slug= slugify(tag.strip())
                )
                if tag_input.exists():
                    t = tag_input.first()
                    blog.tags.add(t)

                else:
                    if tag != '':
                        new_tag = Tag.objects.create(
                            title=tag.strip(),
                            slug=slugify(tag.strip())
                        )
                        blog.tags.add(new_tag)
                        
            messages.success(request, "Blog added successfully")
            return redirect('pending_blog_details', slug=blog.slug)
           
        else:
            print(form.errors)

    context = {
        "form": form
    }
    return render(request, 'add_blog.html',context)

@login_required(login_url='login')
def update_blog(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    form = AddBlogForm(instance=blog)

    if request.method == "POST":
        form = AddBlogForm(request.POST, request.FILES, instance=blog)
        
        if form.is_valid():
            
            if request.user.pk != blog.user.pk:
                return redirect('home')
            
            # if request.method == 'POST':
            #     newlist = list(Blog.values_list('tags', flat=True))
            #     tags = newlist
            tags = request.POST['tags'].split(',')
            user = get_object_or_404(User, pk=request.user.pk)
            category = get_object_or_404(Category, pk=request.POST['category'])
            blog = form.save(commit=False)
            blog.user = user
            blog.category = category
            if(blog.is_approved == False):
                blog.is_new = True
            else:
                blog.is_new = False
                
            blog.is_approved = False
            blog.is_featured = False
            blog.is_updating = True
            blog.save()

            for tag in tags:
                tag_input = Tag.objects.filter(
                    title__iexact=tag.strip(),
                    slug=slugify(tag.strip())
                )
                if tag_input.exists():
                    t = tag_input.first()
                    blog.tags.add(t)

                else:
                    if tag != '':
                        new_tag = Tag.objects.create(
                            title=tag.strip(),
                            slug=slugify(tag.strip())
                        )
                        blog.tags.add(new_tag)

            messages.success(request, "Blog updated successfully")
            return redirect('pending_blog_details', slug=blog.slug)
        else:
            print(form.errors)


    context = {
        "form": form,
        "blog": blog,
    }
    return render(request, 'update_blog.html', context)

@login_required(login_url='login')
def add_sell_post(request):  
    sell_form = AddSellPostForm()

    if request.method == "POST":
        sell_form = AddSellPostForm(request.POST, request.FILES)
        if sell_form.is_valid():
            user = get_object_or_404(User, pk=request.user.pk)
            category = get_object_or_404(Sell_Post_Category, pk=request.POST['category'])
            sellpost = sell_form.save(commit=False)
            sellpost.user = user
            sellpost.category = category
            sellpost.save()

            messages.success(request, "Sell post added successfully")
            return redirect('pending_sell_posts_details', slug=sellpost.slug)
        else:
            print(sell_form.errors)

    context = {
        "form": sell_form
    }
    return render(request, 'sell_post.html',context)

def buy_posts_list(request):
    blogs = Sell_post.objects.filter(is_approved=True).order_by('-created_date')
    # tags = Tag.objects.order_by('-created_date')
    page = request.GET.get('page', 1)
    paginator = Paginator(blogs, 4)
    
    try:
        blogs = paginator.page(page)
    except EmptyPage:
        blogs = paginator.page(1)
    except PageNotAnInteger:
        blogs = paginator.page(1)
        return redirect('buy_posts_list')
    
    context = {
        "blogs": blogs,
        # "tags": tags,
        "paginator": paginator
    }
    return render(request, 'buy_posts_list.html', context)


def category_buy_posts(request, slug):
    category = get_object_or_404(Sell_Post_Category, slug=slug)
    queryset = category.category_sell_post.all().filter(is_approved=True)
    # tags = Tag.objects.order_by('-created_date')[:5]
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 2)
    all_blogs = Sell_post.objects.filter(is_approved=True).order_by('-created_date')[:5]
    
    try:
        blogs = paginator.page(page)
    except EmptyPage:
        blogs = paginator.page(1)
    except PageNotAnInteger:
        blogs = paginator.page(1)
        return redirect('buy_posts_list')

    context = {
        "blogs": blogs,
        # "tags": tags,
        "all_blogs": all_blogs
    }
    return render(request, 'category_buy_posts.html', context)


def buy_post_details(request, slug):
    form = TextForm()
    blog = get_object_or_404(Sell_post, slug=slug)
    category = Sell_Post_Category.objects.get(id=blog.category.id)
    related_blogs = category.category_sell_post.filter(is_approved=True).all()
    # tags = Tag.objects.order_by('-created_date')[:5]
    # liked_by = request.user in blog.likes.all()

    # if request.method == "POST" and request.user.is_authenticated:
    #     form = TextForm(request.POST)
    #     if form.is_valid():
    #         Comment.objects.create(
    #             user=request.user,
    #             blog=blog,
    #             text=form.cleaned_data.get('text')
    #         )
    #         return redirect('blog_details', slug=slug)

    context = {
        "blog": blog,
        "related_blogs": related_blogs,
        # "tags": tags,
        "form": form,
        # "liked_by": liked_by
    }
    return render(request, 'buy_posts_details.html', context)

def pending_sell_posts_details(request, slug):
    form = TextForm()
    blog = get_object_or_404(Sell_post, slug=slug)
    category = Sell_Post_Category.objects.get(id=blog.category.id)
    related_blogs = category.category_sell_post.filter(is_approved=True).all()
    # tags = Tag.objects.order_by('-created_date')[:5]
    # liked_by = request.user in blog.likes.all()

    # if request.method == "POST" and request.user.is_authenticated:
    #     form = TextForm(request.POST)
    #     if form.is_valid():
    #         Comment.objects.create(
    #             user=request.user,
    #             blog=blog,
    #             text=form.cleaned_data.get('text')
    #         )
    #         return redirect('blog_details', slug=slug)

    context = {
        "blog": blog,
        "related_blogs": related_blogs,
        # "tags": tags,
        "form": form,
        # "liked_by": liked_by
    }
    return render(request, 'pending_sell_posts_details.html', context)

@login_required(login_url='login')
def my_sell_posts(request):
    blogs = request.user.user_sell_post.all().filter(is_approved=True)
    page = request.GET.get('page', 1)
    paginator = Paginator(blogs, 6)
    delete = request.GET.get('delete', None)

    if delete:
        blog = get_object_or_404(Sell_post, pk=delete)
        
        if request.user.pk != blog.user.pk:
            return redirect('home')

        blog.delete()
        messages.success(request, "Your blog has been deleted!")
        return redirect('my_sell_posts')

    try:
        blogs = paginator.page(page)
    except EmptyPage:
        blogs = paginator.page(1)
    except PageNotAnInteger:
        blogs = paginator.page(1)
        return redirect('buy_posts_list')

    context = {
        "blogs": blogs,
        "paginator": paginator
    }
    
    return render(request, 'my_sell_posts.html', context)

@login_required(login_url='login')
def pending_sell_posts(request):
    queryset = request.user.user_sell_post.all().filter(is_approved=False)
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 6)
    delete = request.GET.get('delete', None)

    if delete:
        blog = get_object_or_404(Sell_post, pk=delete)
        
        if request.user.pk != blog.user.pk:
            return redirect('home')

        blog.delete()
        messages.success(request, "Your blog has been deleted!")
        return redirect('pending_sell_posts')

    try:
        blogs = paginator.page(page)
    except EmptyPage:
        blogs = paginator.page(1)
    except PageNotAnInteger:
        blogs = paginator.page(1)
        return redirect('blogs')

    context = {
        "blogs": blogs,
        "paginator": paginator,
        "queryset" : queryset
    }
    
    return render(request, 'pending_sell_posts.html', context)


@login_required(login_url='login')
def update_sell_post(request, slug):
    blog = get_object_or_404(Sell_post, slug=slug)
    form = AddSellPostForm(instance=blog)

    if request.method == "POST":
        form = AddSellPostForm(request.POST, request.FILES, instance=blog)
        
        if form.is_valid():
            
            if request.user.pk != blog.user.pk:
                return redirect('home')

            user = get_object_or_404(User, pk=request.user.pk)
            category = get_object_or_404(Sell_Post_Category, pk=request.POST['category'])
            blog = form.save(commit=False)
            blog.user = user
            blog.category = category
            if(blog.is_approved == False):
                blog.is_new = True
            else:
                blog.is_new = False
                
            blog.is_approved = False
            blog.is_featured = False
            blog.is_updating = True
            blog.save()

            # for tag in tags:
            #     tag_input = Tag.objects.filter(
            #         title__iexact=tag.strip(),
            #         slug=slugify(tag.strip())
            #     )
            #     if tag_input.exists():
            #         t = tag_input.first()
            #         blog.tags.add(t)

            #     else:
            #         if tag != '':
            #             new_tag = Tag.objects.create(
            #                 title=tag.strip(),
            #                 slug=slugify(tag.strip())
            #             )
            #             blog.tags.add(new_tag)

            messages.success(request, "Sell post updated successfully")
            return redirect('buy_post_details', slug=blog.slug)
        else:
            print(form.errors)


    context = {
        "form": form,
        "blog": blog
    }
    return render(request, 'update_sell_post.html', context)

def search_buy_posts(request):
    search_key = request.GET.get('search', None)
    # recent_blogs = Blog.objects.order_by('-created_date')
    #tags = Tag.objects.filter(is_approved=True).order_by('-created_date')
    
    if search_key:
        blogs = Sell_post.objects.filter(
            Q(title__icontains=search_key, is_approved=True) |
            Q(category__title__icontains=search_key,is_approved=True) |
            Q(user__username__icontains=search_key,is_approved=True) 
        ).distinct()

        context = {
            "blogs": blogs,
            "search_key": search_key
        }

        return render(request, 'buy_post_search.html', context)

    else:
        return redirect('home')