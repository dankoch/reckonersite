'''
Created on Sept 4, 2011
@author: danko
'''
from datetime import datetime
from xml.etree import cElementTree as cET
from reckonersite.domain.base import Base, buildXml, convertToDateTime

class ReckonerUser(Base):
    '''Object definition of a single user (as defined in the Reckoner DB)  
    Maintained to be synchronized with the Reckoner API'''

    def __init__(self, id=None, username=None, first_name=None, last_name=None, email=None,
                 auth_provider=None, auth_provider_id=None, first_login=None, last_login=None, 
                 profile_picture_url=None, profile_url=None, groups=None, permissions=None,
                 active=True, xml_string=None, xml_element=None):
        
        # Note: Since we're building the XML nodes off of the names of the attributes,
        # these names need to be kept aligned with the API definition.
        self.id = id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.auth_provider = auth_provider
        self.auth_provider_id = auth_provider_id
        self.first_login = first_login
        self.last_login = last_login
        self.profile_picture_url = profile_picture_url
        self.profile_url = profile_url
        self.groups = groups
        self.permissions = permissions
        self.active = active
        
        if not xml_string is None:
            self.buildFromXMLString(xml_string)
            
        if not xml_element is None:
            self.buildFromXMLElement(xml_element)
    
    def getXML(self):
        return (buildXml(self.__dict__, 'user'))
    
    def getXMLString(self):
        return cET.tostring(self.getXML())
    
    def buildFromXMLString(self, xml):
        xml_root = cET.XML(xml)
        self.buildFromXMLElement(xml_root)
    
    def buildFromXMLElement(self, xml_root):
        if (not xml_root.find('id') is None):
            self.id = xml_root.find('id').text
        if (not xml_root.find('username') is None):
            self.username = xml_root.find('username').text
        if (not xml_root.find('first_name') is None):
            self.first_name = xml_root.find('first_name').text
        if (not xml_root.find('last_name') is None):
            self.last_name = xml_root.find('last_name').text
        if (not xml_root.find('email') is None):
            self.email = xml_root.find('email').text
        if (not xml_root.find('auth_provider') is None):
            self.auth_provider = xml_root.find('auth_provider').text
        if (not xml_root.find('auth_provider_id') is None):
            self.auth_provider_id = xml_root.find('auth_provider_id').text
        
        if (not xml_root.find('first_login') is None) and (not xml_root.find('first_login').text is None):
            self.first_login = convertToDateTime(xml_root.find('first_login').text)

        if (not xml_root.find('last_login') is None) and (not xml_root.find('last_login').text is None):
            self.last_login = convertToDateTime(xml_root.find('last_login').text)

        if (not xml_root.find('profile_picture_url') is None):
            self.profile_picture_url = xml_root.find('profile_picture_url').text
        if (not xml_root.find('profile_url') is None):
            self.profile_url = xml_root.find('profile_url').text
        
        groupsElement = xml_root.find('groups')
        if (not groupsElement is None):    
            self.groups=[]
            for groupElement in groupsElement.findall('group'):
                self.groups.append(groupElement.text)   
                
        permissionsElement = xml_root.find('permissions')
        if (not permissionsElement is None):    
            self.permissions=[]
            for permissionsElement in permissionsElement.findall('permission'):
                self.permissions.append(permissionsElement.text) 
              
        if (not xml_root.find('active') is None):
            self.active = (xml_root.find('active').text == 'true')    