import logging
import time
logging.basicConfig(filename='statics_log.log', level=logging.DEBUG,format='%(asctime)s:%(levelname)s:%(message)s')

#This class is Singleton
#The class handles any calculation of processing time requests for the service
class ServiceStatistics:

     __instance = None
     @staticmethod 
     def getInstance():
      if ServiceStatistics.__instance == None:
         ServiceStatistics()
      return ServiceStatistics.__instance
     def __init__(self):
      if ServiceStatistics.__instance != None:
         raise Exception("ServiceStatistics class is a singleton")
      else:
         ServiceStatistics.__instance = self

     __request_count__=0
     __processing_time_count__=0
     __tik__=0
     __tok__=0

    #This method is called when the service starts processing a request
     def start_processing_request(self):
         self.__tik__= time.perf_counter()
    
    #This method is called when the service finishes processing a request
     def completion_processing_request(self):
         self.__tok__= time.perf_counter()
         self.__processing_time_count__+=(self.__tok__-self.__tik__)
         self.__request_count__+=1
         logging.debug('A calculation has been made for a new request. Processing time:{}'.format((self.__tok__-self.__tik__)))
     def get_request_count(self):
         return self.__request_count__

     def get_average_request_time(self)->float:
         if(self.__request_count__!=0):
            return self.__processing_time_count__/self.__request_count__
         else:
            return 0

      


   
