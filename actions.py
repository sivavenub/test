# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from rasa_sdk.forms import FormAction
import re
from rasa_sdk import Action, Tracker
import requests
import json
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Text, Dict, List,Any,Union, Optional
from rasa_sdk.events import (
    UserUtteranceReverted,
    Restarted,
    EventType,
    FollowupAction,
    ActionReverted
)
from datetime import datetime as dt
from api import API
api= API()


def suffix(d):
    return 'th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')
def custom_strftime(format, t):
    t = dt.strptime(t, '%Y-%m-%d')
    return t.strftime(format).replace('{S}', str(t.day) + suffix(t.day))

class ActionBusinessEmail(Action):
    """Business Email Extractions"""
    

    def name(self):
        return "action_business_email"
    
    def run(self,dispatcher,tracker,domain):
        inte = tracker.get_slot("quickreply_value")
        value=tracker.get_slot('business_email')
        if re.match(r"[a-zA-Z0-9_.+-]+@[a-zA-Z]+\.[^@]+",str(value)):
            print(value)
            data = {"token": "null","data": {"user_email": value}}
            # response = requests.post('https://cornerstonesolutions.ai/subs/api_verify_user',data=json.dumps(data))
            # r = response.json()
            r=api.verify_user(data)
            if r == True:
                if(inte=="Show Current Offers"):
                    # response = requests.post('https://cornerstonesolutions.ai/subs/api_offers_list',data=json.dumps(data))
                    # r = response.json()
                    r=api.offers_list(data)
                    dat=(r['data'])
                    q=sum([1 for d in dat if 'serial' in d])
                    for w in range((q)):
                        serial=dat[w]["serial"]
                        name=dat[w]["name"]
                        offers=("{}) {}.".format(serial,name))
                        dispatcher.utter_message(offers)
                    dispatcher.utter_message(template="utter_place_quick_order")
                        
                elif(inte=="Quick Order"):
                    r=api.child_list(data)
                    dat=(r['data'])
                    q=sum([1 for d in dat if 'serial' in d])
                    dispatcher.utter_message(template='Enter_SlNO') 
                    for w in range((q)):
                        serial=dat[w]["serial"]
                        childname=dat[w]["child_name"]
                        out_message=("{})  {}.".format(serial ,childname))
                        dispatcher.utter_message(out_message)
				

				# elif(inte=="fetch invoice"):
    #                 r=api.fetch_invoice(data)
    #                 dat=(r['data'])
    #                 q=sum([1 for d in dat if 'serial' in d])
    #                 dispatcher.utter_message(template='Enter_SlNO') 
    #                 for w in range((q)):
    #                     serial=dat[w]["serial"]
    #                     childname=dat[w]["child_name"]
    #                     order_date = dat[w]['order_date']
    #                     invoice_url = dat[w]['invoice_url']
    #                     out_message=("{}. {} {} {}.".format(serial ,childname,order_date,invoice_url))
    #                     dispatcher.utter_message(out_message)


                     
                elif(inte=="status_of_my_order"):
                    r=api.Order_status(data)
                    dat=(r['data'])
                    q=sum([1 for d in dat if 'serial' in d])
                    # dispatcher.utter_message(template="Enter_SlNO_canel")
                    if q > 1 :
                        for w in range((q)):
                            serial=dat[w]["serial"]
                            childname=dat[w]["child_name"]
                            pack_name = dat[w]['pack_name']
                            order_status= dat[w]['order_status']
                            out_message=("{})  {} {} {}.".format(serial ,childname,pack_name,order_status))
                            dispatcher.utter_message(out_message)
                        # print("status_of_my_order")
                        
                        dispatcher.utter_message(template= "utter_location_more_details")
                    else:

                        serial=dat[0]["serial"]
                        childname=dat[0]["child_name"]
                        pack_name = dat[0]['pack_name']
                        order_status= dat[0]['order_status']
                        delivery_time = dat[0]['expected_time']
                        Current_location = dat[0]['order_location']
                        out_message=("{})  {} {} {} {} {}.".format(serial ,childname,pack_name,order_status,delivery_time,Current_location))
                        dispatcher.utter_message(out_message)
                        # dispatcher.utter_message(template= "utter_location_more_details")

                    
                    
                elif(inte =="todays_Lunchbox_details"):
                    print("todays_lunchBox_details")
                    # response = requests.post('https://cornerstonesolutions.ai/subs/api_today_lunch_detail',data=json.dumps(data))
                    # r = response.json()
                    r=api.Lunch_box_details(data)
                    print(r)
                    j=r['data']
                    if len(j) == 0:
                        dispatcher.utter_message("There is no LunchBox details for today")
                        dispatcher.utter_message(template="utter_feedback")
                      
                    else:
                        for d in j:
                            out_list=[]
                            for k,v in d.items():
                                out_list.append(v)
                            out_message="LunchBox details for today:"+ str(out_list[2])
                            # dispatcher.utter_message(out_message)
                            out_message1= "For:"+str(out_list[6])
                            # dispatcher.utter_message(out_message1)
                            out_message2= "Ingredients:"+str(out_list[1])
                            # dispatcher.utter_message(text="{}\n\n {}\n\n {}\n\n".format(out_message,out_message1,out_message2))
                            dispatcher.utter_message(out_message)
                            dispatcher.utter_message(out_message1)
                            dispatcher.utter_message(out_message2)
                        dispatcher.utter_message(template="utter_feedback")
                            
                elif(inte =="cancel_order_for_next_friday"):
                    r=api.all_order_status(data)
                    dat=(r['data'])
                    q=sum([1 for d in dat if 'serial' in d])
                    dispatcher.utter_message(template="Enter_SlNO_canel")
                    for w in range((q)):
                        serial=dat[w]["serial"]
                        childname=dat[w]["child_name"]
                        pack_name = dat[w]['pack_name']
                        order_date = dat[w]['delivery_date']
                        order_status = dat[w]['order_status']
                        order_date = custom_strftime('%B {S}, %Y', (dat[w]['delivery_date']))
                        # dat[w]['delivery_date']
                        # custom_strftime('%B {S}, %Y', dt(2018, 6, 1))
                        out_message=("{})  {}, {}, {}, {}.".format(serial ,childname,pack_name,order_date,order_status))
                        dispatcher.utter_message(out_message)
                   
                elif(inte=="lunchpacks_available"):
                    # response = requests.post('https://cornerstonesolutions.ai/subs/api_available_lunch_pack',data=json.dumps(data))
                    # r = response.json()
                    r=api.available_lunch_pack(data)
                    if(r['status']== True):
                        dispatcher.utter_message(template="Food_item")
                        dat=(r['data'])
                        q=sum([1 for d in dat if 'serial' in d])
                        for w in range((q)):
                            serial=dat[w]["serial"]
                            name=dat[w]["name"]
                            out_message=("{})  {}.".format(serial ,name))
                            dispatcher.utter_message(out_message)
                        
                        
                    else:
                        dispatcher.utter_message("There is no LunchPacks available for today")
                    
                
                
                else:
                    response=api.Order_for_tomorrow(data)
                    # a = response.json()
                    
                    if(response['status']== True):
                        dat=(response['data'])
                        q=sum([1 for d in dat if 'serial' in d])
                    # dispatcher.utter_message(template="Enter_SlNO_canel")
                        for w in range((q)):
                            serial=dat[w]["serial"]
                            childname=dat[w]["child_name"]
                            pack_name = dat[w]['pack_name']
                            order_status= dat[w]['order_status']
                            out_message=("{}) you have order for {} with the lunch pack name {} and order status is {}.".format(serial ,childname,pack_name,order_status))
                            dispatcher.utter_message(out_message)
                        dispatcher.utter_message(template="utter_feedback")
                        # dispatcher.utter_message('Thank you for your Valuble feedback, we look forward to serve you better.')
   



                    else:
                        dispatcher.utter_message("There is no order found for tommorrow")
                        dispatcher.utter_message(template="utter_place_quick_order")
                    return [SlotSet('quickreply_value',"None")]
                    
                    
            else:
                return(dispatcher.utter_message("User email is not registered"))
               
            # entity was picked up, validate slot
            
        else:
            # no entity was picked up, we want to ask again
            print("inside else")
            dispatcher.utter_message(template="utter_no_email")
            return [UserUtteranceReverted()]
            
            
# class ActionQuickOrder(Action):
    # """Business Email Extractions"""
    

    # def name(self):
        # return "action_Quick Order"
    
    # def run(self,dispatcher,tracker,domain):
        # inte = tracker.get_slot("quickreply_value")
        # value=tracker.get_slot('business_email')
        # if re.match(r"[a-zA-Z0-9_.+-]+@[a-zA-Z]+\.[^@]+",str(value)):
            # print(value)
            # print("inside action_quick_order")
            # data = {"token": "null","data": {"user_email": value}}
            # response = requests.post('https://cornerstonesolutions.ai/subs/api_verify_user',data=json.dumps(data))
            # r = response.json()
            # r=api.verify_user(data)
            # print("r",r)
            # if(r== True):
                # dispatcher.utter_message('Registered')
                # response = requests.post('https://cornerstonesolutions.ai/subs/api_child_list',data=json.dumps(data))
                # r = response.json()
                # r=api.child_list(data)
                # dat=(r['data'])
                # q=sum([1 for d in dat if 'serial' in d])
                # for w in range((q)):
                    # serial=dat[w]["serial"]
                    # childname=dat[w]["child_name"]
                    # out_message=("{})  {}.".format(serial ,childname))
                    # dispatcher.utter_message(out_message)
                # dispatcher.utter_message(template='Enter_SlNO') 
                
            # else:
                # return(dispatcher.utter_message("User email is not registered"))
        # else:
            # print("inside else")
            # dispatcher.utter_message(template="utter_no_email")
            # return [UserUtteranceReverted()]        

def extract_nested_values(it):
	if isinstance(it, list):
		for sub_it in it:
			yield from extract_nested_values(sub_it)
	elif isinstance(it, dict):
		for value in it.values():
			yield from extract_nested_values(value)
	else:
		yield it                       
                
class ActionSerialNumber(Action):
    """Enter the serial  Extractions"""
    

    def name(self):
        return "action_serialNumber"
    
    def run(self,dispatcher,tracker,domain): 
        value=tracker.get_slot('business_email')
        serial = tracker.get_slot('Serial_Number')
        inte= tracker.get_slot('quickreply_value')
        Yes_no=tracker.get_slot("quickreply_value7")
        print(inte)
        # print("action_serialNumber")
        data = {"token": "null","data": {"user_email": value}}
        
        
        
        if(inte=="cancel_order_for_next_friday"):
            results = api.all_order_status(data)
            dat=(results['data'])
            # print('dat',dat)
            # print('len',len(dat))

        
    	# elif(inte=="fetch invoice"):
     #        results = api.fetch_invoice(data)
     #        dat=(results['data'])
     #        # print('dat',dat)
     #        # print('len',len(dat))

        
        elif(inte=="lunchpacks_available"):
            r=api.available_lunch_pack(data)
            dat=(r['data'])
            
        elif(inte=="status_of_my_order"):
            r=api.Order_status(data)
            dat=(r['data'])
            # print(dat)
            
            
        else:
            results=api.child_list(data)
            dat=(results['data'])
            # print(dat)
            
            
        if(serial==None):
            q=sum([1 for d in dat if 'child_id' or 'order_detail_id' or 'id' or 'order_location' in d])
            for w in range((q)):
                serial=dat[w]["serial"]
                childname=dat[w]["child_name"]
                out_message=("Please enter {} if you want to place order for {}.".format(serial ,childname))
                dispatcher.utter_message(out_message)
            return [UserUtteranceReverted()]
           
        else:   
            c= serial.isdigit()
            # print((c))
            q=sum([1 for d in dat if 'child_id' or 'order_detail_id' or 'id' or 'order_location' in d])
            if(c== False):
                dat=(r['data'])
                for w in range((q)):
                    serial=dat[w]["serial"]
                    childname=dat[w]["child_name"]
                    out_message=("Please enter {} if you want to place order for {}.".format(serial ,childname))
                    dispatcher.utter_message(out_message)
                return [UserUtteranceReverted()]
            
            else:
                k=int(serial)
                q=sum([1 for d in dat if 'child_id' or 'order_detail_id' or 'id' or 'order_location' in d])
                if(k > q or k==0):
                    for w in range((q)):
                        serial=dat[w]["serial"]
                        childname=dat[w]["child_name"]
                        out_message=("Please enter {} if you want to place order for {}.".format(serial ,childname))
                        dispatcher.utter_message(out_message)
                    return [UserUtteranceReverted()]
                else:
                    if(inte=="cancel_order_for_next_friday"):
                        # print('cancel_order_for_next_friday')
                    # print("status_select number")
                        # serial=int(serial)
                        k= k-1
                        print('k....',k)
                        results = api.all_order_status(data)
                        dat=(results['data'])
                        # print('dat',dat)
                        print('len',len(dat))
                        # print(len(dat))

                        order_detail_id = dat[k]["order_detail_id"]
                        print('order_detail_id',order_detail_id)
                        # dispatcher.utter_message(order_detail_id)
                        data = {"token": "null","data": {"user_email": value,"order_detail_id":order_detail_id}}
                        if (dt.strptime(dat[k]['delivery_date'],'%Y-%m-%d') > dt.now()) and (dat[k]['order_status'] == 'pending'):# dt.strptime(t, '%Y-%m-%d')
                            # print('inside loop',data)
                        #     serial=dat[w]["serial"]
                        # childname=dat[w]["child_name"]
                        # pack_name = dat[w]['pack_name']
                        # order_date = dat[w]['delivery_date']
                            out_message = ("{}  {} {}".format(dat[k]["child_name"],dat[k]["delivery_date"],dat[k]["pack_name"]))
                            dispatcher.utter_message(out_message)
                            dispatcher.utter_message(template="utter_cancel_order")
                            return [SlotSet('order_detail_id',order_detail_id)]
                            # dispatcher.utter_message(template="Enter_OTP")
                            # results = api.cancel_my_order(data)
                            # # print(results)
                            # # t=results['status']
                            # # if (t==True):
                            # print('success')
                            # dispatcher.utter_message("The order has been cancelled")
                            # dispatcher.utter_message(template="utter_feedback")
                            # # else:
                            # 	out_message = ('The order cant be cancelled as {}'.format(results['msg']))
                            # 	dispatcher.utter_message(out_message)
                        else:
                            results = api.cancel_my_order(data)
                            out_message = ('The order cant be cancelled as {}'.format(results['msg']))
                            dispatcher.utter_message(out_message)
                            dispatcher.utter_message(template="utter_feedback")
                            
                    elif(inte=="status_of_my_order"):
                        if(Yes_no == "affirm"):
                            k= k-1
                            delivery_time = dat[k]['expected_time']
                            Current_location = dat[k]['order_location']
                            out_message = ("The expected time of delivery is {}".format(delivery_time))
                            dispatcher.utter_message(out_message)
                            dispatcher.utter_message(template = "Location_link")
                            dispatcher.utter_message(template="utter_feedback")
                        
                        else:  
                            dispatcher.utter_message(template="utter_feedback")


                    # elif(inte=="fetch_invoice"):

                    #     # if(Yes_no == "affirm"):
                    #     k= k-1
                    #     child_name = dat[k]['child_name']
                    #     order_date = dat[k]['order_date']
                    #     invoice_url = dat[k]['invoice_url']
                    #     out_message = ("{} {} {}".format(child_name,order_date,invoice_url))
                    #     dispatcher.utter_message(out_message)
                    #     # dispatcher.utter_message(template = "Location_link")
                    #     dispatcher.utter_message(template="utter_feedback")
                        
                        # else:  
                        #     dispatcher.utter_message(template="utter_feedback")

                        
                        
                        
                        
                    elif(inte=="lunchpacks_available"):
                        k= k-1
                        idno=dat[k]["id"]
                        data = {"token": "null","data": {"user_email": value, "id":idno}}
                    # response = requests.post('https://cornerstonesolutions.ai/subs/api_lunch_pack_detail',data=json.dumps(data))
                    # r = response.json()
                        r=api.lunch_pack_detail(data)
                        dat= r['pack_products']
                        for key,values in dat.items():
                            details=list(extract_nested_values(values))
#     print(details[0]+".",details[1]+":",details[2])
                            Id=details[0]
                            Name=details[1]
                            Info= details[2:]
#     info = (*Info,sep =",")
                            out_message=("{}.{}:".format(Id ,Name))
                            out_message_1 = ("{}".format(Info))
                            dispatcher.utter_message(out_message)
                            dispatcher.utter_message(out_message_1)
                        dispatcher.utter_message(template="utter_place_quick_order")
                        return [SlotSet('quickreply_value',"None")]
                    
                    else:
                        dispatcher.utter_message(template="utter_lunch_pack")
                            
                            
                            
                            
                        
       
                # else:
                    # if(inte=="Quick Order"):
                        # dispatcher.utter_message(template="utter_lunch_pack")
                    # else:
                        # print("status_select number")
                        # serial=int(serial)
                        # serial= serial-1
                        # child_id=dat[serial]["child_id"]
                        # dispatcher.utter_message(child_id)
             
              
             
            
class ActionOrder(Action):
    """Business Email Extractions"""
    

    def name(self):
        return "action_Order"
    
    def run(self,dispatcher,tracker,domain): 
        inte = tracker.get_slot("quickreply_value1")
        value=tracker.get_slot('business_email')
        serial = tracker.get_slot('Serial_Number')
        print(inte)
        print(serial)
        data = {"token": "null","data": {"user_email": value}}
        # response = requests.post('https://cornerstonesolutions.ai/subs/api_child_list',data=json.dumps(data))
        # r = response.json()
        r=api.child_list(data)
        dat=(r['data'])
        print(dat)
        serial=int(serial)
        serial= serial-1
        child_id=dat[serial]["child_id"]
        
        if(inte=="Favourite_Lunchpack"): 
            data1 = {"token": "null","data": {"user_email": value,"child_id":child_id}}
            # response = requests.post('https://cornerstonesolutions.ai/subs/api_child_favourite_pack',data=json.dumps(data1))
            # w = response.json()
            w=api.child_favourite_pack(data1)
            print(w)
            if(w['status']== True):
                dat1=(w['data'])
                q=sum([1 for d in dat1 if 'serial' in d]) 
                for p in range((q)):
                    serial=dat1[p]["serial"]
                    name=dat1[p]["name"]
                    order_id= dat1[p]["order_detail_id"]
                    sub_total=dat1[p]["sub_total"]
                    out_message=("{})  {} , Total {} .".format(serial ,name,sub_total))
                    dispatcher.utter_message(out_message)
                    dispatcher.utter_message(template='utter_Yes_no')
                    return [SlotSet('child_id',child_id),SlotSet('order_id',order_id)]
                 
                
            else:
                dispatcher.utter_message("There is no childs favourite lunch pack available")
                dispatcher.utter_message("utter_feedback")
        elif(inte=="LunchPack_LastOrder"):
            data1 = {"token": "null","data": {"user_email": value,"child_id":child_id}}
            # response = requests.post('https://cornerstonesolutions.ai/subs/api_child_last_order',data=json.dumps(data1))
            # w = response.json()
            w=api.child_last_order(data1)
            print(w)
            dat1=w['data']
            print(dat1)
            q=sum([1 for d in dat1 if 'serial' in d]) 
            if(w['status']== True):
                for p in range((q)):
                    serial=dat1[p]["serial"]
                    pack_name=dat1[p]["pack_name"]
                    sub_total=dat1[p]["sub_total"]
                    order_id= dat1[p]["order_detail_id"]
                    out_message=("{})  {} , {}.".format(serial ,pack_name,sub_total))
                    dispatcher.utter_message(out_message)
                    dispatcher.utter_message(template='utter_Yes_no')    
                    return [SlotSet('child_id',child_id),SlotSet('order_id',order_id)]
                
            
            else:
                dispatcher.utter_message("utter_feedback")
          
        else:
            dispatcher.utter_message(template="customize_link")
            dispatcher.utter_message(template="utter_feedback")
     
        
# class ActionLunchPacksAvailable(Action):
    # """Business Email Extractions"""
    

    # def name(self):
        # return "action_lunchpacks_available"
    
    # def run(self,dispatcher,tracker,domain):
        # serial = tracker.get_slot("Serial_Number")
        # value=tracker.get_slot('business_email')
        # print(serial)
        
        # data = {"token": "null","data": {"user_email": value}}

        # response = requests.post('https://cornerstonesolutions.ai/subs/api_available_lunch_pack',data=json.dumps(data))
        # r = response.json()
        # r=api.available_lunch_pack(data)
        # dat=(r['data'])
        # print("inside serial")
        # print(serial)
        # if(serial==None):
            # q=sum([1 for d in dat if 'id' in d])
            # for w in range((q)):
               # serial=dat[w]["serial"]
               # name=dat[w]["name"]
               # out_message=("Please enter {} if you want to place order for {}.".format(serial ,name))
               # dispatcher.utter_message(out_message)
            # return [UserUtteranceReverted()]
           
        # else:
            # c= serial.isdigit()
            # q=sum([1 for d in dat if 'id' in d])
            # if(c== False):
                # dat=(r['data'])
                # for w in range((q)):
                    # serial=dat[w]["serial"]
                    # name=dat[w]["name"]
                    # out_message=("Please enter {} if you want to place order for {}.".format(serial ,name))
                    # dispatcher.utter_message(out_message)
                # return [UserUtteranceReverted()]

            # else:
                # k=int(serial)
                # q=sum([1 for d in dat if 'id' in d])
                # if(k>q or k==0):
                    # for w in range((q)):
                        # serial=dat[w]["serial"]
                        # name=dat[w]["name"]
                        # out_message=("Please enter {} if you want to place order for {}.".format(serial ,name))
                        # dispatcher.utter_message(out_message)
                    # return [UserUtteranceReverted()]

                # else:
                    # k= k-1
                    # idno=dat[k]["id"]
                    # data = {"token": "null","data": {"user_email": value, "id":idno}}
                    # response = requests.post('https://cornerstonesolutions.ai/subs/api_lunch_pack_detail',data=json.dumps(data))
                    # r = response.json()
                    # r=api.lunch_pack_detail(data)
                    # dat= r['pack_products']
                    # for key,values in dat.items():
                        # details=list(extract_nested_values(values))
    # print(details[0]+".",details[1]+":",details[2])
                        # Id=details[0]
                        # Name=details[1]
                        # Info= details[2:]
    # info = (*Info,sep =",")
                        # out_message=("{}.{}:".format(Id ,Name))
                        # out_message_1 = ("{}".format(Info))
                        # dispatcher.utter_message(out_message)
                        # dispatcher.utter_message(out_message_1)
            
            
class ActionWhichDate(Action):
    """Selection of date for order to place"""
    

    def name(self):
        return "action_which_date"
    
    def run(self,dispatcher,tracker,domain):
    
        child_id = tracker.get_slot("child_id")
        value=tracker.get_slot('business_email')
        inte = tracker.get_slot("quickreply_value1")
        Yes_no=tracker.get_slot("quickreply_value2")
        print(child_id)
        print("action_which_date")
        if(Yes_no == "affirm"):
            data = {"token": "null","data": {"user_email": value, "child_id":child_id}}
            # response = requests.post('https://cornerstonesolutions.ai/subs/api_child_order_availalable',data=json.dumps(data))
            # w = response.json() 
            w=api.child_order_availalable(data)
                   
            if(w['status']== True):
                dat=(w['data']) 
                q=sum([1 for d in dat if 'date' in d])
                dispatcher.utter_message(template="select_date")
                for w in range((q)):
                    serial=dat[w]["serial"]
                    name=dat[w]["date"]
                    out_message=("{})  {}.".format(serial ,name))
                    dispatcher.utter_message(out_message)
                     
        
            else:
                dispatcher.utter_message("No Dates available for the selected child")        
                dispatcher.utter_message(template="utter_feedback")
        
        else:
             dispatcher.utter_message(template="utter_feedback")



# class ActionLunchPacksAvailable(Action):
#     """Selection of date for order to place"""
    

#     def name(self):
#         return "action_select_date"
    
#     def run(self,dispatcher,tracker,domain):  
#         child_id = tracker.get_slot("child_id")
#         value=tracker.get_slot('business_email')
#         order_id=tracker.get_slot('order_id')
#         print(order_id)
#         data = {"token": "null","data": {"user_email": value, "child_id":child_id}}
#         # response = requests.post('https://cornerstonesolutions.ai/subs/api_child_order_availalable',data=json.dumps(data))
#         # w = response.json()   
#         w=api.child_order_availalable(data)
        
class ActionSelectDate(Action):
    """Selection of date for order to place"""
    

    def name(self):
        return "action_select_date"
    
    def run(self,dispatcher,tracker,domain):  
    
        child_id = tracker.get_slot("child_id")
        value=tracker.get_slot('business_email')
        order_id=tracker.get_slot('order_id')
        serial = tracker.get_slot("Serial_Number")
        print(order_id)
        print(child_id)
        data = {"token": "null","data": {"user_email": value, "child_id":child_id}}
        # response = requests.post('https://cornerstonesolutions.ai/subs/api_child_order_availalable',data=json.dumps(data))
        # w = response.json()
        w=api.child_order_availalable(data)
        dat=(w['data'])
        if(serial==None):
            q=sum([1 for d in dat if 'date' in d])
            for w in range((q)):
                serial=dat[w]["serial"]
                date=dat[w]["date"]
                out_message=("Please select {} for {}.".format(serial ,date))
                dispatcher.utter_message(out_message)
            return [UserUtteranceReverted()]
           
        else:   
            c= serial.isdigit()
            print((c))
            q=sum([1 for d in dat if 'date' in d])
            if(c== False):
                dat=(r['data'])
                for w in range((q)):
                    serial=dat[w]["serial"]
                    date=dat[w]["date"]
                    out_message=("Please select {} for {}.".format(serial ,date))
                    dispatcher.utter_message(out_message)
                return [UserUtteranceReverted()]
            
            else:
                k=int(serial)
                q=sum([1 for d in dat if 'date' in d])
                if(k>q or k==0):
                    for w in range((q)):
                         serial=dat[w]["serial"]
                         date=dat[w]["date"]
                         out_message=("Please select {}  for {}.".format(serial ,date))
                         dispatcher.utter_message(out_message)
                    return [UserUtteranceReverted()]
       
                else:
                    k= k-1
                    date=dat[k]["date"]
                    dispatcher.utter_message(template="Enter_OTP")
                    return [SlotSet('Date',date)]
                    
                    
class ActionValidateOtp(Action):
    """Selection of date for order to place"""
   

    def name(self):
        return "action_validate_otp"
    
    def run(self,dispatcher,tracker,domain):
        otp= tracker.get_slot('Serial_Number')
        child_id = tracker.get_slot("child_id")
        value=tracker.get_slot('business_email')
        order_id=tracker.get_slot('order_id')
        Date= tracker.get_slot('Date')
        order_detail_id=tracker.get_slot('order_detail_id')
        print('order_detail_id is .......',order_detail_id)
        
        inte = tracker.get_slot("quickreply_value") 
        yes_no=tracker.get_slot("quickreply_value4")  
        print('yes_no',yes_no)   
        print('otp is ', otp)    
        print('order_detail_id********',order_detail_id) 
        data = {"token": "null","data": {"user_email": value}}
        # response = requests.post('https://cornerstonesolutions.ai/subs/api_otp_genrate',data=json.dumps(data))
        # r = response.json()
        r=api.otp_genrate(data)
        
        z=(r["data"]['otp'])
        
        if(otp == z):
            print('inside otp loop')
            
            # response = requests.post('https://cornerstonesolutions.ai/subs/api_place_order',data=json.dumps(data1))
            # p = response.json()
            if(inte=="cancel_order_for_next_friday"):
                if(yes_no=="affirm"):
                    print('success')
                    data = {"token": "null","data": {"user_email": value,"order_detail_id":order_detail_id}}
                    print('data..........',data)
                    results = api.cancel_my_order(data)
                    i=(results["status"])
                    print(i)
                    if(i==True):
                        print('almost')
                        dispatcher.utter_message("The order has been cancelled")
                        dispatcher.utter_message(template="utter_feedback")
                    else:
                        dispatcher.utter_message("The order cannot be cancelled")
                        dispatcher.utter_message(template="utter_feedback")
                else:
                    dispatcher.utter_message(template="utter_feedback")
                
               
 
            else:
                data1 = {"token": "null","data": {"user_email": value, "child_id": child_id,"order_detail_id":order_id,"order_date": Date}}
                p=api.place_order(data1)
                n=(p["status"])
                if(n==True):
                    order_id=(p["data"]["order_id"])
                # out_message=("Please enter {} if you want to place order for {}.".format(serial ,date))
                    out_message=("Your order is placed and you order id is {}.".format(order_id))
                    dispatcher.utter_message(out_message)
                    print('went bad')
                    dispatcher.utter_message(template="utter_feedback")
                else:
                    dispatcher.utter_message("Order Already placed for the selected Date")
                    dispatcher.utter_message(template="utter_feedback")
           
        else:
            dispatcher.utter_message(template="Enter_Valid_OTP")
        return [UserUtteranceReverted()]
        
        
class ActionFeedBack(Action):
    """Business Email Extractions"""
    

    def name(self):
        return "action_feedback"
    
    def run(self,dispatcher,tracker,domain): 
        value=tracker.get_slot('business_email')
        feedback = tracker.get_slot('quickreply_value5')
        print(feedback)
        data = {"token": "null","data": {"user_email": value,"comment":feedback}}
        api.place_order(data)
        return()   





class ActionPleaseGoQuickOrder(Action):
    """Business Email Extractions"""
    

    def name(self):
        return "action_Please_go_quickorder"
        
    def run(self,dispatcher,tracker,domain):
        value=tracker.get_slot('business_email')
        data = {"token": "null","data": {"user_email": value}}
        r=api.child_list(data)
        dat=(r['data'])
        q=sum([1 for d in dat if 'serial' in d])
        dispatcher.utter_message(template='Enter_SlNO') 
        for w in range((q)):
            serial=dat[w]["serial"]
            childname=dat[w]["child_name"]
            out_message=("{})  {}.".format(serial ,childname))
            dispatcher.utter_message(out_message)
        return()
        
class ActionForLocation(Action):
    """Business Email Extractions"""
    

    def name(self):
        return "action_for_location"
    
    def run(self,dispatcher,tracker,domain): 
        Yes_no=tracker.get_slot("quickreply_value7")
        if(Yes_no=="affirm"):

            dispatcher.utter_message(template="Location_Time_details")
        else:
             dispatcher.utter_message(template="utter_feedback")
           
        
        
        
        
        

        
  
    
                    
                
        
           
        
        
        
        
        

        
  
    