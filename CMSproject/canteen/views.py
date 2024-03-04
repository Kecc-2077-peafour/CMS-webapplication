from django.shortcuts import render
from core.models import Student, Teacher, Admin, Order, MenuItem , Notification
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
                    student_instance = Student.objects.get(user=customer)
                    customer_img = student_instance.profile_picture.url
                    customer_name = student_instance.name
                    print(customer_name)
                elif customer.usertype == 'teacher':
                    teacher_instance = Teacher.objects.get(user=customer)
                    customer_img = teacher_instance.profile_picture.url
                    customer_name = teacher_instance.name
                    print(customer_name)
                else:
                    raise Http404("User not found")
            except (Student.DoesNotExist, Teacher.DoesNotExist):
                raise Http404("User not found")

            order_data.append({
                'order': order,
                'customer_img': customer_img,
                'customer_name': customer_name,
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

def get_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        order_details = data.get('orderDetails')
        menu_item = MenuItem.objects.get(id=order_details['itemId'])
        student = Student.objects.get(student_id=order_details['customerID'])
        customer = student.user

        # Create a new order in your database
        order = Order.objects.create(
            customer=customer,
            order_name=menu_item,
            quantity=order_details['quantity'],
            created_at=order_details['createdAt'],
        )
        order.save()
        staff_admins = Admin.objects.filter(role='staff')
        notification = Notification.objects.create(
            title="New Order",
            content="Please reload the page to view the order."
        )
        for staff_admin in staff_admins:
            staff_admin.admin_notifications.add(notification)

        return JsonResponse({'message': 'success'})
    return JsonResponse({'message': 'Invalid request method'}, status=405)

def confirm_order(request):
    print('confirm order is called')
    if request.method == 'POST':
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body.decode('utf-8'))
            # Extract order_id and status from the received data
            order_id = data.get('order_id')
            new_status = data.get('status')
            # Retrieve the order from the database
            order = get_object_or_404(Order, id=order_id)
            print('new:old',new_status,order.status)
            # Update the status of the order
            order.status = new_status
            order.save()

            return JsonResponse({'success': True, 'message': 'Order confirmed successfully'})
        except Order.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Order not found'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})
