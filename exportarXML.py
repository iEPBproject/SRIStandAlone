# -\*- coding: utf-8 -\*-
'''
Created on 14/03/2016

@author: mapascual
'''


import getpass
from io import StringIO
import os
import sys

import django

from models import Proyecto


import xml.etree.ElementTree as et
from xml.dom import minidom

nombreUsuario = getpass.getuser()


e=et.Element('SRI2MARKET')




sys.path.append(r'C:\Users\{0}\workspace\SRI2Market'.format(nombreUsuario))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SRI2Market.settings')

django.setup()
from sri.models import *



def getRoot():
    root=et.Element('gbXML',attrib={'xmlns':"http://www.gbxml.org/schema",
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
    


if __name__ == '__main__':
    root = getRoot()
    iEPBxml=et.SubElement(root,'iEPBxml',attrib={"version": "0.1"})  
    sri2MarketElement=et.SubElement(iEPBxml,'SRI2MARKET',attrib={"version": "0.1"})
    projectsElement = et.SubElement(sri2MarketElement, 'Projects')
      
    proyecto = Proyecto.objects.first()
    projectElement = et.SubElement(projectsElement, 'Project',attrib={"id": str(proyecto.id)})
    name = et.SubElement(projectElement, "name")
    name.text = str(proyecto.name)
    
    # Añadimos elemento country a proyecto
    
    country = proyecto.country
    countryElement = et.SubElement(projectElement, 'country', attrib = {"id": str(country.id)})
    
    # Añadimos los elementos al elemento country
    
    nameCountryElement = et.SubElement(countryElement, 'name')
    nameCountryElement.text = str(country.name)
    heatingMandatoryElement = et.SubElement(countryElement, 'heatingMandatory')
    heatingMandatoryElement.text = str(country.heatingMandatory)  
    dhwMandatoryForResidentialElement = et.SubElement(countryElement, 'dhwMandatoryForResidential')
    dhwMandatoryForResidentialElement.text = str(country.dhwMandatoryForResidential)  
    dhwMandatoryForTertiaryElement = et.SubElement(countryElement, 'dhwMandatoryForTertiary')
    dhwMandatoryForTertiaryElement.text = str(country.dhwMandatoryForTertiary)  
    CoolingMandatoryElement = et.SubElement(countryElement, 'CoolingMandatory')
    CoolingMandatoryElement.text = str(country.CoolingMandatory)  
    VentilationMandatoryElement = et.SubElement(countryElement, 'VentilationMandatory')
    VentilationMandatoryElement.text = str(country.VentilationMandatory)
    LightingMandatoryElement = et.SubElement(countryElement, 'LightingMandatory')
    LightingMandatoryElement.text = str(country.LightingMandatory)  
    DynamicBuildingEnvelopeMandatoryElement = et.SubElement(countryElement, 'DynamicBuildingEnvelopeMandatory')
    DynamicBuildingEnvelopeMandatoryElement.text = str(country.DynamicBuildingEnvelopeMandatory)  
    ElectricityMandatoryElement = et.SubElement(countryElement, 'ElectricityMandatory')
    ElectricityMandatoryElement.text = str(country.ElectricityMandatory)  
    ElectricVehicleChargingMandatoryElement = et.SubElement(countryElement, 'ElectricVehicleChargingMandatory')
    ElectricVehicleChargingMandatoryElement.text = str(country.ElectricVehicleChargingMandatory)  
    MonitoringAndControlMandatoryElement = et.SubElement(countryElement, 'MonitoringAndControlMandatory')
    MonitoringAndControlMandatoryElement.text = str(country.MonitoringAndControlMandatory)  
    domainClassNamesElement = et.SubElement(countryElement, 'domainClassNames')
    domainClassNamesElement.text = str(country.domainClassNames)  
    allowUserDefineDomainWeightingsElement = et.SubElement(countryElement, 'allowUserDefineDomainWeightings')
    allowUserDefineDomainWeightingsElement.text = str(country.allowUserDefineDomainWeightings)    
           

    user__id = et.SubElement(projectElement, "user__id")
    user__id.text = str(proyecto.user.id)   

    user__username = et.SubElement(projectElement, "user__name")
    user__username.text = str(proyecto.user.username)         
    
    # country__id = et.SubElement(projectElement, "country__id")
    # country__id.text = str(proyecto.country.id)        
    #
    # country__name = et.SubElement(projectElement, "country__name")
    # country__name.text = str(proyecto.country.name)  
    
    # Añadimos elemento buildingType a proyecto
    
    buildingType = proyecto.buildingType
    
    buildingTypeElement = et.SubElement(projectElement, 'BuildingType', attrib= {"id" : str(buildingType.id)})
    descripcionElement = et.SubElement(buildingTypeElement, 'descripcion')
    descripcionElement.text = str(buildingType.description)
  
    
    domainWeigthing = proyecto.domainWeigthing if not proyecto.customDomain else proyecto.customDomainWeigthings
    elementDomainWeigthing = et.SubElement(projectElement, 'DomainWeigthing',attrib={"id": str(domainWeigthing.id)})
    name = et.SubElement(elementDomainWeigthing, "name")
    name.text = str(domainWeigthing.name)     
    
    domains =['Heating','Cooling','Dhw','Ventilation','Lighting','Electricity','DynamicBuildingEnvelope','ElectricVehicleCharging','MonitoringAndControl']
    impacts = ['energyEfficiency','energyFlexibility','comfort','convenience','healthAccesibility','maintenanceFaultPrediction','informationOccupants']
    
    for domain in domains:
            element = et.SubElement(elementDomainWeigthing, domain)
            for impact in impacts:
                impactValue = et.SubElement(element, impact)
                impactValue.text = str(getattr(domainWeigthing,impact+domain))                     
                
        
    
    impactWeighting = domainWeigthing.impactWeighting
    elementImpactWeighting = et.SubElement(elementDomainWeigthing, 'ImpactWeighting',attrib={"id": str(impactWeighting.id)})
    impacts2 = impacts + ['kF1_energyPerformanceAndOperation','kF2_responseToUserNeeds','kF3_energyFlexibility']
    for impact in impacts2:
        impactValue = et.SubElement(elementImpactWeighting, impact)
        impactValue.text = str(getattr(impactWeighting,impact))          
    
    
    
    
    
    
    catalogo = proyecto.catalogo
    elementCatalogo = et.SubElement(projectElement, 'Catalogue',attrib={"id": str(catalogo.id)})
    description = et.SubElement(elementCatalogo, "description")
    description.text = catalogo.description
    
    domains = et.SubElement(elementCatalogo, 'Domains')
    for domain in catalogo.dominios.all():
        elementDomain = et.SubElement(domains, 'Domain',attrib={"id": str(domain.id)})
        description = et.SubElement(elementDomain, "description")
        description.text = domain.description    
        nameAttribute = et.SubElement(elementDomain, 'nameAttr')
        nameAttribute.text = domain.nameAttr
        services = et.SubElement(elementDomain, 'Services')
        for service in domain.servicios.all():
            elementService = et.SubElement(services, 'Service',attrib={"id": str(service.id)})
            description = et.SubElement(elementService, "description")
            description.text = str(service.description)                     
            
            functionalities = et.SubElement(elementService, 'Functionalities')  
            for functionality in service.funcionalidades.all():
                elementFunctionality = et.SubElement(functionalities, 'Functionality',attrib={"id": str(functionality.id)})
                description = et.SubElement(elementFunctionality, "description")
                description.text = str(functionality.description)         
                energyEfficiencyImpact = et.SubElement(elementFunctionality, "energyEfficiencyImpact")
                energyEfficiencyImpact.text = str(functionality.energyEfficiencyImpact)  
                energyFlexibilityImpact = et.SubElement(elementFunctionality, "energyFlexibilityImpact")
                energyFlexibilityImpact.text = str(functionality.energyFlexibilityImpact)    
                comfortImpact = et.SubElement(elementFunctionality, "comfortImpact")
                comfortImpact.text = str(functionality.comfortImpact)           
                convenienceImpact = et.SubElement(elementFunctionality, "convenienceImpact")
                convenienceImpact.text = str(functionality.convenienceImpact)     
                healthAccesibilityImpact = et.SubElement(elementFunctionality, "healthAccesibilityImpact")
                healthAccesibilityImpact.text = str(functionality.healthAccesibilityImpact)      
                maintenanceFaultPredictionImpact = et.SubElement(elementFunctionality, "maintenanceFaultPredictionImpact")
                maintenanceFaultPredictionImpact.text = str(functionality.maintenanceFaultPredictionImpact)       
                informationOccupantsImpact = et.SubElement(elementFunctionality, "informationOccupantsImpact")
                informationOccupantsImpact.text = str(functionality.informationOccupantsImpact)   
                en15232Residential = et.SubElement(elementFunctionality, "en15232Residential")
                en15232Residential.text = str(functionality.en15232Residential)  
                en15232NonResidential = et.SubElement(elementFunctionality, "en15232NonResidential")
                en15232NonResidential.text = str(functionality.en15232NonResidential)                                                                                                                           
                                                       

    
    assessableDomains = et.SubElement(projectElement, 'assessableDomains')  
    Heating = et.SubElement(assessableDomains, "Heating")
    Heating.text = str(proyecto.Heating)     
    Dhw = et.SubElement(assessableDomains, "Dhw")
    Dhw.text = str(proyecto.Dhw)         
    Cooling = et.SubElement(assessableDomains, "Cooling")
    Cooling.text = str(proyecto.Cooling)        
    Ventilation = et.SubElement(assessableDomains, "Ventilation")
    Ventilation.text = str(proyecto.Ventilation)         
    Lighting = et.SubElement(assessableDomains, "Lighting")
    Lighting.text = str(proyecto.Lighting)       
    DynamicBuildingEnvelope = et.SubElement(assessableDomains, "DynamicBuildingEnvelope")
    DynamicBuildingEnvelope.text = str(proyecto.DynamicBuildingEnvelope)     
    Electricity = et.SubElement(assessableDomains, "Electricity")
    Electricity.text = str(proyecto.Electricity)           
    ElectricVehicleCharging = et.SubElement(assessableDomains, "ElectricVehicleCharging")
    ElectricVehicleCharging.text = str(proyecto.ElectricVehicleCharging)         
    MonitoringAndControl = et.SubElement(assessableDomains, "MonitoringAndControl")
    MonitoringAndControl.text = str(proyecto.MonitoringAndControl)              

    
    
    
    data = et.SubElement(projectElement, 'data')    
    for dato in proyecto.datos.all():
        elementDato = et.SubElement(data, 'datum',attrib={"id": str(dato.id)})      
        chosenFuncionality = et.SubElement(elementDato, "chosenFuncionality")
        chosenFuncionality.text = str(dato.chosenFuncionality.id)                    
        
        comments = et.SubElement(elementDato, "comments")
        comments.text = str(dato.comments)      
        
        justification = et.SubElement(elementDato, "justification")
        justification.text = str(dato.justification)     
        
        percentage = et.SubElement(elementDato, "percentage")
        percentage.text = str(dato.percentage)             
    
    
    
    results = et.SubElement(projectElement, 'results') 
    totalSriScore = et.SubElement(results, "totalSriScore")
    totalSriScore.text = str(proyecto.totalSriScore)      
    scoreKF1 = et.SubElement(results, "scoreKF1")
    scoreKF1.text = str(proyecto.scoreKF1)     
    scoreKF2 = et.SubElement(results, "scoreKF2")
    scoreKF2.text = str(proyecto.scoreKF2)
    scoreKF3 = et.SubElement(results, "scoreKF3")
    scoreKF3.text = str(proyecto.scoreKF3)               
    
        
    
    xmlstr = minidom.parseString(et.tostring(root)).toprettyxml(indent="   ")
    with open(r'c:\temp\test.iEPBXML', "w") as f:
        f.write(xmlstr) 
        
    print("Fin")