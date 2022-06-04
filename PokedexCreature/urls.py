from rest_framework.routers import DefaultRouter
from .views import PokedexCreatureView


router = DefaultRouter()
router.register(r'pokedex', PokedexCreatureView)

urlpatterns = router.urls
