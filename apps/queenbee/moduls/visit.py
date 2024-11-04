from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta

from apps.cms.models import Visit
from apps.queenbee.permissions import permission_required

@staff_member_required(login_url='/admin/login/')
@permission_required('visit_statistics', 'Просмотр раздела Посещаемость сайта')
def visit_statistics(request):
    # Date range for the last 7 days
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=6)  # 6 days back to include today as 7 days total
    
    # Tracked paths for analytics
    tracked_paths = ['/', '/about/', '/contact/', '/faq/', '/services/', '/services_details/']
    
    # Prepare visit data for each path within the 7-day range
    visits_data = []
    for path in tracked_paths:
        daily_counts = (
            Visit.objects.filter(url_path=path, timestamp__date__range=[start_date, end_date])
            .extra(select={'day': "date(timestamp)"})
            .values('day')
            .annotate(count=Count('id'))
            .order_by('day')
        )
        
        # Map days to counts, ensuring missing days have a count of 0
        daily_data = {str(day['day']): day['count'] for day in daily_counts}
        visits_data.append({
            'path': path,
            'daily_data': [daily_data.get(str(start_date + timedelta(days=i)), 0) for i in range(7)]
        })
    
    # Generate date labels for the last 7 days
    labels = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
    
    context = {
        'labels': labels,
        'visits_data': visits_data,
    }
    return render(request, 'queenbee/visit/index.html', context)