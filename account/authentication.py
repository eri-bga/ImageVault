from django.contrib.auth.models import User
from account.models import Profile
from social_django.models import UserSocialAuth

class EmailAuthBackend:
    """
    Authenticate using an email address
    """
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None
        except User.MultipleObjectsReturned:
            return None
        
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        
def create_profile(backend, user, response, *args, **kwargs):
    '''
    Create user profile for social authentication
    '''

    profile, _ = Profile.objects.get_or_create(user=user)
    if backend.name == 'twitter':
        profile.photo = response.get('profile_image_url')
    elif backend.name == 'facebook':
        pict = response.get('picture')
        profile.photo = pict['data']['url']
    profile.save()
    