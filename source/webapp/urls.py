from django.urls import path

from webapp.views import index, create_issue, detail_issue, delete_issue, update_issue

urlpatterns = [
    path('', index, name='main'),
    path('create/', create_issue, name='create'),
    path('issue/<int:pk>/', detail_issue, name="detail"),
    path('issue/<int:pk>/update/', update_issue, name='update'),
    path('issue/<int:pk>/', delete_issue, name="delete"),
]
