from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from .models import Issue, Comment, Department, IssueCategory, Course

class UserRegistrationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('lecturer', 'Lecturer'),
        ('registrar', 'Academic Registrar'),
    ]
    
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)
    student_number = forms.CharField(max_length=20, required=False)
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'role', 'student_number', 'department', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        role = self.cleaned_data['role']
        
        if commit:
            user.save()
            # Assign user to appropriate group
            group, _ = Group.objects.get_or_create(name=role)
            user.groups.add(group)
            
            # Save additional profile info if needed
            if role == 'student':
                user.profile.student_number = self.cleaned_data['student_number']
            if role in ['lecturer', 'registrar']:
                user.profile.department = self.cleaned_data['department']
            user.profile.save()
        
        return user

class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['title', 'description', 'category', 'course', 'semester', 
                 'academic_year', 'attachment', 'priority']
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user and user.groups.filter(name='student').exists():
            # Students can only select their enrolled courses
            self.fields['course'].queryset = Course.objects.all()  # You might want to filter this based on student's department
            self.fields['priority'].widget = forms.HiddenInput()  # Students don't set priority

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'attachment']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a comment...'}),
        }

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'code', 'head_of_department', 'lecturers']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show users who are lecturers
        lecturer_group = Group.objects.get(name='lecturer')
        self.fields['head_of_department'].queryset = User.objects.filter(groups=lecturer_group)
        self.fields['lecturers'].queryset = User.objects.filter(groups=lecturer_group)
        
        # Add Bootstrap classes
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['lecturers'].widget.attrs.update({'class': 'form-control select2'})

class IssueCategoryForm(forms.ModelForm):
    class Meta:
        model = IssueCategory
        fields = ['name', 'category_type', 'description', 'department']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['code', 'name', 'department']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class IssueStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['status', 'assigned_to']
