from django.urls import include, path

from . import views

app_name = 'accounts'
urlpatterns = [
	path('', include('django.contrib.auth.urls')),
	path('signup/', views.SignUpView.as_view(), name='signup'),
	path('signup/student/', views.StudentSignUpView.as_view(), name='student_signup'),
	path('signup/teacher/', views.TeacherSignUpView.as_view(), name='teacher_signup'),
	#path('logout/', views.LogOutView.as_view(), name='logout'),
]