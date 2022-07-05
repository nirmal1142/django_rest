from django.urls import path, include, re_path
from dairymaster.views import daily_milk_details_add ,DairyMasterGetByManyDate,daily_milk_details_update_delete,DailyMilkDetailGetById,DairyMasterUpdateView,daily_milk_details_get_by_month, MonthlyReportView

urlpatterns = [
    path('daily-milk-details-add/', daily_milk_details_add, name='daily_milk_details_add'),
    path('daily-milk-details-update', daily_milk_details_update_delete, name='daily_milk_details_update'),
    path('daily-milk-details-get-by-id', DailyMilkDetailGetById.as_view(), name='daily_milk_details_get_by_id'),
    path('daily-milk-details-updates/<pk>/', DairyMasterUpdateView.as_view(), name='daily_milk_details_update'),
    path('daily-milk-details-get-by-date', DairyMasterGetByManyDate.as_view(), name='daily_milk_details_get_by_many_date'),
    path('daily-milk-details-get-by-month', daily_milk_details_get_by_month, name='daily_milk_details_get_by_month'),
    path('monthly-report', MonthlyReportView.as_view(), name='monthly_report'),


]
