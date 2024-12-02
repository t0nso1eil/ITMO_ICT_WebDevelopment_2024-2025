from django.contrib import admin
from .models import Class, Teacher, Student, QuarterGrade, Classroom, Lesson, Subject

admin.site.register(Class)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(QuarterGrade)
admin.site.register(Classroom)
admin.site.register(Lesson)
admin.site.register(Subject)