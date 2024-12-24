from django.urls import path
from .views import (
    TeachersAPIView, StudentsAPIView, QuarterGradeAPIView,
    LessonAPIView, LessonDetailsAPIView, ClassPerformanceAPIView,
    SubjectInClassAPIView, TeachersPerSubjectAPIView,
    TeachersWithSameSubjectsAPIView, GenderCountInClassesAPIView,
    ClassroomCountAPIView, TeacherDetailsAPIView, StudentDetailsAPIView, QuarterGradeCreateAPIView,
    ClassroomCreateAPIView, SubjectCreateAPIView, KlassAPIView
)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="School API",
        default_version='v2',
        description="API for managing school data",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="your_email@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('teachers/', TeachersAPIView.as_view(), name='teachers-list-create'),
    path('students/', StudentsAPIView.as_view(), name='students-list-create'),
    path('grades/update/', QuarterGradeAPIView.as_view(), name='grade-update'),
    path('lessons/', LessonAPIView.as_view(), name='lessons-list-create'),
    path('lessons/<int:klass_id>/<str:weekday>/<str:lesson_number>/', LessonDetailsAPIView.as_view(), name='lesson-details'),
    path('class/<int:klass_id>/performance/', ClassPerformanceAPIView.as_view(), name='class-performance-report'),
    path('class/<int:klass_id>/<str:weekday>/<str:lesson_number>/subject/', SubjectInClassAPIView.as_view(), name='subject-in-class'),
    path('subjects/teachers/count/', TeachersPerSubjectAPIView.as_view(), name='teachers-per-subject'),
    path('teachers/subject/informatics/<int:klass_id>/', TeachersWithSameSubjectsAPIView.as_view(), name='teachers-with-same-subjects'),
    path('classes/gender/count/', GenderCountInClassesAPIView.as_view(), name='gender-count-in-classes'),
    path('classrooms/count/', ClassroomCountAPIView.as_view(), name='classroom-count'),
    path('doc/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('teachers/<int:teacher_id>/', TeacherDetailsAPIView.as_view(), name='teacher-details'),
    path('students/<int:student_id>/', StudentDetailsAPIView.as_view(), name='student-details'),
    path('grades/', QuarterGradeCreateAPIView.as_view(), name='grade-create'),
    path('classrooms/', ClassroomCreateAPIView.as_view(), name='classroom-create'),
    path('subjects/', SubjectCreateAPIView.as_view(), name='subject-create'),
    path('classes/', KlassAPIView.as_view(), name='klasses-list-create'),
]
