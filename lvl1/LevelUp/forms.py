from django import forms
from .models import UserStatsStrength, UserStatsAgility, UserStatsStamina, UserProfile, Submission

class UserStatsStrengthForm(forms.ModelForm):
    bench_level = forms.IntegerField(required=False, label='Bench Press Level', widget=forms.HiddenInput())
    mark_level = forms.IntegerField(required=False, label='Mark Level', widget=forms.HiddenInput())
    squats_level = forms.IntegerField(required=False, label='Squats Level', widget=forms.HiddenInput())

    class Meta:
        model = UserStatsStrength
        fields = ['bench', 'mark', 'squats']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['bench_level'].initial = self.instance.bench_level
            self.fields['mark_level'].initial = self.instance.mark_level
            self.fields['squats_level'].initial = self.instance.squats_level

class UserStatsAgilityForm(forms.ModelForm):
    speed_level = forms.IntegerField(required=False, label='Speed Level', widget=forms.HiddenInput())
    jump_level = forms.IntegerField(required=False, label='Jump Level', widget=forms.HiddenInput())
    kick_height_level = forms.IntegerField(required=False, label='Kick Height Level', widget=forms.HiddenInput())

    class Meta:
        model = UserStatsAgility
        fields = ['speed', 'jump', 'kick_height']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            # Populate level fields with calculated values
            self.fields['speed_level'].initial = self.instance.speed_level
            self.fields['jump_level'].initial = self.instance.jump_level
            self.fields['kick_height_level'].initial = self.instance.kick_height_level
        
class UserStatsStaminaForm(forms.ModelForm):
    run_level = forms.IntegerField(required=False, label='Run Level', widget=forms.HiddenInput())
    burpees_level = forms.IntegerField(required=False, label='Burpees Level', widget=forms.HiddenInput())
    plank_level = forms.IntegerField(required=False, label='Plank Level', widget=forms.HiddenInput())

    class Meta:
        model = UserStatsStamina
        fields = ['run', 'burpees', 'plank']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            # Populate level fields with calculated values
            self.fields['run_level'].initial = self.instance.run_level
            self.fields['burpees_level'].initial = self.instance.burpees_level
            self.fields['plank_level'].initial = self.instance.plank_level
            
            
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture']
        
class SubmissionForm(forms.ModelForm):
    name = forms.CharField(max_length=100, label='Name')
    email = forms.EmailField(label='Email')
    message = forms.CharField(widget=forms.Textarea, label='Message')
    
    
class MultiMediaForm(forms.Form):
    # Measurements with initial value 0
    benchpress_kg = forms.IntegerField(label='Kg Benchpress', initial=0, required=False)
    deadlift_kg = forms.IntegerField(label='Kg Deadlift', initial=0, required=False)
    squats_kg = forms.IntegerField(label='Kg Squats', initial=0, required=False)
    run_100m_seconds = forms.IntegerField(label='Seconds 100 meter', initial=0, required=False)
    vertical_jump_height_cm = forms.IntegerField(label='Vertical Jump Height', initial=0, required=False)
    kick_height_cm = forms.IntegerField(label='Kick Height', initial=0, required=False)
    run_5km_minutes = forms.IntegerField(label='5 km Run', initial=0, required=False)
    burpees_60sec = forms.IntegerField(label='Burpees 60 sec', initial=0, required=False)
    plank_minutes = forms.IntegerField(label='Plank Minutes', initial=0, required=False)

    # Media uploads
    benchpress_media = forms.FileField(label='Benchpress Media', required=False)
    deadlift_media = forms.FileField(label='Deadlift Media', required=False)
    squats_media = forms.FileField(label='Squats Media', required=False)
    run_100m_media = forms.FileField(label='100m Run Media', required=False)
    vertical_jump_media = forms.FileField(label='Vertical Jump Media', required=False)
    kick_media = forms.FileField(label='Kick Media', required=False)
    run_5km_media = forms.FileField(label='5km Run Media', required=False)
    burpees_media = forms.FileField(label='Burpees Media', required=False)
    plank_media = forms.FileField(label='Plank Media', required=False)