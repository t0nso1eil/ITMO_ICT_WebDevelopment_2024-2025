from django.urls import path
from .views import (
    TeacherAPIView, QuarterGradeAPIView,
    LessonAPIView, ClassPerformanceAPIView,
    SubjectInClassAPIView, TeachersPerSubjectAPIView,
    TeachersWithSameSubjectsAPIView, GenderCountInClassesAPIView,
    ClassroomCountAPIView, StudentAPIView, ClassroomAPIView, SubjectAPIView, KlassAPIView
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
    path('teachers/', TeacherAPIView.as_view(), name='teacher-list'),
    path('teachers/<int:teacher_id>/', TeacherAPIView.as_view(), name='teacher-detail'),

    path('students/', StudentAPIView.as_view(), name='student-list'),
    path('students/<int:student_id>/', StudentAPIView.as_view(), name='student-detail'),

    path('quarter-grades/', QuarterGradeAPIView.as_view(), name='quartergrade-list'),
    path('quarter-grades/<int:grade_id>/', QuarterGradeAPIView.as_view(), name='quartergrade-detail'),

    path('lessons/', LessonAPIView.as_view(), name='lesson-list'),
    path('lessons/<int:lesson_id>/', LessonAPIView.as_view(), name='lesson-detail'),

    path('classrooms/', ClassroomAPIView.as_view(), name='classroom-list'),
    path('classrooms/<int:classroom_id>/', ClassroomAPIView.as_view(), name='classroom-detail'),

    path('subjects/', SubjectAPIView.as_view(), name='subject-list'),
    path('subjects/<int:subject_id>/', SubjectAPIView.as_view(), name='subject-detail'),

    path('klasses/', KlassAPIView.as_view(), name='klass-list'),
    path('klasses/<int:klass_id>/', KlassAPIView.as_view(), name='klass-detail'),

    path('class/<int:klass_id>/<str:weekday>/<str:lesson_number>/subject/', SubjectInClassAPIView.as_view(), name='subject-in-class'),
    path('subjects/teachers/count/', TeachersPerSubjectAPIView.as_view(), name='teachers-per-subject'),
    path('teachers/subject/informatics/<int:klass_id>/', TeachersWithSameSubjectsAPIView.as_view(), name='teachers-with-same-subjects'),
    path('classes/gender/count/', GenderCountInClassesAPIView.as_view(), name='gender-count-in-classes'),
    path('classrooms/count/', ClassroomCountAPIView.as_view(), name='classroom-count'),
    path('class/<int:klass_id>/performance/', ClassPerformanceAPIView.as_view(), name='class-performance'),

    path('doc/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
