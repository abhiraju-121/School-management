from django.contrib import admin
from .models import Student, Teacher,Subject,Course,Question,Choice,Books

@admin.action(description='Approve selected students')
def approve_students(modeladmin, request, queryset):
    queryset.update(is_approved=True)

class StudentAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'roll_number', 'is_approved']
    actions = [approve_students]

class TeacherAdmin(admin.ModelAdmin):
    list_display=['user','full_name','subject']


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4  

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]


class BookAdmin(admin.ModelAdmin):
    list_display=['author','name','image','desc','price']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher,TeacherAdmin)
admin.site.register(Subject)
admin.site.register(Course)
admin.site.register(Books,BookAdmin)


