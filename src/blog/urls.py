from django.urls import path

from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('blogs/', blogs, name='blogs'),
    path('category_blogs/<str:slug>/', category_blogs, name='category_blogs'),
    path('tag_blogs/<str:slug>/', tag_blogs, name='tag_blogs'),
    path('blog/<str:slug>/', blog_details, name='blog_details'),
    path('pending_blog/<str:slug>/', pending_blog_details, name='pending_blog_details'),
    path('pending_sell_post/<str:slug>/', pending_sell_posts_details, name='pending_sell_posts_details'),
    path('add_reply/<int:blog_id>/<int:comment_id>/', add_reply, name='add_reply'),
    path('like_blog/<int:pk>/', like_blog, name='like_blog'),
    path('search_blogs/', search_blogs, name='search_blogs'),
    path('search_buy_posts/', search_buy_posts, name='search_buy_posts'),
    path('my_blogs/', my_blogs, name='my_blogs'),
    path('my_sell_posts/', my_sell_posts, name='my_sell_posts'),
    path('add_blog/', add_blog, name='add_blog'),
    path('update_blog/<str:slug>/', update_blog, name='update_blog'),
    path('update_sell_post/<str:slug>/', update_sell_post, name='update_sell_post'),
    path('sell_post/', add_sell_post, name='sell_post'),
    path('buy_posts_list/', buy_posts_list, name='buy_posts_list'),
    path('buy_post/<str:slug>/', buy_post_details, name='buy_post_details'),
    path('category_buy_posts/<str:slug>/',category_buy_posts,name='category_buy_posts'),
    path('pending_blogs/',pending_blogs,name='pending_blogs'),
    path('pending_sell_posts/',pending_sell_posts,name='pending_sell_posts')
    
    
    # path('category_buy_posts/<str:slug>/', category_buy_posts, name='category_buy_posts'),
    # path('buy_post/<str:slug>/', buy_post_details, name='buy_post_details'),
]
