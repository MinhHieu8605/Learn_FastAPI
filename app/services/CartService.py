from sqlalchemy.ext.asyncio import AsyncSession

from Ecommerce.app.converter.CartConverter import CartConverter
from Ecommerce.app.exception.http import ResourceNotFoundException, InsufficientStockException
from Ecommerce.app.models import Cart, CartItem
from Ecommerce.app.repository.CartItemsRepository import CartItemsRepository
from Ecommerce.app.repository.CartRepository import CartRepository
from Ecommerce.app.repository.ProductRepository import ProductRepository
from Ecommerce.app.repository.UserRepository import UserRepository
from Ecommerce.app.schemas.cartItems import CartItemsCreate


class CartService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.cart_repo = CartRepository(db)
        self.cart_item_repo = CartItemsRepository(db)
        self.product_repo = ProductRepository(db)
        self.user_repo = UserRepository(db)
        self.cart_converter = CartConverter()

    async def get_or_create_cart(self, user_id: int) -> Cart:
        cart = await self.cart_repo.find_by_user_id(user_id)
        if cart:
            return cart
        user = await self.user_repo.get_user_by_id(user_id)
        if not user:
            raise ResourceNotFoundException(f"User not found with id = {user_id}")
        cart = Cart(user=user)
        await self.cart_repo.save(cart)
        return cart

    async def add_item_to_cart(self, user_id: int, request: CartItemsCreate):
        cart = await self.get_or_create_cart(user_id)

        product = await self.product_repo.get_product_by_id(request.product_id)
        if not product:
            raise ResourceNotFoundException(f"Product not found with id = {request.product_id}")

        if product.stock < request.quantity:
            raise InsufficientStockException(f"Insufficient stock for product with id = {request.product_id}")

        existing_item = await self.cart_item_repo.find_by_cart_id_and_product_id(cart.id, product.id)
        if existing_item:
            new_quantity = existing_item.quantity + request.quantity
            if product.stock < new_quantity:
                raise InsufficientStockException(f"Insufficient stock for product with id = {request.product_id}")

            existing_item.quantity = new_quantity
            cart_item_save = await self.cart_item_repo.save(existing_item)
        else:
            cart_item = CartItem(
                cart=cart,
                product=product,
                unit_price=product.price,
                quantity=request.quantity
            )
            cart_item_save = await self.cart_item_repo.save(cart_item)
        return self.cart_converter.to_cart_items_response(cart_item_save)






