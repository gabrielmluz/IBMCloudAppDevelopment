from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'

# Path to acess the views
urlpatterns = [
    path('about', view=views.about, name='about'),
    path('contact', view=views.contact, name='contact'),
    path('signup', view=views.registration_request, name='signup'),
    path('login', view=views.login_request, name='login'),
    path('logout', view=views.logout_request, name='logout'),
    path('', view=views.get_dealerships, name='index'),
    # Parse the dealer id to get the reviews
    path('dealer/<int:dealer_id>/', views.get_dealer_details, name='dealer_details'),
    path('add_review', views.add_review, name='postreview'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)