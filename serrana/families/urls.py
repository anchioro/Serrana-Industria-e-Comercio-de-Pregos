from django.urls import path
from .views.family_management import FamilyListView, FamilyUpdateView, FamilyCreateView, FamilySearchView, FamilyDeleteView, FamilyInformationView, FamilyActionView, FamilyHistoryView, toggle_completion

app_name = "families"
urlpatterns = [
    path("", FamilyListView.as_view(), name="index"),
    path("cadastro/", FamilyCreateView.as_view(), name="create"),
    path("search/", FamilySearchView.as_view(), name="search"),
    path("<int:pk>/delete/", FamilyDeleteView.as_view(), name="delete"),
    path("<slug:slug>/edit/", FamilyUpdateView.as_view(), name="update"),
    path("<slug:slug>/action/", FamilyActionView.as_view(), name="action"),
    path("<slug:slug>/", FamilyInformationView.as_view(), name="information"),
    path("<slug:slug>/history/", FamilyHistoryView.as_view(), name="history"),
    path('toggle_completion/<int:action_id>/', toggle_completion, name='toggle_completion'),
]
