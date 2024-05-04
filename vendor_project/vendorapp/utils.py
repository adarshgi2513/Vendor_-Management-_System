from .models import PurchaseOrder
from django.db.models import Sum, F

def calculate_on_time_delivery_rate(vendor):
    completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
    total_completed_pos = completed_pos.count()
    
    if total_completed_pos == 0:
        return 0
    
    on_time_delivered_pos = completed_pos.filter(delivery_date__lte=F('promised_date')).count()
    
    return (on_time_delivered_pos / total_completed_pos) * 100

def calculate_quality_rating_average(vendor):
    completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed').exclude(quality_rating=None)
    total_completed_pos = completed_pos.count()
    
    if total_completed_pos == 0:
        return 0
    
    quality_rating_sum = completed_pos.aggregate(Sum('quality_rating'))['quality_rating__sum']
    
    return quality_rating_sum / total_completed_pos

def calculate_average_response_time(vendor):
    completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed').exclude(acknowledgment_date=None)
    total_completed_pos = completed_pos.count()
    
    if total_completed_pos == 0:
        return 0
    
    total_response_time = sum((po.acknowledgment_date - po.issue_date).days for po in completed_pos)
    
    return total_response_time / total_completed_pos

def calculate_fulfillment_rate(vendor):
    total_pos = PurchaseOrder.objects.filter(vendor=vendor).count()
    
    if total_pos == 0:
        return 0
    
    fulfilled_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed', issues=None).count()
    
    return (fulfilled_pos / total_pos) * 100
