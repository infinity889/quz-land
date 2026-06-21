from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.index, name='index'),
    path('question/', views.question_view, name='question'),
    path('result/', views.result_view, name='result'),
]
