from CollectionModule.mongo_test import collection_manager

class clean_data(object):

    def get_transactions(self, transactions):
        trans = []
        db = collection_manager("bank", "users")
        for transaction in transactions:
            sender_identity = transaction["sender"]
            print(sender_identity)



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