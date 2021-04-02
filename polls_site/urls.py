from django.urls import path

from . import views

app_name= 'polls_site'
urlpatterns = [
    # это /polls/
    path('', views.index, name='index'),
    # voting details on 6th question /polls/6/
    path('specifics/<int:question_id>/', views.detail, name='detail'),
    # results on 6th question /polls/6/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # voting on 6th question /polls/6/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
    # login page
    path('login', views.log_in, name="login"),
    # logout page
    path('logout', views.log_out, name="logout"),
    # account creation page
    path('signup', views.sign_up, name="signup"),
]