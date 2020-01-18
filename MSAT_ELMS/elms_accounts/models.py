from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
	is_student = models.BooleanField(default=False)
	is_teacher = models.BooleanField(default=False)

class Students(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='user_student')


	def __str__(self):
		return str(self.user)




