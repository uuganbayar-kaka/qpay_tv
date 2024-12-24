from django.urls import path

from base import views

urlpatterns = [
    path('ping', views.ping),
    path('get_invoice/simple', views.GetinvoiceSimpleView.as_view()),
    path('get_invoice/', views.GetinvoiceView.as_view()),
    path('cancel_invoice/', views.CancelInvoiceView.as_view()),
    
    path('get_payment/', views.GetPaymentView.as_view()),
    path('check_payment/', views.CheckPaymentView.as_view()),
    path('cancel_payment/', views.CancelPaymentView.as_view()),
    path('refund_payment/', views.RefundPaymentView.as_view()),
    
    path('payment_list/', views.PaymentListView.as_view()),
]
