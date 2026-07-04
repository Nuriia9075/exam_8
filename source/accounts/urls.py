from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path
from .views.topic import TopicListView, TopicCreateView, TopicDetailView,AnswerDeleteView,AnswerUpdateView
from .views.account import RegisterView

app_name = "account"


urlpatterns = [
    path('login/', LoginView.as_view(template_name='account/login.html'), name='login'),
    path('', TopicListView.as_view(), name='index'),
    # path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('topics/create/', TopicCreateView.as_view(), name="create_topic"),
    path('topics/<int:pk>/', TopicDetailView.as_view(), name="topic_detail"),
    path('answers/<int:pk>/update/', AnswerUpdateView.as_view(), name='answer_update'),
    path('answers/<int:pk>/delete/', AnswerDeleteView.as_view(), name='answer_delete'),

]