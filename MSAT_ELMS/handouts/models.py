from django.db import models


class Handouts(models.Model):
    title = models.CharField(max_length=100, help_text='Handouts title')
    handouts_id = models.AutoField(primary_key = True),
    date = models.DateTimeField(auto_now_add=True, help_text='Date Published')
    file = models.FileField(upload_to = 'handouts', help_text = 'Upload your file here')

    class Meta:
        verbose_name = 'Handout'
        verbose_name_plural = 'Handouts'
