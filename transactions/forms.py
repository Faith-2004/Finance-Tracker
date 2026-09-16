from decimal import Decimal

from django import forms
from django.utils import timezone

from .models import Income, Expense, Category


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