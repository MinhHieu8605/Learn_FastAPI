from Ecommerce.app.models import CartItem, Cart
from Ecommerce.app.schemas.cart import CartResponse
from Ecommerce.app.schemas.cartItems import CartItemsResponse

class CartConverter:

    def to_cart_response(self, cart: Cart) -> CartResponse:
        items = []
        for item in cart.cart_items:
            item_response = self.to_cart_items_response(item)
            items.append(item_response)

        return CartResponse(
            id=cart.id,
            user_id=cart.user_id,
            items=items,
            total_price=cart.get_total_price,
            total_items=len(items)
        )


    def to_cart_items_response(self, cart_item: CartItem) -> CartItemsResponse:
        return CartItemsResponse(
            id=cart_item.id,
            product_id=cart_item.product_id,
            product_name=cart_item.product.name,
            unit_price=cart_item.unit_price,
            quantity=cart_item.quantity,
            total_price=cart_item.unit_price * cart_item.quantity
        )

