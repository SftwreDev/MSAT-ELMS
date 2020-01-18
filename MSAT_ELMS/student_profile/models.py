from django.db import models
from elms_accounts.models import Students, User
from django.db.models.signals import post_save


class StudentProfile(models.Model):
	user = models.OneToOneField(Students, on_delete=models.CASCADE)
	
	
	class Meta:
		verbose_name = 'Student Profile'
		verbose_name_plural = 'Student Profiles'


	def __str__(self):
		return self.last_name





def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = StudentProfile(user=user)
        user_profile.save()
post_save.connect(create_profile, sender=Students)