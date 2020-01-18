from django.urls import path


from . import views


app_name = 'profile'

urlpatterns = [
	path('student-profile/<int:student_id>/', views.StudentProfileView.as_view(), name = 'student-profile'),
]