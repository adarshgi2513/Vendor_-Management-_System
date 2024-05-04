from django.shortcuts import render
from.serializes import VendorSerializer,PurchaseOrderSerializer
from.models import Vendor,PurchaseOrder
from rest_framework import generics, status
from rest_framework.response import Response
from django.db.models import Avg
from datetime import date
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db.models import Avg, Count, F
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
# Create your views here.

#this is the vendor registration and vendor list class
class VendorListCreateAPIView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Vendor.objects.all()      #this funtion done list the all vendor detials(GET method)
    serializer_class = VendorSerializer
      #ths funtions make registrations to the vendors and resnponsing the registerd vendor detials(POST method)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)               
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

    
#this class used to view a specific vendor using the vendor ID(its a get method using speCific VENDOR ID )
class VendorRetrieveAPIView(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    lookup_url_kwarg = 'vendor_id'


#this class is using for update a specific(using ID) vendeor detials(PUT METHOD),update vendor detials using vendors ID,used the UpdateAPIview
class VendorUpdateAPIView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    lookup_url_kwarg = 'vendor_id'



#this class is using for delete a specific(using ID)vendor (Delete method used to DestroyAPIview)
class VendorDestroyAPIView(generics.DestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    lookup_url_kwarg = 'vendor_id'


#this class is used to create purchase oder and view that detail aslo
class PurchaseOrderCreateAPIView(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer



#this class is used list the purchase oder and we can list datas to filter by vendor(api/purchase_orders/?vendor_id=001)
class PurchaseOrderListAPIView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PurchaseOrderSerializer
   #get method fiterd by vendor
    def get_queryset(self):
        queryset = PurchaseOrder.objects.all()
        vendor_id = self.request.query_params.get('vendor_id')
        if vendor_id:
            queryset = queryset.filter(vendor_id=vendor_id)
        return queryset
    



#this class is used for retrive purchase oder detials using purchase order ID(get method using ID)
class PurchaseOrderRetrieveAPIView(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    lookup_url_kwarg = 'po_id'

#this clas used to update purchase oder using specific purchad ID(PUT method using updateAPIview)
class PurchaseOrderUpdateAPIView(generics.UpdateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    lookup_url_kwarg = 'po_id'

#this class used to Delete purchase oder using specific purchad ID(delete method using DestroyAPIview)
class PurchaseOrderDestroyAPIView(generics.DestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    lookup_url_kwarg = 'po_id'



#THIS IS THE PERFORMANCE CALCULATION SECTION
class PerformanceCalculator:
    @staticmethod
    def calculate_on_time_delivery_rate(vendor):
        completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
        total_completed_pos = completed_pos.count()
        
        if total_completed_pos == 0:
            return 0.0
        
        on_time_delivered_pos = completed_pos.filter(delivery_date__lte=F('acknowledgment_date')).count()
        on_time_delivery_rate = (on_time_delivered_pos / total_completed_pos) * 100
        return round(on_time_delivery_rate, 2)
    @staticmethod
    def calculate_quality_rating_avg(vendor):
        completed_pos_with_ratings = PurchaseOrder.objects.filter(vendor=vendor, status='completed', quality_rating__isnull=False)
        return completed_pos_with_ratings.aggregate(Avg('quality_rating'))['quality_rating__avg'] or 0

    @staticmethod
    def calculate_average_response_time(vendor):
        completed_pos_with_acknowledgment = PurchaseOrder.objects.filter(
            vendor=vendor, status='completed'
        ).exclude(acknowledgment_date__isnull=True)
        
        if completed_pos_with_acknowledgment.exists():
            avg_response_time = completed_pos_with_acknowledgment.aggregate(
                avg_response=Avg(F('acknowledgment_date') - F('issue_date'))
            )['avg_response']
            
            if avg_response_time:
                return avg_response_time.total_seconds() / 3600  # Convert to hours
        
        return None

    @staticmethod
    def calculate_fulfillment_rate(vendor):
        total_pos = PurchaseOrder.objects.filter(vendor=vendor)
        successfully_fulfilled_pos = total_pos.filter(status='completed', issues__isnull=True).count()
        if total_pos.count() == 0:
            return 0
        return successfully_fulfilled_pos / total_pos.count()
    
    
class VendorPerformanceAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, vendor_id):
        vendor = get_object_or_404(Vendor, id=vendor_id)
        
        on_time_delivery_rate = PerformanceCalculator.calculate_on_time_delivery_rate(vendor)
        quality_rating_avg = PerformanceCalculator.calculate_quality_rating_avg(vendor)
        average_response_time = PerformanceCalculator.calculate_average_response_time(vendor)
        fulfillment_rate = PerformanceCalculator.calculate_fulfillment_rate(vendor)
        
        performance_data = {
            'on_time_delivery_rate': on_time_delivery_rate,
            'quality_rating_avg': quality_rating_avg,
            'average_response_time': average_response_time,
            'fulfillment_rate': fulfillment_rate
        }
        
        return Response(performance_data)




class MySecuredView(APIView): 
    def get(self, request, format=None):
        content = {
            'message': 'This is a secured endpoint.',
            'user': str(request.user),  # User object associated with the token
        }
        return Response(content)
    
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})