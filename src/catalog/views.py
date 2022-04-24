from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from catalog import models, utils, forms

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
    model = models.Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'List Product'
        return context

class DetailProduct(generic.DetailView):
    model = models.Product

    def get_object(self):
        return get_object_or_404(models.Product, slug=self.kwargs['slug'])

    def post(self, *args, **kwargs):
        order = utils.get_or_set_order_session(self.request)
        product = self.get_object()
        item_filter = order.item.filter(product=product)
        form = forms.AddToCart(self.request.POST)

        if item_filter.exists() and form.is_valid():
            item = item_filter.first()
            item.quantity = int(form.cleaned_data['quantity'])
            item.save()

        else:
            new_item = form.save(commit=False)
            new_item.product = product
            new_item.order = order
            new_item.save()
        
        return redirect('detail', slug=product.slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detail Product'
        context['forms'] = forms.AddToCart()
        context['prueba'] = self.get_object()
        return context

class CartView(generic.TemplateView):
    template_name = 'catalog/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Carrito de compras'
        context['order'] = utils.get_or_set_order_session(self.request)
        return context

class Increase(generic.View):

    def get(self, request, *args, **kwargs):
        order_item = get_object_or_404(models.OrderItem, id=kwargs['pk'])
        order_item.quantity += 1
        order_item.save()
        return redirect('cart')

class Decrease(generic.View):

    def get(self, request, *args, **kwargs):
        order_item = get_object_or_404(models.OrderItem, id=kwargs['pk'])
        if order_item.quantity <= 1:
            order_item.delete()
        else:
            order_item.quantity -= 1
            order_item.save()
        return redirect('cart')