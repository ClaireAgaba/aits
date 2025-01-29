from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Issue, Comment, Department, IssueCategory, IssueHistory, Course
from .forms import (
    IssueForm, CommentForm, UserRegistrationForm,
    DepartmentForm, IssueCategoryForm, IssueStatusUpdateForm, CourseForm
)

def is_registrar(user):
    return user.groups.filter(name='registrar').exists()

def is_lecturer(user):
    return user.groups.filter(name='lecturer').exists()

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! You can now login.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'issues/register.html', {'form': form})

@login_required
def dashboard(request):
    context = {
        'pending_issues': Issue.objects.filter(status='pending').count(),
        'in_progress_issues': Issue.objects.filter(status='in_progress').count(),
        'resolved_issues': Issue.objects.filter(status='resolved').count(),
        'my_issues': Issue.objects.filter(created_by=request.user).order_by('-created_at')[:5],
        'assigned_issues': Issue.objects.filter(assigned_to=request.user).order_by('-created_at')[:5],
    }
    return render(request, 'issues/dashboard.html', context)

class IssueListView(LoginRequiredMixin, ListView):
    model = Issue
    template_name = 'issues/issue_list.html'
    context_object_name = 'issues'
    ordering = ['-created_at']
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status')
        priority = self.request.GET.get('priority')
        category = self.request.GET.get('category')
        
        if status:
            queryset = queryset.filter(status=status)
        if priority:
            queryset = queryset.filter(priority=priority)
        if category:
            queryset = queryset.filter(category_id=category)
            
        return queryset

class IssueDetailView(LoginRequiredMixin, DetailView):
    model = Issue
    template_name = 'issues/issue_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['status_form'] = IssueStatusUpdateForm(instance=self.object)
        return context

class IssueCreateView(LoginRequiredMixin, CreateView):
    model = Issue
    form_class = IssueForm
    template_name = 'issues/issue_form.html'
    success_url = reverse_lazy('issue-list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        IssueHistory.objects.create(
            issue=self.object,
            user=self.request.user,
            action="Created the issue"
        )
        messages.success(self.request, 'Issue created successfully!')
        return response

@login_required
def add_comment(request, pk):
    issue = get_object_or_404(Issue, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.issue = issue
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
    return redirect('issue-detail', pk=pk)

@login_required
def update_issue_status(request, pk):
    issue = get_object_or_404(Issue, pk=pk)
    if request.method == 'POST':
        form = IssueStatusUpdateForm(request.POST, instance=issue)
        if form.is_valid():
            old_status = issue.status
            new_status = form.cleaned_data['status']
            issue = form.save()
            
            if old_status != new_status:
                if new_status == 'resolved':
                    issue.resolved_at = timezone.now()
                    issue.save()
                
                IssueHistory.objects.create(
                    issue=issue,
                    user=request.user,
                    action=f"Changed status from {old_status} to {new_status}"
                )
                
            messages.success(request, 'Issue status updated successfully!')
    return redirect('issue-detail', pk=pk)

# Registrar Management Views
class DepartmentListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Department
    template_name = 'issues/department_list.html'
    context_object_name = 'departments'
    
    def test_func(self):
        return is_registrar(self.request.user)

class DepartmentDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Department
    template_name = 'issues/department_detail.html'
    
    def test_func(self):
        return is_registrar(self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = self.object.courses.all()
        context['lecturers'] = self.object.lecturers.all()
        return context

class DepartmentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'issues/department_form.html'
    success_url = reverse_lazy('department-list')
    
    def test_func(self):
        return is_registrar(self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, 'Department created successfully!')
        return super().form_valid(form)

class DepartmentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'issues/department_form.html'
    success_url = reverse_lazy('department-list')
    
    def test_func(self):
        return is_registrar(self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, 'Department updated successfully!')
        return super().form_valid(form)

class CourseListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Course
    template_name = 'issues/course_list.html'
    context_object_name = 'courses'
    
    def test_func(self):
        return is_registrar(self.request.user)

class CourseCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'issues/course_form.html'
    success_url = reverse_lazy('course-list')
    
    def test_func(self):
        return is_registrar(self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, 'Course created successfully!')
        return super().form_valid(form)

class CourseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'issues/course_form.html'
    success_url = reverse_lazy('course-list')
    
    def test_func(self):
        return is_registrar(self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, 'Course updated successfully!')
        return super().form_valid(form)

class IssueCategoryListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = IssueCategory
    template_name = 'issues/category_list.html'
    context_object_name = 'categories'
    
    def test_func(self):
        return is_registrar(self.request.user)

class IssueCategoryCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = IssueCategory
    form_class = IssueCategoryForm
    template_name = 'issues/category_form.html'
    success_url = reverse_lazy('category-list')
    
    def test_func(self):
        return is_registrar(self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, 'Category created successfully!')
        return super().form_valid(form)
