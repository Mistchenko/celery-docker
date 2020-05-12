from django.shortcuts import render

from .models import PriceFile
from .tasks import my_task, parse_price_file


def index(request):
	val = '?'
	post_val = request.POST.get('val')
	if post_val:
		# назначаем задание
		my_task.delay(post_val)
		
		val = post_val

	price_file = request.FILES.get('price_file')
	if price_file:
		# print(price_file.name)
		# print(price_file.temporary_file_path())
		pf = PriceFile(name=price_file.name, file=price_file)
		pf.save()
		print('\nPriceFile >> id:', pf.id, '\tname:', pf.name, '\tfile:', pf.file)
		parse_price_file.delay(pf.id)

	data = {
		'val': val
	}
	return render(request, 'price/index.html', data)
