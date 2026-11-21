from django.urls import path
from . import views

urlpatterns = [
    path('submit/<int:item_id>/', views.submit_claim, name='submit_claim'),
    path('add-question/<int:item_id>/', views.add_verification_question, name='add_verification_question'),
    path('verify/<int:claim_id>/', views.verify_claim, name='verify_claim'),
    path('my-claims/', views.my_claims, name='my_claims'),
    path('staff-claims/', views.staff_claims, name='staff_claims'),
    path(
    'update/<int:claim_id>/<str:action>/',
    views.update_claim_status,
    name='update_claim_status'
    ),
    path(
    'mark-returned/<int:claim_id>/',
    views.mark_as_returned,
    name='mark_as_returned'
    ),
    path(
    'confirm-received/<int:claim_id>/',
    views.confirm_item_received,
    name='confirm_item_received'
    ),
]