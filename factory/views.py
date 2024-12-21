from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.http import JsonResponse
from .models import Dealer, Product, Order
from .forms import DealerForm, ProductForm, OrderStepOneForm, OrderStepTwoForm, OrderStepThreeForm, OrderStepFourForm, OrderStepFiveForm
from users.decorators import role_required


def home(request):
    return render(request, 'main/home.html')

@login_required
@role_required("seller")
def dashboard(request):
    # Key Metrics
    total_orders = Order.objects.count()
    total_dealers = Dealer.objects.count()
    total_products = Product.objects.count()
    todays_orders = Order.objects.filter(delivery_date__date=timezone.now().date()).count()

    # Recent Orders
    recent_orders = Order.objects.order_by('-delivery_date')

    # Orders by Delivery Type
    orders_by_delivery_type = (
        Order.objects.values('delivery_type')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    context = {
        'total_orders': total_orders,
        'total_dealers': total_dealers,
        'total_products': total_products,
        'todays_orders': todays_orders,
        'recent_orders': recent_orders,
        'orders_by_delivery_type': orders_by_delivery_type,
    }
    return render(request, 'main/dashboard.html', context)

@login_required
@role_required("seller")
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

@login_required
@role_required("seller")
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'main/edit_product.html', {'form': form, 'product': product})


@login_required
@role_required("seller")
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('products')
    return render(request, 'main/delete_product.html', {'product': product})

@login_required
@role_required("seller")
def dealers_page(request):
    dealers = Dealer.objects.all()
    form = DealerForm()
    return render(request, 'main/dealers.html', {'dealers': dealers, 'form': form})

@login_required
@role_required("seller")
def edit_dealer(request, pk):
    dealer = get_object_or_404(Dealer, pk=pk)
    if request.method == 'POST':
        form = DealerForm(request.POST, instance=dealer)
        if form.is_valid():
            form.save()
            return redirect('dealers')
    else:
        form = DealerForm(instance=dealer)
    return render(request, 'main/edit_dealer.html', {'form': form, 'dealer': dealer})


@login_required
@role_required("seller")
def delete_dealer(request, pk):
    dealer = get_object_or_404(Dealer, pk=pk)
    if request.method == 'POST':
        dealer.delete()
        return redirect('dealers')
    return render(request, 'main/delete_dealer.html', {'dealer': dealer})

@login_required
@role_required("seller")
def create_dealer(request):
    if request.method == 'POST':
        form = DealerForm(request.POST)
        if form.is_valid():
            dealer = form.save()
            if request.headers.get('HX-Request'):  # HTMX request
                return render(request, 'main/partials/dealer_row.html', {'dealer': dealer})
            return redirect('dealers')
    return JsonResponse({'error': 'Invalid data'}, status=400)

@login_required
@role_required("seller")
def orders(request):
    return render(request, 'main/orders.html')


@login_required
@role_required("seller")
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
        form = OrderStepTwoForm(request.POST or None, initial={
            'products': Product.objects.filter(id__in=request.session.get('product_ids', []))
        })
        if request.method == 'POST' and form.is_valid():
            request.session['product_ids'] = [product.id for product in form.cleaned_data['products']]
            return redirect('/orders/create/?step=3')
        context['form'] = form
        context['back_url'] = '/orders/create/?step=1'

    # Step 3: Select Delivery Type
    elif step == 3:
        form = OrderStepThreeForm(request.POST or None, initial={
            'delivery_type': request.session.get('delivery_type', '')
        })
        if request.method == 'POST' and form.is_valid():
            request.session['delivery_type'] = form.cleaned_data['delivery_type']
            return redirect('/orders/create/?step=4')
        context['form'] = form
        context['back_url'] = '/orders/create/?step=2'

    # Step 4: Specify Delivery Date and Cost
    elif step == 4:
        form = OrderStepFourForm(request.POST or None, initial={
            'delivery_date': request.session.get('delivery_date', ''),
            'order_cost': request.session.get('order_cost', '')
        })
        if request.method == 'POST' and form.is_valid():
            request.session['delivery_date'] = form.cleaned_data['delivery_date'].isoformat()
            request.session['order_cost'] = float(form.cleaned_data['order_cost'])
            return redirect('/orders/create/?step=5')
        context['form'] = form
        context['back_url'] = '/orders/create/?step=3'

    # Step 5: Write a Comment
    elif step == 5:
        form = OrderStepFiveForm(request.POST or None, initial={
            'comment': request.session.get('comment', '')
        })
        if request.method == 'POST' and form.is_valid():
            request.session['comment'] = form.cleaned_data['comment']
            return redirect('/orders/create/?step=6')
        context['form'] = form
        context['back_url'] = '/orders/create/?step=4'

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
        context['back_url'] = '/orders/create/?step=5'
        if request.method == 'POST':
            order = Order.objects.create(
                dealer_id=request.session['dealer_id'],
                delivery_type=request.session['delivery_type'],
                delivery_date=request.session['delivery_date'],
                order_cost=request.session['order_cost'],
                comment=request.session.get('comment', '')
            )
            order.products.set(request.session['product_ids'])
            return redirect('dashboard')

    return render(request, f'main/create_order_step{step}.html', context)



@login_required
@role_required("seller")
def edit_order(request, pk):
    order = get_object_or_404(Order, pk=pk)

    if request.method == 'POST':
        # Step 1: Edit Dealer
        step1_form = OrderStepOneForm(request.POST)
        # Step 2: Edit Products
        step2_form = OrderStepTwoForm(request.POST)
        # Step 3: Edit Delivery Type
        step3_form = OrderStepThreeForm(request.POST)
        # Step 4: Edit Delivery Date & Cost
        step4_form = OrderStepFourForm(request.POST)
        # Step 5: Edit Comments
        step5_form = OrderStepFiveForm(request.POST)

        if all([step1_form.is_valid(), step2_form.is_valid(), step3_form.is_valid(), step4_form.is_valid(), step5_form.is_valid()]):
            # Save updated data to the order
            order.dealer = step1_form.cleaned_data['dealer']
            order.delivery_type = step3_form.cleaned_data['delivery_type']
            order.delivery_date = step4_form.cleaned_data['delivery_date']
            order.order_cost = step4_form.cleaned_data['order_cost']
            order.comment = step5_form.cleaned_data['comment']

            # Update products
            products = step2_form.cleaned_data['products']
            order.products.set(products)

            order.save()
            return redirect('dashboard')
    else:
        # Pre-fill forms with existing order data
        step1_form = OrderStepOneForm(initial={'dealer': order.dealer})
        step2_form = OrderStepTwoForm(initial={'products': order.products.all()})
        step3_form = OrderStepThreeForm(initial={'delivery_type': order.delivery_type})
        step4_form = OrderStepFourForm(initial={
            'delivery_date': order.delivery_date,
            'order_cost': order.order_cost
        })
        step5_form = OrderStepFiveForm(initial={'comment': order.comment})

    return render(request, 'main/edit_order.html', {
        'order': order,
        'step1_form': step1_form,
        'step2_form': step2_form,
        'step3_form': step3_form,
        'step4_form': step4_form,
        'step5_form': step5_form
    })

@login_required
@role_required("seller")
def delete_order(request, pk):
    order = get_object_or_404(Order, pk=pk)

    if request.method == 'POST':
        order.delete()
        return redirect('dashboard')

    return render(request, 'main/delete_order.html', {'order': order})
