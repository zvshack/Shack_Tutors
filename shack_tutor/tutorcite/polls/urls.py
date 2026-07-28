from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("tutors/<int:tutor_id>/", views.tutor_detail, name="tutor_detail"),
    path("tutors/<int:tutor_id>/leave_review/", views.leave_review, name="leave_review"),
    path("contact/", views.contact, name="contact"),
]