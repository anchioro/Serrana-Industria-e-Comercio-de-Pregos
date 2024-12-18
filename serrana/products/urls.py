from django.urls import path
from .views.product_management import ProductListView, ProductUpdateView, ProductCreateView, ProductSearchView, ProductDeleteView, ProductHistoryView, ProductInformationView, ProductActionView

app_name = "products"
urlpatterns = [
    path("", ProductListView.as_view(), name="index"),
    path("cadastro/", ProductCreateView.as_view(), name="create"),
    path("search/", ProductSearchView.as_view(), name="search"),
    path("<int:pk>/delete/", ProductDeleteView.as_view(), name="delete"),
    path("<slug:slug>/edit/", ProductUpdateView.as_view(), name="update"),
    path("<slug:slug>/history/", ProductHistoryView.as_view(), name="history"),
    path("<slug:slug>/action/", ProductActionView.as_view(), name="action"),
    path("<slug:slug>/", ProductInformationView.as_view(), name="information"),
]
