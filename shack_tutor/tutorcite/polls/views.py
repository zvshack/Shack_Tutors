from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .models import Question, Choice, Tutor, Subject, Review

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

def leave_review(request, tutor_id):
    if request.method == 'POST':
        tutor = Tutor.objects.get(id=tutor_id)
        name = request.POST.get('name')
        comment = request.POST.get('comment')


        review = Review(name=name, tutor=tutor, comment=comment)
        review.save()
        messages.success(request, 'Thank you for submitting your review!')

    return redirect("tutor_detail", tutor_id=tutor_id)
