"""blog_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib import admin
from django.conf import  settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('', include('user_profile.urls')),
    path('', include('gardening_calculator.urls')),
#    path('', home, name='home'),
#     path('blogs/', blogs, name='blogs'),
#     path('category_blogs/<str:slug>/', category_blogs, name='category_blogs'),
#     path('tag_blogs/<str:slug>/', tag_blogs, name='tag_blogs'),
#     path('blog/<str:slug>/', blog_details, name='blog_details'),
#     path('add_reply/<int:blog_id>/<int:comment_id>/', add_reply, name='add_reply'),
#     path('like_blog/<int:pk>/', like_blog, name='like_blog'),
#     path('search_blogs/', search_blogs, name='search_blogs'),
#     path('my_blogs/', my_blogs, name='my_blogs'),
#     path('add_blog/', add_blog, name='add_blog'),
#     path('update_blog/<str:slug>/', update_blog, name='update_blog'),
]

urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)