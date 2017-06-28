from CollectionModule import mongo_test
import time
from cleanData import clean_data
from bottle import run, get, response, post
import json


class Bank_Api(object):

    def __init__(self):
        self.users = mongo_test.collection_manager("banks", "users")
        self.banks = mongo_test.collection_manager("banks", "banks")
        self.transactions = mongo_test.collection_manager("banks", "transactions")
        self.branches = mongo_test.collection_manager("banks", "branches")
        self.data_cleaner = clean_data()

    def login(self, username, password):
        username_query = self.users.find_query({"username": username})
        if len(username_query) == 1 and username_query[0]["password"] == password:
            logged_in_user = username_query[0]
            dict_r = {}
            dict_r["save_variables"] = [{"user_id":str(logged_in_user["_id"]), "balance": logged_in_user["balance"]}]
            return [dict_r]
        dict = {}
        dict["text"] = "Invalid login try again"
        return [dict]

    def refresh(self, user_id):
        login_check = self.users.find_query({"_id":user_id})
        if len(login_check) == 1:
            login = login_check[0]
            return login
        else:
            dict = {}
            dict["text"] = "Invalid login try again"
            return [dict]

    def get_balance(self, user_id):
        user = self.refresh(user_id)
        return user["balance"]


    def find_branches(self, user_id):
        logged_in = None
        login_check = self.users.find_query({"_id": user_id})
        if login_check is not []:
            logged_in = login_check[0]
        if logged_in is not None:
            branches = self.banks.find_query({"_id": logged_in["bank_id"]})["branches"]
            bran_list = []
            for branch in branches:
                bran_list.append(self.branches.find_query({"_id":branch})[0])
            branch_card = self.data_cleaner.generate_gallery_card_transaction(bran_list)
            return [branch_card]
        dict = {}
        dict["text"] = "Invalid login try again"
        return [dict]

    def get_bank(self, text):
        pass

    def add_transaction_to_db(self, sender_obj, receiver_obj, amount):
        query = {
            "sender": sender_obj,
            "receiver": receiver_obj,
            "amount": amount,
            "timestamp": time.time()
        }

        self.transactions.add_query(query)
        trans_obj = self.transactions.find_query(query)[0]
        return trans_obj["_id"]

    def make_transaction(self, user_id, other_username, amount):
        logged_in_user = self.refresh(user_id)
        if logged_in_user is not None:
            other_user = self.users.find_query({"username": other_username})
            if len(other_user) == 1:
                other_user_obj = other_user[0]
                if not self.get_balance(user_id) - amount >= 0:
                    return False
                else:
                    existing_balance = self.get_balance(user_id) - amount
                    transfer_balance = other_user_obj["balance"] + amount
                    self.users.update_query(
                        {"_id": logged_in_user["_id"]},
                            {"$set": {"balance": existing_balance
                        }})
                    self.users.update_query(
                            {"_id": other_user_obj["_id"]},
                            {"$set": {"balance": transfer_balance}}
                    )
                    trans_one = logged_in_user["transactions"]
                    trans_two = other_user_obj["transactions"]
                    trans_id = self.add_transaction_to_db(logged_in_user["_id"], other_user_obj["_id"], amount)
                    trans_one.append(trans_id)
                    trans_two.append(trans_id)
                    self.users.update_query(
                        {"_id": logged_in_user["_id"]},
                        {"$set": {"transactions": trans_one
                                  }})
                    self.users.update_query(
                        {"_id": other_user_obj["_id"]},
                        {"$set": {"transactions": trans_two}}
                    )
                    text = {}
                    text["text"] = "Transaction Successful"
                    return [text]
        text = {}
        text["text"] = "Error with transaction"
        return [text]


    def get_transactions(self, user_id, number):


response.content_type = 'application/json'

x = Bank_Api()

@get("/login/username/<username>/password/<password>")
def do_login(username, password):
    c = x.login(username, password)
    response.content_type = 'application/json'
    return json.dumps(c)

@post("/transaction/user_id/<user_id>/other_username/<other_username>/amount/<amount>")
def do_transaction(user_id, other_username, amount):
    response.content_type = 'application/json'
    c = x.make_transaction(user_id, other_username, amount)
    return json.dumps(c)





run(host='localhost', port=8080, debug=True)


