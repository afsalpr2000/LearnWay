#Context_processors
from django.apps import apps

def user_profile(request):
    if request.user.is_authenticated:
        Profile = apps.get_model('adminpanel', 'Profile')
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = Profile.objects.create(user=request.user)
            print("Profile created in context processor for user:", request.user.username)
        return {'profile': profile}
    return {}
