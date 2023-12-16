from django.db import models
from django.contrib.auth.models import PermissionsMixin , UserManager, AbstractBaseUser
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import Group, Permission

class NewUserManager(UserManager):
    def create_user(self,email,password=None, **extra_fields):
        if not email:
            raise ValueError('User must have an email address')
        
        email = self.normalize_email(email) 
        user = self.model(email=email, **extra_fields) 
        user.set_password(password)
        user.save(using=self.db)
        return user
    class Meta:
        managed = True

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(("email адрес"), unique=True)
    password = models.CharField(max_length=150, verbose_name="Пароль") 
    full_name = models.CharField(max_length=50, default='', verbose_name='ФИО')
    phone_number = models.CharField(max_length=30, default='', verbose_name='Номер телефона')   
    is_staff = models.BooleanField(default=False, verbose_name="Является ли пользователь менеджером?")
    is_superuser = models.BooleanField(default=False, verbose_name="Является ли пользователь админом?")

    USERNAME_FIELD = 'email'

    groups = models.ManyToManyField(Group, related_name='custom_users', related_query_name='custom_user')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_users', related_query_name='custom_user')

    objects =  NewUserManager()

    class Meta:
        managed = True

class Responses(models.Model):
    STATUS_CHOICES = [
        ('registered', 'Зарегистрировано'),
        ('made', 'Сформировано'),
        ('approved', 'Принято'),
        ('denied', 'Отказано'),
        ('deleted', 'Отменено')
    ]
    status = models.CharField(max_length=255, blank=True, null=True, choices=STATUS_CHOICES)
    creation_date = models.DateTimeField(blank=True, null=True)
    editing_date = models.DateTimeField(blank=True, null=True)
    approving_date = models.DateTimeField(blank=True, null=True)
    id_moderator = models.ForeignKey('CustomUser', on_delete=models.CASCADE,  db_column='id_moderator', related_name='moderator_responses', blank=True, null=True)
    id_user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, db_column='id_user', related_name='user_responses')
    suite = models.CharField()

    class Meta:
        managed = False
        db_table = 'responses'


class ResponsesVacancies(models.Model):
    id_responses = models.ForeignKey('Responses', models.DO_NOTHING, db_column='id_responses', blank=True, null=True)
    id_vacancies = models.ForeignKey('Vacancies', models.DO_NOTHING, db_column='id_vacancies', blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['id_responses', 'id_vacancies'], name='composite_key')
        ]
        managed = False
        db_table = 'responses_vacancies'


# class Users(models.Model):
#     login = models.CharField(blank=True, null=True)
#     passw = models.CharField(blank=True, null=True)
#     role = models.CharField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'users'


class Vacancies(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    adress = models.CharField(max_length=255, blank=True, null=True)
    time = models.CharField(max_length=255, blank=True, null=True)
    salary = models.IntegerField()
    company = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True)
    exp = models.CharField(max_length=255, blank=True)
    image = models.TextField(blank=True, null=True)
    info = models.TextField(blank=True, null=True)
    # requirements = ArrayField(models.TextField(blank=True), blank=True)
    # conditions = ArrayField(models.TextField(blank=True), blank=True)
    STATUS_CHOICES = [
        ('enabled', 'enabled'),
        ('deleted', 'deleted'),
    ]
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='enabled')
    def __str__(self):
        return self.title
    # Остальные поля модели

    class Meta:
        managed = False
        db_table = 'vacancies'
