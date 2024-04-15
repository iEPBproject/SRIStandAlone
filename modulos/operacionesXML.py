'''
Created on 19 mar 2024

@author: Efinovatic
'''

import xml.etree.ElementTree as ET
from xml.dom import minidom
from modulos.models import Proyecto
listaProyectosAlmacenado = []

ET.register_namespace('', "http://www.opengis.net/wmts/1.0")
ET.register_namespace('xhtml', "http://www.w3.org/1999/xhtml")
ET.register_namespace('xsi', "http://www.w3.org/2001/XMLSchema-instance")
ET.register_namespace('xsd', "http://www.w3.org/2001/XMLSchema")
ET.register_namespace('temperatureUnit', "C")
ET.register_namespace('lengthUnit', "Meters")
ET.register_namespace('areaUnit', "SquareMeters")
ET.register_namespace('volumeUnit', "CubicMeters")
ET.register_namespace('useSIUnitsForResults', "True")
ET.register_namespace('version', "6.01")
ET.register_namespace('SurfaceReferenceLocation', "Centerline")

def getRoot():
    root=ET.Element('iEPBxml',attrib={'xmlns':"http://www.gbxml.org/schema",
                                                      'xmlns:xhtml':"http://www.w3.org/1999/xhtml",
                                                      'xmlns:xsi':"http://www.w3.org/2001/XMLSchema-instance",
                                                      'xmlns:xsd':"http://www.w3.org/2001/XMLSchema",
                                                      'xsi:schemaLocation':"http://www.gbxml.org/schema http://gbxml.org/schema/6-01/GreenBuildingXML_Ver6.01.xsd",
                                                      'temperatureUnit':"C",
                                                      'lengthUnit':"Meters",
                                                      'areaUnit':"SquareMeters",
                                                      'volumeUnit':"CubicMeters",
                                                      'useSIUnitsForResults':"true",
                                                      'version':"6.01",
                                                      'SurfaceReferenceLocation':"Centerline"})  
    return root

def importarSriStandAlone(nombreArchivo):
    tree = ET.parse(nombreArchivo)
    root = tree.getroot()
    ns = {'d':"http://www.gbxml.org/schema"}
    for projectElement in root.findall('.//d:Project',ns):
        p=Proyecto.creaDesdeXML(projectElement)
        # print(p.getTotalSRI())
        # print(p.sri())
        listaProyectosAlmacenado.append(p)
    
def escribirResultadosSri(rutaArchivo = None):
    tree = ET.parse(rutaArchivo)
    root = tree.getroot()
    ns = {'d':"http://www.gbxml.org/schema"}
    project = root.find('.//d:Project', ns)
    # p = Proyecto.objects.get(id = int(project.attrib['id']))
    p = None
    for instanciaProyecto in listaProyectosAlmacenado:
        if instanciaProyecto.id == int(project.attrib['id']):
            p = instanciaProyecto
    if p:
        print('El resultado Total del SRI: {}'.format(p.getTotalSRI()))
        print('El resultado Total de Energy Perfomance (Kf1): {}'.format(p.getEnergyPerformannceKf1()))
        print('El resultado Total de Response To User Needs (Kf2): {}'.format(p.getResponseToUserNeedsKf2()))
        print('El resultado Total de Energy Flexibility (Kf3): {}'.format(p.getEnergyFlexibilityKf3()))
    else:
        print('Primero debe importar un archivo con la opcion --> -i <inputfile>')
        
def escribirXML(rutaArchivoOriginal, rutaArchivoNuevo):
    tree = ET.parse(rutaArchivoOriginal)
    root = tree.getroot()
    ns = {'d':"http://www.gbxml.org/schema"}
    project = root.find('.//d:Project', ns)
    for instanciaProyecto in listaProyectosAlmacenado:
        if instanciaProyecto.id == int(project.attrib['id']):
            p = instanciaProyecto
            
    if p:
        totalSri = root.find('.//d:totalSriScore', ns)
        totalSri.text = str(p.getTotalSRI())
        
        totalScoreKf1 = root.find('.//d:scoreKF1', ns)
        totalScoreKf1.text = str(p.getEnergyPerformannceKf1())
        
        totalScoreKf2 = root.find('.//d:scoreKF2', ns)
        totalScoreKf2.text = str(p.getResponseToUserNeedsKf2())
        
        totalScoreKf3 = root.find('.//d:scoreKF3', ns)
        totalScoreKf3.text = str(p.getEnergyFlexibilityKf3())
    
    # doc = minidom.parseString(ET.tostring(root))
    # print (doc.toprettyxml(encoding='utf8'))
    # tree.write(rutaArchivoNuevo)
    xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")
    with open(rutaArchivoNuevo, "w") as f:
        f.write(xmlstr) 
if __name__ == '__main__':
    importarSriStandAlone(r'C:\Temp\test.iEPBXML')  
    # escribirResultadosSri(r'C:\Temp\test.iEPBXML')
    escribirXML(r'C:\Temp\test.iEPBXML', r'C:\Temp\test2.iEPBXML')
    # p = Proyecto.objects.first()
    # print(p.catalogo)
    # print(p.dominiosPresentes)
    # print(p.getTotalSRI())
    # print(p.sri())
    

                
                
            
            