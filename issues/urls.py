from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Authentication URLs
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='issues/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Department Management
    path('departments/', views.DepartmentListView.as_view(), name='department-list'),
    path('departments/new/', views.DepartmentCreateView.as_view(), name='department-create'),
    path('departments/<int:pk>/', views.DepartmentDetailView.as_view(), name='department-detail'),
    path('departments/<int:pk>/edit/', views.DepartmentUpdateView.as_view(), name='department-update'),
    
    # Course Management
    path('courses/', views.CourseListView.as_view(), name='course-list'),
    path('courses/new/', views.CourseCreateView.as_view(), name='course-create'),
    path('courses/<int:pk>/edit/', views.CourseUpdateView.as_view(), name='course-update'),
    
    # Category Management
    path('categories/', views.IssueCategoryListView.as_view(), name='category-list'),
    path('categories/new/', views.IssueCategoryCreateView.as_view(), name='category-create'),
    
    # Issue Management
    path('issues/', views.IssueListView.as_view(), name='issue-list'),
    path('issues/new/', views.IssueCreateView.as_view(), name='issue-create'),
    path('issues/<int:pk>/', views.IssueDetailView.as_view(), name='issue-detail'),
    path('issues/<int:pk>/comment/', views.add_comment, name='add-comment'),
    path('issues/<int:pk>/status/', views.update_issue_status, name='update-status'),
]
