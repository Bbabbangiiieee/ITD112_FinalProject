from django.shortcuts import render, redirect
from django.contrib import auth
import pandas as pd
import pyrebase

config={
    "apiKey": "AIzaSyARbvQfC-4RQgzkVOuz70BBb7xbc3W_-Tc",
  "authDomain": "itd112-finalproject.firebaseapp.com",
  "databaseURL": "https://itd112-finalproject-default-rtdb.firebaseio.com",
  "projectId": "itd112-finalproject",
  "storageBucket": "itd112-finalproject.appspot.com",
  "messagingSenderId": "286747772509",
  "appId": "1:286747772509:web:4d988102996b65d7efefb4",
}
firebase=pyrebase.initialize_app(config)
firebase_auth = firebase.auth()
database=firebase.database()

def newuser(request):
    return render (request,"signup.html")

def postSignUp(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    try:
        firebase_auth.create_user_with_email_and_password(email, password)
        success = "Registration Successful. You can now login"
        return render(request, "signIn.html",{"success":success})
    except:
        message = 'Invalid Credentials. Please Try Again'
        print(message)
        return render(request, "signup.html", {"message": message})



def signIn(request):
    return render (request,"signIn.html")

def postSignIn(request):
    email = request.POST.get('email')
    password = request.POST.get('password')

    try:
        user = firebase_auth.sign_in_with_email_and_password(email, password)
        session_id=user['idToken']
        request.session['uid']=str(session_id)
        dataset_link = database.child('Data').child('-NjXtmdDMNO6L9drCTAS').child('dataset_link').get().val()
        data = pd.read_csv(dataset_link)
        data_head_html = data.head(100).to_html()
        
        # Creating Pie Chart
        region_cases = data.groupby('Region')['cases'].sum()
        total_cases = region_cases.sum()
        region_percentages = (region_cases / total_cases) * 100
        region_labels = list(region_percentages.index)
        region_data = list(region_percentages)
        
        #Creating Line Graph
        data['date'] = pd.to_datetime(data['date'])
        data['year'] = data['date'].dt.year
        cases_per_year = data.groupby('year')['cases'].sum()
        year_labels = list(cases_per_year.index)
        cases_data = list(cases_per_year)
        
        #Creating Bar Graph
        data['date'] = pd.to_datetime(data['date'])
        data['year'] = data['date'].dt.year
        deaths_per_year = data.groupby('year')['deaths'].sum()
        year_labels = list(deaths_per_year.index)
        deaths_data = list(deaths_per_year)
        
        return render(request, 'project1.html', {
            'data_head_html': data_head_html,
            'dataset_link':dataset_link,
            'region_labels': region_labels,
            'region_data': region_data,
            'year_labels': year_labels,
            'cases_data': cases_data,
            'deaths_data': deaths_data
            })
    except:
        message = 'Invalid Credentials'
        return render(request, "project1.html", {"message": message})
    
    
def log_out(request):
    auth.logout(request)
    return redirect('signIn.html')

def uploadSubmit(request):
    dataset_name = request.POST.get('dataset_name')
    url = request.POST.get('url')

    data = {
        "dataset_name": dataset_name,
        "dataset_link": url
    }

    # Push the data to the 'Data' node in Firebase
    new_data_ref = database.child('Data').push(data)

    # Retrieve the key of the newly added data
    new_data_key = new_data_ref['name']

    # Retrieve the data using the key
    new_data = database.child('Data').child(new_data_key).get().val()
    data = pd.read_csv(new_data["dataset_link"])
    data_head_html = data.head(100).to_html()
    return render(request, 'others.html', {
        "dataset_name": new_data["dataset_name"],
        'data_head_html': data_head_html
    })


def project1(request):
    dataset_link = database.child('Data').child('-NjXtmdDMNO6L9drCTAS').child('dataset_link').get().val()
    data = pd.read_csv(dataset_link)
    data_head_html = data.head(100).to_html()
    
    # Creating Pie Chart
    region_cases = data.groupby('Region')['cases'].sum()
    total_cases = region_cases.sum()
    region_percentages = (region_cases / total_cases) * 100
    region_labels = list(region_percentages.index)
    region_data = list(region_percentages)
    
    #Creating Line Graph
    data['date'] = pd.to_datetime(data['date'])
    data['year'] = data['date'].dt.year
    cases_per_year = data.groupby('year')['cases'].sum()
    year_labels = list(cases_per_year.index)
    cases_data = list(cases_per_year)
    
     #Creating Bar Graph
    data['date'] = pd.to_datetime(data['date'])
    data['year'] = data['date'].dt.year
    deaths_per_year = data.groupby('year')['deaths'].sum()
    year_labels = list(deaths_per_year.index)
    deaths_data = list(deaths_per_year)
    
    return render(request, 'project1.html', {
        'data_head_html': data_head_html,
        'dataset_link':dataset_link,
        'region_labels': region_labels,
        'region_data': region_data,
        'year_labels': year_labels,
        'cases_data': cases_data,
        'deaths_data': deaths_data
        })

def project2(request):
    return render(request, 'project2.html')

def project3(request):
    return render(request, 'project3.html')

def others(request):
    return render(request, 'others.html')