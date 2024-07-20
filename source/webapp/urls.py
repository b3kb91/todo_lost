from django.urls import path

from webapp.views.issues import IssueListView, CreateIssueView, IssueDetailView, DeleteIssueView, UpdateIssueView

urlpatterns = [
    path('issue/', IssueListView.as_view(), name='main'),
    path('create/', CreateIssueView.as_view(), name='create'),
    path('issue/<int:pk>/', IssueDetailView.as_view(), name="detail"),
    path('issue/<int:pk>/update/', UpdateIssueView.as_view(), name='update'),
    path('delete/<int:pk>/', DeleteIssueView.as_view(), name="delete"),
]
