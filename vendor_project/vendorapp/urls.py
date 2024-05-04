from django.urls import path
from . views import VendorListCreateAPIView,VendorRetrieveAPIView,VendorUpdateAPIView,VendorDestroyAPIView,PurchaseOrderCreateAPIView,PurchaseOrderListAPIView,PurchaseOrderRetrieveAPIView,PurchaseOrderUpdateAPIView,PurchaseOrderDestroyAPIView,VendorPerformanceAPIView,MySecuredView,CustomAuthToken
from . import views
urlpatterns = [
    path('api/vendors/', VendorListCreateAPIView.as_view(), name='vendor-list-create'),
    path('api/vendors/<int:vendor_id>/', VendorRetrieveAPIView.as_view(), name='vendor-detail'),
    path('api/vendors/<int:vendor_id>/update/', VendorUpdateAPIView.as_view(), name='vendor-update'),
    path('api/vendors/<int:vendor_id>/delete/', VendorDestroyAPIView.as_view(), name='vendor-delete'),

    path('api/purchase_orders/create/', PurchaseOrderCreateAPIView.as_view(), name='purchaseorder-create'),
    path('api/purchase_orders/', PurchaseOrderListAPIView.as_view(), name='purchaseorder-list'),
    path('api/purchase_orders/<int:po_id>/', PurchaseOrderRetrieveAPIView.as_view(), name='purchaseorder-detail'),
    path('api/purchase_orders/<int:po_id>/update/', PurchaseOrderUpdateAPIView.as_view(), name='purchaseorder-update'),
    path('api/purchase_orders/<int:po_id>/delete/', PurchaseOrderDestroyAPIView.as_view(), name='purchaseorder-delete'),

    path('api/vendors/<int:vendor_id>/performance/',VendorPerformanceAPIView.as_view(), name='vendor_performance'),



    path('api/token/', MySecuredView.as_view(), name='api_token'),
    path('api/get_token/', CustomAuthToken.as_view(), name='get_token'),
    

]