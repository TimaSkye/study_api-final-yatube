from django.urls import path, include

urlpatterns = [
    'v1/', include('api.v1.urls', namespace='v1'),
]
