from django.urls import path
from . import views

urlpatterns = [
    path("income/add/", views.add_income, name="add_income"),
    path("expense/add/", views.add_expense, name="add_expense"),
    path("transactions/", views.transactions_list, name="transactions_list"),
]