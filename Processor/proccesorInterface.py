from abc import ABCMeta, abstractmethod
import logging
import os
logging.basicConfig(filename='proccesor_log.log', level=logging.DEBUG,format='%(asctime)s:%(levelname)s:%(message)s')

class ProccesorInterface:
    @abstractmethod
    def load_data_source(self, path: str) :
        pass

    @abstractmethod
    def get_potential_attackers(self) -> str:
        pass
    
    @abstractmethod
    def get_statistics(self) -> str:
        pass

    def check_extension(path):
        ext = os.path.splitext(path)[-1].lower()
        if(ext!='.json'):
           raise ExtensionException("json")

class InvalidJsonSchemaException(Exception):
     def __init__(self):
      super().__init__("Invalid Json Schema")
      logging.error("The json file received as input contains an invalid schema") 
      

class ExtensionException(Exception):
     def __init__(self,expectedExtension):
      super().__init__("Invalid file extension\nExected extension : " + expectedExtension) 
      logging.error("The file received as input does not have a .json extension") 

