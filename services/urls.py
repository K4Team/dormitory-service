

from django.urls import path
from services.views import user

urlpatterns = [
    path('UserList', user.GetOneNews.as_view(), name='get_one_news'),

]