from rest_framework import serializers
from .models import Teacher, Student, QuarterGrade, Lesson, Classroom, Subject, Klass

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"

class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = "__all__"

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"

class QuarterGradeSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer()
    student = StudentSerializer()

    class Meta:
        model = QuarterGrade
        fields = ['id', 'student', 'subject', 'grade', 'date']

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Klass
        fields = "__all__"

class KlassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Klass
        fields = "__all__"

class TeacherSerializer(serializers.ModelSerializer):
    class_lead = KlassSerializer()
    classroom = ClassroomSerializer()
    subject = SubjectSerializer(many=True)

    class Meta:
        model = Teacher
        fields = [
            'id', 'first_name', 'last_name', 'middle_name', 'class_lead', 'classroom', 'subject'
        ]