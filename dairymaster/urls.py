from django.urls import path, include, re_path
from dairymaster.views import daily_milk_details_add ,daily_milk_details_get_by_many_date,company_profile,daily_milk_details_update_delete,DailyMilkDetailGetById,DairyMasterUpdateView

urlpatterns = [
    path('daily-milk-details-add/', daily_milk_details_add, name='daily_milk_details_add'),
    path('company-profile/', company_profile, name='company_profile'),
    path('daily-milk-details-update', daily_milk_details_update_delete, name='daily_milk_details_update'),
    path('daily-milk-details-get-by-id', DailyMilkDetailGetById.as_view(), name='daily_milk_details_get_by_id'),
    path('milk-details-get-by-date/', daily_milk_details_get_by_many_date, name='daily_milk_details_get_by_many_date'),
    path('daily-milk-details-updates/<pk>/', DairyMasterUpdateView.as_view(), name='daily_milk_details_update'),

]
