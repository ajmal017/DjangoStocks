from django.shortcuts import render, redirect
from .models import Stocks
from .forms import StockForm
from django.contrib import messages


# pk_cfe6936290284b42b69898122a23ede6

# Create your views here.
def home(request):
    import requests
    import json

    # Pull in ticker from search
    if request.method == 'POST':
        ticker = request.POST['ticker_symbol']  # name of input box
        api_request = requests.get(
            f'https://cloud.iexapis.com/stable/stock/{ticker}/quote?token=pk_cfe6936290284b42b69898122a23ede6')

        # error handling
        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "ERROR..."

        context = {
            'api': api,
        }
        return render(request, 'home.html', context)
    else:
        return render(request, 'home.html', {'ticker': ""})


def about(request):
    context = {
    }
    return render(request, 'about.html', context)


def add_stock(request):
    import requests
    import json

    if request.method == 'POST':
        form = StockForm(request.POST or None)
        ticker = request.POST['ticker']
        if form.is_valid():
            form.save()
            messages.success(request, f'{ticker} Has Been Added')
            return redirect('add_stock')

    else:
        ticker = Stocks.objects.all()

        output = []

        for ticker_item in ticker:
            api_request = requests.get(
                f'https://cloud.iexapis.com/stable/stock/{str(ticker_item)}/quote?token=pk_cfe6936290284b42b69898122a23ede6')

            # error handling
            try:
                api = json.loads(api_request.content)
                output.append(api)
            except Exception as e:
                api = "ERROR..."

        context = {
            'ticker': ticker,
            'output': output
        }

        return render(request, 'add_stock.html', context)


def delete(request, stock_id):
    item = Stocks.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, f"{item} Has Been Deleted")
    return redirect('delete_stock')


def delete_stock(request):
    ticker = Stocks.objects.all()
    return render(request, 'delete_stock.html', {'ticker': ticker})
