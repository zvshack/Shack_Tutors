from django.shortcuts import render
from django.http import HttpResponse
from .models import Question, Choice, Tutor, Subject

def home(request):
    best_tutor = None
    categories = Subject.CATEGORIES
    subjects = Subject.objects.all()
    tutors = Tutor.objects.all()
    if request.method == 'POST':
        # List of selected subject IDs
        selected = request.POST.getlist('subjects')
        highest_score = -1

        for tutor in Tutor.objects.all():
            
            tutor_subjects = tutor.subjects.values_list('id', flat=True)

            score = len(set(selected) & set(tutor_subjects))
            if score > highest_score:
                highest_score = score
                best_tutor = tutor
    
    return render(request,'home.html', {"best_tutor": best_tutor, "categories": categories, "subjects": subjects, "tutors": tutors})

def tutor_detail(request, tutor_id):
    tutor = Tutor.objects.get(id=tutor_id)
    reviews = tutor.reviews.all()
    return render(request, 'detail.html', {'tutor': tutor, 'reviews': reviews})


