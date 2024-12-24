from django.db import IntegrityError
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Avg
from .models import Teacher, Student, QuarterGrade, Lesson, Classroom, Subject, Klass
from .serializers import TeacherSerializer, StudentSerializer, QuarterGradeSerializer, LessonSerializer, \
    SubjectSerializer, ClassroomSerializer, KlassSerializer


class TeachersAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TeacherSerializer

    def get(self, request):
        teachers = Teacher.objects.all()
        serializer = TeacherSerializer(teachers, many=True)
        return Response({"Teachers": serializer.data})

    def post(self, request):
        serializer = TeacherSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            teacher_saved = serializer.save()
            return Response({"Success": f"Teacher '{teacher_saved.first_name} {teacher_saved.last_name}' created successfully."})
        return Response({"Error": "Invalid data provided."}, status=400)


class StudentsAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StudentSerializer

    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response({"Students": serializer.data})

    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            student_saved = serializer.save()
            return Response({"Success": f"Student '{student_saved.first_name} {student_saved.last_name}' created successfully."})
        return Response({"Error": "Invalid data provided."}, status=400)


class QuarterGradeAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = QuarterGradeSerializer

    def post(self, request):
        serializer = QuarterGradeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            grade_saved = serializer.save()
            return Response({"Success": f"Grade for student ID '{grade_saved.student.id}' updated successfully."})
        return Response({"Error": "Invalid data provided."}, status=400)


class LessonAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LessonSerializer

    def get(self, request):
        lessons = Lesson.objects.all()
        serializer = LessonSerializer(lessons, many=True)
        return Response({"Lessons": serializer.data})

    def post(self, request):
        serializer = LessonSerializer(data=request.data)
        if serializer.is_valid():
            try:
                lesson_saved = serializer.save()
                return Response({"Success": f"Lesson '{lesson_saved.id}' created successfully."}, status=201)
            except IntegrityError as e:
                return Response({"Error": "Database error: " + str(e)}, status=400)
        return Response(serializer.errors, status=400)


class LessonDetailsAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LessonSerializer

    def get(self, request, klass_id, weekday, lesson_number):
        try:
            lesson = Lesson.objects.get(klass_id=klass_id, weekday=weekday, lesson_number=lesson_number)
            serializer = LessonSerializer(lesson)
            return Response({"Lesson": serializer.data})
        except Lesson.DoesNotExist:
            return Response({"Error": "Lesson not found."}, status=404)

class SubjectInClassAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, klass_id, weekday, lesson_number):
        try:
            lesson = Lesson.objects.get(klass_id=klass_id, weekday=weekday, lesson_number=lesson_number)
            subject_name = lesson.subject.name
            return Response({"Subject": subject_name})
        except Lesson.DoesNotExist:
            return Response({"Error": "Lesson not found."}, status=404)


class TeachersPerSubjectAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        teachers_count = Teacher.objects.values('subject__name').annotate(count=Count('id'))
        data = {entry['subject__name']: entry['count'] for entry in teachers_count}
        return Response({"TeachersPerSubject": data})


class TeachersWithSameSubjectsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, klass_id):
        try:
            informatics_teacher = Teacher.objects.filter(
                subject__name="Informatics",
                klass__id=klass_id
            ).first()

            if not informatics_teacher:
                return Response({"Error": "Informatics teacher not found in the specified class."}, status=404)

            teachers = Teacher.objects.filter(subject__in=informatics_teacher.subject.all()).exclude(id=informatics_teacher.id)
            serializer = TeacherSerializer(teachers, many=True)
            return Response({"TeachersWithSameSubjects": serializer.data})
        except Exception as e:
            return Response({"Error": str(e)}, status=500)


class GenderCountInClassesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        classes = Klass.objects.all()
        data = {}
        for klass in classes:
            boys = Student.objects.filter(klass=klass, gender="Male").count()
            girls = Student.objects.filter(klass=klass, gender="Female").count()
            data[klass.id] = {"boys": boys, "girls": girls}
        return Response({"GenderCounts": data})


class ClassroomCountAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        classrooms = Classroom.objects.values('type').annotate(count=Count('id'))
        data = {entry['type']: entry['count'] for entry in classrooms}
        return Response({"ClassroomCounts": data})

class ClassPerformanceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, klass_id):
        try:
            students = Student.objects.filter(klass__id=klass_id)
            grades = QuarterGrade.objects.filter(student__klass__id=klass_id)
            subjects = Subject.objects.all()
            report = {}

            for subject in subjects:
                subject_grades = grades.filter(subject=subject)
                if subject_grades.exists():
                    avg_grade = subject_grades.aggregate(avg=Avg('grade'))['avg']
                    report[subject.name] = {"average_grade": avg_grade, "grades": list(subject_grades.values())}

            class_teacher = Klass.objects.get(id=klass_id).class_teacher
            return Response({
                "class_teacher": f"{class_teacher.first_name} {class_teacher.last_name}" if class_teacher else None,
                "total_students": students.count(),
                "report": report
            })
        except Klass.DoesNotExist:
            return Response({"Error": "Class not found."}, status=404)

class TeacherDetailsAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TeacherSerializer

    def get(self, request, teacher_id):
        try:
            teacher = Teacher.objects.get(id=teacher_id)
            serializer = TeacherSerializer(teacher)
            return Response({"Teacher": serializer.data})
        except Teacher.DoesNotExist:
            return Response({"Error": "Teacher not found."}, status=404)


class StudentDetailsAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StudentSerializer

    def get(self, request, student_id):
        try:
            student = Student.objects.get(id=student_id)
            serializer = StudentSerializer(student)
            return Response({"Student": serializer.data})
        except Student.DoesNotExist:
            return Response({"Error": "Student not found."}, status=404)


class QuarterGradeCreateAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = QuarterGradeSerializer

    def post(self, request):
        serializer = QuarterGradeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            grade_saved = serializer.save()
            return Response({"Success": f"Grade for student ID '{grade_saved.student.id}' created successfully."})
        return Response({"Error": "Invalid data provided."}, status=400)


class ClassroomCreateAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClassroomSerializer

    def post(self, request):
        serializer = ClassroomSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            classroom_saved = serializer.save()
            return Response({"Success": f"Classroom '{classroom_saved.id}' created successfully."})
        return Response({"Error": "Invalid data provided."}, status=400)


class SubjectCreateAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubjectSerializer

    def post(self, request):
        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            subject_saved = serializer.save()
            return Response({"Success": f"Subject '{subject_saved.name}' created successfully."})
        return Response({"Error": "Invalid data provided."}, status=400)

class KlassAPIView(APIView):
    def post(self, request):
        serializer = KlassSerializer(data=request.data)
        if serializer.is_valid():
            klass = serializer.save()
            return Response(
                {"Success": f"Klass '{klass.id}' created successfully."},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        klasses = Klass.objects.all()
        serializer = KlassSerializer(klasses, many=True)
        return Response({"Classes": serializer.data}, status=status.HTTP_200_OK)