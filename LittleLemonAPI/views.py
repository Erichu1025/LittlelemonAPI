from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseNotAllowed
from rest_framework.decorators import permission_classes
from .models import MenuItem, Category, Cart, Order, OrderItem
from .serializers import MenuItemSerializer, CategorySerializer, CartSerializer, OrderSerializer, OrderItemSerializer
    
# Template Views
def login_page(request):
    """
    Render the login page.
    """
    return render(request, 'login.html')


def menu_page(request):
    """
    Render the menu page.
    """
    menu_items = MenuItem.objects.all()
    return render(request, 'menu.html', {'menu_items': menu_items})


@login_required
def menu_item_page(request, pk):
    """
    Render the details of a specific menu item and handle adding it to the cart.
    Stay on the same page after adding the item (no redirect).
    """
    menu_item = get_object_or_404(MenuItem, pk=pk)
    message = ""

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            menuitem=menu_item,
            defaults={'quantity': quantity, 'unit_price': menu_item.price},
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        # Provide user feedback on the same page
        message = "Item added to your cart!"

    return render(request, 'menu_item.html', {
        'menu_item': menu_item,
        'message': message
    })

@login_required
def cart_page(request):
    """
    Render the cart page with all items for the authenticated user.
    """
    cart_items = Cart.objects.filter(user=request.user)
    return render(request, 'cart.html', {'cart_items': cart_items})

@login_required
def remove_cart_item(request, pk):
    if request.method == 'POST':
        cart_item = get_object_or_404(Cart, pk=pk, user=request.user)
        cart_item.delete()
        return redirect('cart-page')
    else:
        return HttpResponseNotAllowed(['POST'])


def order_page(request):
    # Fetch all Cart items for the current user.
    # (Ensure that your Cart model uses a foreign key to the user.)
    cart_items = Cart.objects.filter(user=request.user)
    
    # Compute the total price.
    total_price = sum(item.quantity * item.unit_price for item in cart_items)
    
    # Pass the cart items (as order_items) and the total to the template.
    context = {
        'order_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'order.html', context)

# Category Views
class CategoriesView(generics.ListCreateAPIView):
    """
    List all categories or create a new category.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a single category by ID.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]



# MenuItem Views
class MenuItemView(generics.ListCreateAPIView):
    """
    List all menu items or create a new menu item.
    """
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class MenuItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a specific menu item.
    """
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]



# Cart Views

class CartView(generics.ListCreateAPIView):
    """
    List all cart items for the authenticated user or add a new cart item.
    """
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CartDetailView(generics.RetrieveDestroyAPIView):
    """
    Retrieve or delete a specific cart item for the authenticated user.
    """
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    

# Order Views
class OrderView(generics.ListCreateAPIView):
    """
    List all orders for the authenticated user or create a new order.
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



# OrderItem Views
class OrderItemView(generics.ListCreateAPIView):
    """
    List all order items or create a new order item.
    """
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]


class OrderItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a specific order item.
    """
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

