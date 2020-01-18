from django.shortcuts import render

import random

from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import FormView, CreateView
from .forms import ExamForm
from .models import Exams, Category, Progress, Sitting, Question
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse_lazy
from bootstrap_modal_forms.generic import BSModalLoginView
from elms.forms import CustomAuthenticationForm
#from quiz.forms import CreateNewQuiz, QuizQuestionAndAnswer
from .models import ExamsQuestions


class ExamsMarkerMixin(object):
    @method_decorator(login_required)
    @method_decorator(permission_required('exams.view_sittings'))
    def dispatch(self, *args, **kwargs):
        return super(QuizMarkerMixin, self).dispatch(*args, **kwargs)


class SittingFilterTitleMixin(object):
    def get_queryset(self):
        queryset = super(SittingFilterTitleMixin, self).get_queryset()
        quiz_filter = self.request.GET.get('quiz_filter')
        if quiz_filter:
            queryset = queryset.filter(quiz__title__icontains=quiz_filter)

        return queryset


class ExamsListView(ListView):
    model = Exams
    template_name='exams/exams_list.html'
    context_object_name = 'exams_list'
    # @login_required
    def get_queryset(self):
        queryset = super(ExamsListView, self).get_queryset()
        return queryset.filter(draft=False)



class ExamsDetailView(DetailView):
    model = Exams
    slug_field = 'url'
    template_name = 'exams/exams_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.draft and not request.user.has_perm('exams.change_exam'):
            raise PermissionDenied

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class CategoriesListView(ListView):
    model = Category


class ViewExamsListByCategory(ListView):
    model = Exams
    template_name = 'view_quiz_category.html'

    def dispatch(self, request, *args, **kwargs):
        self.category = get_object_or_404(
            Category,
            category=self.kwargs['category_name']
        )

        return super(ViewExamsListByCategory, self).\
            dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ViewExamsListByCategory, self)\
            .get_context_data(**kwargs)

        context['category'] = self.category
        return context

    def get_queryset(self):
        queryset = super(ViewExamsListByCategory, self).get_queryset()
        return queryset.filter(category=self.category, draft=False)


class ExamsUserProgressView(TemplateView):
    template_name = 'progress.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ExamsUserProgressView, self)\
            .dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ExamsUserProgressView, self).get_context_data(**kwargs)
        progress, c = Progress.objects.get_or_create(user=self.request.user)
        context['cat_scores'] = progress.list_all_cat_scores
        context['exams'] = progress.show_exams()
        return context


class ExamsMarkingList(ExamsMarkerMixin, SittingFilterTitleMixin, ListView):
    model = Sitting

    def get_queryset(self):
        queryset = super(ExamsMarkingList, self).get_queryset()\
                                               .filter(complete=True)

        user_filter = self.request.GET.get('user_filter')
        if user_filter:
            queryset = queryset.filter(user__username__icontains=user_filter)

        return queryset

    class Meta:
        pass


class ExamsMarkingDetail(ExamsMarkerMixin, DetailView):
    model = Sitting

    def post(self, request, *args, **kwargs):
        sitting = self.get_object()

        q_to_toggle = request.POST.get('qid', None)
        if q_to_toggle:
            q = Question.objects.get_subclass(id=int(q_to_toggle))
            if int(q_to_toggle) in sitting.get_incorrect_questions:
                sitting.remove_incorrect_question(q)
            else:
                sitting.add_incorrect_question(q)

        return self.get(request)

    def get_context_data(self, **kwargs):
        context = super(ExamsMarkingDetail, self).get_context_data(**kwargs)
        context['questions'] =\
            context['sitting'].get_questions(with_answers=True)
        return context


class ExamsTake(FormView):
    form_class = ExamForm
    template_name = 'exams/question_for_exams.html'

    def dispatch(self, request, *args, **kwargs):
        self.exams = get_object_or_404(Exams, url=self.kwargs['exams_name'])
        if self.exams.draft and not request.user.has_perm('exams.change_exam'):
            raise PermissionDenied

        self.logged_in_user = self.request.user.is_authenticated

        if self.logged_in_user:
            self.sitting = Sitting.objects.user_sitting(request.user,
                                                        self.exams)
        if self.sitting is False:
            return render(request, 'exams/single_complete.html')

        return super(ExamsTake, self).dispatch(request, *args, **kwargs)

    def get_form(self, form_class=ExamForm):
        if self.logged_in_user:
            self.question = self.sitting.get_first_question()
            self.progress = self.sitting.progress()
        return form_class(**self.get_form_kwargs())

    def get_form_kwargs(self):
        kwargs = super(ExamsTake, self).get_form_kwargs()

        return dict(kwargs, question=self.question)

    def form_valid(self, form):
        if self.logged_in_user:
            self.form_valid_user(form)
            if self.sitting.get_first_question() is False:
                return self.final_result_user()
        self.request.POST = {}

        return super(ExamsTake, self).get(self, self.request)

    def get_context_data(self, **kwargs):
        context = super(ExamsTake, self).get_context_data(**kwargs)
        context['question'] = self.question
        context['exams'] = self.exams
        if hasattr(self, 'previous'):
            context['previous'] = self.previous
        if hasattr(self, 'progress'):
            context['progress'] = self.progress
        return context

    def form_valid_user(self, form):
        progress, c = Progress.objects.get_or_create(user=self.request.user)
        guess = form.cleaned_data['answers']
        is_correct = self.question.check_if_correct(guess)

        if is_correct is True:
            self.sitting.add_to_score(1)
            progress.update_score(self.question, 1, 1)
        else:
            self.sitting.add_incorrect_question(self.question)
            progress.update_score(self.question, 0, 1)

        if self.exams.answers_at_end is not True:
            self.previous = {'previous_answer': guess,
                             'previous_outcome': is_correct,
                             'previous_question': self.question,
                             'answers': self.question.get_answers(),
                             'question_type': {self.question
                                               .__class__.__name__: True}}
        else:
            self.previous = {}

        self.sitting.add_user_answer(self.question, guess)
        self.sitting.remove_first_question()

    def final_result_user(self):
        results = {
            'exams': self.exams,
            'score': self.sitting.get_current_score,
            'max_score': self.sitting.get_max_score,
            'percent': self.sitting.get_percent_correct,
            'sitting': self.sitting,
            'previous': self.previous,
        }

        self.sitting.mark_exams_complete()

        if self.exams.answers_at_end:
            results['questions'] =\
                self.sitting.get_questions(with_answers=True)
            results['incorrect_questions'] =\
                self.sitting.get_incorrect_questions

        if self.exams.exam_paper is False:
            self.sitting.delete()

        return render(self.request, 'exams/exam_result.html', results)




def index(request):
    return render(request, 'index.html', {})



def login_user(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in')
            return redirect("index")
        else:
            messages.success(request, 'Error logging in')
            return redirect('login')
    else:
        return render(request, 'login.html', {})




def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out!')
    print('logout function working')
    return redirect('login')


#class CreateExamsView(CreateView):
 #   model = Exams
 #   form_class = CreateNewQuiz
 #   success_url = reverse_lazy("quiz_q&a")
 #   template_name = 'quiz/create_new_quiz.html'


#class ExamsQuestionAndAnswerView(CreateView):
 #   model = ExamsQuestions
#    form_class = QuizQuestionAndAnswer
  #  success_url = reverse_lazy("quiz_index")
  #  template_name = 'quiz/quiz_q&a.html'
