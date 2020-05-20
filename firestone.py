
#sudo pip install requests==1.1.0 (dont need)
#python -m pip install --upgrade pip setuptools wheel
#pip install firebase-admin
#change 
"""
1)rename .async into .async_

2)open__init__ file and change .async into .async_

3)open firebase.py and change .async into .async_

because of .async is the keyword now is current version in python

Done>>>>>>>>>>
"""
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Fetch the service account key JSON file contents
cred = credentials.Certificate('serviceAccountKey.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://pythondb-6b948.firebaseio.com'
})

# As an admin, the app has access to read and write all data, regradless of Security Rules
ref = db.reference('/py_command/command')
print(ref.get())
LIGHTSON = False
def lightsOff():
    print ("Light are now off by server")
    return False

def lightOn():
    print ("Lights have been turned On by servre.")
    return True

def listener(event):
    #print(event.event_type)  # can be 'put' or 'patch'
    #print(event.path)  # relative to the reference, it seems
    print(event.data)  # new data at /reference/event.path. None if deleted
    if(event.data == 'Stop'):
        exit()
    elif(event.data == 'Lights off'):
        LIGHTSON = lightsOff()
    elif(event.data == 'Lights On'):
        LIGHTSON = lightOn()
        
    

firebase_admin.db.reference('/py_command/command').listen(listener)