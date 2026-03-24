'''
Created on 19 mar 2024

@author: Efinovatic
'''

import sys
# Para todo, excepto para escrbir archivos
import xml.etree.ElementTree as ET
from xml.dom import minidom

from lxml import etree as lxml_ET       # Solo para escribir archivos

from modulos.models import Proyecto
from modulos.__init__ import __version__
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
    # Obtener carpetas y nombres de archivos
    rutaXMLTemporal, ficheroXML = os.path.split(rutaXML)
    rutaGBXMLTemporal, ficheroGBXML = os.path.split(rutaGBXML)

    # Revisar y renombrar el XML si es necesario
    if "_iEPB" not in ficheroXML:
        nombre, ext = os.path.splitext(ficheroXML)
        nuevoNombreXML = f"{nombre}_iEPB{ext}"
        nuevaRutaXML = os.path.join(rutaXMLTemporal, nuevoNombreXML)
        os.rename(rutaXML, nuevaRutaXML)
        print(f"Archivo XML renombrado a: {nuevoNombreXML}")
        rutaXML = nuevaRutaXML
        ficheroXML = nuevoNombreXML

    # Revisar y renombrar el GBXML si es necesario
    if "_gbXML" not in ficheroGBXML:
        nombre, ext = os.path.splitext(ficheroGBXML)
        nuevoNombreGBXML = f"{nombre}_gbXML{ext}"
        nuevaRutaGBXML = os.path.join(rutaGBXMLTemporal, nuevoNombreGBXML)
        os.rename(rutaGBXML, nuevaRutaGBXML)
        print(f"Archivo GBXML renombrado a: {nuevoNombreGBXML}")
        rutaGBXML = nuevaRutaGBXML
        ficheroGBXML = nuevoNombreGBXML

    # Generar la ruta del ZIP si no se proporciona
    if not rutaZip:
        nombreFichero = os.path.splitext(ficheroXML)[0]
        rutaZip = os.path.join(rutaXMLTemporal, f'{nombreFichero}.iEPB')

    # Crear el archivo ZIP
    with zipfile.ZipFile(rutaZip, 'w') as zip_object:
        zip_object.write(rutaXML, arcname=ficheroXML)
        zip_object.write(rutaGBXML, arcname=ficheroGBXML)

    # Confirmar creación del ZIP
    if os.path.exists(rutaZip):
        print('New iEPB file created')
    else:
        print('Problem creating the new iEPB file')
    
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
        if '_gbXML' not in names and names.endswith('.xml'):
            rutaXML = os.path.join(rutaGuardar,names)
        else:
            rutagbXML = os.path.join(rutaGuardar,names)
    zip_file.close()
    return rutaXML, rutagbXML

def importarSriStandAlone(nombreArchivo, empaquetar = False):
    if os.path.exists(nombreArchivo):
        rutaXML, rutagbXML = descomprimirZIP(nombreArchivo)

        # 1. Parsear iEPB.xml (SRI + YearOfConstruction)
        tree = ET.parse(rutaXML)
        root = tree.getroot()
        ns = {'d':"http://www.efinovatic.es/sri"}

        # 2. Parsear gbXML (datos del edificio)
        gbxml_root = None
        ns_gbxml = {'gb': "http://www.gbxml.org/schema"}
        if rutagbXML and os.path.exists(rutagbXML):
            try:
                gbxml_tree = ET.parse(rutagbXML)
                gbxml_root = gbxml_tree.getroot()
            except Exception as e:
                print(f"Warning: Could not parse gbXML file: {e}")

        for projectElement in root.findall('.//d:Project',ns):
            p=Proyecto.creaDesdeXML(projectElement)

            # ==========================================
            # DATOS FUERA DE <Project> - iEPB.xml
            # ==========================================
            
            # 1. YearOfConstruction (en <Building>)
            building_id = projectElement.get('buildingIdRef')  # Obtener el buildingIdRef del Project
            if building_id:
                building_xpath = f'.//d:Building[@id="{building_id}"]'
                building_element = root.find(building_xpath, ns)
                if building_element is not None:
                    year_element = building_element.find('d:YearOfConstruction', ns)
                    if year_element is not None and year_element.text:
                        p.yearOfConstruction = float(year_element.text)
            
            # 2. EnergyClass (en <EPC><Results>)
            # Namespace adicional para DatosEnergeticosDelEdificio
            ns_epc = {'epc': "http://www.efinovatic.es/datosEnergeticosDelEdificio"}
            try:
                energy_class_elem = root.find('.//epc:EnergiaPrimariaNoRenovable/epc:Global', ns_epc)
                if energy_class_elem is not None and energy_class_elem.text:
                    p.energyClass = energy_class_elem.text
            except Exception as e:
                print(f"Warning: Could not extract energy class: {e}")
            
            # 3. Results (ahora en <SRI><Results>, fuera de <Project>)
            results_element = root.find('.//d:Results', ns)
            if results_element is not None:
                try:
                    total_sri = results_element.find('.//d:TotalSriScore', ns)
                    if total_sri is not None and total_sri.text:
                        p.totalSriScore = float(total_sri.text)
                    
                    kf1 = results_element.find('.//d:ScoreKF1', ns)
                    if kf1 is not None and kf1.text:
                        p.scoreKF1 = float(kf1.text)
                    
                    kf2 = results_element.find('.//d:ScoreKF2', ns)
                    if kf2 is not None and kf2.text:
                        p.scoreKF2 = float(kf2.text)
                    
                    kf3 = results_element.find('.//d:ScoreKF3', ns)
                    if kf3 is not None and kf3.text:
                        p.scoreKF3 = float(kf3.text)
                except Exception as e:
                    print(f"Warning: Could not extract results: {e}")
            
            # ==========================================
            # DATOS DEL gbXML
            # ==========================================

            # Obtener información del edificio del gbXML
            if gbxml_root is not None:
                try:
                    building = gbxml_root.find('.//gb:Building', ns_gbxml)
                    if building is not None:
                        # Name
                        name_elem = building.find('gb:Name', ns_gbxml)
                        if name_elem is not None and name_elem.text:
                            p.name = name_elem.text
                        
                        # Address
                        address_elem = building.find('gb:StreetAddress', ns_gbxml)
                        if address_elem is not None and address_elem.text:
                            p.address = address_elem.text
                        
                        # Area
                        area_elem = building.find('gb:Area', ns_gbxml)
                        if area_elem is not None and area_elem.text:
                            p.netFloorAreaOfTheBuilding = float(area_elem.text)
                        
                        # Description
                        desc_elem = building.find('gb:Description', ns_gbxml)
                        if desc_elem is not None and desc_elem.text:
                            p.descriptionOfBuilding = desc_elem.text
                except Exception as e:
                    print(f"Warning: Could not extract gbXML data: {e}")
            # print(p.getTotalSRI())
            # print(p.sri())
            listaProyectosAlmacenado.append(p)
        if os.path.exists(rutaXML):os.remove(rutaXML)
    else:
        print('The file does not exist.')
        if not empaquetar:
            sys.exit()
    
def imprimirTodosResultadosSri(rutaArchivo = None):
    if os.path.exists(rutaArchivo):
        rutaXML, rutagbXML = descomprimirZIP(rutaArchivo)
        tree = ET.parse(rutaXML)
        root = tree.getroot()
        ns = {'d':"http://www.efinovatic.es/sri"}
        project = root.find('.//d:Project', ns)
        # Extraer ID desde buildingIdRef
        building_id_ref = project.attrib['buildingIdRef']  # "Building_12"
        project_id = int(building_id_ref.split('_')[-1])  # 12

        # p = Proyecto.objects.get(id = int(project.attrib['id']))
        p = None
        for instanciaProyecto in listaProyectosAlmacenado:
            if instanciaProyecto.id == project_id:
                p = instanciaProyecto
                break
        if p:
            print('Total SRI: {}'.format(p.getTotalSRI()))
            print('Energy Perfomance (Kf1): {}'.format(p.getEnergyPerformannceKf1()))
            print('Response To User Needs (Kf2): {}'.format(p.getResponseToUserNeedsKf2()))
            print('Energy Flexibility (Kf3): {}'.format(p.getEnergyFlexibilityKf3()))
        else:
            print('Please, define the input file --> -i <inputfile>')
        if os.path.exists(rutaXML):os.remove(rutaXML)
        if os.path.exists(rutagbXML):os.remove(rutagbXML)  
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
        # Extraer ID desde buildingIdRef
        building_id_ref = project.attrib['buildingIdRef']  # "Building_12"
        project_id = int(building_id_ref.split('_')[-1])  # 12


        # p = Proyecto.objects.get(id = int(project.attrib['id']))
        p = None
        for instanciaProyecto in listaProyectosAlmacenado:
            if instanciaProyecto.id == project_id:
                p = instanciaProyecto
                break
        if p:
            print(p.getTotalSRI())
        else:
            print('Please, define the input file --> -i <inputfile>')
        if os.path.exists(rutaXML):os.remove(rutaXML)
        if os.path.exists(rutagbXML):os.remove(rutagbXML)
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
        # Extraer ID desde buildingIdRef
        building_id_ref = project.attrib['buildingIdRef']  # "Building_12"
        project_id = int(building_id_ref.split('_')[-1])  # 12

        # p = Proyecto.objects.get(id = int(project.attrib['id']))
        p = None
        for instanciaProyecto in listaProyectosAlmacenado:
            if instanciaProyecto.id == project_id:
                p = instanciaProyecto
                break
        if p:
            print(p.getEnergyPerformannceKf1())
        else:
            print('Please, define the input file --> -i <inputfile>')
        if os.path.exists(rutaXML):os.remove(rutaXML)
        if os.path.exists(rutagbXML):os.remove(rutagbXML)
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
        # Extraer ID desde buildingIdRef
        building_id_ref = project.attrib['buildingIdRef']  # "Building_12"
        project_id = int(building_id_ref.split('_')[-1])  # 12

        # p = Proyecto.objects.get(id = int(project.attrib['id']))
        p = None
        for instanciaProyecto in listaProyectosAlmacenado:
            if instanciaProyecto.id == project_id:
                p = instanciaProyecto
                break
        if p:
            print(p.getResponseToUserNeedsKf2())
        else:
            print('Please, define the input file --> -i <inputfile>')
        if os.path.exists(rutaXML):os.remove(rutaXML)
        if os.path.exists(rutagbXML):os.remove(rutagbXML) 
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
        # Extraer ID desde buildingIdRef
        building_id_ref = project.attrib['buildingIdRef']  # "Building_12"
        project_id = int(building_id_ref.split('_')[-1])  # 12

        # p = Proyecto.objects.get(id = int(project.attrib['id']))
        p = None
        for instanciaProyecto in listaProyectosAlmacenado:
            if instanciaProyecto.id == project_id:
                p = instanciaProyecto
                break
        if p:
            print(p.getEnergyFlexibilityKf3())
        else:
            print('Please, define the input file --> -i <inputfile>')
        if os.path.exists(rutaXML):os.remove(rutaXML)
        if os.path.exists(rutagbXML):os.remove(rutagbXML) 
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
            
            # Parsear con lxml
            tree = lxml_ET.parse(rutaXML)
            root = tree.getroot()
            
            ns = {'d': "http://www.efinovatic.es/sri"}
            project = root.find('.//d:Project', ns)
            
            # Extraer ID desde buildingIdRef
            building_id_ref = project.attrib['buildingIdRef']
            project_id = int(building_id_ref.split('_')[-1])
            
            p = None
            for instanciaProyecto in listaProyectosAlmacenado:
                if instanciaProyecto.id == project_id:
                    p = instanciaProyecto
                    break
                    
            if p:
                # Buscar Results FUERA de <Project>, en <SRI><Results>
                sri_element = root.find('.//d:SRI', ns)
                if sri_element is None:
                    print("Error: No se encontró el elemento <SRI>")
                    sys.exit()
                
                resultados = sri_element.find('.//d:Results', ns)
                
                if resultados is None:
                    # Crear Results si no existe
                    results = lxml_ET.SubElement(sri_element, 'Results')
                    totalSriScore = lxml_ET.SubElement(results, "TotalSriScore")
                    totalSriScore.text = str(p.getTotalSRI())
                    scoreKF1 = lxml_ET.SubElement(results, "ScoreKF1")
                    scoreKF1.text = str(p.getEnergyPerformannceKf1())
                    scoreKF2 = lxml_ET.SubElement(results, "ScoreKF2")
                    scoreKF2.text = str(p.getResponseToUserNeedsKf2())
                    scoreKF3 = lxml_ET.SubElement(results, "ScoreKF3")
                    scoreKF3.text = str(p.getEnergyFlexibilityKf3())
                else:
                    # Actualizar Results existente
                    totalSri = resultados.find('.//d:TotalSriScore', ns)
                    if totalSri is not None:
                        totalSri.text = str(p.getTotalSRI())
                    else:
                        totalSri = lxml_ET.SubElement(resultados, "TotalSriScore")
                        totalSri.text = str(p.getTotalSRI())
                    
                    totalScoreKf1 = resultados.find('.//d:ScoreKF1', ns)
                    if totalScoreKf1 is not None:
                        totalScoreKf1.text = str(p.getEnergyPerformannceKf1())
                    else:
                        totalScoreKf1 = lxml_ET.SubElement(resultados, "ScoreKF1")
                        totalScoreKf1.text = str(p.getEnergyPerformannceKf1())
                    
                    totalScoreKf2 = resultados.find('.//d:ScoreKF2', ns)
                    if totalScoreKf2 is not None:
                        totalScoreKf2.text = str(p.getResponseToUserNeedsKf2())
                    else:
                        totalScoreKf2 = lxml_ET.SubElement(resultados, "ScoreKF2")
                        totalScoreKf2.text = str(p.getResponseToUserNeedsKf2())
                    
                    totalScoreKf3 = resultados.find('.//d:ScoreKF3', ns)
                    if totalScoreKf3 is not None:
                        totalScoreKf3.text = str(p.getEnergyFlexibilityKf3())
                    else:
                        totalScoreKf3 = lxml_ET.SubElement(resultados, "ScoreKF3")
                        totalScoreKf3.text = str(p.getEnergyFlexibilityKf3())
            
            # Crear nombre del archivo de salida para iEPB.xml
            ruta, newFileXML = os.path.split(rutaXML)
            arrayXML = newFileXML.split('.')
            arrayXML[0] = '{}-outputfile'.format(arrayXML[0])
            newFileXML = '.'.join(arrayXML)
            nuevaRutaXML = os.path.join(ruta, newFileXML)
            
            # Escribir con lxml (preserva todo automáticamente)
            tree.write(
                nuevaRutaXML,
                encoding='utf-8',
                xml_declaration=True,
                pretty_print=True
            )
            
            # Grabamos el archivo gbXML
            treeGbXML = lxml_ET.parse(rutagbXML)
            
            rutaGbXML, newFileGbXML = os.path.split(rutagbXML)
            arrayGbXML = newFileGbXML.split('.')
            arrayGbXML[0] = '{}-outputfile'.format(arrayGbXML[0])
            newFileGbXML = '.'.join(arrayGbXML)
            nuevaRutaGbXML = os.path.join(rutaGbXML, newFileGbXML)
            
            treeGbXML.write(
                nuevaRutaGbXML,
                encoding='utf-8',
                xml_declaration=True,
                pretty_print=True
            )
            
            # Comprobamos que existe la ruta del archivo nuevo, si no la creamos
            nuevaRuta, nuevoArchivo = os.path.split(rutaArchivoNuevo)
            if nuevaRuta and not os.path.exists(nuevaRuta):
                os.makedirs(nuevaRuta)
            
            # Creamos el nuevo zip
            exportarZip(rutaArchivoNuevo, nuevaRutaXML, nuevaRutaGbXML)
            
            # Eliminamos todos los archivos temporales
            if os.path.exists(rutaXML):
                os.remove(rutaXML)
            if os.path.exists(rutagbXML):
                os.remove(rutagbXML)
            if os.path.exists(nuevaRutaXML):
                os.remove(nuevaRutaXML)
            if os.path.exists(nuevaRutaGbXML):
                os.remove(nuevaRutaGbXML)
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
    
def empaquetarArchivos(ficheroXMLComprimir, ficheroGBXMLComprimir, rutaDestinoGuardar = None):
    if os.path.exists(ficheroXMLComprimir) and os.path.exists(ficheroGBXMLComprimir):
        exportarZip(rutaDestinoGuardar, ficheroXMLComprimir, ficheroGBXMLComprimir)
    else:
        print('Error alguna ruta de los ficheros a comprimir no existe')
        
def imprimirVersion():
    print(__version__)
     
if __name__ == '__main__':
    # importarSriStandAlone(r'C:\Temp\427.iEPB')  
    # imprimirTodosResultadosSri(r'C:\Temp\427.iEPB')
    # escribirXML(r'C:\Temp\427.iEPB', r'C:\Temp\90-output.iEPB')
    # extraerArchivos(r'C:\Temp\427.iEPB', r'C:\Temp')
    empaquetarArchivos(r'C:\Temp\427.xml', r'C:\Temp\427_gbXML.xml', r'C:\Temp\Prueba.iEPB')
    # imprimirVersion()
    