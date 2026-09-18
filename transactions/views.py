from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum  #for doing additions"

from .forms import IncomeForm, ExpenseForm, SavingsGoalForm
from .models import Income, Expense, SavingsGoal


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
def add_savings_goal(request):
    if request.method == "POST":
        form = SavingsGoalForm(request.POST)

        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()

            return redirect("savings_goals")
    else:
        form = SavingsGoalForm()

    return render(
        request,
        "transactions/add_savings_goal.html",
        {"form": form}
    )

@login_required
def savings_goals(request):
    goals = SavingsGoal.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "transactions/savings_goals.html",
        {"goals": goals}
    )

@login_required
def delete_savings_goal(request, goal_id):
    goal = get_object_or_404(
        SavingsGoal,
        id=goal_id,
        user=request.user
    )

    if request.method == "POST":
        goal.delete()
        return redirect("savings_goals")

    return render(
        request,
        "transactions/delete_savings_goal.html",
        {"goal": goal}
    )


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

@login_required
def dashboard(request):
    total_income = Income.objects.filter(
        user=request.user
    ).aggregate(total=Sum("amount"))["total"] or 0 #calculate the total income for the logged in user

    total_expenses = Expense.objects.filter(
        user=request.user
    ).aggregate(total=Sum("amount"))["total"] or 0 #calculate the total expenses for the logged in user

    balance = total_income - total_expenses

    incomes = Income.objects.filter(
        user=request.user
    ).order_by("-date")[:5] #start with recent transaction and then limit to the latest 5 transactions

    expenses = Expense.objects.filter(
        user=request.user
    ).order_by("-date")[:5] #start with recent transaction and then limit to the latest 5 transactions

    recent_transactions = []

    for income in incomes:
        recent_transactions.append({
            "date": income.date,
            "type": "Income",
            "category": income.source.name,
            "amount": income.amount,
            "description": income.description,
        })

    for expense in expenses:
        recent_transactions.append({
            "date": expense.date,
            "type": "Expense",
            "category": expense.category.name,
            "amount": expense.amount,
            "description": expense.description,
        })

    recent_transactions.sort(
        key=lambda x: x["date"],
        reverse=True
    )

    recent_transactions = recent_transactions[:5] #Limit to 5 recent transactions

    return render(
        request,
        "transactions/dashboard.html",
        {
            "total_income": total_income,
            "total_expenses": total_expenses,
            "balance": balance,
            "recent_transactions": recent_transactions,
        } #show the total income, total expenses, balance and recent transactions on the dashboard
    )