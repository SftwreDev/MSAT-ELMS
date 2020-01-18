from django.contrib import admin
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
# Register your models here.
from .models import Exams, Category, Question, Progress
from .models import ExamsQuestions, Answer
from django.utils.translation import ugettext_lazy as _




class AnswerInline(admin.TabularInline):
    model = Answer


class ExamAdminForm(forms.ModelForm):
    """
        below is from
        http://stackoverflow.com/questions/11657682/
        django-admin-interface-using-horizontal-filter-with-
        inline-manytomany-field
    """

    class Meta:
        model = Exams
        exclude = []

    questions = forms.ModelMultipleChoiceField(
        queryset=Question.objects.all().select_subclasses(),
        required=False,
        label=_("Questions"),
        widget=FilteredSelectMultiple(
            verbose_name=_("Questions"),
            is_stacked=False))

    def __init__(self, *args, **kwargs):
        super(ExamAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['questions'].initial = \
                self.instance.question_set.all().select_subclasses()

    def save(self, commit=True):
        exams = super(ExamAdminForm, self).save(commit=False)
        exams.save()
        exams.question_set.set(self.cleaned_data['questions'])
        self.save_m2m()
        return exams


class ExamAdmin(admin.ModelAdmin):
    form = ExamAdminForm

    list_display = ('title', 'category', )
    list_filter = ('category',)
    search_fields = ('description', 'category', )


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('category', )


class MCQuestionAdmin(admin.ModelAdmin):
    list_display = ('content', 'category', )
    list_filter = ('category',)
    fields = ('content', 'category',
              'figure', 'exams', 'explanation', 'answer_order')

    search_fields = ('content', 'explanation')
    filter_horizontal = ('exams',)

    inlines = [AnswerInline]


class ProgressAdmin(admin.ModelAdmin):
    """
    to do:
            create a user section
    """
    search_fields = ('user', 'score', )


admin.site.register(Exams, ExamAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ExamsQuestions, MCQuestionAdmin)
admin.site.register(Progress, ProgressAdmin)

