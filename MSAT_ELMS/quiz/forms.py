from django import forms

from .models import Quiz
from .models import QuizQuestions, Category, Answer, Question


class CreateNewQuiz(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = '__all__'



class QuizCategory(forms.ModelForm):
	class Meta:
		model = Category
		fields = ['category']

class QuizQandA(forms.ModelForm):
	class Meta:
		model = Question
		fields = '__all__'

class QuestionsforQuiz(forms.ModelForm):
	class Meta:
		model = Answer
		fields = "__all__"


class QuizAnswer(forms.ModelForm):
	pass