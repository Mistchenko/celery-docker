import os
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

import xlrd
from .models import PriceFile


def parser_xlsx(pf):
    # pf: словарь с параметрами
    """
        'id': 1,        ID записи модели PriceFile
        'sn': 0,        парт-номер запчасти [номер колонки]
        'name': 1,      наименование запчасти [номер колонки]
        'price': 3,     цена запчасти [номер колонки]
    """
    err = None
    try:
        parse_file = PriceFile.objects.get(id=pf['id'])
    except ObjectDoesNotExist:
        #parse_file = None
        return 'PriceFile c ID={} не найден'.format(pf['id'])

    file_path = os.path.join(settings.MEDIA_ROOT, parse_file.file.name)
    print('file_path:', file_path)

    # Парсинг xlrd
    book = xlrd.open_workbook(file_path, on_demand=True)
    sheet = book.sheet_by_index(0)
    #print('cell:', sheet.cell(0, 0).value)
    for row in sheet.get_rows():
        # Параметры ячейки
        # https://xlrd.readthedocs.io/en/latest/api.html#xlrd.sheet.Cell
        print('row:', row[0].value, '\t', row[1].ctype, '\t', row[2], '\t', row[3].value)
        part_num = row[pf['sn']].value
        part_name = row[pf['name']].value
        part_price_type = row[pf['price']].ctype
        part_price = row[pf['price']].value


    if err:
        return err
    else:
        return 'Ok'
