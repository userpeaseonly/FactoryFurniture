from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Dealer, Product, Order
from .forms import DealerForm, ProductForm, OrderStepOneForm, OrderStepTwoForm, OrderStepThreeForm, OrderStepFourForm, OrderStepFiveForm


def home(request):
    return render(request, 'main/home.html')

def dashboard(request):
    return render(request, 'main/dashboard.html')

def products_page(request):
    products = Product.objects.all()
    form = ProductForm()
    return render(request, 'main/products.html', {'products': products, 'form': form})

def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            if request.headers.get('HX-Request'):  # HTMX request
                return render(request, 'main/partials/product_row.html', {'product': product})
            return redirect('products')
    return JsonResponse({'error': 'Invalid data'}, status=400)


def dealers_page(request):
    dealers = Dealer.objects.all()
    form = DealerForm()
    return render(request, 'main/dealers.html', {'dealers': dealers, 'form': form})

def create_dealer(request):
    if request.method == 'POST':
        form = DealerForm(request.POST)
        if form.is_valid():
            dealer = form.save()
            if request.headers.get('HX-Request'):  # HTMX request
                return render(request, 'main/partials/dealer_row.html', {'dealer': dealer})
            return redirect('dealers')
    return JsonResponse({'error': 'Invalid data'}, status=400)

def orders(request):
    return render(request, 'main/orders.html')


def create_order(request):
    step = int(request.GET.get('step', 1))
    context = {'step': step}

    # Step 1: Select or Add Dealer
    if step == 1:
        form = OrderStepOneForm(request.POST or None)
        if request.method == 'POST' and form.is_valid():
            request.session['dealer_id'] = form.cleaned_data['dealer'].id
            return redirect('/orders/create/?step=2')
        context['form'] = form

    # Step 2: Select Products
    elif step == 2:
        form = OrderStepTwoForm(request.POST or None)
        if request.method == 'POST' and form.is_valid():
            request.session['product_ids'] = [product.id for product in form.cleaned_data['products']]
            return redirect('/orders/create/?step=3')
        context['form'] = form

    # Step 3: Select Delivery Type
    elif step == 3:
        form = OrderStepThreeForm(request.POST or None)
        if request.method == 'POST' and form.is_valid():
            request.session['delivery_type'] = form.cleaned_data['delivery_type']
            return redirect('/orders/create/?step=4')
        context['form'] = form

    # Step 4: Specify Delivery Date and Cost
    elif step == 4:
        form = OrderStepFourForm(request.POST or None)
        if request.method == 'POST' and form.is_valid():
            request.session['delivery_date'] = form.cleaned_data['delivery_date'].isoformat()
            request.session['order_cost'] = float(form.cleaned_data['order_cost'])
            return redirect('/orders/create/?step=5')
        context['form'] = form

    # Step 5: Write a Comment
    elif step == 5:
        form = OrderStepFiveForm(request.POST or None)
        if request.method == 'POST' and form.is_valid():
            request.session['comment'] = form.cleaned_data['comment']
            return redirect('/orders/create/?step=6')
        context['form'] = form

    # Step 6: Confirm Order
    elif step == 6:
        context['order_summary'] = {
            'dealer': Dealer.objects.get(id=request.session['dealer_id']),
            'products': Product.objects.filter(id__in=request.session['product_ids']),
            'delivery_type': request.session['delivery_type'],
            'delivery_date': request.session['delivery_date'],
            'order_cost': request.session['order_cost'],
            'comment': request.session.get('comment', ''),
        }
        if request.method == 'POST':
            order = Order.objects.create(
                dealer_id=request.session['dealer_id'],
                delivery_type=request.session['delivery_type'],
                delivery_date=request.session['delivery_date'],
                order_cost=request.session['order_cost'],
                comment=request.session.get('comment', '')
            )
            order.products.set(request.session['product_ids'])
            return redirect('orders')

    return render(request, f'main/create_order_step{step}.html', context)