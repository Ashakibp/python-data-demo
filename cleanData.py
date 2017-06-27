from CollectionModule.mongo_test import collection_manager
from bson import ObjectId

class clean_data(object):

    def __init__(self):
        pass

    def get_transactions(self, transactions):
        trans = []
        db = collection_manager("banks", "users")
        for transaction in reversed(transactions):
            sender_identity = transaction["sender"]
            receiver_identity = transaction["receiver"]
            amount = transaction["amount"]
            send_Obj = db.find_query({"_id" : sender_identity})[0]
            receive_obj = db.find_query({"_id": receiver_identity})[0]
            send_name = send_Obj["fullname"]
            receive_name = receive_obj["fullname"]
            print(send_name, " paid ", amount, " to ", receive_name)
            data_dict = {}
            data_dict["sender_name"] = send_name
            data_dict["receiver_name"] = receive_name
            data_dict["amount"] = amount
            data_dict["date"] = transaction["timestamp"]
            trans.append(data_dict)
        print(trans)


    #Gallery card transaction note
    '''
    Title => Account transfer of xxx$
    Subtitle => xxx$ transfered from sender_name to recieved_name
    Button => Click here to view more 
    '''

    def generate_gallery_card_transaction(self, amount, sender, reciever, date):
        gal_card =   {
    "attachment":{
      "type":"template",
      "payload":{
        "template_type":"generic",
        "elements":[
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
        ]
      }
    }
  }


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