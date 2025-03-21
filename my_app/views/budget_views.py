from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from my_app.forms import IncomeForm, BudgetItemFormSet
from my_app.models import Income, Budget  # ✅ Updated to use Budget instead of Transaction
import matplotlib.pyplot as plt
import io
import urllib
import base64

@login_required
def user_budget(request):
    # ✅ Fix: Use correct variable name
    latest_income = Income.objects.filter(user=request.user).order_by("-id").first()
    total_income = latest_income.total_income if latest_income else 0

    # ✅ Fix: Use Budget instead of Transaction
    budget_items = Budget.objects.filter(user=request.user) if request.user.is_authenticated else Budget.objects.none()

    # Debug: Check if budget items exist
    print("\n🔍 DEBUG: Budget Items Retrieved:")
    for item in budget_items:
        print(f"Budget - Type: {item.budget_type}, Category: {item.category}, Amount: {item.amount}")

    # ✅ Fix: Use `.casefold()` for case-insensitive comparison
    total_expenses = sum(item.amount for item in budget_items if item.budget_type.casefold() == "expense")
    total_savings = sum(item.amount for item in budget_items if item.budget_type.casefold() == "savings")

    # Debug: Check calculated totals
    print(f"\n✅ DEBUG: Total Expenses Calculated: {total_expenses}")
    print(f"✅ DEBUG: Total Savings Calculated: {total_savings}")

    # Prepare data for Pie Chart
    expense_categories = {}
    savings_categories = {}

    for item in budget_items:
        category = item.category.capitalize()  # ✅ Capitalize to ensure consistency
        if item.budget_type.casefold() == "expense":
            expense_categories[category] = expense_categories.get(category, 0) + item.amount
        elif item.budget_type.casefold() == "savings":
            savings_categories[category] = savings_categories.get(category, 0) + item.amount

    # Generate Pie Chart
    chart_url = generate_pie_chart(expense_categories, savings_categories)

    return render(request, "budget.html", {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "total_savings": total_savings,
        "chart_url": chart_url,
        "budget_items": budget_items,
    })

# Helper function to generate pie chart
def generate_pie_chart(expense_data, savings_data):
    labels = list(expense_data.keys()) + list(savings_data.keys())
    values = list(expense_data.values()) + list(savings_data.values())

    if not values:  # Avoid errors if there are no expenses or savings
        return None

    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")  # Equal aspect ratio ensures the pie is drawn as a circle

    # Convert chart to URL format
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    string = base64.b64encode(buf.getvalue()).decode()
    buf.close()
    plt.close(fig)

    return "data:image/png;base64," + string

@login_required
def add_budget(request):
    if request.method == "POST":
        print("\n🔵 Received POST request!")  
        print("🔵 Form Data:", request.POST)  # ✅ Show what is being submitted

        income_form = IncomeForm(request.POST)
        formset = BudgetItemFormSet(request.POST, queryset=Budget.objects.none())  # ✅ Empty queryset

        if income_form.is_valid() and formset.is_valid():
            print("✅ Forms are valid!")

            # ✅ Save Income data
            income = income_form.save(commit=False)
            income.user = request.user
            income.save()
            print(f"✅ Income saved! ID: {income.id}")

            # ✅ Save Budget items
            for form in formset:
                if form.cleaned_data:
                    budget_item = form.save(commit=False)
                    budget_item.user = request.user
                    budget_item.save()
                    print(f"✅ Budget item saved! Type: {budget_item.budget_type}, Category: {budget_item.category}, Amount: {budget_item.amount}")

            return redirect("user_budget")  # ✅ Redirect to budget dashboard
        
        else:
            print("\n❌ Income Form Errors:", income_form.errors)
            print("\n❌ Budget Formset Errors:", formset.errors)
    
    else:
        income_form = IncomeForm()
        formset = BudgetItemFormSet(queryset=Budget.objects.none())  # ✅ Ensure empty formset

    return render(request, "add_budget.html", {"income_form": income_form, "formset": formset})