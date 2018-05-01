'''
Created on Apr 1, 2018

@author: Piyawat Pemwattana
'''

from pomServiceDto import pomServiceDto


if __name__ == '__main__':
    pass

def pom_version():
    pom = pomServiceDto('common-service',
                  '1.0.1',
                  '0.0.11-PROTOTYPE',
                  'Created on Dec 11, 2018',
                  'Piyawat Pemwattana')
    return pom

pom = pom_version()
print(pom.get_version())