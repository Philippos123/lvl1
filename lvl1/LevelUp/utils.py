from .models import UserStatsStrength, UserStatsAgility, UserStatsStamina

def get_user_overall_level(user):
    try:
        strength_stats = UserStatsStrength.objects.get(user=user)
        agility_stats = UserStatsAgility.objects.get(user=user)
        stamina_stats = UserStatsStamina.objects.get(user=user)
        
        strength_level = strength_stats.overall_level_strength()
        agility_level = agility_stats.overall_level_agility()
        stamina_level = stamina_stats.overall_level_stamina()
        
        overall_level = (strength_level + agility_level + stamina_level) / 3
        return overall_level
    
    except (UserStatsStrength.DoesNotExist, UserStatsAgility.DoesNotExist, UserStatsStamina.DoesNotExist):
        # Handle the case where the user stats are not found
        return None
    
