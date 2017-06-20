import cherrypy
import json
from CollectionModule.mongo_test import collection_manager




class QueryFinder(object):
    @cherrypy.expose
    def index(self):
        return '''<html>
          <head></head>
          <body>
            <form method="get" action="run_matcher">
              <input type="text" value="" name="name" />
              <button type="submit">Submit</button>
            </form>
          </body>
        </html>'''

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def run_matcher(self, name):
        client = collection_manager("testDatabase", "users")
        query = {"name" : name}
        l_one = client.find_query(query)
        if not l_one:
            return "No Query Results"
        else:
            id_bank = l_one[0]
            id_number = id_bank["_id"]
            client.change_collection("transactions")
            returner = client.find_query({ "user_id" : str(id_number) })
            print(returner)
            if not returner:
                return "No Transaction Results"
            for dict in returner:
                for key in dict:
                    if key == "_id":
                        temp = str(dict[key])
                        n_temp = temp.replace("ObjectId", "")
                        nn_temp = n_temp.replace(")", "")
                        dict[key] = nn_temp
            print(returner)
            return returner



if __name__ == '__main__':
    cherrypy.quickstart(QueryFinder())
    #QueryFinder().run_matcher("Aaron")
