from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import userProfile, User


"""
    we want the profile to be created when the user is created this process is done by using signals
    signals are functions that are executed when a certain event occurs like saving some record in the database
    this means that when a new instance of user is saved in the database then the signal functions will be executed
    every signal function has a sender and a receiver
    the sender is the model that sends the signal
    the receiver is the function that will be executed when the signal is sent
    ....................................................................................................
    we have two ways for connecting the sender and receiver first is:
    post_save.connect(post_save_create_profile_receiver, sender=User)
    and second is to use a decorator receiver as following:
"""


@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender: User, instance: User, created: bool, **kwargs) -> None:
    """
        this function will check if the user is created or not if created was True
        the function will create a new profile with that user so the instance is actually the user
        but if we just wanted to update a user info we dont want to create a new profile
        then we just update the changes to the user profile in the else block
        .....................................................................................
        there is one more scenario where we dont have a profile but we update the user instance
        in this case we first try to update the user profile as we did before but if the profile
        doesn't exist then we just create a new profile using that instance we get from the User model
    """

    if created:
        userProfile.objects.create(user=instance)
    else:
        try:
            profile = userProfile.objects.get(user=instance)
            profile.save()

        except userProfile.DoesNotExist:
            userProfile.objects.create(user=instance)
