from django.shortcuts import render
from django.http import HttpResponse
import requests

Baseurl = "https://api.zbazaarsolutions.biz/api"

def menu_context(request):
    menu_data = request.session.get('menu_data')
 

    if not menu_data:
        try:
            response = requests.get(f"{Baseurl}/get-menu/")
            response.raise_for_status()
            menu_data = response.json()
            # print(f'{menu_data}')
            request.session['menu_data'] = menu_data
        except requests.exceptions.RequestException:
            menu_data = {}

    return {'menu': menu_data}



################################ GET Marque Method #######################################
# yourapp/context_processors.py
import requests


Baseurl = "https://api.zbazaarsolutions.biz/api"
def marquee_context(request,app_menu=None):
    print(f"marquee_context = {app_menu=}")
    marquee_data=[]
    payload={
        'app_menu':app_menu,
    }

  
    try:
        response = requests.get(f"{Baseurl}/get-marquee/",params=payload)
        print(f'{response=}')
        response.raise_for_status()
        marquee_data = response.json()
     
        marquee_data = marquee_data['data']
        # print(f'{marquee_data=}')
        
     
      
    except Exception as e:
    
        marquee_data = []

    return marquee_data




def banner_context(request,app_menu=None):
    # print(f"banner_context ={app_menu=}")
    banner_data=[]

    payload={
        'app_menu':app_menu,
    }

  
    try:
        response = requests.get(f"{Baseurl}/get-banners/",params=payload)
     
        response.raise_for_status()
        banner_data = response.json()
        # print(f'rrrrrrrrrrrrrrrrrrr=={banner_data=}')
        banner_data = banner_data['data']
     
      
    except requests.exceptions.RequestException:
        banner_data = []

    return banner_data



'''===============================  Popup Image Method ============================================'''
def PopupImage_view(request,app_menu=None):
    # print(f"Popup_Context = {app_menu=}")
  
    Popup_data = []

    payload={
        'app_menu':app_menu,
    }

    # print(f'{payload=}')
    try:
        response = requests.get(f"{Baseurl}/get-popimages/",params=payload)
        # print(f'{response=}')
        # print(f'{response.text=}')
        # if response.status_code == 200:
        response.raise_for_status()
        data = response.json()
        # print(f'{data=}')
        Popup_data = data['data']
        # print(f'{Popup_data=}')
        return Popup_data
        # return HttpResponse(f'{Popup_data=}')
         

  
    except requests.exceptions.RequestException:
        Popup_data = []
        # print(f"Error fetching testimonials: {e}")
    return Popup_data    
    # return HttpResponse('test')
 



