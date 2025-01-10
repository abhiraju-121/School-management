from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Student, Teacher,Subject,Course,Question,Choice,Books
from .forms import SubjectForm,CourseForm
from django.contrib import messages
from django.urls import reverse



def home(request):
    return render(request,'home.html')

def index(request):
    return render(request,'index.html')

def t_index(request):
    return render(request,'t_index.html')

def student_register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        full_name = request.POST['full_name']
        roll_number = request.POST['roll_number']
        date_of_birth = request.POST['date_of_birth']
        
        
        user = User.objects.create_user(username=username, password=password)
        
        Student.objects.create(
            user=user,
            full_name=full_name,
            roll_number=roll_number,
            date_of_birth=date_of_birth,
            is_approved=False 
        )
        return redirect('login')
    return render(request, 'student_register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if hasattr(user, 'student') and not user.student.is_approved:
                return render(request, 'not_approved.html')
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password")
            return render(request, 'login.html')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('home')

def teacher_register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        full_name = request.POST['full_name']
        subject = request.POST['subject']
        
        user = User.objects.create_user(username=username, password=password)
    
        Teacher.objects.create(
            user=user,
            full_name=full_name,
            subject=subject
        )
        
        return redirect('teacher_login')
    return render(request, 'teacher_register.html')

def teacher_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('t_dash')
        else:
            messages.error(request, 'Invalid username or password')
        return redirect('teacher_login')
    
    return render(request, 't_login.html')

def teacher_logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def add_course(request):
    if request.method == "POST":
        form=CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:   
        form=CourseForm()
    return render(request,'add_course.html',{'form':form})

@login_required
def add_subject(request):
    if request.method == "POST":
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save()
            student = get_object_or_404(Student, user=request.user)
            student.subjects.add(subject)
            return redirect('dashboard')
    else:
        form = SubjectForm()
    return render(request, 'add_subject.html', {'form': form})


@login_required
def remove_subject(request, subject_id):
    student = get_object_or_404(Student, user=request.user)
    subject = get_object_or_404(Subject, id=subject_id)
    student.subjects.remove(subject)
    subject.is_removed=True
    subject.save()
    return redirect('dashboard')


@login_required
def dashboard_view(request):
    student = get_object_or_404(Student, user=request.user)
    subjects = student.subjects.all()
    available_subjects=Subject.objects.exclude(id__in=subjects.values_list('id',flat=True)).filter(is_removed=True)
    courses = Course.objects.all() 
    # teachers = Teacher.objects.all()

    return render(request, 'dashboard.html', {
        'student': student,
        'subjects': subjects,
        'available_subjects':available_subjects,
        'courses': courses
        # 'teachers': teachers,
    })

def t_dash(request):
    teacher=Teacher.objects.get(user=request.user)
    return render(request,'t_dashboard.html',{'teacher':teacher})



@login_required
def question_view(request):
    questions = list(Question.objects.all())
    if not questions:
        return render(request, 'result.html', {'error': "No questions available."})

    current_index = int(request.GET.get('current_index', 0))
    score = int(request.GET.get('score', 0))

    if current_index >= len(questions):
        context = {
            'score': score,
            'total': len(questions),
        }
        return render(request, 'result.html', context)

    question = questions[current_index]
    choices = question.choices.all()
    result = None

    if request.method == 'POST':
        if 'previous' in request.POST and current_index > 0:
    
            return redirect(f"{reverse('q_dashboard')}?current_index={current_index - 1}&score={score}")

        selected_choice_id = request.POST.get('choice')
        if selected_choice_id:
            selected_choice = choices.filter(id=selected_choice_id).first()
            if selected_choice:
                if selected_choice.is_correct:
                    result = "Correct!"
                    score += 1
                else:
                    result = "Incorrect. Try again!"
          
            return redirect(f"{reverse('q_dashboard')}?current_index={current_index + 1}&score={score}")

    context = {
        'question': question,
        'choices': choices,
        'result': result,
        'current_index': current_index + 1,
        'total_questions': len(questions),
    }
    return render(request, 'q_dashboard.html', context)

def retry(request):
    return redirect('q_dashboard')


def book(request):
    books=Books.objects.all()
    return render(request,'Book.html',{'books':books})


def book_detail(request,book_id):
    book=get_object_or_404(Books,id=book_id)
    return render(request,'b_detail.html',{'book':book})


def purchase_book(request,book_id):
    book=get_object_or_404(Books,id=book_id)
    messages.success(request,f'You have successfully purchased "{book.name}".')
    return redirect('b_details', book_id=book_id)

def cart_page(request, book_id=None):
    cart = request.session.get('cart', {})
    if book_id:
        book = get_object_or_404(Books, id=book_id)
        if str(book_id) in cart:
            cart[str(book_id)]['quantity'] += 1
            cart[str(book_id)]['subtotal'] = float(cart[str(book_id)]['quantity'] * book.price)
        else:
            cart[str(book_id)] = {
                'name': book.name,
                'price': float(book.price), 
                'quantity': 1,
                'subtotal': float(book.price),
            }
        request.session['cart'] = cart
        book.cart = True
        book.save()
    total_price = sum(item['subtotal'] for item in cart.values())
    return render(request, 'cart.html', {'cart': cart, 'total_price': total_price})



# def remove_cart(request, book_id):
#     cart = request.session.get('cart', {})
#     if str(book_id) in cart:
#         del cart[str(book_id)]
#         request.session['cart'] = cart
#         request.session.modified = True  # Ensure session is updated
#     return redirect('cart_page')

def success_pur(request):
    return render(request,'purchase_success.html')