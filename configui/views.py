from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse

DEBUG = False

def debug_print(message):
    if DEBUG:
        print(f"DEBUG: {message}")

@csrf_exempt   
@require_POST   
def handle_ajax_request(request):
    try:
        # Parse the incoming JSON data
        jobj = json.loads(request.POST['data'])
        
        module = jobj.get('module', None)
        ctrlflow = jobj.get('ctrlflow', None)

        debug_print("module: " + module)
        debug_print("ctrlflow: " + ctrlflow)

        if module == "PREREQUISITS":

                if ctrlflow == "saveloaderconfigfile":
                    
                    configfile = jobj.get('configfile', None)
                    
                    if configfile:
                        with open('config.json', 'w') as json_file:
                            json.dump(configfile, json_file, indent=4) 
                        debug_print("Config file saved successfully!")
                    else:
                        debug_print("No configfile found in the data.")                    
                    
                elif ctrlflow == "getloaderconfigfile":
                    
                    try:
                        with open('config.json', 'r') as file:
 
                            config_data = json.load(file)
                            jobj["configfile"] = config_data
                            return JsonResponse({"message": "Data received successfully", "responseResult": jobj})

                            
                    except FileNotFoundError:
                        debug_print("config.json file not found!")
                    except json.JSONDecodeError:
                        debug_print("Error decoding JSON from config.json")
                    except Exception as e:
                        debug_print(f"An error occurred: {e}")
            
                    
        return JsonResponse({"message": "Data received successfully", "responseResult": jobj})
    
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)


def home(request):
    return render(request, 'login.html')

def config_view(request):
    return render(request, 'config.html')

def loadersettings_view(request):
    return render(request, 'loadersettings.html')

def submit_form(request):
    if request.method == 'POST':
        dropdown_value = request.POST.get('dropdown')
        user_input_value = request.POST.get('user_input')

        return HttpResponse(f"Dropdown Value: {dropdown_value}, User Input: {user_input_value}")
    else:
        return HttpResponse("Invalid form submission.")
    
    
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('config')  
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid form data")
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    messages.success(request, "You have logged out successfully.")
    return redirect('login')    