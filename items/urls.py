
from django.urls import path
from . import views

urlpatterns = [
    path('report/', views.report_item, name='report_item'),
    path('my-reports/', views.my_reports, name='my_reports'),
    path('browse/', views.browse_items, name='browse_items'),
    path('review/<int:item_id>/', views.review_item, name='review_item'),
]
