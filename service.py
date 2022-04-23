import sys
sys.path.append("site-packages")

from xmlrpc.client import boolean
from flask import Flask
from flask_restful import Api, Resource,reqparse
from Processor.data.dataInterface import VmIdDoesntExistError
from Processor.proccesor import Proccesor
from ServiceStatistics import ServiceStatistics
from werkzeug.serving import is_running_from_reloader
from logging import log

app = Flask(__name__)
api = Api(app)
processor = Proccesor.getInstance()

def startup():
    print()
    get_user_input()
    app.run(debug=False,port=80)
    
attack_get_args = reqparse.RequestParser()
attack_get_args.add_argument("vm_id", type=str, help="vm_id is required", required=True)

#The method get input from the user
#In case the input is invalid the method will print the error to the console and ask input again
def get_user_input():
       json_file_path=input("Please type the full path of the json file\n")
       try:
          processor.load_data_source(json_file_path)
       except Exception as e:
          print(e)
          get_user_input()
    

class Attack(Resource):
    processor=Proccesor.getInstance()
    service_statistics=ServiceStatistics.getInstance()

   
    def get(self):
         args = attack_get_args.parse_args()
         self.service_statistics.start_processing_request()
         try:
              json_response=processor.get_potential_attackers(args['vm_id'])
         except VmIdDoesntExistError as e:
             return str(e)
         self.service_statistics.completion_processing_request()
         return json_response

api.add_resource(Attack, "/api/v1/attack")      

class Stats(Resource):
    processor=Proccesor.getInstance()
    service_statistics=ServiceStatistics.getInstance()
    
    def get(self):
         self.service_statistics.start_processing_request()
         if(self.service_statistics.get_request_count()==0):
             return "No requests have been made yet"
         stats_response = {"vm_count": self.processor.get_vm_count(),"request_count": self.service_statistics.get_request_count(),"average_request_time": "{:.18f}".format(self.service_statistics.get_average_request_time())}
         self.service_statistics.completion_processing_request()
         return stats_response
      
api.add_resource(Stats, "/api/v1/stats")

if __name__ == "__main__":
    startup()
	