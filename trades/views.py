from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import TradeForm

@login_required
def log_trade(request):
    if request.method == 'POST':
        form = TradeForm(request.POST)
        if form.is_valid():
            trade = form.save(commit=False)
            trade.user_one = request.user
            trade.save()
            return redirect('trade_history')
    else:
        form = TradeForm()

    return render(request, 'trades/log_trade.html', {'form': form})

@login_required
def trade_history(request):
    trades = request.user.initiated_trades.all() | request.user.received_trades.all()
    trades = trades.order_by('-agreed_on')
    return render(request, 'trades/history.html', {'trades': trades})

