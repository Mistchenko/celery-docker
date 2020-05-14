import os
import json
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

import xlrd
from .models import PriceFile, PriceList
from tools.serializer import as_int, as_decimal


def parser_xlsx(pf):
    # pf: словарь с параметрами
    """
        'id': 1,        ID записи модели PriceFile
    """
    err = ''
    try:
        parse_file = PriceFile.objects.get(id=pf['id'])
    except ObjectDoesNotExist:
        #parse_file = None
        return 'PriceFile c ID={} не найден'.format(pf['id'])

    # Статус: В обработке
    parse_file.status = 2
    parse_file.save()

    file_path = os.path.join(settings.MEDIA_ROOT, parse_file.file.name)

    try:
        params = json.loads(parse_file.params)
    except json.decoder.JSONDecodeError as e:
        params = {}
        err = str(e)

    col_sn = as_int(params.get('sn'))
    col_name = as_int(params.get('name'))
    col_price = as_int(params.get('price'))
    all_save = 0  # Всего сохранено цен в PriceList
    if col_sn > 0 and col_name > 0 and col_price > 0:
        # Парсинг xlrd
        try:
            book = xlrd.open_workbook(file_path, on_demand=True)
            sheet = book.sheet_by_index(0)
        except:
            book = None
            err = 'Ошибка открытия файла, вероятно неверный формат'

        if book:
            #print('cell:', sheet.cell(0, 0).value)
            row_no_sn = []
            row_no_name = []
            row_no_price = []
            #print('nrows', sheet.nrows)
            if sheet.nrows == 0:
                err = '{}\nВ документе отсутствуют строки'.format(err)

            if col_sn > sheet.ncols:
                err = '{}\nНомер колонки с парт-номером: {}, больше количества колонок [{}] в документе'.format(err, col_sn, sheet.ncols)

            if col_name > sheet.ncols:
                err = '{}\nНомер колонки с наименованием: {}, больше количества колонок [{}] в документе'.format(err, col_name, sheet.ncols)

            if col_price > sheet.ncols:
                err = '{}\nНомер колонки с ценой: {}, больше количества колонок [{}] в документе'.format(err, col_price, sheet.ncols)

            if len(err) == 0:
                for i, row in enumerate(sheet.get_rows()):
                    # Параметры ячейки
                    # https://xlrd.readthedocs.io/en/latest/api.html#xlrd.sheet.Cell
                    #print(i, 'row:', row[0].value, '\t', row[1].ctype, '\t', row[2], '\t', row[3].value)
                    row_err = 0
                    part_num = str(row[col_sn-1].value).strip()
                    if len(part_num) == 0:
                        row_err += 1
                        row_no_sn.append(str(i+1))

                    part_name = str(row[col_name-1].value).strip()
                    if len(part_name) == 0:
                        row_err += 1
                        row_no_name.append(str(i+1))

                    part_price_type = row[col_price-1].ctype
                    part_price = 0
                    # https://xlrd.readthedocs.io/en/latest/api.html#xlrd.sheet.Cell
                    if part_price_type != 2:
                        row_err += 1
                        row_no_price.append(str(i+1))
                    else:
                        part_price = as_decimal(row[col_price - 1].value)
                        if part_price == 0:
                            row_err += 1
                            row_no_price.append(str(i+1))

                    if row_err == 0:
                        # Если нет ошибок
                        PriceList.objects.update_or_create(
                            part_num=part_num,
                            price_name=parse_file.name,
                            defaults={
                                'name': part_name,
                                'price': part_price,
                            }
                        )
                        all_save += 1
                if len(row_no_sn):
                    s = 'Строки без парт-номера: {}'.format(','.join(row_no_sn))
                    err = '{}\n{}'.format(err, s)

                if len(row_no_name):
                    s = 'Строки без наименования: {}'.format(','.join(row_no_name))
                    err = '{}\n{}'.format(err, s)

                if len(row_no_price):
                    s = 'Строки без цены: {}'.format(','.join(row_no_price))
                    err = '{}\n{}'.format(err, s)

    else:
        err = '{}\n{}'.format(err, 'Неверные парметры для парсинга файла')

    # Статус: Обработан
    parse_file.status = 3
    parse_file.log = 'Всего сохранено цен в прас-лист: {} {}'.format(all_save, err)
    parse_file.save()

    if len(err) > 0:
        return err
    else:
        return 'Ok'
