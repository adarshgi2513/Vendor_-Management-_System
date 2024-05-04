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

# Vendor views

class VendorListCreateAPIView(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating vendors.

    Authentication:
    - Token-based authentication is required.

    Permissions:
    - Users must be authenticated to access this endpoint.

    Methods:
    - GET: Retrieve a list of all vendors.
        - Parameters: None
        - Response (200 OK):
            [
                {
                    "id": 1,
                    "name": "Vendor 1",
                    "contact_person": "John Doe",
                    "email": "john@example.com",
                    ...
                },
                ...
            ]
    - POST: Create a new vendor.
        - Parameters (Request Body):
            {
                "name": "New Vendor",
                "contact_person": "Jane Smith",
                "email": "jane@example.com",
                ...
            }
        - Response (201 Created):
            {
                "id": 2,
                "name": "New Vendor",
                "contact_person": "Jane Smith",
                "email": "jane@example.com",
                ...
            }
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    def post(self, request, *args, **kwargs):
        """
        Create a new vendor.

        Parameters:
        - name (string): Name of the vendor.
        - contact_person (string): Contact person of the vendor.
        - email (string): Email address of the vendor.

        Returns:
        - Response (201 Created): Details of the newly created vendor.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class VendorRetrieveAPIView(generics.RetrieveAPIView):
    """
    API endpoint for retrieving a specific vendor.

    Authentication:
    - Token-based authentication is required.

    Permissions:
    - Users must be authenticated to access this endpoint.

    Methods:
    - GET: Retrieve details of a specific vendor by ID.
        - Parameters:
            - vendor_id (int): ID of the vendor.
        - Response (200 OK):
            {
                "id": 1,
                "name": "Vendor 1",
                "contact_person": "John Doe",
                "email": "john@example.com",
                ...
            }
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    lookup_url_kwarg = 'vendor_id'

class VendorUpdateAPIView(generics.UpdateAPIView):
    """
    API endpoint for updating a specific vendor.

    Authentication:
    - Token-based authentication is required.

    Permissions:
    - Users must be authenticated to access this endpoint.

    Methods:
    - PUT: Update details of a specific vendor by ID.
        - Parameters:
            - vendor_id (int): ID of the vendor.
            - Request Body: Updated vendor details.
        - Response (200 OK):
            {
                "id": 1,
                "name": "Updated Vendor Name",
                "contact_person": "Updated Contact Person",
                "email": "updated_email@example.com",
                ...
            }
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    lookup_url_kwarg = 'vendor_id'

class VendorDestroyAPIView(generics.DestroyAPIView):
    """
    API endpoint for deleting a specific vendor.

    Authentication:
    - Token-based authentication is required.

    Permissions:
    - Users must be authenticated to access this endpoint.

    Methods:
    - DELETE: Delete a specific vendor by ID.
        - Parameters:
            - vendor_id (int): ID of the vendor.
        - Response (204 No Content): Vendor deleted successfully.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    lookup_url_kwarg = 'vendor_id'

# Purchase Order views

class PurchaseOrderCreateAPIView(generics.CreateAPIView):
    """
    API endpoint for creating a purchase order.

    Authentication:
    - Token-based authentication is required.

    Permissions:
    - Users must be authenticated to access this endpoint.

    Methods:
    - POST: Create a new purchase order.
        - Parameters (Request Body):
            {
                "vendor": 1,
                "order_date": "2024-05-03",
                ...
            }
        - Response (201 Created): Details of the newly created purchase order.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class PurchaseOrderListAPIView(generics.ListAPIView):
    """
    API endpoint for listing purchase orders.

    Authentication:
    - Token-based authentication is required.

    Permissions:
    - Users must be authenticated to access this endpoint.

    Methods:
    - GET: Retrieve a list of purchase orders.
        - Parameters:
            - vendor_id (int, optional): Filter by vendor ID.
        - Response (200 OK):
            [
                {
                    "id": 1,
                    "vendor": 1,
                    "order_date": "2024-05-03",
                    ...
                },
                ...
            ]
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PurchaseOrderSerializer

    def get_queryset(self):
        queryset = PurchaseOrder.objects.all()
        vendor_id = self.request.query_params.get('vendor_id')
        if vendor_id:
            queryset = queryset.filter(vendor_id=vendor_id)
        return queryset

class PurchaseOrderRetrieveAPIView(generics.RetrieveAPIView):
    """
    API endpoint for retrieving a specific purchase order.

    Authentication:
    - Token-based authentication is required.

    Permissions:
    - Users must be authenticated to access this endpoint.

    Methods:
    - GET: Retrieve details of a specific purchase order by ID.
        - Parameters:
            - po_id (int): ID of the purchase order.
        - Response (200 OK):
            {
                "id": 1,
                "vendor": 1,
                "order_date": "2024-05-03",
                ...
            }
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    lookup_url_kwarg = 'po_id'

class PurchaseOrderUpdateAPIView(generics.UpdateAPIView):
    """
    API endpoint for updating a specific purchase order.

    Authentication:
    - Token-based authentication is required.

    Permissions:
    - Users must be authenticated to access this endpoint.

    Methods:
    - PUT: Update details of a specific purchase order by ID.
        - Parameters:
            - po_id (int): ID of the purchase order.
            - Request Body: Updated purchase order details.
        - Response (200 OK):
            {
                "id": 1,
                "vendor": 1,
                "order_date": "2024-05-03",
                ...
            }
    """
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    lookup_url_kwarg = 'po_id'

class PurchaseOrderDestroyAPIView(generics.DestroyAPIView):
    """
    API endpoint for deleting a specific purchase order.

    Authentication:
    - Token-based authentication is required.

    Permissions:
    - Users must be authenticated to access this endpoint.

    Methods:
    - DELETE: Delete a specific purchase order by ID.
        - Parameters:
            - po_id (int): ID of the purchase order.
        - Response (204 No Content): Purchase order deleted successfully.
    """
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    lookup_url_kwarg = 'po_id'

# Performance views

class VendorPerformanceAPIView(APIView):
    """
    API endpoint for calculating vendor performance metrics.

    Authentication:
    - Token-based authentication is required.

    Permissions:
    - Users must be authenticated to access this endpoint.

    Methods:
    - GET: Retrieve performance metrics for a specific vendor by ID.
        - Parameters:
            - vendor_id (int): ID of the vendor.
        - Response (200 OK):
            {
                "on_time_delivery_rate": 80.0,
                "quality_rating_avg": 4.5,
                "average_response_time": 24.5,
                "fulfillment_rate": 0.85
            }
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, vendor_id):
        """
        Calculate performance metrics for a specific vendor.

        Parameters:
        - vendor_id (int): ID of the vendor.

        Returns:
        - Response (200 OK): Performance metrics.
        """
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
    """
    API endpoint for accessing a secured resource.

    Authentication:
    - Token-based authentication is required.

    Permissions:
    - Users must be authenticated to access this endpoint.

    Methods:
    - GET: Retrieve a secured resource.
        - Parameters: None
        - Response (200 OK): Secured resource details.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """
        Retrieve a secured resource.

        Returns:
        - Response (200 OK): Secured resource details.
        """
        content = {
            'message': 'This is a secured endpoint.',
            'user': str(request.user),  # User object associated with the token
        }
        return Response(content)

class CustomAuthToken(ObtainAuthToken):
    """
    Custom API endpoint for obtaining authentication tokens.

    Authentication:
    - Basic authentication is required.

    Permissions:
    - All users have access to this endpoint.

    Methods:
    - POST: Obtain an authentication token.
        - Parameters:
            - username (string): User's username.
            - password (string): User's password.
        - Response (200 OK):
            {
                "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
            }
    """
    def post(self, request, *args, **kwargs):
        """
        Obtain an authentication token.

        Parameters:
        - username (string): User's username.
        - password (string): User's password.

        Returns:
        - Response (200 OK): Authentication token.
        """
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
