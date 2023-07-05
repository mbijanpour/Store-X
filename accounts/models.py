from django.db import models

# the Base will give you the permission of having full control over the django user and user management models
# you can override these two the way you want
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class AccountManager(BaseUserManager):
    """
        this class have two methods:
        create_user => which is for creating a new user but in django user model the username is defined as the login field
        but in here we have override this in the way we want
        create_superuser => which is for creating a new superuser by using create_user method
    """

    def create_user(self, first_name: str, last_name: str, username: str, email: str, password: str = None):
        """
            django user model only has username, email and password but here
            we have add firstname and lastname as the registration field
        """

        if not email:
            raise ValueError('User must have an email address')

        if not username:
            raise ValueError('User must have an username')

        # the model has been inherited from BaseUserManager for creating a new user
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        # we cannot save the password directly so we use set_password()
        user.set_password(password)

        # using = ? will defined which database we want to save the user for when we have multiple
        # databases but here we user the default database we have defined in settings.py
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name: str, last_name: str, email: str, username: str, password: str = None):
        """
            creates a user with the above method then set the flowing states true
        """

        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin      = True
        user.is_active     = True
        user.is_staff      = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """
        this class is used to override the django user model
        in extra methods:
        has_perm => this method is used to check if the user has a specific permission in here we return admins only
        has_module_perms => this method is used to check if the user has permission to a specific module or not
        here we return True which indicates that the user has permission to any module
    """

    PROVIDER = 1
    COSTUMER = 2

    ROLE_CHOICES = (
        (PROVIDER, 'Provider'),
        (COSTUMER, 'Costumer'),
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50)
    # we have three roles: provider, costumer, admin
    # we have to define the role of the user when creating one
    role = models.SmallIntegerField(
        choices=ROLE_CHOICES, blank=True, null=True)

    # required fields

    date_joined   = models.DateTimeField(auto_now_add=True)
    last_login    = models.DateTimeField(auto_now_add=True)
    created_date  = models.DateTimeField(auto_now_add=True)
    modifies_date = models.DateTimeField(auto_now=True)
    is_admin      = models.BooleanField(default=False)
    is_staff      = models.BooleanField(default=False)
    is_active     = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    # authentication

    # set the email instead of the username as the authentication field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    # extra methods

    # our user model uses the AccountManager class for handling so
    # we can use those methods in the AccountManager class
    objects = AccountManager()

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True

    def __str__(self) -> str:
        return self.email


class userProfile(models.Model):
    """
        this class is used to create a user profile for the user 
        so obviously we have one to one relation with the user model
        meaning that one user can have one profile with its email address
        .................................................................
        the PictureField requires pillow package to be installed
        the upload_to = ? is the folder where the picture will be stored
        .................................................................
        for the picture files we should have configure the media directories as we do
        the static files in the settings.py      
    """

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=True, null=True)
    
    # user profile pictures
    profile_picture = models.ImageField(
        upload_to='users/profile_pictures', blank=True, null=True)
    cover_photo = models.ImageField(
        upload_to='users/cover_photos', blank=True, null=True)
    
    # other user details that are only for the profile not the user instance itself
    first_address = models.TextField(blank=True, null=True)
    second_address = models.TextField(blank=True, null=True)
    province = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    zipcode = models.CharField(max_length=6, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.user.email
