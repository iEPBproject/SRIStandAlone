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
import tempfile
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
        print('New iEPB file created')
    else:
        print('Problem creating the new iEPB file ')
    
def descomprimirZIP(path, pathDestino = None, extraer = False):
#     files=os.listdir(path)
#     for file in files:
#         if file.endswith('.iEPB'):
    # filePath=path+'/'+file
    zip_file = zipfile.ZipFile(path)
    ruta, fichero = os.path.split(path)
    if pathDestino:
        rutaGuardar = pathDestino
    elif extraer:
        rutaGuardar = ruta
    else:
        rutaGuardar = tempfile.gettempdir()
        
    for names in zip_file.namelist():
        zip_file.extract(names,rutaGuardar)
        if '_gbXML' not in names:
            rutaXML = os.path.join(rutaGuardar,names)
        else:
            rutagbXML = os.path.join(rutaGuardar,names)
    zip_file.close()
    return rutaXML, rutagbXML

def importarSriStandAlone(nombreArchivo):
    if os.path.exists(nombreArchivo):
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
        if os.path.exists(rutaXML):os.remove(rutaXML)
    else:
        print('The file does not exist.')
        sys.exit()
    
def imprimirTodosResultadosSri(rutaArchivo = None):
    if os.path.exists(rutaArchivo):
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
            print('Total SRI: {}'.format(p.getTotalSRI()))
            print('Energy Perfomance (Kf1): {}'.format(p.getEnergyPerformannceKf1()))
            print('Response To User Needs (Kf2): {}'.format(p.getResponseToUserNeedsKf2()))
            print('Energy Flexibility (Kf3): {}'.format(p.getEnergyFlexibilityKf3()))
        else:
            print('Please, define the input file --> -i <inputfile>')
        if os.path.exists(rutaXML):os.remove(rutaXML) 
    else:
        print('The input file does not exist.')
        sys.exit()
        
def imprimirResultadoSRI(rutaArchivo = None):
    if os.path.exists(rutaArchivo):
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
            print(p.getTotalSRI())
        else:
            print('Please, define the input file --> -i <inputfile>')
        if os.path.exists(rutaXML):os.remove(rutaXML) 
    else:
        print('The input file does not exist.')
        sys.exit()
        
def imprimirResultadoKf1(rutaArchivo = None):
    if os.path.exists(rutaArchivo):
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
            print(p.getEnergyPerformannceKf1())
        else:
            print('Please, define the input file --> -i <inputfile>')
        if os.path.exists(rutaXML):os.remove(rutaXML) 
    else:
        print('The input file does not exist')
        sys.exit()
        
def imprimirResultadoKf2(rutaArchivo = None):
    if os.path.exists(rutaArchivo):
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
            print(p.getResponseToUserNeedsKf2())
        else:
            print('Please, define the input file --> -i <inputfile>')
        if os.path.exists(rutaXML):os.remove(rutaXML) 
    else:
        print('The input file does not exist')
        sys.exit()
        
def imprimirResultadoKf3(rutaArchivo = None):
    if os.path.exists(rutaArchivo):
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
            print(p.getEnergyFlexibilityKf3())
        else:
            print('Please, define the input file --> -i <inputfile>')
        if os.path.exists(rutaXML):os.remove(rutaXML) 
    else:
        print('The input file does not exist')
        sys.exit()
        
def escribirXML(rutaArchivoOriginal, rutaArchivoNuevo):
    if os.path.exists(rutaArchivoOriginal):
        if rutaArchivoOriginal == rutaArchivoNuevo:
            print('Error: Both files should be the same')
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
                if resultados == None:
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
                else:
                    totalSri = root.find('.//d:TotalSriScore', ns)
                    totalSri.text = str(p.getTotalSRI())
                    
                    totalScoreKf1 = root.find('.//d:ScoreKF1', ns)
                    totalScoreKf1.text = str(p.getEnergyPerformannceKf1())
                    
                    totalScoreKf2 = root.find('.//d:ScoreKF2', ns)
                    totalScoreKf2.text = str(p.getResponseToUserNeedsKf2())
                    
                    totalScoreKf3 = root.find('.//d:ScoreKF3', ns)
                    totalScoreKf3.text = str(p.getEnergyFlexibilityKf3())
                    
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
            rutaGbXML, newFileGbXML = os.path.split(rutagbXML)
            arrayGbXML = newFileGbXML.split('.')
            arrayGbXML[0] = '{}-outputfile'.format(arrayGbXML[0])
            newFileGbXML = '.'.join(arrayGbXML)  
            nuevaRutaGbXML = os.path.join(rutaGbXML, newFileGbXML)
            treeGbXML.write(nuevaRutaGbXML)
            
            # Creamos el nuevo zip
            exportarZip(rutaArchivoNuevo, nuevaRutaXML, nuevaRutaGbXML)
            #Eliminamos todos los archivos temporales
            if os.path.exists(rutaXML):os.remove(rutaXML)
            if os.path.exists(rutagbXML):os.remove(rutagbXML)
            if os.path.exists(nuevaRutaXML):os.remove(nuevaRutaXML)
            if os.path.exists(nuevaRutaGbXML):os.remove(nuevaRutaGbXML)
        else:
            print('Error: The out file is required')
    else:
        print('Error: output file does not exist')
        sys.exit()
def extraerArchivos(ficheroDescomprimir, rutaDestinoExtraer = None):
    if os.path.exists(ficheroDescomprimir):
        if rutaDestinoExtraer  and os.path.exists(rutaDestinoExtraer):
            if os.path.isfile(rutaDestinoExtraer):
                print('Error: Output file already exists')
                sys.exit()
            else:
                rutaXML, rutagbXML = descomprimirZIP(ficheroDescomprimir, rutaDestinoExtraer)
                print('XML has been extracted in {}'.format(rutaXML))
                print('gbXML has been extracted in {}'.format(rutagbXML))
        else:
            print('Destination folder is not defined or does not exists.')
            print('Extracting')
            rutaXML, rutagbXML = descomprimirZIP(ficheroDescomprimir, extraer=True)
            print('XML has been extracted in {}'.format(rutaXML))
            print('gbXML has been extracted in {}'.format(rutagbXML))
    else:
        print('Extracting folder does not exists')
    # xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")
    # with open(rutaArchivoNuevo, "w") as f:
    #     f.write(xmlstr) 
if __name__ == '__main__':
    # importarSriStandAlone(r'C:\Temp\427.iEPB')  
    # imprimirTodosResultadosSri(r'C:\Temp\427.iEPB')
    # escribirXML(r'C:\Temp\427.iEPB', r'C:\Temp\427-output.iEPB')
    extraerArchivos(r'C:\Temp\427.iEPB', r'C:\Temp\427.iEPB')
    