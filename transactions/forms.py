from decimal import Decimal

from django import forms
from django.utils import timezone

from .models import Income, Expense, Category, SavingsGoal, SavingsTransaction


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ["source", "amount", "date", "description"]
        widgets = {
            "date": forms.DateInput(
                attrs={
                    "type": "date",
                    "max": timezone.localdate().isoformat(),
                }
            ),
            "description": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["source"].queryset = Category.objects.filter(
            category_type="income"
        )

    def clean_date(self):
        date = self.cleaned_data["date"]

        if date > timezone.localdate():
            raise forms.ValidationError(
                "Future dates are not allowed."
            )

        return date

    def clean_amount(self):
        amount = self.cleaned_data["amount"]

        if amount <= Decimal("0"):
            raise forms.ValidationError(
                "Invalid Amount."
            )

        return amount


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ["category", "amount", "date", "description"]
        widgets = {
            "date": forms.DateInput(
                attrs={
                    "type": "date",
                    "max": timezone.localdate().isoformat(),
                }
            ),
            "description": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["category"].queryset = Category.objects.filter(
            category_type="expense"
        )

    def clean_date(self):
        date = self.cleaned_data["date"]

        if date > timezone.localdate():
            raise forms.ValidationError(
                "Future dates are not allowed."
            )

        return date

    def clean_amount(self):
        amount = self.cleaned_data["amount"]

        if amount <= Decimal("0"):
            raise forms.ValidationError(
                "Invalid Amount."
            )

        return amount


class SavingsGoalForm(forms.ModelForm):
    class Meta:
        model = SavingsGoal
        fields = ["name", "target_amount", "target_date", "description"]
        widgets = {
            "target_date": forms.DateInput(
                attrs={"type": "date"}
            ),
            "description": forms.Textarea(
                attrs={"rows": 3}
            ),
        }

    def clean_target_amount(self):
        amount = self.cleaned_data["target_amount"]

        if amount <= Decimal("0"):
            raise forms.ValidationError(
                "Target amount must be greater than zero."
            )

        return amount

    def clean_target_date(self):
        date = self.cleaned_data["target_date"]

        if date and date < timezone.localdate():
            raise forms.ValidationError(
                "Target date cannot be in the past."
            )

        return date

class SavingsTransactionForm(forms.ModelForm):
    class Meta:
        model = SavingsTransaction
        fields = ["amount", "date", "description"]
        widgets = {
            "date": forms.DateInput(
                attrs={
                    "type": "date",
                    "max": timezone.localdate().isoformat(),
                }
            ),
            "description": forms.Textarea(
                attrs={"rows": 3}
            ),
        }

    def clean_date(self):
        date = self.cleaned_data["date"]

        if date > timezone.localdate():
            raise forms.ValidationError(
                "Future dates are not allowed."
            )

        return date

    def clean_amount(self):
        amount = self.cleaned_data["amount"]

        if amount <= Decimal("0"):
            raise forms.ValidationError(
                "Amount must be greater than zero."
            )

        return amount