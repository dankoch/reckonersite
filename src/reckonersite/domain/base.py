'''
Created on Aug 23, 2011
@author: danko
'''
import sys
from datetime import datetime
from xml.etree import cElementTree as cET

class Base(object):
    '''Base object used for all reckoner domain pieces'''
        
    def getXML(self):
        pass
        #override this method
    
    def getXMLString(self):
        pass
        #override this method
        

def buildXml(object, root):
    '''Accepts a dictionary, list, or tuple of XML elements along with the name of the root node
       and returns an ElementTree XML Element object'''
    
    root_node = cET.Element(root)
    # Check to see if the item is a dictionary, list/tuple, Reckoner base type or other type.
    # For dictionaries, assume it's a subtree built beneath the key value and recur
    # For lists, assume it's a list of items built beneath the current root and recur
    # For Reckoner base types, have them build their own subtree.  Exclude the root - it provides its own.
    # For other types, assume they're str or unicode.  If not, we'll catch the exception
    
    if object is None:
        pass
    elif (isinstance(object, dict)):
        for attr, value in object.iteritems():
            if (value is not None):
                node = buildXml(value, attr)
                root_node.append(node)
    elif (isinstance(object, list) or isinstance(object, tuple)):
        for item in object:
            node = buildXml(item, root)
            root_node.append(node)
    elif (isinstance(object, Base)):
        node = object.getXML()
        return node
    elif (isinstance(object, datetime)):
        root_node.text=object.strftime("%Y-%m-%dT%H:%M:%S")
    elif (isinstance(object, bool)):
        if (not object):
            root_node.text='false'
        else:
            root_node.text='true'
    else:
        root_node.text=str(object)      
        
    return root_node

def convertToDateTime(xml_text):
    time = datetime.strptime(xml_text[0:18], "%Y-%m-%dT%H:%M:%S")
    return time
