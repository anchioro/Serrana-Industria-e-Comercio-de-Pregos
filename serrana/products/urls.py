from django.urls import path
from .views.product_management import ProductListView, ProductUpdateView, ProductCreateView, ProductSearchView, ProductDeleteView, ProductHistoryView, ProductInformationView
from django.views.generic import RedirectView

app_name = "products"
urlpatterns = [
    path("", ProductListView.as_view(), name="index"),
    path("cadastro", ProductCreateView.as_view(), name="create"),
    path("search", ProductSearchView.as_view(), name="search"),
    path("<slug:slug>/edit", ProductUpdateView.as_view(), name="update"),
    path("<int:pk>/delete", ProductDeleteView.as_view(), name="delete"),
    path("<slug:slug>/history", ProductHistoryView.as_view(), name="history"),
    path("<slug:slug>/info", ProductInformationView.as_view(), name="information"),
    path("<slug:slug>/", RedirectView.as_view(pattern_name="products:information", permanent=False)),
]