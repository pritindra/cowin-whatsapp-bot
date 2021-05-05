# +12525926432
from flask import Flask,request
import requests
import json
from twilio.twiml.messaging_response import MessagingResponse
import time

app = Flask(__name__)

# today = date.today
d = time.strftime("%d-%m-%Y")

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/bot', methods = ['GET','POST'])
def bot():
    incoming_msg = request.values.get('Body', '')
    #print(incoming_msg)
    resp = MessagingResponse()
    msg = resp.message()
    responded = False

    if 'Hi' in incoming_msg or 'Hey' in incoming_msg or 'Heya' in incoming_msg or 'Menu' in incoming_msg:
        text = f'Hello Fella!, \nThis is a Covid-Bot developed by Pritindra Das to provide latest information updates on vaccination drives you and your family stay safe.\n For any emergency 👇 \n 📞 Helpline: 011-23978046 | Toll-Free Number: 1075 \n ✉ Email: ncov2019@gov.in \n\n Please enter one of the following option 👇 \n *A*. Get list of states. \n *B*. Get list of districts. \n *C*.Get vaccination sessions by PIN. \n *D*. Get vaccination sessions by district. \n *E*. Coronavirus cases in *Italy*. \n *F*. How does it *Spread*? \n *G*. *Preventive measures* to be taken.'
        msg.body(text)
        responded = True
    
    if 'A' in incoming_msg:
        # return total cases
        r = requests.get('https://cdn-api.co-vin.in/api/v2/admin/location/states')
        if r.status_code == 200:
            data = r.json()
            text = f'_List of States_ \n\nState id : *{data["state_id"]}* \n\nState name : *{data["state_name"]}* \n\n 👉 Type *B, C, D, E, F, G* to see other options \n 👉 Type *Menu* to view the Main Menu'
            print(text)
        else:
            text = 'I could not retrieve the results at this time, sorry.'
        msg.body(text)
        responded = True

    if 'C' in incoming_msg:
        # return total cases
        print('\nEnter your PIN\n')
        pin_msg = request.values.get('Body', '')
        
        payload = {'pincode':pin_msg, 'date':d}
        r = requests.get('https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin',params=payload)
        if r.status_code == 200:
            data = r.json()
            text = f'_Sessions_ \n\nCentre Id : *{data["center_id"]}* \n\nName : *{data["name"]}* \n\naddress : *{data["address"]}* \n\nState Name : *{data["state_name"]}* \n\nDistrict name : *{data["district_name"]}* \n\nBlock Name : *{data["block_name"]}* \n\nFrom : *{data["from"]}* \n\nTo : *{data["to"]}* \n\nFEE : *{data["fee"]}* \n\nFee type : *{data["fee_type"]}* \n\ndate : *{data["date"]}* \n\nAvailabilty : *{data["available_capacity"]}* \n\nvaccine : *{data["vaccine"]}* \n\nSlots : *{data["slots"]}* \n\n 👉 Type *B, C, D, E, F, G* to see other options \n 👉 Type *Menu* to view the Main Menu'
            print(text)
        else:
            text = 'I could not retrieve the results at this time, sorry.'
        msg.body(text)
        responded = True
        
    return str(resp)

if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)

