from django.db import models
from accounts.models import User, userProfile

class Vendor(models.Model): 
    """
        this class is for venders registration
    """
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(userProfile, related_name='userprofile', on_delete=models.CASCADE)
    Vendor_name = models.CharField(max_length=100)
    Vendor_license = models.ImageField(upload_to='vendor/license')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.Vendor_name
    
    