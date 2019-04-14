from django.urls import path, include

from .views import (
    CommentAPIView,
    MovieAPIView,
    MovieDeleteUpdateAPIView,
    MovieTopAPIView,
)

app_name = 'movies'

urlpatterns = [
    path('movies', MovieAPIView.as_view(), name='add-fetch'),
    path('movies/<int:pk>', MovieDeleteUpdateAPIView.as_view(), name='update-delete'),
    path('comments', CommentAPIView.as_view(), name='comments'),
    path('top', MovieTopAPIView.as_view(), name='top'),
]
