# when you make the sql tables, add their location to the config file
# and then put the location of file in the default preferences in preferences.py (some variable, look at port or endpoint as example)

# for functions common amongst script, scriptLog, computer and user classes

from abc import ABC, abstractmethod 

class Entry(ABC):
    # abstract method
    def __init__(self):
        raise NotImplementedError("Subclasses should implement this!")

    # abstract method
    def toJson(self):
        raise NotImplementedError("Subclasses should implement this!")

class Table(ABC): 
    # This function is for initializing an sql table of the programs database 
    # returns 1 if table is successfully created, -1 otherwise
    #abstract method
    @staticmethod
    def createTable():
        raise NotImplementedError("Subclasses should implement this!")

    # abstract method
    @staticmethod 
    def getByID(ID: int): 
        raise NotImplementedError("Subclasses should implement this!")

    #abstract method
    @staticmethod
    def getAll():
        raise NotImplementedError("Subclasses should implement this!")

    #abstract method
    @staticmethod
    def createEntry(values: tuple):
        raise NotImplementedError("Subclasses should implement this!")

    #abstract method
    @staticmethod
    def getAttrByID(attr: str, ID: int):
        raise NotImplementedError("Subclasses should implement this!")

    #abstract method
    @staticmethod
    def getWithQuery(query: str):
        raise NotImplementedError("Subclasses should implement this!")

    #abstract method
    @staticmethod
    def add(entry):
        raise NotImplementedError("Subclasses should implement this!")

    #abstract method
    @staticmethod
    def delete(ID: int):
        raise NotImplementedError("Subclasses should implement this!")

    #abstract method
    @staticmethod
    def editEntry(values: tuple):
        raise NotImplementedError("Subclasses should implement this!")
    
