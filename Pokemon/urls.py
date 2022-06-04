from rest_framework.routers import DefaultRouter
from .views import PokemonView


router = DefaultRouter()
router.register(r'pokemon', PokemonView)

urlpatterns = router.urls
