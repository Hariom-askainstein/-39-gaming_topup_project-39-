from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta
from .models import TopUpOrder, TopUpProduct
from .serializers import TopUpOrderSerializer

class TopUpOrderCreateAPIView(APIView):
    def post(self, request):
        serializer = TopUpOrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            return Response({'message': 'Top-up order created', 'order_id': order.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DashboardView(APIView):
    # permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        # Top 5 products
        top_products = (TopUpOrder.objects.filter(status='success')
                        .values('product__name')
                        .annotate(purchase_count=Count('id'))
                        .order_by('-purchase_count')[:5])

        # Daily revenue (last 7 days)
        today = timezone.now().date()
        last_7_days = [
            {
                'date': (today - timedelta(days=i)).strftime('%Y-%m-%d'),
                'revenue': TopUpOrder.objects.filter(
                    created_at__date=today - timedelta(days=i),
                    status='success'
                ).aggregate(total=Sum('product__price'))['total'] or 0
            } for i in range(7)
        ]

        # Failed payments (current month)
        failed_count = TopUpOrder.objects.filter(
            status='failed',
            created_at__month=today.month
        ).count()

        return Response({
            'top_products': list(top_products),
            'daily_revenue': last_7_days,
            'failed_count': failed_count
        })
