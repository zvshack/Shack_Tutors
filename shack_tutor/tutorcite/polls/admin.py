from django.contrib import admin
from .models import Question, Choice, Tutor, Subject

admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Tutor)
admin.site.register(Subject)
# Register your models here.
