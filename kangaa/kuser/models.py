from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext as _

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,\
                                       PermissionsMixin, UserManager


'''   Custom Kangaa user manager. '''
class CustomUserManager(BaseUserManager):

    ''' (private) Create a custom user model. We can create both regular, and super,
        users by toggling the 'is_staff' and 'is_superuser' options.
        Args:
            email:  The email address of the new user.
            password: The new user's password.
            is_staff: Is a staff member.
            is_superuser: Is a superuser.
            **extra_fields: Fields like 'first_name', 'address', etc.
    '''
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):

        if not email:
            raise ValueError('Email field is not optional.')
        
        now     = timezone.now()
        email   = self.normalize_email(email)
        user    = self.model(email=email,
                             is_staff=is_staff, is_superuser=is_superuser,
                             join_date=now,
                             last_login=now,
                             **extra_fields
        )
        
        # Set the password, & save the user in the DB.
        user.set_password(password)
        user.save(using=self._db)
        
        # Create a default profile.
        profile = Profile.objects.create(kuser=user)
        
        return user

    ''' Create a regular custom user. '''
    def create_user(self, email, password=None, **extra_fields):

        return self._create_user(email, password,
                                 is_staff=False, is_superuser=False,
                                 **extra_fields)
    
    ''' Create a super user (aka Admin). '''
    def create_superuser(self, email, password, **extra_fields):

        return self._create_user(email, password,
                                 is_staff=True, is_superuser=True,
                                 **extra_fields)


'''   Custom Kangaa user class. '''
class KUser(AbstractBaseUser, PermissionsMixin):
    
    email           = models.EmailField(unique=True, db_index=True)
    
    is_staff        = models.BooleanField(default=False)
    is_admin        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    join_date       = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = []

    objects         = CustomUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


    ''' Returns the full name of the user. '''
    def get_fullname(self):

        return #self.first_name + ' ' + self.last_name

    def get_short_name():

        return self.email

    ''' Returns the user's email. '''
    def get_email(self):

        return self.email
    
    ''' Unicode / String representation of a user. '''
    def __unicode__(self):

        return self.email


'''   Profile model for user. '''
class Profile(models.Model):

    kuser           = models.OneToOneField(settings.AUTH_USER_MODEL,
                        related_name='profile', on_delete=models.CASCADE)

    first_name      = models.CharField(max_length=25, blank=True)
    last_name       = models.CharField(max_length=25, blank=True)
    bio             = models.CharField(max_length=250, blank=True)
    location        = models.CharField(max_length=50, blank=True)

    prof_pic        = models.ImageField(upload_to='profiles/',
                        default='profiles/default.svg')

