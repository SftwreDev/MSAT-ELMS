from django.contrib import admin

from .models import Category, Quiz, Question, Answer, TakenQuiz, StudentAnswer




admin.site.register(Category)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(TakenQuiz)
admin.site.register(StudentAnswer)