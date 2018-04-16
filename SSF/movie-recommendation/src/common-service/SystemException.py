'''
Created on Apr 14, 2018

@author: Piyawat Pemwattana
'''
from SystemConstant import SystemConstant
from SystemMessage import SystemMessage

class SystemException(Exception):
    
    def __init__(self, code):
        self.code = code
    def __str__(self):
        return repr(self.code)
    
    '''       '''         '''
        Access Deniend
    '''       '''         '''
        
    def message_validate_signIn_status(self, language):
        messageError = SystemMessage.Msg['accessDenied-'+language] + ': ' + SystemMessage.Msg['statusInactive-'+language] + SystemMessage.Msg['policyStatus-'+language]
        return  messageError
    
    def message_validate_not_authen(self, language):
        messageError = SystemMessage.Msg['accessDenied-'+language] + ': ' + SystemMessage.Msg['policyAuthen-'+language]
        return  messageError
    
