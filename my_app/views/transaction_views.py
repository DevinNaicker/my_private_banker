from django.shortcuts import render, redirect

def user_transactions(request):
    transactions = Transaction.objects.filter(user=request.user)
    return render(request, "transactions.html", {"transactions": transactions})

def add_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user  # Link transaction to logged-in user
            transaction.save()
            return redirect("user_transactions")  # Redirect to transactions page
    else:
        form = TransactionForm()
    
    return render(request, "add_transaction.html", {"form": form})