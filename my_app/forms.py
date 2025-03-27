from django import forms
from .models import Income, Budget
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import modelformset_factory

# 🔐 Signup Form
class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


# 💰 Income Form
class IncomeForm(forms.ModelForm):
    total_income = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label="Total Income"
    )

    class Meta:
        model = Income
        fields = ["total_income"]


# 📋 Budget Item Form
class BudgetItemForm(forms.ModelForm):
    BUDGET_TYPE_CHOICES = [
        ("Expense", "Expense"),
        ("Savings", "Savings"),
    ]

    EXPENSE_CATEGORIES = [
        ("Housing", "Housing"),
        ("Transportation", "Transportation"),
        ("Food & Groceries", "Food & Groceries"),
        ("Personal", "Personal"),
        ("Family", "Family"),
        ("Health & Medical", "Health & Medical"),
        ("Entertainment & Leisure", "Entertainment & Leisure"),
        ("Shopping", "Shopping"),
        ("Education & Self Development", "Education & Self Development"),
        ("Debt, Loans & Accounts", "Debt, Loans & Accounts"),
        ("Gifts & Donations", "Gifts & Donations"),
        ("Miscellaneous & Unexpected", "Miscellaneous & Unexpected"),
    ]

    SAVINGS_CATEGORIES = [
        ("General", "General"),
        ("Emergency", "Emergency"),
        ("Short Term Goals", "Short Term Goals"),
        ("Long Term Goals", "Long Term Goals"),
        ("Investments & Wealth", "Investments & Wealth"),
        ("Miscellaneous", "Miscellaneous"),
    ]

    budget_type = forms.ChoiceField(
        choices=BUDGET_TYPE_CHOICES,
        label="Type",
        widget=forms.Select(attrs={"class": "type-dropdown"}),
    )

    category = forms.ChoiceField(
        label="Category",
        required=True,
        widget=forms.Select(attrs={"class": "category-dropdown"}),
    )

    class Meta:
        model = Budget
        fields = ["budget_type", "category", "description", "amount"]
        widgets = {
            "description": forms.TextInput(attrs={"placeholder": "Enter details"}),
            "amount": forms.NumberInput(attrs={"step": "0.01"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Default fallback
        selected_type = "Expense"

        # ✅ 1. If POST data, prioritize that
        if self.data:
            selected_type = self.data.get(self.add_prefix("budget_type"), "Expense")

        # ✅ 2. If editing, use instance value
        elif self.instance and self.instance.pk:
            selected_type = self.instance.budget_type

        # ✅ 3. Now set category choices based on correct type
        if selected_type == "Savings":
            self.fields["category"].choices = self.SAVINGS_CATEGORIES
        else:
            self.fields["category"].choices = self.EXPENSE_CATEGORIES

    # Optional: Prevent saving zero amounts
    def clean_amount(self):
        amount = self.cleaned_data.get("amount")
        if amount == 0:
            raise forms.ValidationError("Amount must be greater than zero.")
        return amount


# 🧾 Budget Formset Factory
BudgetItemFormSet = modelformset_factory(
    Budget,
    form=BudgetItemForm,
    extra=1,
    can_delete=True
)