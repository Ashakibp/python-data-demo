from CollectionModule import mongo_test
import time
from cleanData import clean_data


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
            return logged_in_user
        return None

    def refresh(self, username, password):
        login = self.login(username, password)
        if login is not None:
            return login

    def get_balance(self, username, password):
        login = self.login(username, password)
        if login is not None:
            return login["balance"]

    def find_branches(self, username, password):
        logged_in = self.login(username, password)
        if logged_in is not None:
            branches = self.banks.find_query({"_id":self.login(username, password)["bank_id"]})["branches"]
            bran_list = []
            for branch in branches:
                bran_list.append(self.branches.find_query({"_id":branch})[0])
            return bran_list
        return False

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

    def make_transaction(self, username, password, other_username, amount):
        logged_in_user = self.login(username, password)
        if logged_in_user is not None:
            other_user = self.users.find_query({"username": other_username})
            if len(other_user) == 1:
                other_user_obj = other_user[0]
                if not self.get_balance(username, password) - amount >= 0:
                    return False
                else:
                    existing_balance = self.get_balance(username, password) - amount
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
                    trans_id = self.add_transaction_to_db(logged_in_user["_id"],other_user_obj["_id"], amount)
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
                    x = []
                    for trans in self.transactions.find_query({"sender":logged_in_user["_id"]}):
                        x.append(trans)
                    self.data_cleaner.get_transactions(x, 10)
                    return True
        return False







x = Bank_Api()
print(x.get_balance("sleeze", "121213"))
prof = x.make_transaction("sleeze", "121213","ashak", 100)
print(x.get_balance("sleeze", "121213"))