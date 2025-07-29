from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
import requests
from django.shortcuts import render, redirect
from django.contrib import messages

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render

from django.contrib import messages
from django.shortcuts import redirect

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
import requests


from .context_processors import *
from django.core.paginator import Paginator
from django.core.paginator import Paginator
from django.shortcuts import render
import json


from django.shortcuts import render
from django.core.paginator import Paginator
import json

import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt



Baseurl = "https://api.zbazaarsolutions.biz/api"


'''=============================== New User Register Method ============================================'''


def new_user_register_view(request):
    
    message = None  
    if request.method == 'POST':
        data = {
            'username': request.POST.get('username', '').strip(),
            'email': request.POST.get('email', '').strip(),
            'mobile': request.POST.get('mobile', '').strip(),
            'tpin': request.POST.get('tpin', '').strip(),
            'password': request.POST.get('password', '').strip(),
            'confirm_password': request.POST.get('confirm_password', '').strip(),
   
        }

        try:
            response = requests.post(f"{Baseurl}/register-user/", json=data)
            api_response = response.json()
            if api_response.get('status') is True:
              
                message = api_response.get('message', 'Account created successfully.')
                
            else:
                message = api_response.get('message', 'Failed to register.')
        except ValueError:
            message = 'Invalid response from API.'
        except requests.exceptions.RequestException as e:
            message = f'API request failed: {str(e)}'


    return render(request, 'new_user_register.html',{'form_type': 'create', 'message': message})


'''=============================== Home Method ============================================'''

def home(request):
    products= product_list_view(request)
    try:
        pd = products['data']
    except:
        pd = []    

    return render(request, 'home.html', {'products': pd})


'''=============================== Products Method ============================================'''

def product_list_view(request):
    products=[]
    try:
        # response = requests.get(f"{Baseurl}/products/")
        response = requests.get(
            f"{Baseurl}/products/",
            params={'page': 1, 'size': 15}
        )
        if response.status_code == 200:
            data = response.json()
            product_list = data  
            products = product_list
          
        
            return products
          
        else:
            messages.error(request, "Failed to fetch products.")
         
            return products
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
     
        return products


'''=============================== Register user Method ============================================'''
def create_account(request):
    message = None  
    if request.method == 'POST':
        data = {
            'username': request.POST.get('username', '').strip(),
            'email': request.POST.get('email', '').strip(),
            'mobile': request.POST.get('mobile', '').strip(),
            'tpin': request.POST.get('tpin', '').strip(),
            'password': request.POST.get('password', '').strip(),
            'confirm_password': request.POST.get('confirm_password', '').strip(),
            'sponsor': request.POST.get('sponsor', '').strip(),
        }

        try:
            response = requests.post(f"{Baseurl}/register-user/", json=data)
            api_response = response.json()
            if api_response.get('status') is True:
                message = 'Account created successfully.'
            else:
                message = api_response.get('message', 'Failed to register.')
        except ValueError:
            message = 'Invalid response from API.'
        except requests.exceptions.RequestException as e:
            message = f'API request failed: {str(e)}'

    return render(request, 'login.html', {'form_type': 'create', 'message': message})



import requests
from django.shortcuts import render, redirect
from django.contrib import messages
import json


'''=============================== Sigin Method ============================================'''

def sign_in(request):
    if request.method == 'POST':
        identifier = request.POST.get('identifier', '').strip()
        password = request.POST.get('password', '').strip()
        tpin = request.POST.get('tpin', '').strip()
        remember_me = request.POST.get('remember_me') 

        payload = {
            'identifier': identifier,
            'password': password,
            'tpin': tpin
        }

        try:
            response = requests.post(f"{Baseurl}/user/login/", json=payload)
            data = response.json()
    
            if data['status'] == 'success':
                request.session['access_token'] = data.get('access')
                request.session['user_data'] = data

                if remember_me:
                    # Session expires in 7 days
                    request.session.set_expiry(7 * 24 * 60 * 60)
                else:
                    # Session expires when the browser is closed
                    request.session.set_expiry(0)

                # messages.success(request, 'Login successful!')
                return redirect('homepage_view')  
            else:
                msg = data.get('message')
                messages.error(request, data.get('message', f'{msg}'))

        except requests.exceptions.RequestException as e:
            messages.error(request, f"API request failed: {str(e)}")
        except ValueError:
            messages.error(request, "Invalid response from login API.")

    return render(request, 'login.html', {'form_type': 'signin'})


'''=============================== Logout Method ============================================'''

from django.shortcuts import redirect
from django.contrib import messages

def logout_view(request):
    # Clear all session data
    request.session.flush()
    
    # Optionally clear messages
    # messages.success(request, "You have been logged out successfully.")
    return redirect('/')  

'''=============================== Homepage Method ============================================'''

# def homepage_view(request, app_menu):
#     print(f'{app_menu=}')
#     user_data = request.session.get("user_data") 
#     app_menu = app_menu.replace('-', ' ').title()
#     page_number = request.GET.get('page', 1)
#     size = 10
#     product_response = product_Show_view(request, page=page_number, size=size)
#     product_list = product_response.get('data', []) if isinstance(product_response, dict) else []

#     # Paginate
#     paginator = Paginator(product_list, size)
#     try:
#         products = paginator.page(page_number)
#     except:
#         products = paginator.page(1)

#     # Marquee
#     marquee_data = marquee_context(request, app_menu)
#     marquee_text = ''
#     if marquee_data and isinstance(marquee_data, list):
#         marquee_text = marquee_data[0].get('marquee_text', '')
#     marquee_text_list = [marquee_text] if marquee_text else []

#     # Banners
#     all_banners = banner_context(request, app_menu)
#     banners_home1 = [banner for banner in all_banners if banner.get('Banner_type') == f'{app_menu}1']
#     banners_home2 = [banner for banner in all_banners if banner.get('Banner_type') == f'{app_menu}2']
#     # print(f'111111{banners_home1=}')
#     # print(f'2222222{banners_home2=}')
#     # print(f'tttttttttttttttttttttt=={all_banners=}')

#     cart_count = cart_count_view(request)

#     # ✅ Wapas session me save karna:
#     request.session['cart_count'] = cart_count
        
#     cart_count = request.session.get("cart_count")
      
#     # print(f'ppppppppp{cart_count=}')     

#     return render(request, 'homepage.html', {
#         'products': products,
#         'page_obj': products,
#         'marquee_text': json.dumps(marquee_text_list),
#         'banner_data': banners_home1,
#         'banners_home2':banners_home2,
#         'user_data':user_data,
#         "cart_count": cart_count,
      
#     })

from django.shortcuts import render
from django.core.paginator import Paginator
from .template_config import APP_MENU_TEMPLATE_MAP, DEFAULT_TEMPLATE
import json

# def homepage_view(request, app_menu):
#     print(f'{app_menu=}')
#     user_data = request.session.get("user_data") 
#     app_menu_cleaned = app_menu.replace('-', ' ').title()

#     page_number = request.GET.get('page', 1)
#     print(f'page numbrrrr{page_number=}')
#     size = 2

#     print(f'{app_menu_cleaned=}')
#     # ✅ Dynamic template include
#     template_include = APP_MENU_TEMPLATE_MAP.get(app_menu_cleaned, DEFAULT_TEMPLATE)
#     print(f'{template_include=}')


      
   

#     product_categories = []
#    # ✅ API Call Based on app_menu_cleaned
#     if app_menu_cleaned == "Home":
#         # You can call homepage-specific API or reuse product API if same
#         data_response = product_Show_view(request, page=page_number, size=size)

#     elif app_menu_cleaned == "Products":
#         print('elif products')
#         # For product-specific page (like product listing or filtering)
#         data_response = product_Show_view(request, page=page_number, size=size)
#         print(f'{data_response=}')
     
        
#         product_categories = Product_Category_view(request) 
#         # print(f'{product_categories=}')
         

#     # elif app_menu_cleaned == "Service":
#     #     data_response = service_Show_view(request, page=page_number, size=size)

#     # elif app_menu_cleaned == "Uva Class":
#     #     data_response = uva_class_view(request, page=page_number, size=size)

#     # # Add more cases as needed
#     # elif app_menu_cleaned == "Ineed":
#     #     data_response = Ineed_view(request)
#         # sidebar_items = get_ineed_categories()
#         # sidebar_title = "Ineed Categories"

#     # elif app_menu_cleaned == "Sewa":
#     #     data_response = sewa_view(request, page=page_number, size=size)

#     # elif app_menu_cleaned == "Business":
#     #     data_response = business_view(request, page=page_number, size=size)

#     # elif app_menu_cleaned == "Uva Pay":
#     #     data_response = uva_pay_view(request, page=page_number, size=size)

#     else:
#         # Default fallback
#         data_response = {"data": []}
#         product_categories=[]


#     data_list = data_response.get('data', []) if isinstance(data_response, dict) else []

#     # ✅ Paginate
#     paginator = Paginator(data_list, size)
#     try:
#         page_obj = paginator.page(page_number)
#     except:
#         page_obj = paginator.page(1)

#     # ✅ Marquee, Banners, Cart, etc. (same as before)
#     marquee_data = marquee_context(request, app_menu_cleaned)
#     marquee_text = marquee_data[0].get('marquee_text', '') if marquee_data else ''
#     marquee_text_list = [marquee_text] if marquee_text else []

#     all_banners = banner_context(request, app_menu_cleaned)
#     # print(f'{all_banners=}')
#     banners_home1 = [b for b in all_banners if b.get('Banner_type') == f'{app_menu_cleaned}1']
#     banners_home2 = [b for b in all_banners if b.get('Banner_type') == f'{app_menu_cleaned}2']

#     cart_count = cart_count_view(request)
#     request.session['cart_count'] = cart_count

#     return render(request, "homepage.html", {
#         'page_obj': page_obj,
#         'products': page_obj,  # ✅ name products hi rehne do for all
#         'template_include': template_include,
#         'marquee_text': json.dumps(marquee_text_list),
#         'banner_data': banners_home1,
#         'banners_home2': banners_home2,
#         'user_data': user_data,
#         "cart_count": cart_count,
#         'product_categories':product_categories
    
#     })
from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib import messages
import json
import requests

def get_products_from_api(page, size, category=None):
    try:
        params = {
            'page': page,
            'size': size
        }
        if category:
            params['category'] = category

        response = requests.get(f"{Baseurl}/products/", params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def homepage_view(request, app_menu):
    print(f'{app_menu=}')
    user_data = request.session.get("user_data") 
    app_menu_cleaned = app_menu.replace('-', ' ').title()
    print(f'{app_menu_cleaned=}')
    page_number = int(request.GET.get('page', 1))
    size = 10
    category = request.GET.get("category")

    template_include = APP_MENU_TEMPLATE_MAP.get(app_menu_cleaned, DEFAULT_TEMPLATE)

    categories = []
    products = []
    pagination = {}

    if app_menu_cleaned == "Products":
        response = get_products_from_api(page=page_number, size=size, category=category)
        if response:
            products = response.get("data", [])
            pagination = {
                'page': response.get("page", 1),
                'size': response.get("size", size),
                'total_pages': response.get("total_pages", 1),
                'total_items': response.get("total_items", 0),
            }
            categories = Product_Category_view(request)

    # --- Banners, Marquee, etc ---
    marquee_data = marquee_context(request, app_menu_cleaned)
    marquee_text = marquee_data[0].get('marquee_text', '') if marquee_data else ''
    marquee_text_list = [marquee_text] if marquee_text else []

    all_banners = banner_context(request, app_menu_cleaned)
    banners_home1 = [b for b in all_banners if b.get('Banner_type') == f'{app_menu_cleaned}1']
    banners_home2 = [b for b in all_banners if b.get('Banner_type') == f'{app_menu_cleaned}2']

    cart_count = cart_count_view(request)
    request.session['cart_count'] = cart_count

    return render(request, "homepage.html", {
        'products': products,
        'pagination': pagination,
        'template_include': template_include,
        'marquee_text': json.dumps(marquee_text_list),
        'banner_data': banners_home1,
        'banners_home2': banners_home2,
        'user_data': user_data,
        'cart_count': cart_count,
        'categories': categories,
        'selected_category': category,
        'app_menu':app_menu
    })


# def Ineed_view(request):
#     # sidebar_items = get_ineed_categories()
#     # sidebar_title = "Ineed Categories"
    
#     return render(request, 'includes/Ineed.html', {
#         # 'sidebar_items': sidebar_items,
#         # 'sidebar_title': sidebar_title
#     })

# def get_ineed_categories():
#     return [
#         {"name": "Plumber"},
#         {"name": "Electrician"},
#         {"name": "Mechanic"},
#         {"name": "AC Service"},
#         {"name": "Painter"},
#     ]

# def get_product_categories():
#     # Sample static data (replace with DB/API fetch)
#     return [
#         {"id": 1, "name": "Fashion"},
#         {"id": 2, "name": "Electronics"},
#         {"id": 3, "name": "Home & Living"},
#         {"id": 4, "name": "Grocery"},
#         {"id": 5, "name": "Beauty"},
#         {"id": 6, "name": "Kids"},
#         {"id": 7, "name": "Toys"},
#         {"id": 8, "name": "More"},
#     ]


'''=============================== Product List Method ============================================'''
from django.core.paginator import Paginator
# def product_Show_view(request, page, size):
#     products = []
#     page = int(page)  # ensure it's an int
#     total_pages = 1

#     try:
#         params = {'page': page, 'size': size}
#         category = request.GET.get("category")
#         if category:
#             params['category'] = category

#         response = requests.get(f"{Baseurl}/products/", params=params)

#         if response.status_code == 200:
#             data = response.json()
       

#             products = data.get('data', [])  # Actual products
#             total_pages = data.get('total_pages', 1)
#         else:
#             messages.error(request, "Failed to fetch products.")

#     except Exception as e:
#         messages.error(request, f"Error: {str(e)}")

#     # ✅ Return structured pagination data
#     return {
#         "products": products,
#         "page": page,
#         "total_pages": total_pages
#     }


'''=============================== Product detail Method ============================================'''

def product_detail_view(request, Product_id):
    user_data = request.session.get("user_data")
    cart_count = request.session.get("cart_count") 
    products = {}

    try:
        response = requests.get(
            f"{Baseurl}/products/detail/",
            params={'Product_id': Product_id}
        )

        if response.status_code == 200:
            data = response.json()
            products = data
            # print(f'{products=}')
        else:
            messages.error(request, "Failed to fetch product details.")

    except Exception as e:
        messages.error(request, f"Error: {str(e)}")

 
    return render(request, 'products_details.html', {'product': products ,'user_data':user_data, "cart_count": cart_count,})

'''=============================== Profile Method ============================================'''
import requests
from django.http import JsonResponse
import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings



def get_profile_view(request):
    access_token = request.session.get('access_token')
    user_data = request.session.get("user_data") 
    # user_id = request.session.get("user_id")  # ✅ ID session se lo
    cart_count = request.session.get("cart_count")
    print(f'{user_data=}')
    print(f'{access_token=}')
    if not access_token :
        return redirect('sign_in')
    # if not access_token:
    #     return redirect('sign_in')
    

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    try:
        # response = requests.get(f"{Baseurl}/get-user/details/", headers=headers)
        # ✅ User ID se API call
        response = requests.get(f"{Baseurl}/get-user/details/", headers=headers)
        print(f'{response=}')
        if response.status_code == 200:
            response.raise_for_status()
            profile_data = response.json()
            # print(f'{user_data=}')

            profile_data = profile_data.get('data', {})
            # return JsonResponse(profile_data)
            return render(request, 'profile.html', {'user_data': user_data ,"profile_data":profile_data
                                               ,"cart_count": cart_count,})
        else:
            return redirect('sign_in')
    


    except requests.exceptions.RequestException as e:
        # print(f'API Request Error: {e}')
        return render(request, 'profile.html', {'user_data': None, 'error': 'Failed to load user details'})
    

'''=============================== Update Profile Method ============================================'''

from django.shortcuts import render, redirect
from django.contrib import messages
import requests
import datetime

def update_profile_view(request):
    cart_count = request.session.get("cart_count")
    # if 'access_token' not in request.session:
    #     return redirect('login')

    access_token = request.session.get('access_token')
   
    user_data = request.session.get("user_data") 

    # print(f'{user_data=}')
    # print(f'{access_token=}')
    user_details = []
    
    if request.method == "POST":
        dob = request.POST.get("dob")
        gender = request.POST.get("gender")
        nominee_name = request.POST.get("nominee_name")
        nominee_relation = request.POST.get("nominee_relation")
        profile_photo = request.FILES.get("profile")

        data = {
            'dob': dob,
            'gender': gender,
            'nominee_name': nominee_name,
            'nominee_relation': nominee_relation,
        }
        # print(f'{data=}')
       
        files = {}
        if profile_photo:
            files['profile'] = (profile_photo.name, profile_photo.read(), profile_photo.content_type)

        try:
            headers = {
                'Authorization': f'Bearer {access_token}',
                
            }
            response = requests.post(
                f"{Baseurl}/update-profile/",
                data=data,
                files=files,
                headers=headers
            )
            
            result = response.json()
            if response.status_code == 200:
                messages.success(request, "Profile updated successfully.")
            else:
                messages.error(request, result.get("message", "Failed to update profile."))
        except Exception as e:
            messages.error(request, f"Error occurred: {str(e)}")

    try:
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        response = requests.get(f"{Baseurl}/get-user/details/", headers=headers)
        # print(f'{response=}')

        
    
        if response.status_code == 200:
            user_details = response.json().get("data", {})
            # print(f'{user_details=}')
              # ✅ Convert DOB format if available
            if 'dob' in user_details and user_details['dob']:
                dob_str = user_details['dob']
                
             
                try:
                    # If contains '/', assume DD/MM/YYYY
                    if '/' in dob_str:
                        parsed_dob = datetime.datetime.strptime(dob_str, '%d/%m/%Y')
                    else:
                        parsed_dob = datetime.datetime.strptime(dob_str, '%Y-%m-%d')

                    user_details['dob'] = parsed_dob.strftime('%Y-%m-%d')
                    # print(f'Converted DOB: {user_details["dob"]}')
                except ValueError:
                    user_details['dob'] = ''
                    # print('DOB format not recognized. Set as empty.')
     
            user_details = user_details 
           
        else:
            return render(request, "error.html", {"message": "Failed to load profile"}, status=400)
         

    except Exception as e:
        pass 
    return render(request, "update_profile.html", {'user_data':user_data,'user_details':user_details,
                                                    "cart_count": cart_count,})

'''=============================== Cart Count Method ============================================'''

def cart_count_view(request):
 
    access_token = request.session.get('access_token')
    user_data = request.session.get("user_data") 

    if 'access_token' not in request.session:
        return 0
    
    userid = user_data.get("userid")
 
    if not userid:
       return 0
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    params = {
        "userid": userid
    }
    try:
        response = requests.get(f"{Baseurl}/cart/count/", headers=headers,params=params)

        response.raise_for_status()
        cart_count = response.json()
        cart_product_count = cart_count.get('cart_product_count', {})
        # print(f'{cart_product_count=}')
        # return 0
        # ✅ Wapas session me save karna:
        request.session['cart_count'] = cart_product_count
        return cart_product_count
      

    except requests.exceptions.RequestException as e:
        # print(f'API Request Error: {e}')
        return 0
        # return redirect('sign_in')


'''=============================== Add Cart Method ============================================'''


def Addcart_view(request):
    access_token = request.session.get('access_token')
    user_data = request.session.get("user_data") 
    cart_count = request.session.get("cart_count")
    # print(f'access_token={access_token}')
    # print(f'user_data={user_data}')


    if 'access_token' not in request.session:
        return redirect('new_user_register')
    

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity',1)
        sizes = request.POST.get('sizes')  
      
    userid = user_data.get("userid")
    if not userid:
       return redirect('sign_in')



    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
   
    json = {
        "userid": userid,
        'product_id': product_id,
        'quantity': int(quantity),
        "size":sizes,
        "purchase_for":userid
    }
 
    # print(f'{json=}')
    try:
        response = requests.post(f"{Baseurl}/add/cart/", headers=headers,json=json)
        # print(f'{response=}')
        if response.status_code == 201:
            response.raise_for_status()
            addcart_data = response.json()
            # print(f'{addcart_data=}')

            addcart_data = user_data.get('data', {})
            cart_count_view(request)
        else:
            return redirect('sign_in')



    except requests.exceptions.RequestException as e:
        pass
        # print(f'API Request Error: {e}')
    
    return redirect(request.META.get('HTTP_REFERER', 'homepage_view'))


  
'''===============================  CartList Method ============================================'''


def cart_list_view(request):

    access_token = request.session.get('access_token')
    user_data = request.session.get("user_data") 
    cart_count = request.session.get("cart_count")


    # print(f'{access_token=}')

    if 'access_token' not in request.session:
        return redirect('sign_in')
    

    userid = user_data.get("userid")
 
    if not userid:
       return 0
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    total_mrp = 0
    total_amount = 0
    zv = 0
    discount_mrp = total_mrp - total_amount
    # print(f'{discount_mrp=}')
    # print(f'{total_amount=}')
    params = {
        "userid": userid
    }
    cart_data = []
 
    try:
        response = requests.get(f"{Baseurl}/cart/list/", headers=headers,params=params)
        
        # print(f'{response=}')
        # response.raise_for_status()  
        if response.status_code == 200:

            data = response.json()
       
            cart_data = data.get("data", []) 
            print(f'cart data{data=}')
            # return render(request, 'cart.html', {'cart_items': cart_data , "user_data":user_data ,  "cart_count": cart_count,})
            for i in cart_data:
                # print(f'{i=}')
              
                
                quantity = float(i['quantity']) 
                total_mrp = total_mrp + float(i['original_price']) * quantity
               
           
              
                total_amount += float(i['discounted_price']) * quantity 
                # print(f'{total_amount=}')
                discount_mrp = total_mrp - total_amount
                # print(f'{discount_mrp=}')

                zv = zv + float(i['zv'])

           
            return render(request, "cart.html", {'cart_items': cart_data ,   "user_data":user_data ,   
                "cart_count": cart_count,"total": total_mrp, "total_amount": total_amount,"discount_mrp":discount_mrp,
                "zv": zv})   
        else:
            return redirect('sign_in')                     

    except requests.exceptions.RequestException as e:
        pass
        # print(f'API Request Error: {e}')
        # return HttpResponse(f'{e=}')
    return render(request, "cart.html", {'cart_items': cart_data ,   "user_data":user_data ,    "cart_count": cart_count, 
             "total": total_mrp,"total_amount": total_amount,"discount_mrp":discount_mrp,"zv": zv})    





'''===============================  Remove Cart item Method ============================================'''

import requests
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

@require_POST
def RemoveCartItem_view(request):
    access_token = request.session.get('access_token')
    user_data = request.session.get("user_data")
    # print(f'{access_token=}')
    # print(f'{user_data=}')
    # cart_count = request.session.get("cart_count")

    if not access_token or not user_data:
        return redirect('sign_in')

    cart_id = request.POST.get('cart_id')
    userid = user_data.get("userid")
    # print(f'{cart_id=}')
    if not cart_id or not userid:
        return redirect(request.META.get('HTTP_REFERER', '/'))

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    json_data = {
        "id": int(cart_id),
        "userid": userid
    }
 

    try:
        response = requests.delete(f"{Baseurl}/remove/count/", headers=headers, json=json_data)
        # print(f'{response=}')
        if response.status_code == 200:

        
            response.raise_for_status()
            # print(f'ddddd{response=}')
            cart_count_view(request)

    except requests.RequestException as e:
        # print(f"Cart deletion error: {e}")
        pass

    # Redirect back to the same page
    return redirect(request.META.get('HTTP_REFERER', '/'))

'''===============================  Check address Method ============================================'''


def checkout_view(request):
    # if 'access_token' not in request.session:
    #     return redirect('sign_in')
    access_token = request.session.get('access_token')
    user_data = request.session.get("user_data")
    # print(f'{access_token=}')

   
    total_mrp = 0
    total_amount = 0
    zv = 0
    discount_mrp = total_mrp - total_amount
    # print(f'{discount_mrp=}')
    # print(f'{total_amount=}')


    userid = user_data.get("userid")
    if not userid:
       return redirect('sign_in')
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    params = {
        "userid": userid
    }
 
    address_data=[]
    message=[]
    try:
        response = requests.get(f"{Baseurl}/checkout-address/get/", headers=headers,params=params)
        # print(f'{response=}')
        # print(f'{response.text=}')
        
        if response.status_code == 200:
            data = response.json()
            address_data = data.get('data', {}).get('address', {})
            # print(f'adresssssssssssssssssss==={address_data=}')
         #   return render(request, 'checkout_address.html', {'addresses': addresses})

            for i in address_data:
                # print(f'{i=}')
              
                
                quantity = float(i['quantity']) 
                total_mrp = total_mrp + float(i['original_price']) * quantity
               
           
              
                total_amount += float(i['discounted_price']) * quantity 
                # print(f'{total_amount=}')
                discount_mrp = total_mrp - total_amount
                # print(f'{discount_mrp=}')


                zv = zv + float(i['zv'])
        else:
            data = response.json()
            # print(f'{data=}')
            # return HttpResponse('something went wrong')
         #   return render(request, 'checkout_address.html', {'addresses': [],message:'message'})

    except Exception as e:
        pass

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    total_mrp = 0
    total_amount = 0
    zv = 0
    discount_mrp = total_mrp - total_amount
    # print(f'{discount_mrp=}')
    # print(f'{total_amount=}')
    params = {
        "userid": userid
    }
    cart_data = []
 
    try:
        response = requests.get(f"{Baseurl}/cart/list/", headers=headers,params=params)
        
        # print(f'{response=}')
        # response.raise_for_status()  
        if response.status_code == 200:

            data = response.json()
       
            cart_data = data.get("data", []) 
            # print(f'cart data{data=}')
            # return render(request, 'cart.html', {'cart_items': cart_data , "user_data":user_data ,  "cart_count": cart_count,})
            for i in cart_data:
                # print(f'{i=}')
              
                
                quantity = float(i['quantity']) 
                total_mrp = total_mrp + float(i['original_price']) * quantity
               
           
              
                total_amount += float(i['discounted_price']) * quantity 
                # print(f'{total_amount=}')
                discount_mrp = total_mrp - total_amount
                # print(f'{discount_mrp=}')

                zv = zv + float(i['zv'])

            
        else:
            return redirect('sign_in')                     

    except requests.exceptions.RequestException as e:
        pass

    return render(request, 'checkout_address.html', {'addresses': address_data,'user_data':user_data,'cart_items': cart_data ,
                                                         'cart_count' :request.session.get("cart_count"),"total": total_mrp,
                                                           "total_amount": total_amount,"discount_mrp":discount_mrp,  "zv": zv })
              
                                              
'''===============================  List address Method ============================================'''

def addresses_list_view(request):
    # if 'access_token' not in request.session:
    #     return redirect('sign_in')
    access_token = request.session.get('access_token')
    user_data = request.session.get("user_data")
    # print(f'{access_token=}')
    # print(f'{user_data=}')

    userid = user_data.get("userid")
    if not userid:
       return redirect('sign_in')
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    params = {
        "userid": userid
    }
 
    addresses_list=[]

    try:
        response = requests.get(f"{Baseurl}/user/addresses/", headers=headers,params=params)
        # print(f'{response=}')
        # print(f'{response.text=}')
        
        if response.status_code == 200:
            data = response.json()
            addresses_list = data.get("data", []) 
        
            # return HttpResponse(f'{addresses_list=}')
       
        else:
            data = response.json()
            # print(f'{data=}')
            # return HttpResponse('something went wrong')
   

    except Exception as e:
        pass
     
    return render(request, 'address_list.html', {'addresses_list': addresses_list ,
                                                 "user_data" : request.session.get("user_data"),
                                                 'cart_count' :request.session.get("cart_count")
                                                 })

'''===============================  Add address Method ============================================'''



@csrf_exempt
def Add_address_view(request):
    access_token = request.session.get('access_token')
    user_data = request.session.get("user_data")
    # print(f'{access_token=}')
    # print(f'{user_data=}')
    add_address=[]
    userid = user_data.get("userid")
    if not userid:
       return redirect('sign_in')
    

    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    params = {
        "userid": userid
    }
    # print(f'{params=}')


    if request.method == "POST":
        # ✅ Get all values without commas
        name = request.POST.get("name")
        # print(f'{name=}')
        mobile = request.POST.get("mobile")
        address = request.POST.get("address")
        city = request.POST.get("city")
        district = request.POST.get("district")
        state = request.POST.get("state")
        pincode = request.POST.get("pincode")
        label = request.POST.get("label")
        is_display = True

        # ✅ Debug # # print types and values
        data = {
            "userid": userid,
            'name': name,
            'mobile': mobile,
            'address': address,
            'city': city,
            'district': district,
            'state': state,
            'pincode': pincode,
            'label': label,
            'is_display': is_display,             
   
        }

        # print("\n🟡 JSON to be sent to API:")
        # print(f'{data=}')
        for key, value in data.items():
            pass
            # # print(f"{key}: {value} (type: {type(value)})")
        # # print()
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
      
        try:
            pass
            response = requests.post(
                f"{Baseurl}/user/addresses/add/",
                headers=headers,
                json=data
            )
        

            if response.status_code == 201:
                data = response.json()
                # print(f'{add_address=}')
                add_address = data.get("data", []) 
                messages.success(request, "Address added successfully.")
           
                return redirect("addresses_list_view")
            else:
           
                messages.error(request, f"Error from server: {response}")

        except Exception as e:
            return HttpResponse('test')
            # # print(f"🔴 Exception: {e}")
            # messages.error(request, f"An error occurred while adding the address. {e=}")

    return render(request, "add_address.html",{"user_data" : request.session.get("user_data")})
 



'''===============================  Set address Method ============================================'''

 
def Set_address_view(request):
    # if 'access_token' not in request.session:
    #     return redirect('sign_in')
    access_token = request.session.get('access_token')
    user_data = request.session.get("user_data")
    # print(f'{access_token=}')

   
    if request.method == "POST":
        # ✅ Get all values without commas
        address_id = request.POST.get("address_id")


        userid = user_data.get("userid")
        if not userid:
            return redirect('sign_in')
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        data = {
            "userid": userid,
            'id':int(address_id)
        }
        # print(f'{data=}')

        try:
            response = requests.post(f"{Baseurl}/checkout-address/set/", headers=headers,json=data)
            # print(f'{response=}')
        
            
            if response.status_code == 200:
                data = response.json()
                addresses = data.get("data", [])
                # print(f'{addresses=}') 
                return redirect('checkout_view')
            else:
                return redirect('addresses_list_view')

        

        except Exception as e:
            # print(f'{e=}')
            return redirect('addresses_list_view')

   

'''===============================  Delete address Method ============================================'''


import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import redirect
import requests

@csrf_exempt  # Optional: only if you're not using @login_required or CSRF token
def delete_address_view(request):
  

    access_token = request.session.get('access_token')
    user_data = request.session.get("user_data")
    if not access_token or not user_data:
        return JsonResponse({"error": "Unauthorized"}, status=401)

    try:
        data = json.loads(request.body)
        address_id = data.get("address_id")
    except Exception:
        return JsonResponse({"error": "Invalid request body"}, status=400)

    userid = user_data.get("userid")
    if not address_id or not userid:
        return JsonResponse({"error": "Missing data"}, status=400)

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    json_data = {
        "userid": userid,
        "id": int(address_id)
    }

    try:
        res = requests.delete(f"{Baseurl}/user/addresses/delete/", headers=headers, json=json_data)
        if res.status_code == 200:
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"error": "Failed to delete address"}, status=400)
    except Exception:
        return JsonResponse({"error": "Server error"}, status=500)









@csrf_exempt
def edit_address_view(request):
    access_token = request.session.get('access_token')
    user_data = request.session.get("user_data")
    cart_count = request.session.get("cart_count")

    if not access_token or not user_data:
        return redirect('sign_in')

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

  
    if request.method == "POST":
        post_data = {
            "id": request.POST.get("address_id"),
            "name": request.POST.get("name"),
            "mobile": request.POST.get("mobile"),
            "address": request.POST.get("address"),
            "city": request.POST.get("city"),
            "district": request.POST.get("district"),
            "state": request.POST.get("state"),
            "pincode": request.POST.get("pincode"),
            "label": request.POST.get("label"),
            "is_display": 1 if request.POST.get("is_display") == "true" else 0,
          
        }
        # print(f'{post_data=}')
        response = requests.put(f"{Baseurl}/user/addresses/update/", headers=headers, json=post_data)
        if response.status_code == 200:
       
  
            return redirect("addresses_list_view") 
        else:
            return render(request, "edit_address.html", {
                "error": "Failed to update address",
                "address": post_data,
                "cart_count": cart_count
            })

 
    address_id = request.GET.get("id")
    if not address_id:
        return redirect('addresses_list_view')  

    try:
        response = requests.get(f"{Baseurl}/user/get-address-by-id/", headers=headers, params={"id": address_id})
        if response.status_code == 200:
            data = response.json()
            address_data = data.get('data', {})

            return render(request, 'edit_address.html', {
                'address': address_data,
                'cart_count': cart_count
            })

        else:
            return redirect('addresses_list_view')

    except requests.exceptions.RequestException:
        return redirect('addresses_list_view')

'''===============================  Setting page Method ============================================'''
def setting_view(request):
    access_token = request.session.get('access_token')
    user_data = request.session.get("user_data")
    cart_count = request.session.get("cart_count")

    if not access_token or not user_data:
        return redirect('sign_in')

    return render(request,'setting.html',{ "cart_count": cart_count,"user_data" : request.session.get("user_data")})

'''===============================  Business page Method ============================================'''

def Business_view(request,app_menu):
    access_token = request.session.get('access_token')
    user_data = request.session.get("user_data")
    cart_count = request.session.get("cart_count")
    getfree_team = today_Team_count(request)
    # print(f'{getfree_team=}')
    free_users = getfree_team.get('free_users')
    # print(f'{free_users=}')
    paid_users = getfree_team.get('paid_users')
    # print(f'{paid_users=}')

      # Marquee
    marquee_data = marquee_context(request, app_menu)
    marquee_text = ''
    if marquee_data and isinstance(marquee_data, list):
        marquee_text = marquee_data[0].get('marquee_text', '')
    marquee_text_list = [marquee_text] if marquee_text else []

    if not access_token or not user_data:
        return redirect('sign_in')

    return render(request,'Business.html',{ "cart_count": cart_count,"user_data" : request.session.get("user_data"),'getfree_team':getfree_team, "free_users": free_users,
        "paid_users": paid_users, 'marquee_text': json.dumps(marquee_text_list),})


'''=============================== free_users,paid_users,total_users   Method ============================================'''

def get_team_count(request):
    access_token = request.session.get('access_token')
    user_data = request.session.get("user_data")
    cart_count = request.session.get("cart_count")
 
    if not access_token:
        return redirect('sign_in')  # Or handle unauthorized access


    # search_team_user= search_team_user_view(request)
    # print('serch method called'f'{search_team_user=}')
  

    
    
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    # day = request.GET.get('day', '')
    # print(f'{day=}')

    get_team_levels= get_teamlevel_count_view(request)
  
   

   
    
    msg=''
    free_users = paid_users = total_users = 0
    try:
        response = requests.post(f'{Baseurl}/get-team_count/', headers=headers)
        # print(f'eetfgdd====================={response=}')
        # print(f'{response.text=}')
        if response.status_code == 200:
            get_count = response.json().get('data', {})
            # print(f'{get_count=}')
            free_users = get_count.get('free_users', 0)
            paid_users = get_count.get('paid_users', 0)
            total_users = get_count.get('total_users', 0)

        # elif response.status_code == 404:
        #     msg = response.json().get('message', '')
        #     print(f'mmmmmmmmmmmmmmm{msg=}')

    except requests.exceptions.RequestException as e:
        # return HttpResponse('test')
        return render(request, 'Myteam.html', {'error': str(e)})

    return render(request, 'Myteam.html', {
    "cart_count": cart_count,
    'free_users': free_users,
    'paid_users': paid_users,
    'total_users': total_users,
    
    'get_team_levels':get_team_levels,
    "user_data" : request.session.get("user_data"),
    # 'search_team_user':search_team_user
})



'''===============================  Team level count Method ============================================'''

def get_teamlevel_count_view(request):
    access_token = request.session.get('access_token')
    user_data = request.session.get("user_data")
    cart_count = request.session.get("cart_count")
    # print(f'Access Token: {access_token}')
    # print(f'{user_data=}')

    get_team_levels =[]

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    try:
        response = requests.post(f"{Baseurl}/get-team_level_count/", headers=headers)
        # print(f"team-level-count response: {response.status_code} - {response.text}")

        if response.status_code == 200:
            get_team_levels = response.json().get("data", [])
            # print(f'team levelsssss{get_team_levels=}')
            return get_team_levels
       
        else:
            return get_team_levels

    except Exception as e:
        return get_team_levels
     
'''===============================  Today freeTeam count Method ============================================'''


def today_Team_count(request):
    access_token = request.session.get('access_token')
    user_data = request.session.get("user_data")
    cart_count = request.session.get("cart_count")
    # print(f'Access Token: {access_token}')
    # print(f'{user_data=}')

    getfree_team ={}
    
    # getfree_team =[]
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    try:
        response = requests.post(f"{Baseurl}/get-team_count/",json={"day": "Today"}, headers=headers)
        print(f"team-level-count response: {response.status_code} - {response.text}")

        if response.status_code == 200:
            getfree_team = response.json().get("data", {})
            print(f'{getfree_team=}')
            return getfree_team
          
       
        else:
            return getfree_team
           

    except Exception as e:
        return getfree_team

'''===============================  Today Team count view Method ============================================'''

# def todayTeam_count_view(request,level,package):
#     access_token = request.session.get('access_token')
#     user_data = request.session.get("user_data")
#     cart_count = request.session.get("cart_count")
#     # print(f'Access Token: {access_token}')
#     # print(f'{user_data=}')

#     team_levels =[]
#     headers = {
#         'Authorization': f'Bearer {access_token}',
#         'Content-Type': 'application/json'
#     }
#     # page = int(request.GET.get("page", 1))
#     # day = request.GET.get("day", '')
#     data = {
#         # "page": 1,
#         "level": level,
#         "status": 1,
#         "day": "",
#         "package": package   # Free , paid,All
#     }
#     try:
#         response = requests.post(f"{Baseurl}/get-team_levels/", headers=headers,json=data,)

#         if response.status_code == 200:
#             team_levels = response.json().get("data", [])
       
        
#     except Exception as e:
#         pass
#     return render(request, "team.html", {
#             "team_levels": team_levels,
#             "user_data" : request.session.get("user_data"),
#             "cart_count": cart_count,
#             # "error_message": f"Exception: {str(e)}"
               
#         }) 
  
'''===============================  Team level count view Method ============================================'''

def TeamLevelCount_view(request,level,package):
    access_token = request.session.get('access_token')
    user_data = request.session.get("user_data")
    cart_count = request.session.get("cart_count")
    # print(f'Access Token: {access_token}')
    # print(f'{user_data=}')

    team_levels =[]
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    page = int(request.GET.get("page", 1))
    # day = request.GET.get("day", '')
    data = {
        "page": 1,
        "level": level,
        "status": 1,
        "day": "",
        "package": package   # Free , paid,All
    }
    try:
        response = requests.post(f"{Baseurl}/get-team_levels/", headers=headers,json=data,)

        if response.status_code == 200:
            team_levels = response.json().get("data", [])


          # ✅ Paginate
            paginator = Paginator(team_levels, 6)  # 6 members per page
            paginated_team = paginator.get_page(page)    
       
        
    except Exception as e:
        pass
    return render(request, "team.html", {
            "team_levels": team_levels,
            "team_levels": paginated_team,
            "user_data" : request.session.get("user_data"),
            "cart_count": cart_count,
            # "error_message": f"Exception: {str(e)}"
               
        })     


'''===============================  Today Team level count view Method ============================================'''

def today_TeamLevelCount_view(request,package):
    access_token = request.session.get('access_token')
    user_data = request.session.get("user_data")
    cart_count = request.session.get("cart_count")
    # print(f'Access Token: {access_token}')
    # print(f'{user_data=}')

    team_levels =[]
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    page = int(request.GET.get("page", 1))
    # day = request.GET.get("day", '')
    data = {
        "page": 1,
       
        "status": 1,
        "day": "Today",
        "package": package   # Free , paid,All
    }
    try:
        response = requests.post(f"{Baseurl}/get-team_levels/", headers=headers,json=data,)
        # print(f'{response=}')
        if response.status_code == 200:
            team_levels = response.json().get("data", [])
            # print(f'{team_levels=}')

          # ✅ Paginate
            paginator = Paginator(team_levels, 6)  # 6 members per page
            paginated_team = paginator.get_page(page)    
            
        
    except Exception as e:
        pass
    return render(request, "team.html", {
            "team_levels": team_levels,
            "team_levels": paginated_team,
            "user_data" : request.session.get("user_data"),
            "cart_count": cart_count,
            # "error_message": f"Exception: {str(e)}"
               
        })     
'''===============================  Serch team count Method ============================================'''

import requests
from django.shortcuts import render
from django.contrib import messages
def search_team_user_view(request):
    print('serch method called')
    access_token = request.session.get('access_token')
    user_data = request.session.get("user_data")
    cart_count = request.session.get("cart_count")

    search_team_user = []
    error_msg = None  # For showing API message in template

    if request.method == "POST":
        search_user_id = request.POST.get("searchUserId")
        print(f'{search_user_id=}')

        payload = {
            "searchUserId": search_user_id
        }

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        try:
            response = requests.post(f"{Baseurl}/get-search_team_user/", json=payload, headers=headers)
            print(f'{response=}')
            if response.status_code == 200:
                data = response.json()
                print(f'{data=}')
                search_team_user = [data.get('data')]

            elif response.status_code == 404:
                error_msg = response.json().get('message', "data not found.")  # 🟢 Direct API message

        except Exception as e:
            error_msg = f"Request failed: {e}"  # 🟠 Fallback message

    return render(request, "serch_team.html", {
        "user_data": user_data,
        "cart_count": cart_count,
        "search_team_user": search_team_user,
        "error_msg": error_msg  # 🟢 Pass to template
    })


'''=============================== get Rank count Method ============================================'''
import requests
from django.shortcuts import render, redirect
from django.contrib import messages



def team_rank_view(request):
    access_token = request.session.get("access_token")
    user_data = request.session.get("user_data")
    cart_count = request.session.get("cart_count")

    rank_data = {}
    error_msg = None

    headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

    try:
        response = requests.get(f"{Baseurl}/get-rank_team_count/", headers=headers)
        print(f"{response=}")
        print(f"{response.text=}")
        if response.status_code == 200:
            data = response.json()
       
            rank_data = data.get("data",[])
            # print(f'{rank_data=}')
            # return HttpResponse(f'{rank_data=}')
        
       
        elif  response.status_code == 404:
            error_msg = response.json().get('message',  "Something went wrong.")  # 🟢 Direct API message
            print(f'{error_msg=}')

        
    except Exception as e:
        error_msg = f"Request failed: {e}"
        # return HttpResponse(f'{error_msg=}')
    return render(request, "team_rank.html", {
        "user_data": user_data,
        "cart_count": cart_count,
        "rank_data": rank_data,
        "error_msg": error_msg,
    })


'''===============================  Category Method ============================================'''

def Product_Category_view(request):
    # if 'access_token' not in request.session:
    #     return redirect('sign_in')
   
   
  
    product_categories=[]

    try:
        response = requests.get(f"{Baseurl}/products-categories/")
        # print(f'{response=}')
        # print(f'{response.text=}')
        
        if response.status_code == 200:
            data = response.json()
            product_categories = data.get("data", []) 
            return product_categories
        
            # return HttpResponse(f'{product_categories=}')
       
    except Exception as e:
        pass
    return product_categories 
  