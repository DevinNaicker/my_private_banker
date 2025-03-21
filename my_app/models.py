from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

class Income(models.Model):  # ✅ Correctly Renamed from Budget to Income
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    month = models.DateField(auto_now_add=True)  # ✅ Ensures correct date handling
    total_income = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        db_table = "my_app_income"  # ✅ Correct database table name

    def __str__(self):
        return f"{self.user.username} - {self.month} - ${self.total_income}"

class Budget(models.Model):  # ✅ Renamed from Transaction to Budget
    BUDGET_TYPE_CHOICES = [
        ("Expense", "Expense"),
        ("Savings", "Savings"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    budget_type = models.CharField(max_length=10, choices=BUDGET_TYPE_CHOICES, default="Expense")  # ✅ Updated for clarity
    category = models.CharField(max_length=100, default="general")
    description = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        db_table = "my_app_budget"  # ✅ Ensure the database table name is correct

    def __str__(self):
        return f"{self.user.username} - {self.budget_type} - {self.category} - ${self.amount}"