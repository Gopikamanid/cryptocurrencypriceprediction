from django.urls import path
from dashboard.views import home1,home,login,login1,register,register1,prices,predict,emailverify,details

urlpatterns = [
    path("",home1),
    path('register',register),
    path('register1',register1),
    path('login1',login1),
    path('login',login),
    path('prices',prices),
    path('predict',predict),
    path('emailverify',emailverify),
    path('details',details)
]
