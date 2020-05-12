from django.db import models


class PriceFile(models.Model):
    class Meta:
        verbose_name = 'Price файл'
        verbose_name_plural = 'Price файлы'
        ordering = ['name']

    def __str__(self):
        return self.name

    name = models.CharField(max_length=100, verbose_name='Наименование')
    file = models.FileField(max_length=100, upload_to='price_file/')

    def delete(self, *args, **kwargs):
        """Удаляем файлы при удалении записи"""
        self.file.delete(save=False)
