from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class UserStatsStrength(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bench = models.PositiveIntegerField(default=0)
    mark = models.PositiveIntegerField(default=0)
    squats = models.PositiveIntegerField(default=0)
    
    @staticmethod
    def calculate_level(weight, min_weight, max_weight, min_level=1, max_level=100):
        if weight == 0:
            return 0
        
        if weight < min_weight:
            weight = min_weight
        elif weight > max_weight:
            weight = max_weight

        level = ((weight - min_weight) / (max_weight - min_weight)) * (max_level - min_level) + min_level
        return round(level)

    @property
    def bench_level(self):
        return self.calculate_level(self.bench, min_weight=10, max_weight=240)
    
    @property
    def mark_level(self):
        return self.calculate_level(self.mark, min_weight=10, max_weight=320)
    
    @property
    def squats_level(self):
        return self.calculate_level(self.squats, min_weight=10, max_weight=280)

    def overall_level_strength(self):
        total_level = self.bench_level + self.mark_level + self.squats_level
        return total_level / 3

    def __str__(self):
        return f"{self.user.username} - Stats"
    
    
class UserStatsAgility(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    speed = models.PositiveIntegerField(default=0)
    jump = models.PositiveIntegerField(default=0)
    kick_height = models.PositiveIntegerField(default=0)
    
    @staticmethod
    def calculate_level_agility(value, min_value, max_value, min_level=1, max_level=100, inverse=False):
        if value == 0:
            return 0
        
        if inverse:
            # For time-based metrics, lower values are better, so invert the calculation
            if value < min_value:
                value = min_value
            elif value > max_value:
                value = max_value
            
            level = ((max_value - value) / (max_value - min_value)) * (max_level - min_level) + min_level
        else:
            if value < min_value:
                value = min_value
            elif value > max_value:
                value = max_value
            
            level = ((value - min_value) / (max_value - min_value)) * (max_level - min_level) + min_level
        
        return round(level)

    @property
    def speed_level(self):
        # Inverse=True because lower time is better
        return self.calculate_level_agility(self.speed, min_value=5, max_value=20, inverse=True)
    
    @property
    def jump_level(self):
        # Higher is better for jump, so inverse=False
        return self.calculate_level_agility(self.jump, min_value=50, max_value=200)
    
    @property
    def kick_height_level(self):
        # Higher is better for kick height, so inverse=False
        return self.calculate_level_agility(self.kick_height, min_value=50, max_value=250)

    def overall_level_agility(self):
        total_level = self.speed_level + self.jump_level + self.kick_height_level
        return total_level / 3

    def __str__(self):
        return f"{self.user.username} - Agility Stats"


class UserStatsStamina(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    run = models.PositiveIntegerField(default=0)  # Time in minutes for 5km run
    burpees = models.PositiveIntegerField(default=0)  # Number of burpees in 5 minutes
    plank = models.PositiveIntegerField(default=0)  # Time in seconds for plank hold

    @staticmethod
    def calculate_level(value, min_value, max_value, min_level=1, max_level=100, inverse=False):
        if value == 0:
            return 0
        if inverse:
            # For time-based metrics, lower values are better, so invert the calculation
            if value < min_value:
                value = min_value
            elif value > max_value:
                value = max_value
            
            level = ((max_value - value) / (max_value - min_value)) * (max_level - min_level) + min_level
        else:
            if value < min_value:
                value = min_value
            elif value > max_value:
                value = max_value
            
            level = ((value - min_value) / (max_value - min_value)) * (max_level - min_level) + min_level
        
        return round(level)

    @property
    def run_level(self):
        # Inverse=True because lower time is better for the run
        return self.calculate_level(self.run, min_value=15, max_value=60, inverse=True)
    
    @property
    def burpees_level(self):
        # Higher is better for burpees, so inverse=False
        return self.calculate_level(self.burpees, min_value=10, max_value=40)
    
    @property
    def plank_level(self):
        # Higher is better for plank time, so inverse=False
        return self.calculate_level(self.plank, min_value=1, max_value=30)

    def overall_level_stamina(self):
        total_level = self.run_level + self.burpees_level + self.plank_level
        return total_level / 3

    def __str__(self):
        return f"{self.user.username} - Stamina Stats"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True,)

    def __str__(self):
        return self.user.username
    
class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='submissions/images/', blank=True, null=True)
    video = models.FileField(upload_to='submissions/videos/', blank=True, null=True)
    submission_date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)  # New field to track approval

    def __str__(self):
        return f"Submission by {self.user.username} on {self.submission_date}"
    
    
    

class MediaSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='media_submissions', null=True, blank=True)
    # Measurements with default value 0
    benchpress_kg = models.IntegerField(default=0)
    deadlift_kg = models.IntegerField(default=0)
    squats_kg = models.IntegerField(default=0)
    run_100m_seconds = models.IntegerField(default=0)
    vertical_jump_height_cm = models.IntegerField(default=0)
    kick_height_cm = models.IntegerField(default=0)
    run_5km_minutes = models.IntegerField(default=0)
    burpees_60sec = models.IntegerField(default=0)
    plank_minutes = models.IntegerField(default=0)

    # Media uploads (optional)
    benchpress_media = models.FileField(upload_to='media/benchpress/', null=False, blank=True)
    deadlift_media = models.FileField(upload_to='media/deadlift/', null=True, blank=True)
    squats_media = models.FileField(upload_to='media/squats/', null=True, blank=True)
    run_100m_media = models.FileField(upload_to='media/run_100m/', null=True, blank=True)
    vertical_jump_media = models.FileField(upload_to='media/vertical_jump/', null=True, blank=True)
    kick_media = models.FileField(upload_to='media/kick/', null=True, blank=True)
    run_5km_media = models.FileField(upload_to='media/run_5km/', null=True, blank=True)
    burpees_media = models.FileField(upload_to='media/burpees/', null=True, blank=True)
    plank_media = models.FileField(upload_to='media/plank/', null=True, blank=True)
    
class LeaderboardEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.IntegerField(default=0)  # Or use a different type based on your requirements

    def __str__(self):
        return f"{self.user.username} - Level: {self.level}"
    
