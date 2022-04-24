from catalog import models


def get_or_set_order_session(request):
	"""Con esto podemos agregar al carito y hara
	relacion al usuario
	"""
	order_id = request.session.get('order_id', None)
	if order_id is None:
		order = models.Order()
		order.save()
		request.session['order_id'] = order.id

	else:
		try:
			order = models.Order.objects.get(id=order_id, transaccion_id=False)
		except models.Order().DoesNotExist:		
			order = models.Order()
			order.save()
			request.session['order_id'] = order.id
	
	if request.user.is_authenticated :
		order.client = request.user
		order.save()

	return order