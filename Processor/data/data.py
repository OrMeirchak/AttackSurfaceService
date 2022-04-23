import logging
from Processor.data.dataInterface import *

logging.basicConfig(filename='data_log.log', level=logging.DEBUG,format='%(asctime)s:%(levelname)s:%(message)s')

class VirtualMachinesList(DataInterface):
    __vm_list__=set()
    __tags_list__=set()
    __vm_count__=0

   #In case there is already a machine with the same id the machine will not be added and the method raise VmIdAlreadyExistError
    def add_virtual_machine(self,vm_id):
       self.__check_if_id_exist__(self.__vm_list__)
       self.__vm_list__.add(self.virtualMachine(vm_id))
       self.__vm_count__+=1
       logging.debug('The virtual machine {} was added'.format(vm_id))
    
    #The method recieve the ID of a virtual machine and the name of a tag
    #and attaches the virtual machine to the list of virtual machines of the tag
    #In case the tag does not exist the method will add the tag to the list of tags
    def attach_tag_to_vm(self,vm_id,tag_name):
        try:
           self.__get_tag__(tag_name).vm_list.add(vm_id)
        except:
            new_tag=self.tag(tag_name)
            new_tag.vm_list.add(vm_id)
            self.__tags_list__.add(new_tag)
        logging.debug('The {} virtual machine has been added to the list of machines of the {} tag'.format(vm_id,tag_name))
     

    #The method recieve names of src_tag and dst_tag
    #and attaches all machines that relevant to the src tag to the list of threatening machines of each machine relevant to dst tag
    #In case one of the tags does not exist the method raise TagNameDoesntExistError 
    def add_potentially_attack(self,src_tag,dst_tag):
          for src_vm in self.__get_tag__(src_tag).vm_list:
              for dst_vm in self.__get_tag__(dst_tag).vm_list:
                   if(src_vm!=dst_vm):
                     self.__get_machine__(dst_vm).threatening_vm.add(src_vm)
                     logging.debug('The virtual machine {} has been added to the list of virtual machines that threaten the virtual machine {}'.format(dst_vm,src_vm))
          

    def get_potentially_attack(self,vm_id)->list:
        return list(self.__get_machine__(vm_id).threatening_vm)

    def get_vm_count(self)->int:
        return self.__vm_count__

    def __get_tag__(self,tag_name):
        for tag in self.__tags_list__:
            if(tag.get_name()==tag_name):
                return tag
        raise TagNameDoesntExistError(tag_name)

    def __get_machine__(self,vm_id):
        for vm in self.__vm_list__:
            if (vm.get_id()==vm_id):
                return vm
        raise VmIdDoesntExistError(vm_id)

    #In case the Id exist the function throw exception
    def __check_if_id_exist__(self,vm_id):
        for v_m in self.__vm_list__:
            if(v_m.get_id()==vm_id):
                raise VmIdAlreadyExistError()
            

    class virtualMachine:
         __id__=None

         def __init__(self,id):
             self.__id__=id
             self.threatening_vm=set()

         def get_id(self):
             return self.__id__

    class tag:
        __tag_name__=None

        def __init__(self,tag_name):
            self.__tag_name__=tag_name
            self.vm_list=set()

        def get_name(self):
            return self.__tag_name__


            





    
        

    
        
   


    

         
        
         
