from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from .models import Question, Choice, Tutor, Subject, Review
from django.core.mail import send_mail

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
    reviews = tutor.reviews.filter(approved=True).order_by('-created_at')
    return render(request, 'detail.html', {'tutor': tutor, 'reviews': reviews})

def leave_review(request, tutor_id):
    if request.method == 'POST':
        tutor = Tutor.objects.get(id=tutor_id)
        name = request.POST.get('name')
        comment = request.POST.get('comment')        
        review_key = request.POST.get('review_key')
        if review_key != tutor.review_key:
            messages.error(request, 'Invalid review key. Please ask your tutor for their review key or try again.')
            return redirect("tutor_detail", tutor_id=tutor_id)

        review = Review(name=name, tutor=tutor, comment=comment)
        review.save()
        messages.success(request, '🎉           Thank you for submitting your review!           🎉')

    return redirect("tutor_detail", tutor_id=tutor_id)

def contact(request):
    if request.method == 'POST':
        tutor_id = request.POST.get('tutor')
        tutor = get_object_or_404(Tutor, id=tutor_id)

        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Send an email
        send_mail(
            'Scheduling Request from ' + name,
            (
                'Hello, my name is ' + name + '.\n\n' + 
                'I would like to schedule a time to call to talk about tutoruing. Here are any additional details: ' + message + 
                '\n\nYou can reach me at: ' + email
            ),
            None,  # From email (None uses the DEFAULT_FROM_EMAIL setting)
            [tutor.email],
        )
        messages.success(request, '🎉           Your message has been sent!           🎉')
    return redirect("home")
