'''
Created on 19 mar 2024

@author: Efinovatic
'''

import xml.etree.ElementTree as ET
from xml.dom import minidom
from modulos.models import Proyecto

def importarSriStandAlone(nombreArchivo):
    print(nombreArchivo)
    tree = ET.parse(nombreArchivo)
    root = tree.getroot()
    ns = {'d':"http://www.gbxml.org/schema"}
    for projectElement in root.findall('.//d:Project',ns):
        p=Proyecto.creaDesdeXML(projectElement)
        print(p.getTotalSRI())
        print(p.sri())
    
def escribirResultadosSri(rutaArchivo):
    tree = ET.parse(rutaArchivo)
    root = tree.getroot()
    ns = {'d':"http://www.gbxml.org/schema"}
    project = root.find('.//d:Project', ns)
    p = Proyecto.objects.get(id = int(project.attrib['id']))
    if p:
        print('El resultado Total del SRI: {}'.format(p.getTotalSRI()))
        print('El resultado Total del SRI: {}'.format(p.getEnergyPerformannceKf1()))
        print('El resultado Total del SRI: {}'.format(p.getResponseToUserNeedsKf2()))
        print('El resultado Total del SRI: {}'.format(p.getEnergyFlexibilityKf3()))
    else:
        print('Primero debe importar un archivo con la opcion --> -i <inputfile>')

if __name__ == '__main__':
    # importarSriStandAlone(r'C:\Temp\test.iEPBXML')  
    escribirResultadosSri(r'C:\Temp\test.iEPBXML')
    # p = Proyecto.objects.first()
    # print(p.catalogo)
    # print(p.dominiosPresentes)
    # print(p.getTotalSRI())
    # print(p.sri())
    

                
                
            
            