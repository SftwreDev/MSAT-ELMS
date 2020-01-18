from django.conf.urls import url
from django.urls import path
from quiz import views
from quiz.views import QuizTake


urlpatterns = [
    path('home/', views.index, name='index'),
    path('', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('quizzes/', views.QuizListView.as_view(), name='quiz_index'),
    path('category/', views.CategoriesListView.as_view(), name='quiz_category_list_all'),
    path('category/<str:category_name>/', views.ViewQuizListByCategory.as_view(), name='quiz_category_list_matching'),
    path('progress/', views.QuizUserProgressView.as_view(), name='quiz_progress'),
    path('marking/', views.QuizMarkingList.as_view(), name='quiz_marking'),
    path('marking/<int:pk>/', views.QuizMarkingDetail.as_view(), name='quiz_marking_detail'),
    path('quizzes/<str:slug>/', views.QuizDetailView.as_view(), name='quiz_start_page'),
    #path('<str:slug>/', views.QuizTake.as_view(), name='quiz_question'),
    #url(regex=r'^(?P<slug>[\w-]+)/$', view=QuizDetailView.as_view(), name='quiz_start_page'),

    url(regex=r'^(?P<quiz_name>[\w-]+)/take/$',view=QuizTake.as_view(), name='quiz_question'),
    path('create-new-quiz/', views.CreateQuizView.as_view(), name='create_new_quiz'),
    path('quiz-question-and-answer/', views.AnswerforQuiz.as_view(), name='quiz_q&a'),
    path('quiz-category/', views.QuizCategoryView.as_view(), name='quiz_create_category'),
    path('questions-quiz/', views.QuestionforQuiz.as_view(), name = 'questions_for_quiz'),

]
