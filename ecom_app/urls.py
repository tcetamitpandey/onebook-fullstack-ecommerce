from django.urls import path

from ecom_app.views import Home_page_view
from ecom_app.views import Register_page_view
from ecom_app.views import Login_page_view
from ecom_app.views import load_api_data
from ecom_app.views import Add_to_Cart
from ecom_app.views import AboutView
from ecom_app.views import detailed_view


urlpatterns=[

    path("",Home_page_view,name="home"),
    path("register/",Register_page_view,name="register"),
    path("login/",Login_page_view,name="login"),
    path("load/",load_api_data,name="load"),
    path("cart/<int:product_id>",Add_to_Cart,name="add_to_cart"),
    path("product/<int:product_id>",detailed_view,name="detailed_view"),
    path("about/",AboutView,name="about"),

]