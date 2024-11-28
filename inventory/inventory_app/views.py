from rest_framework import generics, serializers
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from .models import Category, Product, StockMovement
from .serializers import CategorySerializer, ProductSerializer, StockMovementSerializer


class CategoryListCreateView(generics.ListCreateAPIView):
    """
    View for listing and creating categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Override to ensure that only staff users can create categories.
        """
        if self.request.user.is_staff:
            serializer.save()
        else:
            raise PermissionDenied("You don't have permission to create categories.")


class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, and deleting categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        """
        Override to ensure that only staff users can update categories.
        """
        if self.request.user.is_staff:
            serializer.save()
        else:
            raise PermissionDenied("You do not have permission to update categories.")

    def perform_destroy(self, instance):
        """
        Override to ensure that only staff users can delete categories.
        """
        if self.request.user.is_staff:
            instance.delete()
        else:
            raise PermissionDenied("You do not have permission to delete categories.")


class ProductListCreateView(generics.ListCreateAPIView):
    """
    View for listing and creating products.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Override to ensure that only staff users can create products.
        """
        if self.request.user.is_staff:
            serializer.save()
        else:
            raise PermissionDenied("You do not have permission to create products.")


class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, and deleting products.   
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        """
        Override to ensure that only staff users can update products.
        """
        if self.request.user.is_staff:
            serializer.save()
        else:
            raise PermissionDenied("You do not have permission to update products.")

    def perform_destroy(self, instance):
        """
        Override to ensure that only staff users can delete products.
        """
        if self.request.user.is_staff:
            instance.delete()
        else:
            raise PermissionDenied("You do not have permission to delete products.")


class StockMovementListCreateView(generics.ListCreateAPIView):
    """
    View for listing and creating stock movements.
    Handles stock updates based on the type of movement (IN/OUT).
    """
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Override to handle stock updates based on the movement type (IN/OUT).
        Only accessible to staff users.
        """
        # Check if the user is a staff member
        if self.request.user.is_staff:
            validated_data = serializer.validated_data
            product = validated_data["product"]
            movement_type = validated_data["movement_type"]
            quantity = validated_data["quantity"]

            # Handle stock update based on movement type
            if movement_type == "IN":
                # Increase the stock
                product.stock_quantity += quantity
            elif movement_type == "OUT":
                # Decrease the stock, ensure it doesn't go negative
                if product.stock_quantity >= quantity:
                    product.stock_quantity -= quantity
                else:
                    raise serializers.ValidationError(f"Error. Available stock is {product.stock_quantity}.")

            # Save the product with the updated stock
            product.save()

            stock_movement = serializer.save()

            return stock_movement
        else:
            raise PermissionDenied("You do not have permission to modify stock.")


class StockMovementRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, and deleting stock movements.
    Updates stock based on the difference between the old and new movement when updating.
    """
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        """
        Override to update stock based on the difference between the old and new stock movement.
        Only accessible to staff users.
        """
        if self.request.user.is_staff:
            # Retrieve the current and new data
            instance = self.get_object()
            validated_data = serializer.validated_data
            product = validated_data["product"]
            movement_type = validated_data["movement_type"]
            quantity = validated_data["quantity"]

            # Get the original movement type and quantity
            old_movement_type = instance.movement_type
            old_quantity = instance.quantity

            # Update stock based on the difference between old and new movement
            if old_movement_type == "IN":
                product.stock_quantity -= old_quantity  # Subtract stock for the old movement

            elif old_movement_type == "OUT":
                product.stock_quantity += old_quantity  # Add stock for the old movement

            if movement_type == "IN":
                product.stock_quantity += quantity  # Add stock for the new movement
            elif movement_type == "OUT":
                product.stock_quantity -= quantity  # Subtract stock for the new movement

            # Save the product with updated stock
            product.save()

            # Save the updated stock movement record
            serializer.save()
        else:
            raise PermissionDenied("You do not have permission to update stock movements.")

    def perform_destroy(self, instance):
        """
        Override to adjust stock when a stock movement is deleted.
        Only accessible to staff users.
        """
        if self.request.user.is_staff:
            # Adjust the stock of the related product when a stock movement is deleted
            product = instance.product
            movement_type = instance.movement_type
            quantity = instance.quantity

            # Update stock based on the type of movement
            if movement_type == "IN":
                product.stock_quantity -= quantity  # Decrease stock for "IN" movement
            elif movement_type == "OUT":
                product.stock_quantity += quantity  # Increase stock for "OUT" movement

            # Save the product with the updated stock
            product.save()

            # Delete the stock movement record
            instance.delete()
        else:
            raise PermissionDenied("You do not have permission to delete stock movements.")