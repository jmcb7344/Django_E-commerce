from django import forms 
from catalog import models

class AddToCart(forms.ModelForm):

	class Meta:
		model = models.OrderItem
		fields = ['quantity']