from . import views
from users import views as user_views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('users', user_views.UserViewSet, basename='users')
router_v1.register('titles', views.TitleViewSet, basename='titles')
router_v1.register('genres', views.GenreViewSet)
router_v1.register('categories', views.CategoryViewSet, basename='categories')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewsViewSet, basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentsViewSet, basename='comments'
)
urlpatterns = [
    path(
        'auth/signup/',
        user_views.CreateUserViewSet.as_view({'post': 'create'})
    ),
    path(
        'auth/token/',
        user_views.ObtainTokenView.as_view(),
        name='token_obtain_pair'),
    path('v1/', include(router_v1.urls)),
]
