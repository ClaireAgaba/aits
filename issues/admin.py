from django.contrib import admin
from .models import Department, IssueCategory, Issue, Comment, IssueHistory

# Register your models here.

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'created_at')
    search_fields = ('name', 'code')
    ordering = ('name',)

@admin.register(IssueCategory)
class IssueCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'created_at')
    list_filter = ('department',)
    search_fields = ('name', 'department__name')
    ordering = ('name',)

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'priority', 'created_by', 'assigned_to', 'created_at')
    list_filter = ('status', 'priority', 'category', 'created_at')
    search_fields = ('title', 'description', 'created_by__username', 'assigned_to__username')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('issue', 'author', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'author__username', 'issue__title')
    ordering = ('-created_at',)

@admin.register(IssueHistory)
class IssueHistoryAdmin(admin.ModelAdmin):
    list_display = ('issue', 'user', 'action', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('issue__title', 'user__username', 'action')
    ordering = ('-timestamp',)
