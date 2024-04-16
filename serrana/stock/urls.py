from django.urls import path
from .views.stock_management import StockListView, StockUpdateView, StockCreateView, StockSearchView, StockDeleteView, StockHistoryView, StockInformationView, StockActionView

app_name = "stock"
urlpatterns = [
    path("", StockListView.as_view(), name="index"),
    path("cadastro/", StockCreateView.as_view(), name="create"),
    path("search/", StockSearchView.as_view(), name="search"),
    path("<int:pk>/delete/", StockDeleteView.as_view(), name="delete"),
    path("<slug:slug>/edit/", StockUpdateView.as_view(), name="update"),
    path("<slug:slug>/history/", StockHistoryView.as_view(), name="history"),
    path("<slug:slug>/action/", StockActionView.as_view(), name="action"),
    path("<slug:slug>/", StockInformationView.as_view(), name="information"),
]
