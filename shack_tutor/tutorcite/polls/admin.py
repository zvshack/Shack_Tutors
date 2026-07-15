from django.contrib import admin
from .models import Question, Choice, Tutor, Subject, Review

admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Tutor)
admin.site.register(Subject)
admin.site.register(Review)
# Register your models here.
