from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("tutors/<int:tutor_id>/", views.tutor_detail, name="tutor_detail"),
]