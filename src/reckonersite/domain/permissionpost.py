'''
Created on Sept 14, 2011
@author: danko
'''
from reckonersite.domain.base import Base, buildXml
from xml.etree import cElementTree as cET

class PermissionPost(Base):
    '''Object used to post user permission changes back to the Reckoner Content Services'''

    def __init__(self, action=None, groups=None, active=False, user_id=None, session_id=None, 
                 xml_string=None, xml_element=None):
        
        self.action = action
        self.active = active
        self.user_id = user_id
        self.session_id = session_id
        
        # This takes groups as a list of strings and converts them to 'Group' type
        # for XML marshalling purposes. Beware for those who read group after they
        # write it.
        
        if not groups is None:
            self.groups = self.buildGroupList(groups)
        
        if not xml_string is None:
            self.buildFromXMLString(xml_string)
            
        if not xml_element is None:
            self.buildFromXMLElement(xml_element)
        
    def getXML(self):
        return (buildXml(self.__dict__, 'permission_post'))
    
    def getXMLString(self):
        return cET.tostring(self.getXML())
    
    def buildFromXMLString(self, xml):
        xml_root = cET.XML(xml)
        self.buildFromXMLElement(xml_root)
    
    def buildFromXMLElement(self, xml_root):
        if (not xml_root.find('action') is None):
            self.action = xml_root.find('action').text
            
        groupsElement = xml_root.find('groups')
        if (not groupsElement is None):
            self.groups=[]
            for groupElement in groupsElement.findall('group'):
                self.groups.append(groupElement.text)
                
        if (not xml_root.find('active') is None):
            self.active = (xml_root.find('question').text == 'true')
        if (not xml_root.find('user_id') is None):
            self.user_id = xml_root.find('user_id').text
        if (not xml_root.find('session_id') is None):
            self.session_id = xml_root.find('session_id').text

    def buildGroupList(self, groups):
        groupList = []
        for group in groups:
            groupList.append(Group(group))
        
        return groupList

class Group(Base):
    def __init__(self, value=None):
        self.value = value
        
    def getXML(self):
        return (buildXml(self.value, 'group'))
    
    def getXMLString(self):
        return cET.tostring(self.getXML())        