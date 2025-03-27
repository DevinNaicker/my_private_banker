from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from my_app.forms import IncomeForm, BudgetItemFormSet
from my_app.models import Income, Budget
import matplotlib.pyplot as plt
import io
import base64

@login_required
def add_budget(request):
    # Load latest income entry if it exists
    latest_income = Income.objects.filter(user=request.user).order_by("-id").first()

    # Load or initialize form and formset
    if request.method == "POST":
        print("\n🔵 Received POST request!")  
        print("🔵 Form Data:", request.POST)

        income_form = IncomeForm(request.POST, instance=latest_income)
        formset = BudgetItemFormSet(request.POST, queryset=Budget.objects.filter(user=request.user))

        if income_form.is_valid() and formset.is_valid():
            print("✅ Forms are valid!")

            # Save or update income
            income = income_form.save(commit=False)
            income.user = request.user
            income.save()
            print(f"✅ Income saved! ID: {income.id}")

            # Save, update, or delete budget items
            instances = formset.save(commit=False)

            # Delete marked budget items
            for form in formset.deleted_forms:
                if form.instance.pk:
                    form.instance.delete()
                    print(f"🗑️ Deleted budget item ID: {form.instance.pk}")

            # Save updated or new budget items
            for instance in instances:
                instance.user = request.user
                instance.save()
                print(f"✅ Budget item saved! Type: {instance.budget_type}, Category: {instance.category}, Amount: {instance.amount}")

            return redirect("user_budget")

        else:
            print("❌ Income Form Errors:", income_form.errors)
            print("❌ Formset Errors:", formset.errors)

    else:
        # GET request – prefill total income and show existing budget items
        income_form = IncomeForm(instance=latest_income)
        formset = BudgetItemFormSet(queryset=Budget.objects.filter(user=request.user))

    return render(request, "add_budget.html", {
        "income_form": income_form,
        "formset": formset,
    })


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from my_app.models import Income, Budget
import matplotlib.pyplot as plt
import io
import base64

def generate_pie_chart(expense_data, savings_data):
    labels = list(expense_data.keys()) + list(savings_data.keys())
    values = list(expense_data.values()) + list(savings_data.values())

    if not values:
        return None

    # ✅ Make the figure larger
    fig, ax = plt.subplots(figsize=(10, 10))  # ⬅️ Larger width and height

    # ✅ Plot pie chart
    wedges, texts, autotexts = ax.pie(
        values,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90,
        textprops={"fontsize": 14},
    )

    # ✅ Equal aspect ratio ensures pie is drawn as a circle
    ax.axis("equal")

    
    # ✅ Add title inside the image
    plt.title("Budget Breakdown", fontsize=16, fontweight="bold", pad=1)

    # ✅ Prevent label clipping
    #plt.tight_layout()
    fig.subplots_adjust(top=1.05, bottom=0.05, left=0.05, right=0.95)

    # ✅ Save chart to buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight", pad_inches=0.05)  # ⬅️ Ensure no clipping
    buf.seek(0)
    image_png = buf.getvalue()
    buf.close()
    plt.close(fig)

    return "data:image/png;base64," + base64.b64encode(image_png).decode("utf-8")

@login_required
def user_budget(request):
    latest_income = Income.objects.filter(user=request.user).order_by("-id").first()
    total_income = latest_income.total_income if latest_income else 0

    budget_items = Budget.objects.filter(user=request.user)

    # ✅ Group items
    expenses = [item for item in budget_items if item.budget_type.lower() == "expense"]
    savings = [item for item in budget_items if item.budget_type.lower() == "savings"]

    # ✅ Calculate totals
    total_expenses = sum(item.amount for item in expenses)
    total_savings = sum(item.amount for item in savings)

    # ✅ Group by category
    expense_categories = {}
    savings_categories = {}

    for item in budget_items:
        category = item.category
        if item.budget_type.lower() == "expense":
            expense_categories[category] = expense_categories.get(category, 0) + item.amount
        elif item.budget_type.lower() == "savings":
            savings_categories[category] = savings_categories.get(category, 0) + item.amount

    # ✅ Generate the chart URL
    chart_url = generate_pie_chart(expense_categories, savings_categories)
    print("📊 Chart URL:", chart_url is not None)

    return render(request, "budget.html", {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "total_savings": total_savings,
        "expenses": expenses,
        "savings": savings,
        "budget_items": budget_items,
        "chart_url": chart_url,  # ✅ Pass this to the template
    })