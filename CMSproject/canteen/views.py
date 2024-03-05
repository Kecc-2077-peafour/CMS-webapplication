from django.shortcuts import render
from core.models import Student, Teacher, Admin, Order, MenuItem , Notification,OrderDetail
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
import json
from django.shortcuts import get_object_or_404
from django.http import Http404
 
@login_required
def c_canteen_view(request):
    user_role = request.session.get('user_role', None)  # Django's authenticated user
    menu_items = MenuItem.objects.all()

    if user_role == 'student':
        student_instance = request.user.student
        notifications = student_instance.notifications.filter(is_seen=False)
        context = {
            'student_instance': student_instance,
            'teacher_instance': None,
            'user_type': 'student',
            'menu_items': menu_items,
            'notifications': notifications,
        }
        return render(request, 'canteen/c_canteen.html', context)
    elif user_role == 'teacher':
        teacher_instance = request.user.teacher
        notifications = teacher_instance.notifications.filter(is_seen=False)
        context = {
            'student_instance': None,
            'teacher_instance': teacher_instance,
            'user_type': 'teacher',
            'menu_items': menu_items,
            'notifications': notifications,
        }
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
        admin_notifications = admin_instance.notifications.filter(is_seen=False)
        for notification in admin_notifications:
            print(notification.content)
        context = {
            'admin_instance': admin_instance,
            'menu_items': menu_items,
            'admin_notifications': admin_notifications,
        }
        return render(request, 'canteen/s_canteen.html', context)
    else:
        raise Http404("Admin not found")

@login_required
def sales_view(request):
    user_role = request.session.get('user_role', None)  # Django's authenticated user
    order_details = OrderDetail.objects.all()

    if user_role == 'admin':
        user = request.user
        admin_instance = user.admin

        admin_notifications = admin_instance.notifications.filter(is_seen=False)
        for notification in admin_notifications:
            print(notification.content)

        context = {
            'admin_instance': admin_instance,
            'order_details': order_details,
            'admin_notifications': admin_notifications,
        }
        return render(request, 'canteen/sales.html', context)
    else:
        raise Http404("Admin not found")
     
@login_required
def orders_view(request):
    print('to display order page')
    user_role = request.session.get('user_role', None)  # Django's authenticated user
    print('so the authentication failed?')
    
    if user_role == 'admin':
        user = request.user
        admin_instance = user.admin

        admin_notifications = admin_instance.notifications.filter(is_seen=False)
        for notification in admin_notifications:
            print(notification.content)
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
        context = {
            'admin_instance': admin_instance,
            'order_items': order_data,
            'admin_notifications': admin_notifications,
        }
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
    
    # Check if the MenuItem is linked to any Order
    linked_orders = Order.objects.filter(menu_item=item)
    for order in linked_orders:
        # Check if the Order is linked to any OrderDetail
        linked_order_details = OrderDetail.objects.filter(order=order)
        for order_detail in linked_order_details:
            order_detail.delete()
        order.delete()

    # Now delete the MenuItem
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
            staff_admin.notifications.add(notification)

        return JsonResponse({'message': 'success'})
    return JsonResponse({'message': 'Invalid request method'}, status=405)

def confirm_order(request):
    print('confirm order is called')
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            order_id = data.get('order_id')
            new_status = data.get('status')
            order = get_object_or_404(Order, id=order_id)
            print('new:old',new_status,order.status)
            order.status = new_status
            order.save()
            customer = order.customer
            student_notification = Notification.objects.create(
                title="Order Confirmed",
                content=f"Your order with ID {order.order_name.name} has been confirmed."
            )
            customer.notifications.add(student_notification)

            return JsonResponse({'success': True, 'message': 'Order confirmed successfully'})
        except Order.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Order not found'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

def reject_order(request):
    print('confirm order is called')
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            order_id = data.get('order_id')
            order = get_object_or_404(Order, id=order_id)
            order.delete()
            customer = order.customer
            student_notification = Notification.objects.create(
                title="Order Rejected",
                content=f"Your order with {order.order_name.name} has been rejected."
            )
            customer.notifications.add(student_notification)

            return JsonResponse({'success': True, 'message': 'Order rejected successfully'})
        except Order.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Order not found'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

def completed_order(request):
    print('confirm order is called')
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            order_id = data.get('order_id')
            new_status = data.get('status')
            order = get_object_or_404(Order, id=order_id)
            print('new:old',new_status,order.status)
            order.status = new_status
            order.save()
            order_detail = OrderDetail.objects.create(
                order=order,
                total_amount=(order.quantity * order.order_name.price)
            )
            order_detail.save()
            return JsonResponse({'success': True, 'message': 'Order status changed successfully'})
        except Order.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Order not found'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

def get_notifications(request):
    user_role = request.session.get('user_role', None)
    user_id = request.user.id  # Assuming your user model has an 'id' field

    # Filter notifications based on the user's role
    if user_role == 'admin':
        admin_instance = request.user.admin
        notifications = admin_instance.notifications.filter(is_seen=False)
    elif user_role == 'student':
        student_instance = request.user.student
        notifications = student_instance.notifications.filter(is_seen=False)
    elif user_role == 'teacher':
        teacher_instance = request.user.teacher
        notifications = teacher_instance.notifications.filter(is_seen=False)
    else:
        # Handle other user roles or raise an exception if needed
        raise NotImplementedError("User role not supported")

    # Render HTML representation of notifications directly in the view
    notification_html = ""
    for notification in notifications:
        notification_html += f'<div class="notification-item" data-notification-id="{notification.id}">'
        notification_html += f'<h4>{notification.title}</h4>'
        notification_html += f'<p>{notification.content}</p>'
        notification_html += '</div>'

    # Count the notifications
    notification_count = notifications.count()

    return JsonResponse({
        'notification_count': notification_count,
        'notification_html': notification_html,
    })


def mark_notifications_as_seen(request):
    # Get notification IDs from the JSON payload
    data = json.loads(request.body)
    notification_ids = data.get('notification_ids', [])
    print('notification laii is_seen garna aako')
    # Mark the specified notifications as seen
    Notification.objects.filter(id__in=notification_ids).update(is_seen=True)

    return JsonResponse({'message': 'Notifications marked as seen.'})