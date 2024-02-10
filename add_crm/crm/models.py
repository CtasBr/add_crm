from django.db import models


class Task(models.Model):
    """Задачи

    Поля:
        Название
        Описание
        Изображение
        Дата создания
        Дэдлайн
        #todo Подумать про количество подзадач
        Количество подзадач
        Состояние выполненности
    """
    
    class Meta:
        db_table = "tasks"
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
    
    title = models.TextField(verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    img = models.ImageField(verbose_name="Изображение", blank=True, upload_to='photos/%Y/%m/%d/')
    date_add = models.DateField(verbose_name="Дата создания", auto_now_add=True)
    deadline = models.DecimalField(verbose_name="Дата сдачи", blank=True)
    done = models.BooleanField(verbose_name="Выполнено")
    
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
        
    title = models.TextField(verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    date_add = models.DateField(verbose_name="Дата создания", auto_now_add=True)
    deadline = models.DecimalField(verbose_name="Дата сдачи", blank=True)
    main_task_id = models.ForeignKey(to="Task", on_delete=models.PROTECT)
    done = models.BooleanField(verbose_name="Выполнено")
    executors_id = models.ManyToManyField("User")
    

class User(models.Model):
    """Пользователи

    Поля:
        Имя
        Имя пользователя в ТГ
    """
    
    class Meta:
        db_table = "users"
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
    
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, blank=True)