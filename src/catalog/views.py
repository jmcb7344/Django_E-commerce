from django.shortcuts import render
from django.views import generic
from catalog import models

# Create your views here.
class HomeView(generic.TemplateView):
	''' 
	Vista prinpical de la tienda 
	'''
	template_name = 'index.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Music Store'
		return context

class ListProduct(generic.ListView):
	pass

class DetailProduct(generic.DetailView):
	model = models.Product

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Detail Product'
		return context