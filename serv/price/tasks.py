from serv.celery import app
from .price_file_prepare import parser_xlsx


@app.task
def my_task(params):
	p='print task: {}'.format(params)
	print(p)
	return 'get params: {}'.format(params)


@app.task
def parse_price_file(params):
	return parser_xlsx(params)
