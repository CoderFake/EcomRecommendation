from accounts.models import UserProfile

def get_user_profile(user):
    if user.is_authenticated:
        profile, created = UserProfile.objects.get_or_create(user=user)
        if created:
            profile.save()
        return profile
    return None