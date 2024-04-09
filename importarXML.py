'''
Created on 19 mar 2024

@author: Efinovatic
'''

import xml.etree.ElementTree as ET
from models import Proyecto

def importarSriStandAlone(nombreArchivo):
    tree = ET.parse(r'ejemplos/{}'.format(nombreArchivo))
    root = tree.getroot()
    ns = {'d':"http://www.gbxml.org/schema"}
    for projectElement in root.findall('.//d:Project',ns):
        Proyecto.creaDesdeXML(projectElement)

if __name__ == '__main__':
    importarSriStandAlone()  
    # p = Proyecto.objects.first()
    # print(p.catalogo)
    # print(p.dominiosPresentes)
    # print(p.getTotalSRI())
    # print(p.sri())
    

                
                
            
            