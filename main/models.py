from django.db import models

class Joke(models.Model):
    title = models.CharField('Заголовок', max_length=255)
    joke = models.TextField('Анекдот')
    votes = models.IntegerField('Голоса', default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Анекдот'
        verbose_name_plural = 'Анекдоты'

