'''
Created on 19 mar 2024

@author: Efinovatic
'''

import xml.etree.ElementTree as ET
from modulos.models import Proyecto

def importarSriStandAlone(nombreArchivo):
    tree = ET.parse(nombreArchivo)
    root = tree.getroot()
    ns = {'d':"http://www.gbxml.org/schema"}
    for projectElement in root.findall('.//d:Project',ns):
        p=Proyecto.creaDesdeXML(projectElement)
        print(p.getTotalSRI())
        print(p.sri())        

if __name__ == '__main__':
    importarSriStandAlone()  
    # p = Proyecto.objects.first()
    # print(p.catalogo)
    # print(p.dominiosPresentes)
    # print(p.getTotalSRI())
    # print(p.sri())
    

                
                
            
            