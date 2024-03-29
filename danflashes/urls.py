from django.contrib import admin
from rest_framework.routers import DefaultRouter
from django.conf.urls import include
from django.urls import path
from danflashesapi.views import register_user, login_user, FlashesUserView, ShirtView, ColorView, PatternView, FavoriteView, MyShirtView


router = DefaultRouter(trailing_slash=False)
router.register(r'users', FlashesUserView, 'user')
router.register(r'shirts', ShirtView, 'shirt')
router.register(r'colors', ColorView, 'color')
router.register(r'patterns', PatternView, 'pattern')
router.register(r'favorites', FavoriteView, 'favorite')
router.register(r'myshirts', MyShirtView, 'shirt')

urlpatterns = [
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
