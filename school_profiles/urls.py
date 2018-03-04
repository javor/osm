from django.urls import path

from school_profiles.views import CreateStudentProfileView

urlpatterns = [
    path('/create/student', CreateStudentProfileView.as_view(), name='create_student_profile'),
]
