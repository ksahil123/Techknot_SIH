from django.urls import path
from . import views


urlpatterns = [
	
	path('',views.firstPage,name='First Page'),
	path('about/',views.aboutPage,name='About Page'),
	path('locations/',views.setAddressPage,name='Address Page'),
	
]
