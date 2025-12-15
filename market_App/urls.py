from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name="signup"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logOut, name='logout'),
    path('profile/', views.profile, name='profile'),
    path("listings/create/", views.create_Listing, name="create_listing"),
    path('listing-confirmation/', views.listing_confirmation, name="listing_confirmation"),
    path('edit_listing/<int:pk>/', views.edit_listing, name='edit_listing'),
    path('delete_listing/<int:pk>/', views.delete_listing, name='delete_listing'),
    path('listing/<int:pk>/', views.view_listing, name='view_listing'),
    path("inbox/", views.inbox, name="inbox"),
    path("bookmark/<int:pk>/", views.toggle_bookmark, name="toggle_bookmark"),
    path("bookmarks/", views.bookmarks, name="bookmarks"),
]