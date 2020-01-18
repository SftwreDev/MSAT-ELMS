from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe

from elms_accounts.models import Students


class Category(models.Model):
    category_title = models.CharField(max_length=30,help_text='Category Title')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category_title

class Quiz(models.Model):
    posted_by = models.ForeignKey(Students, on_delete=models.CASCADE, related_name='quizzes', help_text='Posted By')
    quiz_title = models.CharField(max_length=255, help_text='Quiz Title')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='quizzes', help_text='Category')

    class Meta:
        verbose_name = 'Quiz'
        verbose_name_plural = 'Quizzes'

    def __str__(self):
        return self.quiz_title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question = models.CharField(max_length=300, help_text='Question')

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    def __str__(self):
        return self.question


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    answer = models.CharField(max_length=300, help_text='List of Answer')
    is_correct = models.BooleanField(default=False, help_text='Is this the correct answer?')

    def __str__(self):
        return self.answer

class TakenQuiz(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE, related_name='taken_quizzes')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='taken_quizzes')
    score = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'TakenQuiz'
        verbose_name_plural = 'TakenQuizzes'


class StudentAnswer(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE, related_name='quiz_answers')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='+')

    class Meta:
        verbose_name = 'StudentAnswer'
        verbose_name_plural = 'StudentAnswers'