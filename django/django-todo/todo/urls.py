from django.urls import path
from . import views

app_name = "todo"
urlpatterns = [
    path("", views.TodoListListView.as_view(), name="list"),
    path("<int:pk>/", views.TodoListDetailView.as_view(), name="detail"),
    path("<int:pk>/checked", views.checked, name="checked")
]
