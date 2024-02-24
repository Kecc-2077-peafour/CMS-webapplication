from django.shortcuts import render
from core.models import Student, Teacher, Admin, Order, MenuItem
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
import json
from uuid import UUID
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages
from django.http import Http404

def logout_view(request):
    print('this view was invoked')
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('login:login')
 
@login_required
def c_canteen_view(request):
    user_role = request.session.get('user_role', None)  # Django's authenticated user
    menu_items = MenuItem.objects.all()

    if user_role == 'student':
        context = {'student_instance': request.user.student, 'teacher_instance': None, 'user_type': 'student', 'menu_items': menu_items}
        return render(request, 'canteen/c_canteen.html', context)
    elif user_role == 'teacher':
        context = {'student_instance': None, 'teacher_instance': request.user.teacher, 'user_type': 'teacher', 'menu_items': menu_items}
        return render(request, 'canteen/c_canteen.html', context)
    else:
        raise Http404("User not found")
    
@login_required
def s_canteen_view(request):
    user_role = request.session.get('user_role', None)  # Django's authenticated user
    menu_items = MenuItem.objects.all()

    if user_role == 'admin':
        user = request.user
        admin_instance = user.admin
        context = {'admin_instance': admin_instance, 'menu_items': menu_items}
        return render(request, 'canteen/s_canteen.html', context)
    else:
        raise Http404("Admin not found")
    
@login_required
def orders_view(request):
    print('to display order page')
    user_role = request.session.get('user_role', None)  # Django's authenticated user
    print('so the authentication failed?')
    
    if user_role == 'admin':
        user = request.user
        # If the user is an admin, proceed with the logic
        order_items = Order.objects.all()
        for order in order_items:
            print(order)

        order_data = []

        for order in order_items:
            customer = order.customer
            try:
                if customer.usertype == 'student':
                    customer_instance = customer.student
                    customer_img = customer_instance.profile_picture.url
                elif customer.usertype == 'teacher':
                    customer_instance = customer.teacher
                    customer_img = customer_instance.profile_picture.url
                else:
                    raise Http404("User not found")
            except (Student.DoesNotExist, Teacher.DoesNotExist):
                raise Http404("User not found")

            order_data.append({
                'order': order,
                'customer_img': customer_img,
            })

        context = {'admin_instance': user.admin, 'order_items': order_data}
        return render(request, 'canteen/orders.html', context)
    else:
        # If the user is not an admin, you may want to handle this case differently
        raise Http404("Admin not found")



@csrf_protect
def add_menuItem(request):
    try:
        item_name = request.POST.get('itemsName')
        item_price = request.POST.get('itemsPrice')
        item_description = request.POST.get('itemsDescription')
        item_image = request.FILES.get('itemsImageInput')

        new_item = MenuItem(name=item_name, price=item_price, description=item_description, image=item_image)
        new_item.save()

        response_data = {
            'message': 'Item added successfully',
            'item': {
                'name': new_item.name,
                'price': new_item.price,
                'description': new_item.description,
                'image_url': new_item.image.url,
            }
        }

        return JsonResponse(response_data)
    except Exception as e:
        print(f"Error in add_menuItem view: {e}")
        return JsonResponse({'error': 'Internal Server Error'}, status=500)


@csrf_protect
def add_specialItem(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_name = data.get('itemName')
        special_status = data.get('special', False)

        # Update the MenuItem's special status
        menu_item = get_object_or_404(MenuItem, name=item_name)
        menu_item.special = special_status
        menu_item.save()

        return JsonResponse({'message': 'Special status updated successfully.'})
    return JsonResponse({'error': 'Invalid request method.'}, status=400)

@csrf_protect
def delete_menuItem(request):
    data = json.loads(request.body)
    item_id = data.get('item_id')

    item = get_object_or_404(MenuItem, pk=item_id)
    item.delete()

    return JsonResponse({'message': 'Item deleted successfully'})

@csrf_protect
def delete_specialItem(request):
    data = json.loads(request.body)
    item_id = data.get('item_id')

    item = get_object_or_404(MenuItem, id=item_id)
    item.special = False
    item.save()
    
    return JsonResponse({'message': 'Item deleted successfully'})

def confirm_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        order_details = data.get('orderDetails')
        status = data.get('status')

        # Assuming 'itemId' is the unique identifier for MenuItem
        menu_item = MenuItem.objects.get(id=order_details['itemId'])

        # Assuming 'studentID' is the ID of a specific Student
        student = Student.objects.get(id=order_details['customerID'])
        
        # Retrieve the associated CustomUser instance through the student field
        customer = student.user

        # Create a new order in your database
        order = Order.objects.create(
            customer=customer,
            order_name=menu_item,
            quantity=order_details['quantity'],
            created_at=order_details['createdAt'],
            status=status,
        )

        return JsonResponse({'message': 'Order confirmed successfully'})