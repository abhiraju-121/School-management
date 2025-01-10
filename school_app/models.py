from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    name=models.CharField(max_length=200)
    description=models.TextField()

    def __str__(self):
        return self.name
    

class Subject(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE,related_name="subjects")
    sub_name=models.CharField(max_length=200)
    is_removed = models.BooleanField(default=False)

    def __str__(self):
        return self.sub_name

class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subjects=models.ManyToManyField(Subject,related_name="subjects")
    full_name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=10, unique=True)
    date_of_birth = models.DateField()
    score=models.IntegerField(default=0)
    is_approved = models.BooleanField(default=False)
    

    def __str__(self):
        return self.user.username

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username
    

class Question(models.Model):
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text} (Correct)" if self.is_correct else self.text

class Books(models.Model):
    author=models.ForeignKey(Teacher,on_delete=models.CASCADE)
    name=models.CharField(max_length=150)
    image=models.ImageField(upload_to='books/')
    desc= models.CharField(max_length=200)
    price=models.DecimalField(decimal_places=2,max_digits=10)
    cart=models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
