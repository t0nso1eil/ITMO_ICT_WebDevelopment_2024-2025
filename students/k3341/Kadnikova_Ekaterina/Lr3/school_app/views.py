from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Avg
from .models import Teacher, Student, QuarterGrade, Lesson, Classroom, Subject, Klass
from .serializers import TeacherSerializer, StudentSerializer, QuarterGradeSerializer, LessonSerializer, \
    SubjectSerializer, ClassroomSerializer, KlassSerializer


class TeacherAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()

    def get(self, request, teacher_id=None, *args, **kwargs):
        if teacher_id:
            try:
                teacher = Teacher.objects.get(id=teacher_id)
                serializer = self.serializer_class(teacher)
                return Response({"Teacher": serializer.data})
            except Teacher.DoesNotExist:
                return Response({"Error": "Teacher not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            teachers = Teacher.objects.all()
            serializer = self.serializer_class(teachers, many=True)
            return Response({"Teachers": serializer.data})

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            teacher = serializer.save()
            return Response({"Success": f"Teacher '{teacher.first_name} {teacher.last_name}' created successfully."}, status=status.HTTP_201_CREATED)
        return Response({"Error": "Invalid data provided."}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, teacher_id=None, *args, **kwargs):
        try:
            teacher = Teacher.objects.get(id=teacher_id)
            serializer = self.serializer_class(teacher, data=request.data)
            if serializer.is_valid():
                teacher_updated = serializer.save()
                return Response({"Success": f"Teacher '{teacher_updated.first_name} {teacher_updated.last_name}' updated successfully."})
            return Response({"Error": "Invalid data provided."}, status=status.HTTP_400_BAD_REQUEST)
        except Teacher.DoesNotExist:
            return Response({"Error": "Teacher not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, teacher_id=None, *args, **kwargs):
        try:
            teacher = Teacher.objects.get(id=teacher_id)
            teacher.delete()
            return Response({"Success": "Teacher deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Teacher.DoesNotExist:
            return Response({"Error": "Teacher not found."}, status=status.HTTP_404_NOT_FOUND)


class StudentAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StudentSerializer
    queryset = Student.objects.all()

    def get(self, request, student_id=None, *args, **kwargs):
        if student_id:
            try:
                student = Student.objects.get(id=student_id)
                serializer = self.serializer_class(student)
                return Response({"Student": serializer.data})
            except Student.DoesNotExist:
                return Response({"Error": "Student not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            students = Student.objects.all()
            serializer = self.serializer_class(students, many=True)
            return Response({"Students": serializer.data})

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            student = serializer.save()
            return Response({"Success": f"Student '{student.first_name} {student.last_name}' created successfully."}, status=status.HTTP_201_CREATED)
        return Response({"Error": "Invalid data provided."}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, student_id=None, *args, **kwargs):
        try:
            student = Student.objects.get(id=student_id)
            serializer = self.serializer_class(student, data=request.data)
            if serializer.is_valid():
                updated_student = serializer.save()
                return Response({"Success": f"Student '{updated_student.first_name} {updated_student.last_name}' updated successfully."})
            return Response({"Error": "Invalid data provided."}, status=status.HTTP_400_BAD_REQUEST)
        except Student.DoesNotExist:
            return Response({"Error": "Student not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, student_id=None, *args, **kwargs):
        try:
            student = Student.objects.get(id=student_id)
            student.delete()
            return Response({"Success": "Student deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Student.DoesNotExist:
            return Response({"Error": "Student not found."}, status=status.HTTP_404_NOT_FOUND)


class QuarterGradeAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = QuarterGradeSerializer
    queryset = QuarterGrade.objects.all()

    def get(self, request, grade_id=None, *args, **kwargs):
        if grade_id:
            try:
                grade = QuarterGrade.objects.get(id=grade_id)
                serializer = self.serializer_class(grade)
                return Response({"Grade": serializer.data})
            except QuarterGrade.DoesNotExist:
                return Response({"Error": "Grade not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            grades = QuarterGrade.objects.all()
            serializer = self.serializer_class(grades, many=True)
            return Response({"Grades": serializer.data})

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            grade = serializer.save()
            return Response({"Success": f"Grade for student '{grade.student.first_name} {grade.student.last_name}' created successfully."}, status=status.HTTP_201_CREATED)
        return Response({"Error": "Invalid data provided."}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, grade_id=None, *args, **kwargs):
        try:
            grade = QuarterGrade.objects.get(id=grade_id)
            serializer = self.serializer_class(grade, data=request.data)
            if serializer.is_valid():
                updated_grade = serializer.save()
                return Response({"Success": f"Grade updated successfully."})
            return Response({"Error": "Invalid data provided."}, status=status.HTTP_400_BAD_REQUEST)
        except QuarterGrade.DoesNotExist:
            return Response({"Error": "Grade not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, grade_id=None, *args, **kwargs):
        try:
            grade = QuarterGrade.objects.get(id=grade_id)
            grade.delete()
            return Response({"Success": "Grade deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except QuarterGrade.DoesNotExist:
            return Response({"Error": "Grade not found."}, status=status.HTTP_404_NOT_FOUND)


class LessonAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    def get(self, request, lesson_id=None, *args, **kwargs):
        if lesson_id:
            try:
                lesson = Lesson.objects.get(id=lesson_id)
                serializer = self.serializer_class(lesson)
                return Response({"Lesson": serializer.data})
            except Lesson.DoesNotExist:
                return Response({"Error": "Lesson not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            lessons = Lesson.objects.all()
            serializer = self.serializer_class(lessons, many=True)
            return Response({"Lessons": serializer.data})

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            lesson = serializer.save()
            return Response({"Success": f"Lesson '{lesson.id}' created successfully."}, status=status.HTTP_201_CREATED)
        return Response({"Error": "Invalid data provided."}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, lesson_id=None, *args, **kwargs):
        try:
            lesson = Lesson.objects.get(id=lesson_id)
            serializer = self.serializer_class(lesson, data=request.data)
            if serializer.is_valid():
                updated_lesson = serializer.save()
                return Response({"Success": f"Lesson '{updated_lesson.id}' updated successfully."})
            return Response({"Error": "Invalid data provided."}, status=status.HTTP_400_BAD_REQUEST)
        except Lesson.DoesNotExist:
            return Response({"Error": "Lesson not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, lesson_id=None, *args, **kwargs):
        try:
            lesson = Lesson.objects.get(id=lesson_id)
            lesson.delete()
            return Response({"Success": "Lesson deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Lesson.DoesNotExist:
            return Response({"Error": "Lesson not found."}, status=status.HTTP_404_NOT_FOUND)


class ClassroomAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClassroomSerializer
    queryset = Classroom.objects.all()

    def get(self, request, classroom_id=None, *args, **kwargs):
        if classroom_id:
            try:
                classroom = Classroom.objects.get(id=classroom_id)
                serializer = self.serializer_class(classroom)
                return Response({"Classroom": serializer.data})
            except Classroom.DoesNotExist:
                return Response({"Error": "Classroom not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            classrooms = Classroom.objects.all()
            serializer = self.serializer_class(classrooms, many=True)
            return Response({"Classrooms": serializer.data})

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            classroom = serializer.save()
            return Response({"Success": f"Classroom '{classroom.name}' created successfully."}, status=status.HTTP_201_CREATED)
        return Response({"Error": "Invalid data provided."}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, classroom_id=None, *args, **kwargs):
        try:
            classroom = Classroom.objects.get(id=classroom_id)
            serializer = self.serializer_class(classroom, data=request.data)
            if serializer.is_valid():
                updated_classroom = serializer.save()
                return Response({"Success": f"Classroom '{updated_classroom.name}' updated successfully."})
            return Response({"Error": "Invalid data provided."}, status=status.HTTP_400_BAD_REQUEST)
        except Classroom.DoesNotExist:
            return Response({"Error": "Classroom not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, classroom_id=None, *args, **kwargs):
        try:
            classroom = Classroom.objects.get(id=classroom_id)
            classroom.delete()
            return Response({"Success": "Classroom deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Classroom.DoesNotExist:
            return Response({"Error": "Classroom not found."}, status=status.HTTP_404_NOT_FOUND)


class SubjectAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubjectSerializer
    queryset = Subject.objects.all()

    def get(self, request, subject_id=None, *args, **kwargs):
        if subject_id:
            try:
                subject = Subject.objects.get(id=subject_id)
                serializer = self.serializer_class(subject)
                return Response({"Subject": serializer.data})
            except Subject.DoesNotExist:
                return Response({"Error": "Subject not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            subjects = Subject.objects.all()
            serializer = self.serializer_class(subjects, many=True)
            return Response({"Subjects": serializer.data})

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            subject = serializer.save()
            return Response({"Success": f"Subject '{subject.name}' created successfully."}, status=status.HTTP_201_CREATED)
        return Response({"Error": "Invalid data provided."}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, subject_id=None, *args, **kwargs):
        try:
            subject = Subject.objects.get(id=subject_id)
            serializer = self.serializer_class(subject, data=request.data)
            if serializer.is_valid():
                updated_subject = serializer.save()
                return Response({"Success": f"Subject '{updated_subject.name}' updated successfully."})
            return Response({"Error": "Invalid data provided."}, status=status.HTTP_400_BAD_REQUEST)
        except Subject.DoesNotExist:
            return Response({"Error": "Subject not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, subject_id=None, *args, **kwargs):
        try:
            subject = Subject.objects.get(id=subject_id)
            subject.delete()
            return Response({"Success": "Subject deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Subject.DoesNotExist:
            return Response({"Error": "Subject not found."}, status=status.HTTP_404_NOT_FOUND)


class KlassAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = KlassSerializer
    queryset = Klass.objects.all()

    def get(self, request, klass_id=None, *args, **kwargs):
        if klass_id:
            try:
                klass = Klass.objects.get(id=klass_id)
                serializer = self.serializer_class(klass)
                return Response({"Klass": serializer.data})
            except Klass.DoesNotExist:
                return Response({"Error": "Klass not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            klasses = Klass.objects.all()
            serializer = self.serializer_class(klasses, many=True)
            return Response({"Klasses": serializer.data})

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            klass = serializer.save()
            return Response({"Success": f"Klass '{klass.name}' created successfully."}, status=status.HTTP_201_CREATED)
        return Response({"Error": "Invalid data provided."}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, klass_id=None, *args, **kwargs):
        try:
            klass = Klass.objects.get(id=klass_id)
            serializer = self.serializer_class(klass, data=request.data)
            if serializer.is_valid():
                updated_klass = serializer.save()
                return Response({"Success": f"Klass '{updated_klass.name}' updated successfully."})
            return Response({"Error": "Invalid data provided."}, status=status.HTTP_400_BAD_REQUEST)
        except Klass.DoesNotExist:
            return Response({"Error": "Klass not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, klass_id=None, *args, **kwargs):
        try:
            klass = Klass.objects.get(id=klass_id)
            klass.delete()
            return Response({"Success": "Klass deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Klass.DoesNotExist:
            return Response({"Error": "Klass not found."}, status=status.HTTP_404_NOT_FOUND)


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
            klass = Klass.objects.get(id=klass_id)
            students = Student.objects.filter(klass__id=klass_id)
            grades = QuarterGrade.objects.filter(student__klass__id=klass_id)
            subjects = Subject.objects.all()
            report = {}

            for subject in subjects:
                subject_grades = grades.filter(subject=subject)
                if subject_grades.exists():
                    avg_grade = subject_grades.aggregate(avg=Avg('grade'))['avg']
                    report[subject.name] = {
                        "average_grade": avg_grade,
                        "grades": QuarterGradeSerializer(subject_grades, many=True).data
                    }

            class_teacher = klass.class_teacher
            class_teacher_data = TeacherSerializer(class_teacher).data if class_teacher else None
            total_students = students.count()

            response_data = {
                "class_teacher": class_teacher_data,
                "total_students": total_students,
                "report": report
            }

            return Response(response_data)

        except Klass.DoesNotExist:
            return Response({"Error": "Class not found."}, status=status.HTTP_404_NOT_FOUND)