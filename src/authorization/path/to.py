from src.authorization.models import CustomUser


def save_activ_email(backend, user, response, *args, **kwargs):
    profile = user
    if profile is None:
        profile = CustomUser(id=user.id)
    profile.activ_email = True
    profile.save()
