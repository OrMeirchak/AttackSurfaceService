from abc import ABCMeta, abstractclassmethod, abstractmethod


class DataInterface:
    @abstractmethod
    def add_virtual_machine(self,vm_id: str):
        pass

    @abstractmethod 
    def attach_tag_to_vm(self,vm_id: str,tag_name: str):
        pass
    
    @abstractmethod  
    def add_potentially_attack(self,src_tag: str,dst_tag: str):
        pass

    @abstractmethod    
    def get_vm_count(self):
        pass

class VmIdAlreadyExistError(Exception):
     pass 


class VmIdDoesntExistError(Exception):
     def __init__(self,vm_id):
         super().__init__(vm_id+" virtual machine does not exist in the schema")

class TagNameDoesntExistError(Exception):
    __tag_name__=None
    def  __init__(self,tag_name):
        self.__tag_name__=tag_name
    def get_tag_name(self):
        return self.__tag_name__
