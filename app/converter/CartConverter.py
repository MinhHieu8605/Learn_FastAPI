from Ecommerce.app.models import CartItem
from Ecommerce.app.schemas.cartItems import CartItemsResponse

class CartConverter:

    def to_cart_items_response(self, cart_item: CartItem) -> CartItemsResponse:
        return CartItemsResponse(
            id=cart_item.id,
            product_id=cart_item.product_id,
            product_name=cart_item.product.name,
            unit_price=cart_item.unit_price,
            quantity=cart_item.quantity,
            total_price=cart_item.unit_price * cart_item.quantity
        )

