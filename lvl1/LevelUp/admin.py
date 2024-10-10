from django.contrib import admin
from .models import Submission, LeaderboardEntry
admin.site.register(Submission)


from django.contrib import admin
from .models import MediaSubmission

@admin.register(MediaSubmission)
class MediaSubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'benchpress_kg', 'deadlift_kg', 'squats_kg', 'run_100m_seconds', 'vertical_jump_height_cm', 'kick_height_cm', 'run_5km_minutes', 'burpees_60sec', 'plank_minutes')
    
    
@admin.register(LeaderboardEntry)
class LeaderboardEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'level')
    search_fields = ('user__username',)
    list_filter = ('user',)
    
