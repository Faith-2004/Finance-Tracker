from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("income/add/", views.add_income, name="add_income"),
    path("expense/add/", views.add_expense, name="add_expense"),
    path("savings/add/",views.add_savings_goal,name="add_savings_goal"),
    path("savings/", views.savings_goals, name="savings_goals"),
    path("savings/<int:goal_id>/delete/",views.delete_savings_goal,name="delete_savings_goal"),
    path("transactions/", views.transactions_list, name="transactions_list"),
]