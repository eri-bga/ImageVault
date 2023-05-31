from django.urls import path
from . import views

app_name = 'images'

urlpatterns = [
    path('create/', views.create_image, name='create'),
    path('detail/<int:id>/<slug:slug>', views.image_detail, name='detail'),
    path('like/', views.image_like, name='like'),
    # path('images_list/', views.images_list, name='images_list'),
    path('', views.images_list, name='images_list'),
    path('ranking/', views.image_ranking, name='ranking')
]
