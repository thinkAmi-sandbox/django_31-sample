from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('warn$', TemplateView.as_view(template_name='silence_app/index.html')),
]
