from fastapi import APIRouter
from .endpoints.auth import router as auth_router
from .endpoints.movies import router as movies_router
from .endpoints.genres import router as genres_router
from .endpoints.categories import router as categories_router
from .endpoints.favorites import router as favorites_router
from .endpoints.search import router as search_router
from .endpoints.reviews import router as reviews_router
from .endpoints.notifications import router as notifications_router
from .endpoints.profile import router as profile_router

router = APIRouter(prefix="/api/v1")

router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(movies_router, prefix="/movies", tags=["movies"])
router.include_router(genres_router, prefix="/genres", tags=["genres"])
router.include_router(categories_router, prefix="/categories", tags=["categories"])
router.include_router(favorites_router, prefix="/favorites", tags=["favorites"])
router.include_router(search_router, prefix="/search", tags=["search"])
router.include_router(reviews_router, prefix="/reviews", tags=["reviews"])
router.include_router(notifications_router, prefix="/notifications", tags=["notifications"])
router.include_router(profile_router, prefix="/profile", tags=["profile"])