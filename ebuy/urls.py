from django.conf.urls import include, url
from ebuy import views as ebuy_views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', ebuy_views.home, name='home'),
    url(r'^profile$', ebuy_views.profile, name='profile'),
    # Route for built-in authentication with our own custom login page
    url(r'^login', auth_views.login, {'template_name':'login.html'},name='login'),
    # Route to logout a user and send them back to the login page
    url(r'^logout$', auth_views.logout_then_login, name='logout'),
    url(r'^register$', ebuy_views.register, name='register'),
    url(r'^item/(?P<id>\d+)$', ebuy_views.see_item, name='item'),
    url(r'^category/(?P<category>\w+)$', ebuy_views.displayByCategory, name='displayByCategory'),
    url(r'^allhome$', ebuy_views.displayall, name='displayall'),
    url(r'^get_img1/(?P<id>\d+)', ebuy_views.get_img1,name='get_img1'),
    url(r'^get_img2/(?P<id>\d+)', ebuy_views.get_img2,name='get_img2'),
    url(r'^get_img3/(?P<id>\d+)', ebuy_views.get_img3,name='get_img3'),
    url(r'^get_share_img1/(?P<id>\d+)', ebuy_views.get_share_img1,name='get_share_img1'),
    url(r'^get_profilephoto/(?P<id>\d+)', ebuy_views.get_profilephoto,name='get_profilephoto'),
    # url(r'^edit_profile$', ebuy_views.edit_profile,name='edit_profile'),
    url(r'^get-title-json$', ebuy_views.get_title_json),
    url(r'^display_by_search$', ebuy_views.display_by_search, name='display_by_search'),
    url(r'^bagview$', ebuy_views.see_bag, name = 'bag'),
    url(r'^updatebag/(?P<id>\d+)$', ebuy_views.update_bag, name = 'updatebag'),
    url(r'^addBag/(?P<id>\d+)$', ebuy_views.add_to_bag, name='addBag'),
    # add to wish list
    url(r'^addWish/(?P<id>\d+)$', ebuy_views.add_to_wish, name='addWish'),
    url(r'^wishlist$', ebuy_views.see_wish, name = 'wishlist'),
    url(r'^removeWish/(?P<id>\d+)$', ebuy_views.remove_from_wishlist, name='removeWish'),
    url(r'^putInBag/(?P<id>\d+)$', ebuy_views.change_to_bag, name='putInBag'),
    url(r'^putInWish/(?P<id>\d+)$', ebuy_views.change_to_wish, name='change_to_wish'),
    url(r'^profile_wishlist$', ebuy_views.profile_wishlist, name = 'profile_wishlist'),
    url(r'^delete-item/(?P<id>\d+)$', ebuy_views.delete_item, name='delete'),
    url(r'^delete-share/(?P<id>\d+)$', ebuy_views.delete_share, name='delete_share'),
    url(r'^profile_share$', ebuy_views.profile_share, name = 'profile_share'),
    url(r'^previous_orders$', ebuy_views.prev_orders, name = 'orders'),
    url(r'^add_orders$', ebuy_views.bag_to_orders, name = 'addOrders'),
    url(r'^comment/(?P<id>\d+)$', ebuy_views.comment, name = 'comment'),
    url(r'^confirm-registration/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$',
        ebuy_views.confirm_registration, name='confirm'),
]

