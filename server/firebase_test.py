import firebase_admin

cred_obj = firebase_admin.credentials.Certificate('server/private_key.json')
default_app = firebase_admin.initialize_app(cred_obj, {
    'databaseURL':"https://notebookai-79e56-default-rtdb.firebaseio.com/"
    })
