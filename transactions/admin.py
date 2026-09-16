from django.contrib import admin

from .models import Income, Expense, SavingsGoal, SavingsTransaction, Category

admin.site.register(Income)
admin.site.register(Expense)
admin.site.register(SavingsGoal)
admin.site.register(SavingsTransaction)
admin.site.register(Category)

