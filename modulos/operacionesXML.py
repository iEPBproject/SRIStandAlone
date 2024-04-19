'''
Created on 19 mar 2024

@author: Efinovatic
'''

import sys
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
    root=ET.Element('iEPBxml',attrib={'xmlns':"http://www.efinovatic.es/sri",
                                                      'xmlns:xhtml':"http://www.w3.org/1999/xhtml",
                                                      'xmlns:xsi':"http://www.w3.org/2001/XMLSchema-instance",
                                                      'xmlns:xsd':"http://www.w3.org/2001/XMLSchema",
                                                      'xsi:schemaLocation':"http://www.efinovatic.es/sri http://gbxml.org/schema/6-01/GreenBuildingXML_Ver6.01.xsd",
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
    ns = {'d':"http://www.efinovatic.es/sri"}
    for projectElement in root.findall('.//d:Project',ns):
        p=Proyecto.creaDesdeXML(projectElement)
        # print(p.getTotalSRI())
        # print(p.sri())
        listaProyectosAlmacenado.append(p)
    
def escribirResultadosSri(rutaArchivo = None):
    tree = ET.parse(rutaArchivo)
    root = tree.getroot()
    ns = {'d':"http://www.efinovatic.es/sri"}
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
    if rutaArchivoOriginal == rutaArchivoNuevo:
        print('Error no pueden ser el mismo archivo')
        sys.exit()
        
    elif rutaArchivoOriginal != '':
        ns = {'d':"http://www.efinovatic.es/sri"}
        project = root.find('.//d:Project', ns)
    
        for instanciaProyecto in listaProyectosAlmacenado:
            if instanciaProyecto.id == int(project.attrib['id']):
                p = instanciaProyecto
                
        if p:
            totalSri = root.find('.//d:TotalSriScore', ns)
            totalSri.text = str(p.getTotalSRI())
            
            totalScoreKf1 = root.find('.//d:ScoreKF1', ns)
            totalScoreKf1.text = str(p.getEnergyPerformannceKf1())
            
            totalScoreKf2 = root.find('.//d:ScoreKF2', ns)
            totalScoreKf2.text = str(p.getResponseToUserNeedsKf2())
            
            totalScoreKf3 = root.find('.//d:ScoreKF3', ns)
            totalScoreKf3.text = str(p.getEnergyFlexibilityKf3())
    else:
        print('Error neceseitas utilizar la opcion -i <inputfile>')
    if rutaArchivoNuevo != '':
        tree.write(rutaArchivoNuevo)
    else:
        print('Error necesitas aprotar un archivo de salida')
    # xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")
    # with open(rutaArchivoNuevo, "w") as f:
    #     f.write(xmlstr) 
if __name__ == '__main__':
    # importarSriStandAlone(r'C:\Users\efinovatic\Desktop\Proyectos Sri2Market\175.xml')  
    # escribirResultadosSri(r'C:\Users\efinovatic\Desktop\Proyectos Sri2Market\175.xml')
    # escribirXML(r'C:\Users\efinovatic\Desktop\Proyectos Sri2Market\175.xml', r'C:\Temp\test.iEPBXML')
    # p = Proyecto.objects.first()
    # print(p.catalogo)
    # print(p.dominiosPresentes)
    # print(p.getTotalSRI())
    # print(p.sri())
    

                
                
            
            