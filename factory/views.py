from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse
from users.decorators import role_required
from .models import Dealer, Product, Order, OrderItem, FutureStock
from .forms import (
    DealerForm, 
    ProductForm, 
    OrderStepOneForm, 
    OrderStepTwoForm, 
    OrderStepThreeForm, 
    OrderStepFourForm, 
    OrderStepFiveForm, 
    StockIncrementForm,
    FutureStockForm,
)


def home(request):
    return render(request, 'main/home.html')

@login_required
@role_required("seller", "boss")
def dashboard(request):
    # Key Metrics
    total_orders = Order.objects.count()
    total_dealers = Dealer.objects.count()
    total_products = Product.objects.count()
    todays_orders = Order.objects.filter(delivery_date__date=timezone.now().date()).count()

    # Recent Orders
    recent_orders = Order.objects.filter(approved_by_seller=False, approved_by_delivery=False).order_by('-delivery_date')

    # Orders by Delivery Type
    orders_by_delivery_type = (
        Order.objects.values('delivery_type')
        .annotate(count=Count('id'))
        .order_by('-count'),
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
@role_required("seller", "boss")
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
@role_required("seller", "boss")
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('products')
    return render(request, 'main/delete_product.html', {'product': product})

@login_required
@role_required("seller", "boss")
def dealers_page(request):
    dealers = Dealer.objects.all()
    form = DealerForm()
    return render(request, 'main/dealers.html', {'dealers': dealers, 'form': form})

@login_required
@role_required("seller", "boss")
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
@role_required("seller", "boss")
def delete_dealer(request, pk):
    dealer = get_object_or_404(Dealer, pk=pk)
    if request.method == 'POST':
        dealer.delete()
        return redirect('dealers')
    return render(request, 'main/delete_dealer.html', {'dealer': dealer})

@login_required
@role_required("seller", "boss")
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
@role_required("seller", "boss")
def orders(request):
    return render(request, 'main/orders.html')

@login_required
@role_required("seller", "boss")
def archived_orders(request):
    orders = Order.objects.filter(approved_by_seller=True).order_by('-delivery_date')
    context = {
        'orders': orders,
    }
    return render(request, 'main/archived_orders.html', context)


@login_required
@role_required("seller", "boss")
def archive_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order_items = OrderItem.objects.filter(order=order)
    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'main/archive_order_details.html', context)

@login_required
@role_required("seller", "boss", "delivery")
def manage_orders(request):
    orders = Order.objects.filter(approved_by_seller=False).order_by('-delivery_date')
    context = {
        'orders': orders,
    }
    return render(request, 'main/manage_orders.html', context)

@login_required
@role_required("seller", "boss")
def approve_seller(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        if not order.approved_by_delivery:
            messages.error(request, "!!! Buyurtma hali Omborxonachi tomonidan tasdiqlanmagan !!!")
            return redirect('manage_orders')
        
        print("Order:", order)
        print("Order Items: ", order.items.all())
        
        for item in order.items.all():
            product = item.product
            product.stock -= item.quantity
            product.save()
            print("Product:", product.name, "Stock after deduction:", product.stock)
        
        order.approved_by_seller = True
        print("Order:", order)
        order.save()
        messages.success(request, "Buyurtma Sotuvchi tomonidan tasdiqlandi.")
    return redirect('manage_orders')


@login_required
@role_required("delivery", "boss")
def approve_delivery(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.approved_by_delivery = True
        print("Order:", order)
        order.save()
        messages.success(request, "Buyurtma Omborxonachi tomonidan tasdiqlandi.")
    return redirect('manage_orders')


@login_required
@role_required("seller", "boss")
def create_order(request):
    step = int(request.GET.get("step", 1))
    context = {"step": step}
    
    if step == 1:
        form = OrderStepOneForm(request.POST or None)
        if request.method == "POST" and form.is_valid():
            request.session["dealer_id"] = form.cleaned_data["dealer"].id
            return redirect("/orders/create/?step=2")
        context["form"] = form
    
    elif step == 2:
        form = OrderStepTwoForm(request.POST or None)
        if request.method == "POST" and form.is_valid():
            selected_products = request.POST.getlist("products")
            
            if not selected_products:
                messages.error(request, "Mahsulot va miqdor tanlash kerak!")
                return redirect("/orders/create/?step=2")
            
            # Get quantities only for selected products
            product_quantities = []
            for product_id in selected_products:
                quantity = request.POST.get(f"quantities_{product_id}")
                if quantity:
                    product_quantities.append(quantity)
            
            print("Selected Products:", selected_products)
            print("Product Quantities:", product_quantities)
            
            product_data = {int(pid): int(qty) for pid, qty in zip(selected_products, product_quantities)}
            request.session["order_products"] = product_data
            print("Selected Products:", product_data)
            return redirect("/orders/create/?step=3")
        
        context["form"] = form
        context['back_url'] = '/orders/create/?step=1'
    
    elif step == 3:
        form = OrderStepThreeForm(request.POST or None)
        if request.method == "POST" and form.is_valid():
            request.session["delivery_type"] = form.cleaned_data["delivery_type"]
            return redirect("/orders/create/?step=4")
        context["form"] = form
        context['back_url'] = '/orders/create/?step=2'
    
    elif step == 4:
        selected_products = Product.objects.filter(id__in=request.session.get("order_products", {}).keys())
        order_summary = []
        total_cost = 0
        
        for product in selected_products:
            qty = request.session["order_products"].get(str(product.id), 1)
            cost = product.price * qty
            total_cost += cost
            print("Product ID:", product.id, "Qty:", qty, "Cost:", cost)
            order_summary.append({"name": product.name, "quantity": qty, "cost": cost})
        context['back_url'] = '/orders/create/?step=3'
        
        print("Total Cost:", total_cost)
        form = OrderStepFourForm(request.POST or None, initial={
            "delivery_date": request.session.get("delivery_date", ""),
            "order_cost": total_cost,
        })
        if request.method == "POST" and form.is_valid():
            request.session["delivery_date"] = form.cleaned_data["delivery_date"].isoformat()
            request.session["order_cost"] = float(form.cleaned_data["order_cost"])
            return redirect("/orders/create/?step=5")
        
        context.update({"form": form, "order_summary": order_summary})
    
    elif step == 5:
        form = OrderStepFiveForm(request.POST or None, initial={
            "comment": request.session.get("comment", ""),
        })
        if request.method == "POST" and form.is_valid():
            request.session["comment"] = form.cleaned_data["comment"]
            return redirect("/orders/create/?step=6")
        context["form"] = form
        context['back_url'] = '/orders/create/?step=4'
    
    elif step == 6:
        selected_products = Product.objects.filter(id__in=request.session.get("order_products", {}).keys())
        order_summary = []
        total_cost = request.session.get("order_cost", 0)
        
        for product in selected_products:
            qty = request.session["order_products"].get(str(product.id), 1)
            cost = product.price * qty
            order_summary.append({"name": product.name, "quantity": qty, "cost": cost})
        
        context.update({
            "order_summary": order_summary,
            "delivery_date": request.session.get("delivery_date", ""),
            "order_cost": total_cost,
            "comment": request.session.get("comment", ""),
        })
        context['back_url'] = '/orders/create/?step=5'
        
        if request.method == "POST":
            order = Order.objects.create(
                dealer_id=request.session["dealer_id"],
                delivery_type=request.session["delivery_type"],
                delivery_date=request.session["delivery_date"],
                order_cost=request.session["order_cost"],
                comment=request.session.get("comment", ""),
            )
            
            for product in selected_products:
                qty = request.session["order_products"].get(str(product.id), 1)
                print("Creating OrderItem for", product.name, "with qty", qty)
                OrderItem.objects.create(order=order, product=product, quantity=qty)
                # product.stock -= qty  # Allow negative stock
                product.save()
            
            return redirect("dashboard")
    
    return render(request, f"main/create_order_step{step}.html", context)



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

@login_required
@role_required("seller", "boss")
def manage_stock(request):
    products = Product.objects.all().order_by('name')
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        form = StockIncrementForm(request.POST, instance=product)
        if form.is_valid():
            increment = form.cleaned_data['increment']
            product.stock += increment
            product.save()
            messages.success(request, f"{product.name} uchun {increment} miqdor qo'shildi.")
            return redirect('manage_stock')
    else:
        form = StockIncrementForm()
    return render(request, 'stocks/manage_stock.html', {'products': products, 'form': form})


@login_required
@role_required("seller", "boss")
def manage_product_stock(request, pk):
    product = get_object_or_404(Product, pk=pk)
    future_stock = product.futurestock if hasattr(product, 'futurestock') else None

    if request.method == 'POST':
        form = FutureStockForm(request.POST, instance=future_stock)
        if form.is_valid():
            future_stock = form.save(commit=False)
            future_stock.product = product
            future_stock.save()
            messages.success(request, f"{product.name} uchun kelajakdagi miqdor qo'shildi.")
            return redirect('manage_product_stock', pk=pk)
    else:
        form = FutureStockForm(instance=future_stock)

    return render(request, 'product/product_page.html', {
        'product': product,
        'future_stock': future_stock,
        'form': form
    })


@login_required
@role_required("seller", "boss")
def future_stock_finished(request, pk):
    product = get_object_or_404(Product, pk=pk)
    future_stock = product.futurestock if hasattr(product, 'futurestock') else None

    if future_stock:
        future_stock.finished = True
        product.stock += future_stock.future_stock
        product.save()
        future_stock.save()
        future_stock.delete()
        messages.success(request, f"{product.name} uchun kelajakdagi miqdor tugatildi.")
    else:
        messages.error(request, f"{product.name} uchun kelajakdagi miqdor topilmadi.")

    return redirect('manage_product_stock', pk=product.pk)



# def product_stock_view(request):
#     # Fetch all products
#     products = Product.objects.all()

#     # Create a list to store product data along with future stock information
#     product_data = []
    
#     for product in products:
#         # Get the future stock for the product (if it exists)
#         future_stock = FutureStock.objects.filter(product=product).first()

#         sold_items_before_future_stock = 0
#         sold_items_after_future_stock = 0

#         # Append product data to the list
#         product_data.append({
#             'product': product,
#             'stock': product.stock,
#             'future_stock_date': future_stock.date if future_stock else None,
#             'future_stock_quantity': future_stock.future_stock if future_stock else None,
#             'sold_items_before_future_stock': sold_items_before_future_stock,
#             'sold_items_after_future_stock': sold_items_after_future_stock,
#         })
    
#     # Pass the data to the template
#     context = {
#         'product_data': product_data,
#     }
#     return render(request, 'stocks/product_stock_table.html', context)

from django.shortcuts import render
from .models import Product, FutureStock, OrderItem

def product_stock_view(request):
    # Fetch all products
    products = Product.objects.all()

    # Create a list to store product data along with future stock information
    product_data = []
    
    for product in products:
        # Get the future stock for the product (if it exists)
        future_stock = FutureStock.objects.filter(product=product).first()

        # Initialize counters for sold items
        sold_items_before_future_stock = 0
        sold_items_after_future_stock = 0

        # Get all order items for the product
        order_ids = Order.objects.filter(approved_by_seller=False, approved_by_delivery=False).values_list('id', flat=True)
        print("Order IDs:", order_ids)
        order_items = OrderItem.objects.filter(product=product, order__id__in=order_ids)
        print("Order Items:", order_items)

        # Calculate sold items before and after future stock date
        if future_stock:
            # Items sold before the future stock date
            sold_items_before_future_stock = sum(
                item.quantity for item in order_items
                if item.order.delivery_date < future_stock.date
            )
            # Items sold after the future stock date
            sold_items_after_future_stock = sum(
                item.quantity for item in order_items
                if item.order.delivery_date >= future_stock.date
            )
        else:
            # If no future stock exists, all items are considered sold before
            sold_items_before_future_stock = sum(item.quantity for item in order_items)
            sold_items_after_future_stock = 0
        
        ready_to_sell = product.stock - sold_items_before_future_stock
        
        
        print("Product:", product.name)
        print("Sold Items Before Future Stock:", sold_items_before_future_stock)
        print("Sold Items After Future Stock:", sold_items_after_future_stock)

        # Append product data to the list
        product_data.append({
            'product': product,
            'stock': product.stock,
            'ready_to_sell': ready_to_sell,
            'future_stock_date': future_stock.date if future_stock else None,
            'future_stock_quantity': future_stock.future_stock if future_stock else None,
            'sold_items_before_future_stock': sold_items_before_future_stock,
            'sold_items_after_future_stock': sold_items_after_future_stock,
        })
    
    # Pass the data to the template
    context = {
        'product_data': product_data,
    }
    return render(request, 'stocks/product_stock_table.html', context)