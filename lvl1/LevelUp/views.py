from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UserStatsStrengthForm, UserStatsAgilityForm, UserStatsStaminaForm
from .models import UserStatsStrength, UserStatsAgility, UserStatsStamina
from .forms import UserProfileForm, MultiMediaForm
from .models import UserProfile
from .models import Submission, UserProfile, MediaSubmission, LeaderboardEntry
from .forms import SubmissionForm
from django.http import HttpResponse
from rest_framework import generics
from rest_framework.response import Response




def home(request):
    return render(request, "home.html")

def login(request):
    
    return render(request, "profile.html")

def view_stats(request):
    
    user_stats, created = UserStatsStrength.objects.get_or_create(user=request.user)
    return render(request, 'profile.html', {'user_stats': user_stats})

@login_required

def profile(request):
    
    user = request.user

    # Create default records if they don't exist
    strength_stats, _ = UserStatsStrength.objects.get_or_create(user=user)
    agility_stats, _ = UserStatsAgility.objects.get_or_create(user=user)
    stamina_stats, _ = UserStatsStamina.objects.get_or_create(user=user)
    
    # Calculate overall level if necessary
    overall_level = (strength_stats.overall_level_strength() + 
                     agility_stats.overall_level_agility() + 
                     stamina_stats.overall_level_stamina()) / 3

    return render(request, 'profile.html', {
        'strength_stats': strength_stats,
        'agility_stats': agility_stats,
        'stamina_stats': stamina_stats,
        'overall_level': overall_level,
    })

@login_required
def edit_stats_strength(request):
    print("Hello world! This works fine3!")
    user = request.user
    
    if request.method == 'POST':
        form = UserStatsStrengthForm(request.POST, instance=get_object_or_404(UserStatsStrength, user=user))
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserStatsStrengthForm(instance=get_object_or_404(UserStatsStrength, user=user))
    
    return render(request, 'edit_stats_strength.html', {'form': form})

@login_required
def edit_stats_agility(request):
    print("Hello world! This works fine2!")  # Debugging line
    user = request.user
    
    if request.method == 'POST':
        form = UserStatsAgilityForm(request.POST, instance=get_object_or_404(UserStatsAgility, user=user))
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserStatsAgilityForm(instance=get_object_or_404(UserStatsAgility, user=user))
    
    return render(request, 'edit_stats_agility.html', {'form': form})


@login_required
def edit_stats_stamina(request):
    print("Hello world! Is it you1!")  # Debugging line
    user = request.user
    
    if request.method == 'POST':
        form = UserStatsStaminaForm(request.POST, instance=get_object_or_404(UserStatsStamina, user=user))
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserStatsStaminaForm(instance=get_object_or_404(UserStatsStamina, user=user))
    
    return render(request, 'edit_stats_stamina.html', {'form': form})

def get_rank(overall_level):
    print(f"get_rank called with overall_level: {overall_level}")
    
    if overall_level >= 90:
        rank = 'S'
    elif overall_level >= 80:
        rank = 'A'
    elif overall_level >= 70:
        rank = 'B'
    elif overall_level >= 55:
        rank = 'C'
    elif overall_level >= 40:
        rank = 'D'
    elif overall_level >= 20:
        rank = 'E'
    else:
        rank = 'F'
        
    print(f"Determined rank: {rank}")
    return rank
    
@login_required
def profile(request):
    print("profile_view function started")
    
    user = request.user
    print(f"User: {user}")

    # Create default records if they don't exist
    strength_stats, _ = UserStatsStrength.objects.get_or_create(user=user)
    agility_stats, _ = UserStatsAgility.objects.get_or_create(user=user)
    stamina_stats, _ = UserStatsStamina.objects.get_or_create(user=user)
    



    # Calculate overall level
    strength_level = strength_stats.overall_level_strength()
    agility_level = agility_stats.overall_level_agility()
    stamina_level = stamina_stats.overall_level_stamina()



    overall_level = (strength_level + agility_level + stamina_level) / 3
    print(f"Calculated Overall Level: {overall_level}")

    # Determine rank and CSS class based on rank
    rank = get_rank(overall_level)


    pic_class = f'rank-{rank.lower()}'
    font_class = f'font-{rank.lower()}'
    header_class = f'header-{rank.lower()}'
    wing_class = f'wing-{rank.lower()}'
    

    
    context = {
        'strength_stats': strength_stats,
        'agility_stats': agility_stats,
        'stamina_stats': stamina_stats,
        'overall_level': overall_level,
        'rank': rank,
        'pic_class': pic_class,
        'font_class': font_class,
        'header_class': header_class,
        'wing_class': wing_class,
    }
    

    
    return render(request, 'profile.html', context)


@login_required
def update_profile_picture(request):
    # Ensure UserProfile exists for the user
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'update_profile_picture.html', {'form': form})

def Submission(request):
    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        
def submit_form(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # Process the data in form.cleaned_data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            # You can save this data to a database, send an email, etc.
            
            return HttpResponse('Thank you for your submission!')
    else:
        form = UserForm()
    
    return render(request, 'submit_form.html', {'form': form})

def submit_media_form(request):
    if request.method == 'POST':
        form = MultiMediaForm(request.POST, request.FILES)
        if form.is_valid():
            media_submission = MediaSubmission(
                user=request.user,
                benchpress_kg=form.cleaned_data.get('benchpress_kg', 0),
                deadlift_kg=form.cleaned_data.get('deadlift_kg', 0),
                squats_kg=form.cleaned_data.get('squats_kg', 0),
                run_100m_seconds=form.cleaned_data.get('run_100m_seconds', 0),
                vertical_jump_height_cm=form.cleaned_data.get('vertical_jump_height_cm', 0),
                kick_height_cm=form.cleaned_data.get('kick_height_cm', 0),
                run_5km_minutes=form.cleaned_data.get('run_5km_minutes', 0),
                burpees_60sec=form.cleaned_data.get('burpees_60sec', 0),
                plank_minutes=form.cleaned_data.get('plank_minutes', 0),

                benchpress_media=request.FILES.get('benchpress_media'),
                deadlift_media=request.FILES.get('deadlift_media'),
                squats_media=request.FILES.get('squats_media'),
                run_100m_media=request.FILES.get('run_100m_media'),
                vertical_jump_media=request.FILES.get('vertical_jump_media'),
                kick_media=request.FILES.get('kick_media'),
                run_5km_media=request.FILES.get('run_5km_media'),
                burpees_media=request.FILES.get('burpees_media'),
                plank_media=request.FILES.get('plank_media'),
            )
            media_submission.save()
            return redirect('profile')
    else:
        form = MultiMediaForm()
    
    return render(request, 'submit_media_form.html', {'form': form})



def leaderboard(request):
    # Fetch and order leaderboard entries by level
    leaderboard_entries = LeaderboardEntry.objects.order_by('-level')
    
    return render(request, 'leaderboard.html', {'leaderboard_entries': leaderboard_entries})

