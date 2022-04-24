from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from catalog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomeView.as_view(), name = 'home'),
    path('list_product', views.ListProduct.as_view(), name='list_product'),
    path('detail/<slug>', views.DetailProduct.as_view(), name='detail'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('increase-cant/<pk>', views.Increase.as_view(), name='increase'),
    path('decrease-cant/<pk>', views.Decrease.as_view(), name='decrease')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
