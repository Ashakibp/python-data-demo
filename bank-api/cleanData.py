import time
from CollectionModule.mongo_db_handler import collection_manager
from bson import ObjectId


class clean_data(object):



    #Gallery card transaction note
    '''
    Title => Account transfer of xxx$
    Subtitle => xxx$ transfered from sender_name to recieved_name
    Button => Click here to view more
    username,password => [{'save_variables': [{'user_id': 'bla_bla', 'balance': ''}]}]
    '''

    def generate_gallery_card_from_list(self, list_name, data):
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
        for entry in data:
            element_list = gal_card["attachment"]["payload"]["elements"]
            element = {
                "title": "{0}",
                "buttons": [
                    {
                        "type": "web_url",
                        "url": "https://google.com",
                        "title": "click here to view more"
                    }
                ]
            }

            element["title"] = entry
            element_list.append(element)

        return [gal_card]





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
        return [gal_card]

    def get_transactions(self, transactions, amounts):
        trans = []
        db = collection_manager("banks", "users")
        db_trans = collection_manager("banks", "transactions")
        if amounts == 0:
            amounts = 10
        for transaction in reversed(transactions):
            amounts = amounts - 1
            transaction = db_trans.find_query({"_id": ObjectId(transaction)})[0]
            sender_identity = transaction["sender"]
            receiver_identity = transaction["receiver"]
            amount = transaction["amount"]
            send_Obj = db.find_query({"_id": sender_identity})[0]
            receive_obj = db.find_query({"_id": receiver_identity})[0]
            send_name = send_Obj["fullname"]
            receive_name = receive_obj["fullname"]
            data_dict = {}
            data_dict["sender_name"] = send_name
            data_dict["receiver_name"] = receive_name
            data_dict["amount"] = amount
            data_dict["date"] = time.strftime('%Y-%m-%d', time.localtime(transaction["timestamp"]))
            data_dict["time"] = time.strftime('%H:%M:%S', time.localtime(transaction["timestamp"]))
            trans.append(data_dict)
            if amounts == 0:
                break
        return self.generate_gallery_card_transaction(trans)


    def generate_branch_card(self, branchArray):
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
        for branch in branchArray:
            element_list = gal_card["attachment"]["payload"]["elements"]
            title = "{0} branch located at of {1}".format(branch["name"], branch["location"])
            subtitle = "branch ID is: {0}".format(str(branch["branch_id"]))

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
        return [gal_card]










