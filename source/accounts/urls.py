from django.contrib.auth.views import LogoutView
from django.urls import path
# from .views.member import RegisterView, ProfileDetailView, login_view
from .views.topic import TopicListView, TopicCreateView

app_name = "account"

urlpatterns = [
    # path('login/',login_view, name='login'),
    path('', TopicListView.as_view(), name='index'),
    # path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    # path('register/', RegisterView.as_view(), name='register'),
    path('topics/create/', TopicCreateView.as_view(), name="create_topic"),
]