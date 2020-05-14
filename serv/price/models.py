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
    FILE_STATUS = (
        (0, 'Загружен',),
        (1, 'В очереди на обработку',),
        (2, 'В процессе обработки',),
        (3, 'Обработан',),
    )
    status = models.SmallIntegerField(choices=FILE_STATUS, default=0, verbose_name='Статус')
    """
        {
            'price_name':'',   Название прайса (строка)
            'sn':0,            Парт-номер (номер колонки)
            'name':0,          Название запчасти (номер колонки)
            'price':0,         Цена (номер колонки)
        }
    """
    params = models.TextField(default="", blank=True, verbose_name='Параметры', help_text='JSON объект. Значения для парсинга')
    log = models.TextField(default="", blank=True, verbose_name='Лог', help_text='ошибки, сообщения, отладочная информация')
    date_create = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    def delete(self, *args, **kwargs):
        """Удаляем файлы при удалении записи"""
        self.file.delete(save=False)


class PriceList(models.Model):
    class Meta:
        verbose_name = 'Прайс-лист'
        verbose_name_plural = 'Прайс-листы'

    part_num = models.CharField(max_length=60, verbose_name='Парт номер')
    name = models.CharField(max_length=128, verbose_name='Название')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена', default=0.0)
    price_name = models.CharField(max_length=60, verbose_name='Название прайса')

    date_updated = models.DateTimeField(auto_now=True)
    #author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Автор', help_text='Пользователь который сохранил')
    #company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='Компания', help_text='Компания, пользователи которой имеют доступ к сохраненному объекту')

    def __str__(self):
        return self.part_num
