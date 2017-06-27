from CollectionModule.mongo_test import collection_manager
from bson import ObjectId
import time
import json

class clean_data(object):



    #Gallery card transaction note
    '''
    Title => Account transfer of xxx$
    Subtitle => xxx$ transfered from sender_name to recieved_name
    Button => Click here to view more 
    '''

    def generate_gallery_card_transaction(self, transactions):
        gal_card =   {
            "attachment":{
            "type":"template",
            "payload":{
                "template_type":"generic",
                    "elements":[
                    ]
                }
            }
        }

        for trans in transactions:
            element_list = gal_card["attachment"]["payload"]["elements"]
            title = "Account transfer of ${0}".format(trans["amount"])
            subtitle = "${0} transfered from {1} to {2} on {3} at {4}".format(
                trans["amount"],
                trans["sender_name"],
                trans["receiver_name"],
                trans["date"],
                trans["time"])

            element = {
                "title": "{0}",
                "subtitle": "{1}",
                "buttons": [
                    {
                        "type": "web_url",
                        "url": "https://google.com",
                        "title": "click here to view more"
                    }
                ]
            }

            element["title"] = title
            element["subtitle"] = subtitle
            element_list.append(element)
        print(json.dumps(gal_card))

    def get_transactions(self, transactions, amounts):
        trans = []
        db = collection_manager("banks", "users")
        if amounts == 0:
            amounts = 10
        for transaction in reversed(transactions):
            amounts = amounts - 1
            sender_identity = transaction["sender"]
            receiver_identity = transaction["receiver"]
            amount = transaction["amount"]
            send_Obj = db.find_query({"_id": sender_identity})[0]
            receive_obj = db.find_query({"_id": receiver_identity})[0]
            send_name = send_Obj["fullname"]
            receive_name = receive_obj["fullname"]
            print(send_name, " paid ", amount, " to ", receive_name)
            data_dict = {}
            data_dict["sender_name"] = send_name
            data_dict["receiver_name"] = receive_name
            data_dict["amount"] = amount
            data_dict["date"] = time.strftime('%Y-%m-%d', time.localtime(transaction["timestamp"]))
            data_dict["time"] = time.strftime('%H:%M:%S', time.localtime(transaction["timestamp"]))
            trans.append(data_dict)
            if amounts == 0:
                break
        self.generate_gallery_card_transaction(trans)


"""    
             
        {
            "title":"Welcome to Peter\'s Hats",
            "subtitle":"We\'ve got the right hat for everyone.",
            "buttons":[
              {
                "type":"web_url",
                "url":"https://google.com",
                "title":"click here to view more"
              } 
            ]      
          }
          
          
          
"""