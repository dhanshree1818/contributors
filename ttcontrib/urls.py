from django.contrib import admin
from django.urls import path, include

from ttcontrib.views import MyIndex, MyView
from . import views

urlpatterns = [
    path('', MyIndex.as_view()),
    path('contributors/', MyView.as_view(), name="MyView"),
]
