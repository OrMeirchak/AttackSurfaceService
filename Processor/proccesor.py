import json
import logging
import os
from Processor.data.dataInterface import TagNameDoesntExistError, VmIdDoesntExistError,VmIdAlreadyExistError
from Processor.proccesorInterface import ProccesorInterface,InvalidJsonSchemaException
from Processor.data.data import VirtualMachinesList

logging.basicConfig(filename='proccesor_log.log', level=logging.DEBUG,format='%(asctime)s:%(levelname)s:%(message)s')

#This class is Singleton
#The class receives a json file and Processes it into a VirtualMachinesList object
class Proccesor(ProccesorInterface):
    __instance = None
    @staticmethod 
    def getInstance():
      if Proccesor.__instance == None:
         Proccesor()
      return Proccesor.__instance
    def __init__(self):
      if Proccesor.__instance != None:
         raise Exception("Proccesor class is a singleton")
      else:
         Proccesor.__instance = self


    vm_list=VirtualMachinesList()

    #This method recieve path of json file
    #In case the file extension is not '.json' the method raise ExtensionException
    #In case the file is not in the format that the method expected to receive,the method raise InvalidJsonSchemaException
    #else the function will processes the file into a VirtualMachinesList object
    def load_data_source(self, path: str) :
        ProccesorInterface.check_extension(path)
        with open(path,'r') as input_file:
           js=json.load(input_file)
           logging.debug('The file {} was uploaded successfully'.format(os.path.basename(path)))
        try:
         for v_m in js["vms"]:
            try:
               self.vm_list.add_virtual_machine(v_m["vm_id"]) 
            except VmIdAlreadyExistError():
               logging.warn('The virtual machine {} was not added because there is already a machine with the id {}'.format(v_m["name"],v_m["vm_id"]))
            for tag in v_m["tags"]:
               self.vm_list.attach_tag_to_vm(v_m["vm_id"],tag)

         for fw_rule in js["fw_rules"]:
            try:
                 self.vm_list.add_potentially_attack(fw_rule["source_tag"],fw_rule["dest_tag"])
            except TagNameDoesntExistError as e:
               logging.warn('The firewall rule {} was not added because the {} tag does not exist in the list of machines'.format(fw_rule["fw_id"],e.get_tag_name()))  
        except KeyError:
         raise InvalidJsonSchemaException()
                
          
    def get_potential_attackers(self,vm_id):
          return self.vm_list.get_potentially_attack(vm_id)
        
    def get_vm_count(self):
        return self.vm_list.get_vm_count()
    


