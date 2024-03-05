from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from ecom_app.forms import Registration_form
from django.http import Http404
import requests

from ecom_app.models import Product_Model
from ecom_app.models import User_Model
from ecom_app.models import Cart_Model

# Create your views here.
def Home_page_view(req):
    #if user has logined then only they are allowed to view home page else they are redirected to registration page

    islogin=req.session.get("username")

    if islogin:
        # print(f"\n\nwhat is inside is login : {islogin} \n\n")

        logined_user=User_Model.objects.get(username=islogin)

        all_data=Product_Model.objects.all()

        user_id=logined_user.id

        context={
            "username" : islogin,
            "user_id":user_id,
            "all_data":all_data,
        }

        return render(req,"home.html", context)
    else:
        return redirect("register")
    
    
def Login_page_view(req):
    
    return render(req,"login.html")


def Register_page_view(req):

    if req.method=="POST":
        
        new_user=Registration_form(req.POST)
        
        usrname_exists=User_Model.objects.filter(username=req.POST.get("username"))

        if usrname_exists:
            return HttpResponse("<h3>Username Already Taken</h3>")
        
        elif new_user.is_valid():

            new_user.save()

            req.session["username"]=req.POST.get("username")

            req.session["user_id"]=req.POST.get("id")

            return redirect("home")

    context={
        "Registration_form" : Registration_form
    }

    return render(req,"register.html",context)

def load_api_data(req):

    api_data=requests.get("https://fakestoreapi.com/products")

    if api_data.status_code==200:

        json_data=api_data.json()

        for item in json_data:
            title=item.get("title")
            price=item.get("price")
            desc=item.get("description")
            category=item.get("category","Unknown")
            image=item.get("image")
            # here this "rating" itself is a dictionary and it contain rate and count
            rating_dict=item["rating"]

            rating=rating_dict["rate"]
            rating_count=rating_dict["count"]

            Product_Model.objects.create(
                title=title,
                price=price,
                desc=desc,
                category=category,
                image=image,
                rating=rating,
                rating_count=rating_count,
            )

        return redirect("home")
    else:
        return HttpResponse("Failed to Fetch Data :( ")


# Short Summary how we are adding products into the cart
"""
You retrieve the product instance based on the provided product ID. Then, you check if a user is logged in. If a user is logged in, you retrieve the corresponding user instance. After that, you create or retrieve the cart associated with the user. If the cart doesn't exist, it's created. Next, you add the retrieved product to the cart. Finally, you render the cart page with the updated list of products in the cart (Frontend).
"""
def Add_to_Cart(req,product_id):
    product_to_add=get_object_or_404(Product_Model,id=product_id)

    islogin=req.session.get("username")

    if islogin:

        try:
            curr_user=get_object_or_404(User_Model,username=islogin)
        except User_Model.DoesNotExist:
            raise Http404("User does not Exist")
        
        #created/ retreving a Cart for this specific User

        #The _ in this line is used to discard the second element of the tuple (i.e., the boolean value indicating whether the instance was created or not)
        cart,_ = Cart_Model.objects.get_or_create(user=curr_user)

        #adding products to that cart
        cart.products_in_cart.add(product_to_add)

        # product_in_cart=Cart_Model.objects.all() # previously i was getting all the data  for all user 

        product_in_cart=Cart_Model.objects.filter(user=curr_user)
        product_in_cart=product_in_cart

        # sending user id to fix nav bar issue
        logined_user=User_Model.objects.get(username=islogin)
        user_id=logined_user.id
        username=req.session.get("username")
        context={
            "product_in_cart":product_in_cart,
            "user_id":user_id,
            "username":username
        }

        return render(req,"cart.html",context)
    
    else:
        return redirect("login")
    

def AboutView(req):
    # sending user id to fix nav bar issue
    islogin=req.session.get("username")
    logined_user=User_Model.objects.get(username=islogin)
    user_id=logined_user.id
    username=req.session.get("username")
    context={
        "user_id":user_id,
        "username":username,
    }
    return render(req,"about.html",context)

def detailed_view(req,product_id):
    # sending user id to fix nav bar issue
    islogin=req.session.get("username")

    logined_user=User_Model.objects.get(username=islogin)
    user_id=logined_user.id
    username=req.session.get("username")

    this_product_data=Product_Model.objects.get(id=product_id)

    context={
        "user_id":user_id,
        "username":username,
        "this_product_data" : this_product_data

    }
    return render(req,"detailed_html.html",context)