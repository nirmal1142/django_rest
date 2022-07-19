from django.urls import path, include, re_path
from dairymaster.views import daily_milk_details_add ,DairyMasterUpdateView,RetailRateView,GetAllReportsCardView,DairyMasterGetByManyDate,daily_milk_details_update_delete,DailyMilkDetailGetById,daily_milk_details_get_by_month, MonthlyReportView

urlpatterns = [
    path('daily-milk-details-add/', daily_milk_details_add, name='daily_milk_details_add'),
    path('daily-milk-details-update', daily_milk_details_update_delete, name='daily_milk_details_update'),
    path('daily-milk-details-get-by-id', DailyMilkDetailGetById.as_view(), name='daily_milk_details_get_by_id'),
    path('daily-milk-details-get-by-date', DairyMasterGetByManyDate.as_view(), name='daily_milk_details_get_by_many_date'),
    path('daily-milk-details-get-by-month', daily_milk_details_get_by_month, name='daily_milk_details_get_by_month'),
    path('monthly-report', MonthlyReportView.as_view(), name='monthly_report'),
    path('get-all-reports-card', GetAllReportsCardView.as_view(), name='get_all_reports_card'),
    path('retail-rate', RetailRateView.as_view(), name='retail_rate_add'),
    path('dairy-master-update', DairyMasterUpdateView.as_view(), name='dairy_master_update'),

]
