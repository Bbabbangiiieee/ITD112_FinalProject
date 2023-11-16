from django.shortcuts import render
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
authe = firebase.auth()
database=firebase.database()

def index(request):
    dataset_name = database.child('Data').child('dataset_name').get().val()
    dataset_file = database.child('Data').child('dataset_file').get().val()
    return render(request, 'index.html', {
        "dataset_name":dataset_name,
        "dataset_file":dataset_file
    })
