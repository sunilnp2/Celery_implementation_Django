from django.urls import path 
app_name = 'blog'
from blog.views import *

urlpatterns = [
    path("", HomeView.as_view(), name='home' ),
    path('signup', signup, name='signup'),
    path('login', login, name='login'),
    path('add', add, name='add'),
    path('logout', logout, name='logout'),
    path('delete<int:pk>', del_blog, name = 'delete'),
    path('activate/<uidb64>/<token>', enumerate, name='activate'),
]
