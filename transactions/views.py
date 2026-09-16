from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import IncomeForm, ExpenseForm
from .models import Income, Expense


@login_required
def add_income(request):
    if request.method == "POST":
        form = IncomeForm(request.POST)

        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            return redirect("add_income")
    else:
        form = IncomeForm()

    return render(request, "transactions/add_income.html", {"form": form})


@login_required
def add_expense(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)

        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect("add_expense")
    else:
        form = ExpenseForm()

    return render(request, "transactions/add_expense.html", {"form": form})


@login_required
def transactions_list(request):
    incomes = Income.objects.filter(user=request.user).order_by("-date")
    expenses = Expense.objects.filter(user=request.user).order_by("-date")

    transactions = []

    for income in incomes:
        transactions.append({
            "date": income.date,
            "type": "Income",
            "category": income.source.name,
            "amount": income.amount,
            "description": income.description,
        })

    for expense in expenses:
        transactions.append({
            "date": expense.date,
            "type": "Expense",
            "category": expense.category.name,
            "amount": expense.amount,
            "description": expense.description,
        })

    transactions.sort(key=lambda x: x["date"], reverse=True)

    return render(
        request,
        "transactions/transactions_list.html",
        {"transactions": transactions}
    )