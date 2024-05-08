from django.contrib.auth.models import User
from django.db import models


class Project(models.Model):
    """Проекты

    Поля:
        Название
        Описание
        Дата добавления
        Срок сдачи
        Готовность
    """
    class Meta:
        db_table = "projects"
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"
    
    title = models.CharField(verbose_name="Название", max_length=500)
    description = models.TextField(verbose_name="Описание")
    date_add = models.DateField(verbose_name="Дата начала")
    deadline = models.DateField(verbose_name="Дата сдачи", blank=True)
    is_done = models.BooleanField(verbose_name="Выполнено")
    
    def __str__(self):
        return self.title

class Task(models.Model):
    """Задачи

    Поля:
        Название
        Описание
        Изображение
        Дата создания
        Дэдлайн
        Количество подзадач
        Состояние выполненности
    """
    
    class Meta:
        db_table = "tasks"
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
    
    title = models.CharField(verbose_name="Название", max_length=500)
    description = models.TextField(verbose_name="Описание")
    date_add = models.DateField(verbose_name="Дата начала")
    deadline = models.DateField(verbose_name="Дата сдачи", blank=True)
    main_project_id = models.ForeignKey(to="Project", on_delete=models.PROTECT)
    is_done = models.BooleanField(verbose_name="Выполнено")
    executors_id = models.ManyToManyField("Empl", blank=True)
    
    def __str__(self):
        return self.title
    

class Subtask(models.Model):
    """Подзадачи

    Поля:
        Название
        Описание
        Дата создания
        Срок сдачи
        Основная задача
        Готовность
    """
    class Meta:
        db_table = "subtasks"
        verbose_name = "Подзадача"
        verbose_name_plural = "Подзадачи"
        
    title = models.CharField(verbose_name="Название", max_length=500)
    date_add = models.DateField(verbose_name="Дата начала", auto_now=True)
    deadline = models.DateField(verbose_name="Дата сдачи", blank=True)
    main_task_id = models.ForeignKey(to="Task", on_delete=models.PROTECT)
    is_done = models.BooleanField(verbose_name="Выполнено")
    
    
    def __str__(self):
        return self.title


class Empl(models.Model):
    """Пользователи

    Поля:
        Имя
        Имя пользователя в ТГ
    """
    
    class Meta:
        db_table = "empl"
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
    
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.name
    
    

class Experiment(models.Model):
    
    class Meta:
        db_table = "experiments"
        verbose_name = "эксперимент"
        verbose_name_plural = "эксперименты"
    
    title = models.CharField(verbose_name="Название", max_length=500)
    instruction = models.TextField(verbose_name="Инструкция")
    main_project_id = models.ForeignKey(to="Project", on_delete=models.PROTECT)
    def __str__(self):
        return self.title 
    

class Variation(models.Model):
    
    class Meta:
        db_table = "Variation"
        verbose_name = "вариация эксперимента"
        verbose_name_plural = "вариации экспериментов"
        
    code = models.CharField(verbose_name="Шифр", max_length=20)
    date_start = models.DateField(verbose_name="Дата начала")
    date_end = models.DateField(verbose_name="Дата конца")
    comment = models.TextField(verbose_name="Комментарий")
    content = models.TextField(verbose_name="Изменения в составе")
    main_experiment_id = models.ForeignKey(to="Experiment", on_delete=models.PROTECT)
    def __str__(self):
        return self.code
    

class Comment(models.Model):
    class Meta:
        db_table = "comments"
        verbose_name = "комментарий"
        verbose_name_plural = "комментарии"
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    text = models.TextField(verbose_name="Текст")
    file = models.FileField(verbose_name="Файл", upload_to='comment_files/', blank=True, null=True)
    main_task_id = models.ForeignKey(to="Task", on_delete=models.PROTECT)
    
    def __str__(self):
        return str(self.id)