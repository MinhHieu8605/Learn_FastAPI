from fastapi import APIRouter

from Ecommerce.app.api.v1.endpoints import user, product, auth, cart

router = APIRouter()
router.include_router(user.router, prefix="/user", tags=["User"])
router.include_router(product.router, prefix="/products", tags=["Products"])
router.include_router(auth.router, tags=["Register"])
router.include_router(cart.router, prefix="/cart", tags=["Cart"])