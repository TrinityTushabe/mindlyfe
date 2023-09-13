from django.urls import path, include
from .views import InboxView, UserListsView, MessagesListView, signup
from django.contrib.auth import views as auth_views

from . import views
from .feeds import AtomSiteNewsFeed, LatestPostsFeed

app_name = 'chat'


urlpatterns = [
    path('signup/', signup, name='signup'),
    path('', MessagesListView.as_view(), name='message_list'),
    path('meet/', UserListsView.as_view(), name='users_list'),
    path('inbox/<str:username>/', InboxView.as_view(), name='inbox'),
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(next_page='chat:message_list'), name='logout'),
    path("feed/rss", LatestPostsFeed(), name="post_feed"),
    path("feed/atom", AtomSiteNewsFeed()),

     path("summernote/", include("django_summernote.urls")),
     path('editor/', include('django_summernote.urls')),
     

    path("blog/", views.PostList.as_view(), name="home"),
    # path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path("<slug:slug>/", views.post_detail, name="post_detail"),

]