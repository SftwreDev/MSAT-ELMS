from django.db import models



class Announcements(models.Model):
	title = models.CharField(max_length = 150, blank=False, help_text = 'Enter your announcement title')
	date_posted = models.DateTimeField(auto_now_add = True)
	slug = models.AutoField(primary_key = True)
	content = models.TextField(max_length = 1000, blank = False, help_text = 'Enter the content of announcement')


	class Meta:
		verbose_name = 'Announcement'
		verbose_name_plural = 'Announcements'