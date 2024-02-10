from django.urls import path
from .views.product_management import ProductListView, ProductUpdateView, ProductCreateView, ProductSearchView

app_name = "products"
urlpatterns = [
    path("produtos/", ProductListView.as_view(), name="index"),
    path("produtos/cadastro", ProductCreateView.as_view(), name="create"),
    path("products/search", ProductSearchView.as_view(), name="search"),
    path("products/<slug:slug>/", ProductUpdateView.as_view(), name="update"),
]
