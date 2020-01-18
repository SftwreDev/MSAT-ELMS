from django.db import models



class Category(models.Model):
	title = models.CharField(max_length = 100, related_name= 'Title of Category', help_text = 'Title of Category')



class QuizQuestions(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	title =  models.CharField(max_length = 300, related_name='Quiz', help_text='Question for Quiz')
	date_published = models.DateTimeField(auto_now_add = True)



class Answers(models.Model):
	question = models.ForeignKey(QuizQuestions, on_delete=models.CASCADE)
	choices = models.CharField(max_length = 100, related_name = 'Answers', help_text = 'Answer Choices')
	is_correct = models.BooleanField()

	