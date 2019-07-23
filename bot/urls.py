from django.urls import path

from bot import views

app_name = 'bot'

urlpatterns = [
    path('api/answer/', views.answer, name='answer'),
]
