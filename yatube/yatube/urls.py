from django.contrib import admin
from django.urls import include, path

"""yatube URL Configuration"""

urlpatterns = [
    path('', include('posts.urls', namespace='posts')),
    path('auth/', include('users.urls', namespace='users')),
    path('about/', include('about.urls', namespace='about')),
    path('auth/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
]
