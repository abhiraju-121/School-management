from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('index',views.index,name='index'),
    path('t_index',views.t_index,name='t_index'),
    path('register', views.student_register_view,name='register'),
    path('teacher', views.teacher_register_view, name='teacher'),
    path('login', views.login_view, name='login'),
    path('dashboard', views.dashboard_view, name='dashboard'),
    path('logout', views.logout_view, name='logout'),
    path('add_course',views.add_course,name='add_course'),
    path('add_subject',views.add_subject,name='add_subject'),
    path('remove_sub/<int:subject_id>/', views.remove_subject, name='remove_sub'),
    path('t_dash',views.t_dash,name='t_dash'),
    path('t_login/', views.teacher_login_view, name='teacher_login'),
    path('t_logout/', views.teacher_logout_view, name='teacher_logout'),
    path('q_dashboard/', views.question_view, name='q_dashboard'),
    path('retry',views.retry,name='retry'),
    path('book',views.book,name='book'),
    path('purchase/<int:book_id>/', views.purchase_book, name='purchase'),
    path('b_details/<int:book_id>/', views.book_detail, name='b_details'),
    path('cart_page/add/<int:book_id>/',views.cart_page,name='cart_page'),
    path('cart/', views.cart_page, name='view_cart'),
    # path('cart_page/remove/<int:book_id>/',views.remove_cart,name='remove_cart'),
    path('success',views.success_pur,name='success'),
]
