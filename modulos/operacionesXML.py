'''
Created on 19 mar 2024

@author: Efinovatic
'''

import sys
import xml.etree.ElementTree as ET
from xml.dom import minidom
from modulos.models import Proyecto
import zipfile
import os
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
    
def exportarZip(rutaZip, rutaXML, rutaGBXML):
    # Create a ZipFile Object
    rutaXMLTemporal, ficheroXML = os.path.split(rutaXML)
    rutaGBXMLTemporal, ficheroGBXML = os.path.split(rutaGBXML)
    with zipfile.ZipFile(rutaZip, 'w') as zip_object:
        # Adding files that need to be zipped
        zip_object.write(rutaXML, arcname = ficheroXML)
        zip_object.write(rutaGBXML, arcname = ficheroGBXML)
    
    # Check to see if the zip file is created
    if os.path.exists(rutaZip):
        print('Se ha creado correctamente el nuevo archivo iEPB')
    else:
        print('No se ha crear correctamente el nuevo archivo iEPB')
    
def descomprimirZIP(path):
#     files=os.listdir(path)
#     for file in files:
#         if file.endswith('.iEPB'):
    # filePath=path+'/'+file
    zip_file = zipfile.ZipFile(path)
    ruta, fichero = os.path.split(path)
    for names in zip_file.namelist():
        zip_file.extract(names,ruta)
        if '_gbXML' not in names:
            rutaXML = os.path.join(ruta,names)
        else:
            rutagbXML = os.path.join(ruta,names)
    zip_file.close()
    return rutaXML, rutagbXML

def importarSriStandAlone(nombreArchivo):
    rutaXML, rutagbXML = descomprimirZIP(nombreArchivo)
    tree = ET.parse(rutaXML)
    root = tree.getroot()
    ns = {'d':"http://www.efinovatic.es/sri"}
    for projectElement in root.findall('.//d:Project',ns):
        p=Proyecto.creaDesdeXML(projectElement)
        p.yearOfConstruction = float(root.find('.//d:YearOfConstruction', ns).text)
        # print(p.getTotalSRI())
        # print(p.sri())
        listaProyectosAlmacenado.append(p)
    
def escribirResultadosSri(rutaArchivo = None):
    rutaXML, rutagbXML = descomprimirZIP(rutaArchivo)
    tree = ET.parse(rutaXML)
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
    if rutaArchivoOriginal == rutaArchivoNuevo:
        print('Error no pueden ser el mismo archivo')
        sys.exit()
        
    elif rutaArchivoOriginal != '':
        rutaXML, rutagbXML = descomprimirZIP(rutaArchivoOriginal)
        
        # Grabamos el primer archivo xml
        tree = ET.parse(rutaXML)
        root = tree.getroot()
        ET.register_namespace("", "http://www.efinovatic.es/sri")
        ns = {'d':"http://www.efinovatic.es/sri"}
        project = root.find('.//d:Project', ns)
    
        for instanciaProyecto in listaProyectosAlmacenado:
            if instanciaProyecto.id == int(project.attrib['id']):
                p = instanciaProyecto
                
        if p:
            resultados = root.find('.//d:Results', ns)
            if resultados:
                totalSri = root.find('.//d:TotalSriScore', ns)
                totalSri.text = str(p.getTotalSRI())
                
                totalScoreKf1 = root.find('.//d:ScoreKF1', ns)
                totalScoreKf1.text = str(p.getEnergyPerformannceKf1())
                
                totalScoreKf2 = root.find('.//d:ScoreKF2', ns)
                totalScoreKf2.text = str(p.getResponseToUserNeedsKf2())
                
                totalScoreKf3 = root.find('.//d:ScoreKF3', ns)
                totalScoreKf3.text = str(p.getEnergyFlexibilityKf3())
            else:
                results = ET.SubElement(project, 'Results') 
                totalSriScore = ET.SubElement(results, "TotalSriScore")
                totalSriScore.text = str(p.getTotalSRI())      
                scoreKF1 = ET.SubElement(results, "ScoreKF1")
                scoreKF1.text = str(p.getEnergyPerformannceKf1())     
                scoreKF2 = ET.SubElement(results, "ScoreKF2")
                scoreKF2.text = str(p.getResponseToUserNeedsKf2())
                scoreKF3 = ET.SubElement(results, "ScoreKF3")
                scoreKF3.text = str(p.getEnergyFlexibilityKf3())  
        ET.indent(tree, space="\t", level=0)
        ruta, newFileXML = os.path.split(rutaXML)
        arrayXML = newFileXML.split('.')
        arrayXML[0] = '{}-outputfile'.format(arrayXML[0])
        newFileXML = '.'.join(arrayXML)        
        nuevaRutaXML = os.path.join(ruta, newFileXML)
        tree.write(nuevaRutaXML)
        
        # Grabamos el archivo gbXML
        treeGbXML = ET.parse(rutagbXML)
        rootGbXML = treeGbXML.getroot()
        ET.register_namespace("", "http://www.gbxml.org/schema")
        ET.indent(tree, space="\t", level=0)
        rutaGbXML, newFileGbXML = os.path.split(rutagbXML)
        arrayGbXML = newFileGbXML.split('.')
        arrayGbXML[0] = '{}-outputfile'.format(arrayGbXML[0])
        newFileGbXML = '.'.join(arrayGbXML)  
        nuevaRutaGbXML = os.path.join(rutaGbXML, newFileGbXML)
        treeGbXML.write(nuevaRutaGbXML)
        
        # Creamos el nuevo zip
        exportarZip(rutaArchivoNuevo, nuevaRutaXML, nuevaRutaGbXML)
    else:
        print('Error necesitas aprotar un archivo de salida')
    # xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")
    # with open(rutaArchivoNuevo, "w") as f:
    #     f.write(xmlstr) 
if __name__ == '__main__':
    importarSriStandAlone(r'C:\Temp\427.iEPB')  
    escribirResultadosSri(r'C:\Temp\427.iEPB')
    # escribirXML(r'C:\Temp\427.iEPB', r'C:\Temp\427-output.iEPB')
    # p = Proyecto.objects.first()
    # print(p.catalogo)
    # print(p.dominiosPresentes)
    # print(p.getTotalSRI())
    # print(p.sri())