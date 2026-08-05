from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from .models import Question, Choice, Tutor, Subject, Review
from django.core.mail import send_mail
from django.http import JsonResponse
from itertools import combinations
from collections import Counter
import resend
from django.conf import settings

def home(request):
    #Creates all sets, variables, and database lists
    sor_resp = None
    error = None


    categories = Subject.CATEGORIES
    subjects = Subject.objects.all()
    tutors = Tutor.objects.all()

    selected = []
    valid_combos = []
    
    if request.method == 'POST':
        # List of selected subject IDs
        selected = request.POST.getlist('subjects')
        
        #Send error message if no one is selected
        if not selected:
            error = "Please select at least one subject."

        else:
            tutor_matches = []
            selected_set = set(selected)
            #creates a set of subjects for tutors that teaches at least one of the selected subjects of the matching subjects
            for tutor in tutors:
                teaches = set(tutor.subjects.values_list("id", flat=True)) & selected_set
                if teaches:
                    tutor_matches.append({
                        "tutor": tutor,
                        "subjects": teaches
                    })
            
            #iterates through each tutor for all possible combinations of them (order doesn't matter) finding least possible amount of combos
            for r in range(1, len(tutor_matches) + 1):
                for combo in combinations(tutor_matches, r):

                    #creates blank set and merges set with each tutor or combo 
                    covered = set()

                    for tutor in combo:
                        covered |= tutor["subjects"]
                    
                    #if the covered set is completed add this combo of tutors to a list
                    if covered == selected_set:
                        valid_combos.append(combo)
                #if there was at least one tutor combo, stop combinations from increasing if not go to find more combinations of tutors
                if valid_combos:
                    break           
            #send a sorry response if no valid combos were found
            if not valid_combos:
                sor_resp = "Unfortunately, we currently have no tutors available for the selected subjects."
        
    return render(request,'home.html', {"valid_combos" : valid_combos, "categories": categories, "subjects": subjects, "tutors": tutors, "error": error, "sor_resp": sor_resp, "selected": selected})

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

        if tutor.email:
            # Send an email
            resend.api_key = settings.RESEND_API_KEY
            resend.Emails.send({
                "from": "onboarding@resend.dev",
                "to" : [tutor.email],
                "subject" : "Scheduling Request from " + name,
                "text" : (
                    'Hello, my name is ' + name + '.\n\n' + 
                    'I would like to schedule a time to call to talk about tutoruing. Here are any additional details: ' + message + 
                    '\n\nYou can reach me at: ' + email
                ),
            })
            messages.success(request, '🎉           Your message has been sent!           🎉')
            return redirect(request.POST.get("next", "home"))
    return redirect("home")
