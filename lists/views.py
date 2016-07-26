from django.shortcuts import render, redirect
from lists.models import Item


def home_page(request):
	if request.method == 'POST':
		Item.objects.create(text=request.POST['item_text'])
		return redirect('/lists/the_only_list_in_the_world')
	return render(request, 'home.html')


def view_list(request):
	items = Item.objects.all()
	return render(request, 'list.html', {'items': items})
