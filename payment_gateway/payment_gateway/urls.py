# from django.contrib import admin
# from django.urls import path, include
# from django.shortcuts import redirect 

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/v2/', include('payments.urls')),
#     path('', lambda request: redirect('api/v2/'), name='root'),  # Redirect / to /api/v2/
# ]
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v2/', include('payments.urls')),  # Route all /api/v2/ requests to payments app
]