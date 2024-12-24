from rest_framework import serializers
from .models import Teacher, Student, QuarterGrade, Lesson, Classroom, Subject, Klass

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = "__all__"

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"

class QuarterGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuarterGrade
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

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Klass
        fields = "__all__"

class KlassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Klass
        fields = "__all__"