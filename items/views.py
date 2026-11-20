
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ItemForm
from .models import Item


@login_required
def report_item(request):
    if request.user.role != 'STUDENT':
        return redirect('login')

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)

            if item.item_type == 'LOST':
                item.private_details = ''

            item.reported_by = request.user
            item.save()

            messages.success(request, 'Item reported successfully!')
            return redirect('report_item')

    else:
        form = ItemForm()

    return render(request, 'items/report_item.html', {'form': form})



@login_required
def my_reports(request):
    items = Item.objects.filter(
        reported_by=request.user
    ).order_by('-created_at')

    return render(request, 'items/my_reports.html', {'items': items})



@login_required
def browse_items(request):
    items = Item.objects.all().order_by('-created_at')

    search = request.GET.get('search')
    item_type = request.GET.get('item_type')
    category = request.GET.get('category')
    location = request.GET.get('location')

    if search:
        items = items.filter(name__icontains=search)

    if item_type:
        items = items.filter(item_type=item_type)

    if category:
        items = items.filter(category=category)

    if location:
        items = items.filter(location__icontains=location)

    return render(request, 'items/browse_items.html', {
        'items': items,
    })



@login_required
def review_item(request, item_id):
    if request.user.role != 'STAFF':
        return redirect('login')

    item = get_object_or_404(
        Item,
        id=item_id,
        item_type='FOUND'
    )

    return render(request, 'items/review_item.html', {
        'item': item,
    })
