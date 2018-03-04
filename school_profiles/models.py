from django.contrib.auth.models import AbstractUser
from django.db import models

from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    # TODO: User model for authenticating
    ...


class UserProfile(models.Model):
    names = models.CharField(blank=False, max_length=150, null=False, verbose_name=_('names'))
    surname = models.CharField(blank=False, max_length=150, null=False, verbose_name=_('surname'))

    class Meta:
        abstract = True


class ParentProfile(UserProfile):
    # address = TODO: add address model (in this case it is not required field)
    user = models.OneToOneField(User, blank=True, db_column='user_id', on_delete=models.PROTECT, null=True,
                                primary_key=False, related_name='parent_profile', verbose_name=_('user object'))

    def __str__(self):
        return '{0} {1}'.format(self.names, self.surname)


class StudentProfile(UserProfile):
    # address = TODO: add address model (in this case it is required field)
    date_of_birth = models.DateField(blank=False, null=False, verbose_name=_('date of birth'))
    pesel = models.CharField(blank=False, max_length=9, null=False, verbose_name=_('PESEL'))
    place_of_birth = models.TextField(verbose_name=_('place of birth'))
    parents_profiles = models.ManyToManyField(ParentProfile, blank=True, null=True, related_name='children',
                                              verbose_name=_('parent profile'))
    user = models.OneToOneField(User, blank=True, db_column='user_id', on_delete=models.PROTECT, null=True,
                                primary_key=False, related_name='student_profile', verbose_name=_('user object'))

    def __str__(self):
        return '{0} {1}'.format(self.names, self.surname)


class TeacherProfile(UserProfile):
    user = models.OneToOneField(User, blank=True, db_column='user_id', on_delete=models.PROTECT, null=True,
                                primary_key=False, related_name='teacher_profile', verbose_name=_('user object'))

    def __str__(self):
        return '{0} {1}'.format(self.names, self.surname)
