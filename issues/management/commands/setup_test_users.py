from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from issues.models import Issue, Department, Course

class Command(BaseCommand):
    help = 'Creates test users and groups for the system'

    def handle(self, *args, **kwargs):
        # Create groups
        student_group, _ = Group.objects.get_or_create(name='student')
        lecturer_group, _ = Group.objects.get_or_create(name='lecturer')
        registrar_group, _ = Group.objects.get_or_create(name='registrar')

        # Create a test department
        dept, _ = Department.objects.get_or_create(
            name='School of Computing and IT',
            code='SCIT'
        )

        # Create test users
        test_users = [
            {
                'username': 'student1',
                'email': 'student1@example.com',
                'password': 'testpass123',
                'group': student_group,
                'is_staff': False,
                'profile_data': {'student_number': 'S13/1234/2021'}
            },
            {
                'username': 'lecturer1',
                'email': 'lecturer1@example.com',
                'password': 'testpass123',
                'group': lecturer_group,
                'is_staff': True,
                'profile_data': {'department': dept}
            },
            {
                'username': 'registrar1',
                'email': 'registrar1@example.com',
                'password': 'testpass123',
                'group': registrar_group,
                'is_staff': True,
                'profile_data': {'department': dept}
            }
        ]

        for user_data in test_users:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                email=user_data['email']
            )
            if created:
                user.set_password(user_data['password'])
                user.is_staff = user_data['is_staff']
                user.save()
                user.groups.add(user_data['group'])
                
                # Update profile
                profile = user.profile
                if 'student_number' in user_data['profile_data']:
                    profile.student_number = user_data['profile_data']['student_number']
                if 'department' in user_data['profile_data']:
                    profile.department = user_data['profile_data']['department']
                profile.save()

                self.stdout.write(self.style.SUCCESS(f'Successfully created user: {user.username}'))
            else:
                self.stdout.write(f'User {user.username} already exists')
