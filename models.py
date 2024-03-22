# # -\*- coding: utf-8 -\*-
import copy

# from ckeditor_uploader.widgets import CKEditorUploadingWidget
# from django import forms
# from django.contrib.auth.models import User
# from django.core.validators import MaxValueValidator, MinValueValidator
from tabulate import tabulate

import pandas as pd
from miDjangoModel3.models import ChoiceField, Model, CharField, FloatField, BooleanField, ForeignKey, Manager

class User(Model):
    
    objects = Manager()
    
    name = CharField(default = '',
                     max_length = 1000,
                     verbose_name = "User-Name")
                     
    email = CharField(default = '',
                      max_length = 1000,
                      verbose_name = 'User e-mail address')
                      
    @classmethod    
    def creaDesdeXML(cls, element):
        ns = {'d':"http://www.gbxml.org/schema"}
        nuevaInstancia = cls()
        nuevaInstancia.id = element.find('.//d:user__id', ns).text
        nuevaInstancia.name = element.find('.//d:user__name', ns).text
        return nuevaInstancia

class BuildingType(Model):
    objects = Manager()
    description = CharField(default = '',
                            max_length = 100,
                            verbose_name = 'Description')
                            
    def __str__(self):
        ''' 
        Clase BuildindgType
        '''
        
        return f"{self.description}"
        
    class Meta:
        verbose_name = 'Buiding Type'
        verbose_name_plural = '11. Buiding Type'

class Country(Model):
    
    objects = Manager()
    
    name = CharField(default = '',
                       max_length = 1000,
                       verbose_name = "Name")
    
    heatingMandatory = BooleanField(default = True, verbose_name = "Mandatory Heating Domain")
    dhwMandatoryForResidential = BooleanField(default = True, verbose_name = "Mandatory DWH for residential Domain")
    dhwMandatoryForTertiary = BooleanField(default = True, verbose_name = "Mandatory DWH for tertiary Domain")
    CoolingMandatory = BooleanField(default = True, verbose_name = "Mandatory Cooling Domain")
    VentilationMandatory = BooleanField(default = True, verbose_name = "Mandatory Ventilation Domain")
    LightingMandatory = BooleanField(default = True, verbose_name = "Mandatory Lighting Domain")
    DynamicBuildingEnvelopeMandatory = BooleanField(default = True, verbose_name = "Mandatory Dynamic Building Envelope Domain")
    ElectricityMandatory = BooleanField(default = True, verbose_name = "Mandatory Electricity Domain")
    ElectricVehicleChargingMandatory = BooleanField(default = True, verbose_name = "Mandatory Electric Vehicle Charging Domain")
    MonitoringAndControlMandatory = BooleanField(default = True, verbose_name = "Mandatory Monitoring And Control Domain")    
    
    domainClassNames = CharField(default = 'A,B,C,D,E,F,G',
                                                        max_length = 1000,
                                                        verbose_name = "Class names list (separated by comma) with 7 class names")
    
    
    allowUserDefineDomainWeightings = BooleanField(default = False, verbose_name = "Allow user defined domain weightings", )

    def __str__(self):
        ''' 
        Clase Country
        
        '''
        return 'Id: {} - {} '.format(self.id, self.name)

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = '6. Country'
        ordering = ('id',)
    @classmethod    
    def creaDesdeXML(cls, element):
        ns = {'d':"http://www.gbxml.org/schema"}
        nuevaInstancia = cls()
        nuevaInstancia.id = element.find('.//d:country__id', ns).text
        nuevaInstancia.name = element.find('.//d:country__name', ns).text
        return nuevaInstancia
        

class Catalogo(Model):
    
    objects = Manager()
    
    description = CharField(default = '',
                            max_length = 1000,
                            verbose_name = "Description")
    
    country = ForeignKey(Country,
                         verbose_name = 'Country',
                         related_name = 'catalogos',)
                                     
    buildingType = ForeignKey(BuildingType,
                              verbose_name = 'Building Types',
                              related_name = 'catalogos',)
                  
    class Meta:
        verbose_name = 'Catalogue'
        verbose_name_plural = '1.Catalogue'
        ordering = ('id',)

    def __str__(self):
        ''' 
        Clase Catalogo
        
        '''
        return str(self.description)

    @property
    def tieneDatos(self):
        return True
    
    def delete(self, using=None, keep_parents=False):
        if self.tieneDatos:
            return False
        return Model.delete(self, using=using, keep_parents=keep_parents)
    def duplicar(self, padre = None): 
        ''' 
        Clase Catalogo
        
        '''         
        copyId = copy.deepcopy(self.id) 
        
        if hasattr(self, 'description'):
            self.description = self.description + ' copy'
        
        listadoDominios = Dominio.objects.filter(catalogo_id = copyId)
        
        self.id = None
        self.pk = None
        
        if (padre != None) :
            self.proyectos = padre
        self.save()
        for dominio in listadoDominios:
            dominio.duplicar(padre = self)
        
        return self
    
#     def getImpactMaxEnergyEfficiency(self, proyecto = None):
#         '''
#         Clase Catalogo
#         Cuando es no aplicable no se tiene en cuenta sus valores maximos
#         '''
#         if proyecto:
#             return sum([dominio.getImpactMaxEnergyEfficiency(proyecto = proyecto) for dominio in self.dominios.all()])
#         else:
#             return self.impactMaxEnergyEfficiency
#     
#     def getImpactMaxEnergyFlexibility(self, proyecto = None):
#         '''
#         Clase Catalogo
#         Cuando es no aplicable no se tiene en cuenta sus valores maximos
#         '''
#         if proyecto:
#             return sum([dominio.getImpactMaxEnergyFlexibility(proyecto = proyecto) for dominio in self.dominios.all()])
#         else:
#             return self.impactMaxEnergyFlexibility
#         
#     def getImpactMaxComfort(self, proyecto = None):
#         '''
#         Clase Catalogo
#         Cuando es no aplicable no se tiene en cuenta sus valores maximos
#         '''
#         if proyecto:
#             return sum([dominio.getImpactMaxComfort(proyecto = proyecto) for dominio in self.dominios.all()])
#         else:
#             return self.impactMaxComfort
#         
#     def getImpactMaxConvenience(self, proyecto = None):
#         '''
#         Clase Catalogo
#         Cuando es no aplicable no se tiene en cuenta sus valores maximos
#         '''
#         if proyecto:
#             return sum([dominio.getImpactMaxConvenience(proyecto = proyecto) for dominio in self.dominios.all()])
#         else:
#             return self.impactMaxConvenience
#         
#     def getImpactMaxHealthAccesibility(self, proyecto = None):
#         '''
#         Clase Catalogo
#         Cuando es no aplicable no se tiene en cuenta sus valores maximos
#         '''
#         if proyecto:
#             return sum([dominio.getImpactMaxHealthAccesibility(proyecto = proyecto) for dominio in self.dominios.all()])
#         else:
#             return self.impactMaxHealthAccesibility
#         
#     def getImpactMaxMaintenanceFaultPrediction(self, proyecto = None):
#         '''
#         Clase Catalogo
#         Cuando es no aplicable no se tiene en cuenta sus valores maximos
#         '''
#         if proyecto:
#             return sum([dominio.getImpactMaxMaintenanceFaultPrediction(proyecto = proyecto) for dominio in self.dominios.all()])
#         else:
#             return self.impactMaxMaintenanceFaultPrediction
#         
#     def getImpactMaxInformationOccupants(self, proyecto = None):
#         '''
#         Clase Catalogo
#         Cuando es no aplicable no se tiene en cuenta sus valores maximos
#         '''
#         if proyecto:
#             return sum([dominio.getImpactMaxInformationOccupants(proyecto = proyecto) for dominio in self.dominios.all()])
#         else:
#             return self.impactMaxInformationOccupants
#     
    @property
    def impactMaxEnergyEfficiency(self):
        ''' 
        Clase Catalogo
        
        '''
        
        impactoMaximo = sum([dominio.impactMaxEnergyEfficiency for dominio in self.dominios.all()])
        return impactoMaximo

    @property
    def impactMaxEnergyFlexibility(self):
        ''' 
        Clase Catalogo
        
        '''
        impactoMaximo = sum([dominio.impactMaxEnergyFlexibility for dominio in self.dominios.all()])
        return impactoMaximo

    @property
    def impactMaxComfort(self):
        ''' 
        Clase Catalogo
        
        '''
        impactoMaximo = sum([dominio.impactMaxComfort for dominio in self.dominios.all()])
        return impactoMaximo

    @property
    def impactMaxConvenience(self):
        ''' 
        Clase Catalogo
        
        '''
        impactoMaximo = sum([dominio.impactMaxConvenience for dominio in self.dominios.all()])
        return impactoMaximo

    @property
    def impactMaxHealthAccesibility(self):
        ''' 
        Clase Catalogo
        
        '''
        impactoMaximo = sum([dominio.impactMaxHealthAccesibility for dominio in self.dominios.all()])
        return impactoMaximo

    @property
    def impactMaxMaintenanceFaultPrediction(self):
        ''' 
        Clase Catalogo
        
        '''
        impactoMaximo = sum([dominio.impactMaxMaintenanceFaultPrediction for dominio in self.dominios.all()])
        return impactoMaximo

    @property
    def impactMaxInformationOccupants(self):
        ''' 
        Clase Catalogo
        
        '''
        impactoMaximo = sum([dominio.impactMaxInformationOccupants for dominio in self.dominios.all()])
        return impactoMaximo
        
    @classmethod
    def creaDesdeXML(cls,catalogoElement):
        ns = {'d':"http://www.gbxml.org/schema"}
        nuevaInstancia = cls()
        print("\t",catalogoElement,catalogoElement.attrib)
        description = catalogoElement.find('.//d:description',ns)
        id = catalogoElement.attrib['id']
        nuevaInstancia.description = description.text
        nuevaInstancia.id = id
        
        return nuevaInstancia
        

class Climate(Model):
    
    objects = Manager()
    
    description = CharField(default = '',
                            max_length = 1000,
                            verbose_name = "Description")
    country = ForeignKey(Country,
                         verbose_name = 'Countries',
                         related_name = 'climates',)

    def __str__(self):
        ''' 
        Clase Climate
        
        '''
        return 'Id: {} - {} '.format(self.id, self.description)

    class Meta:
        verbose_name = 'Climate'
        verbose_name_plural = '9. Climate'
        ordering = ('id',)
    
class Dominio(Model):
    
    objects = Manager()
    
    catalogo = ForeignKey(Catalogo,
                          verbose_name = 'Catalogue',
                          related_name = 'dominios')
    
    description = CharField(default = '',
                            max_length = 1000,
                            verbose_name = "Description")
    
    nameAttr = CharField(default = '',  # Este campo se va a utilizar para los getatt() de los campos.
                         max_length = 1000,
                         verbose_name = "Name Attribute")
                  
    class Meta:
        verbose_name = 'Domain'
        verbose_name_plural = '2.Domain'
        ordering = ('id',)

    def __str__(self):
        ''' 
        Clase Dominio
        
        '''
        return f"{self.description}"
    
    def duplicar(self, padre = None):
        ''' 
        Clase Dominio
        
        '''
        copyId = copy.deepcopy(self.id)
        
        listaServicios = Servicio.objects.filter(dominio_id = copyId)
        
        self.id = None
        self.pk = None

        if (padre != None):
            self.catalogo = padre
            
        self.save()
        for service in listaServicios:
            service.duplicar(padre = self)
        return self

#     def getImpactMaxEnergyEfficiency(self, proyecto = None):
#         '''
#         Clase Dominio
#         Cuando es no aplicable no se tiene en cuenta sus valores maximos
#         '''
#         if proyecto:
#             return sum([servicio.getImpactMaxEnergyEfficiency(proyecto = proyecto) for servicio in self.servicios.all()])
#         else:
#             return self.impactMaxEnergyEfficiency
#     
#     def getImpactMaxEnergyFlexibility(self, proyecto = None):
#         '''
#         Clase Dominio
#         Cuando es no aplicable no se tiene en cuenta sus valores maximos
#         '''
#         if proyecto:
#             return sum([servicio.getImpactMaxEnergyFlexibility(proyecto = proyecto) for servicio in self.servicios.all()])
#         else:
#             return self.impactMaxEnergyFlexibility
#     
#     def getImpactMaxComfort(self, proyecto = None):
#         '''
#         Clase Dominio
#         Cuando es no aplicable no se tiene en cuenta sus valores maximos
#         '''
#         if proyecto:
#             return sum([servicio.getImpactMaxComfort(proyecto = proyecto) for servicio in self.servicios.all()])
#         else:
#             return self.impactMaxComfort
#         
#     def getImpactMaxConvenience(self, proyecto = None):
#         '''
#         Clase Dominio
#         Cuando es no aplicable no se tiene en cuenta sus valores maximos
#         '''
#         if proyecto:
#             return sum([servicio.getImpactMaxConvenience(proyecto = proyecto) for servicio in self.servicios.all()])
#         else:
#             return self.impactMaxConvenience
#         
#     def getImpactMaxHealthAccesibility(self, proyecto = None):
#         '''
#         Clase Dominio
#         Cuando es no aplicable no se tiene en cuenta sus valores maximos
#         '''
#         if proyecto:
#             return sum([servicio.getImpactMaxHealthAccesibility(proyecto = proyecto) for servicio in self.servicios.all()])
#         else:
#             return self.impactMaxHealthAccesibility
#         
#     def getImpactMaxMaintenanceFaultPrediction(self, proyecto = None):
#         '''
#         Clase Dominio
#         Cuando es no aplicable no se tiene en cuenta sus valores maximos
#         '''
#         if proyecto:
#             return sum([servicio.getImpactMaxMaintenanceFaultPrediction(proyecto = proyecto) for servicio in self.servicios.all()])
#         else:
#             return self.impactMaxMaintenanceFaultPrediction
#         
#     def getImpactMaxInformationOccupants(self, proyecto = None):
#         '''
#         Clase Dominio
#         Cuando es no aplicable no se tiene en cuenta sus valores maximos
#         '''
#         if proyecto:
#             return sum([servicio.getImpactMaxInformationOccupants(proyecto = proyecto) for servicio in self.servicios.all()])
#         else:
#             return self.impactMaxInformationOccupants
#     
    @property
    def icono(self):
        ''' 
        Clase Dominio
        
        '''
        return self.nameAttr
        
    @property
    def impactMaxEnergyEfficiency(self):
        ''' 
        Clase Dominio
        
        '''
        impactoMaximo = sum([servicio.impactMaxEnergyEfficiency for servicio in self.servicios.all()])
        return impactoMaximo

    @property
    def impactMaxEnergyFlexibility(self):
        ''' 
        Clase Dominio
        
        '''
        impactoMaximo = sum([servicio.impactMaxEnergyFlexibility for servicio in self.servicios.all()])
        return impactoMaximo

    @property
    def impactMaxComfort(self):
        ''' 
        Clase Dominio
        
        '''
        impactoMaximo = sum([servicio.impactMaxComfort for servicio in self.servicios.all()])
        return impactoMaximo

    @property
    def impactMaxConvenience(self):
        ''' 
        Clase Dominio
        
        '''
        impactoMaximo = sum([servicio.impactMaxConvenience for servicio in self.servicios.all()])
        return impactoMaximo

    @property
    def impactMaxHealthAccesibility(self):
        ''' 
        Clase Dominio
        
        '''
        impactoMaximo = sum([servicio.impactMaxHealthAccesibility for servicio in self.servicios.all()])
        return impactoMaximo

    @property
    def impactMaxMaintenanceFaultPrediction(self):
        ''' 
        Clase Dominio
        
        '''
        impactoMaximo = sum([servicio.impactMaxMaintenanceFaultPrediction for servicio in self.servicios.all()])
        return impactoMaximo

    @property
    def impactMaxInformationOccupants(self):
        ''' 
        Clase Dominio
        
        '''
        impactoMaximo = sum([servicio.impactMaxInformationOccupants for servicio in self.servicios.all()])
        return impactoMaximo
        
    @classmethod
    def creaDesdeXML(cls,domainElement):
        ns = {'d':"http://www.gbxml.org/schema"}
        nuevaInstancia = cls()
        print("\t",domainElement,domainElement.attrib)
        description = domainElement.find('.//d:description',ns)
        id = domainElement.attrib['id']
        nuevaInstancia.description = description.text
        nuevaInstancia.id = id
        
        return nuevaInstancia  
    
    # def getForm(self, proyectoId = None):
    #     '''
    #     Clase Dominio
    #     '''
    #     from sri.forms import DominioForm
    #     new_fields = {}
    #     for servicio in self.servicios.all():
    #         choices1 = [] 
    #         cont = 0
    #         for x in servicio.funcionalidades.all(): choices1.append((x.id, x.description))
    #         listadoDatos = Dato.objects.filter(chosenFuncionality__service__id = servicio.id, proyect = proyectoId)
    #         porcTotal = 0
    #         # if len(listadoDatos) == 0:
    #         new_fields['{0}--{1}--{2}'.format(servicio.id, 'Choice', cont) ] = forms.ChoiceField(label = servicio.description,
    #                                                                                              help_text = servicio.description,
    #                                                                                              choices = choices1)
    #
    #         new_fields['{0}--{1}--{2}'.format(servicio.id, 'Percentage', cont) ] = forms.FloatField(label = 'Percentage',
    #                                                                                                 help_text = servicio.description,
    #                                                                                                 initial = 100.0,
    #                                                                                                 validators=[MinValueValidator(0.0),MaxValueValidator(100.0, u"Please introduce a lower value")])
    #
    #         new_fields['{0}--{1}--{2}'.format(servicio.id, 'Justificacion', cont) ] = forms.CharField(widget = CKEditorUploadingWidget(),
    #                                                                                                   label = 'Justification',
    #                                                                                                   help_text = servicio.description,
    #                                                                                                   required = False)
    #
    #         new_fields['{0}--{1}--{2}'.format(servicio.id, 'Comentario', cont) ] = forms.CharField(widget = CKEditorUploadingWidget(),
    #                                                                                                label = 'Comments',
    #                                                                                                help_text = servicio.description,
    #                                                                                                required = False)
    #         # else:
    #
    #         for dato in listadoDatos:
    #             porcTotal += dato.percentage
    #             if porcTotal < 100.: 
    #                 cont += 1
    #
    #                 new_fields['{0}--{1}--{2}'.format(servicio.id, 'Choice', cont) ] = forms.ChoiceField(label = servicio.description,
    #                                                                                                      help_text = servicio.description,
    #                                                                                                      choices = choices1)
    #
    #                 new_fields['{0}--{1}--{2}'.format(servicio.id, 'Percentage', cont) ] = forms.FloatField(label = 'Percentage',
    #                                                                                                         help_text = servicio.description,
    #                                                                                                         initial = 100 - porcTotal)
    #
    #                 new_fields['{0}--{1}--{2}'.format(servicio.id, 'Justificacion', cont) ] = forms.CharField(widget = CKEditorUploadingWidget(),
    #                                                                                                           label = 'Justification',
    #                                                                                                           help_text = servicio.description,
    #                                                                                                           required = False)
    #
    #                 new_fields['{0}--{1}--{2}'.format(servicio.id, 'Comentario', cont) ] = forms.CharField(widget = CKEditorUploadingWidget(),
    #                                                                                                        label = 'Comments',
    #                                                                                                        help_text = servicio.description,
    #                                                                                                        required = False)
    #
    #     DynamicDominionForm = type('DynamicDominionForm', (DominioForm,), new_fields)
    #
    #     return DynamicDominionForm

    
class Servicio(Model):
    
    objects = Manager()
    
    dominio = ForeignKey(Dominio,
                         verbose_name = 'Domain',
                         related_name = 'servicios')
    
    description = CharField(default = '',
                            max_length = 1000,
                            verbose_name = "Description")

    reference = CharField(default = '',
                          max_length = 20,
                          verbose_name = "Reference code")    
                  
    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = '3.Service'
        ordering = ('id',)

    def __str__(self):
        ''' 
        Clase Servicio
        
        '''
        return str(self.description)
    
    def duplicar(self, padre = None):
        ''' 
        Clase Servicio
        
        '''
        copiaId = copy.deepcopy(self.id)
        
        listaFuncionalidades = Funcionalidad.objects.filter(service_id = copiaId)
        
        self.id = None
        self.pk = None

        if (padre != None):
            self.dominio = padre
        
        self.save()
        for funcionalidad in listaFuncionalidades:
            funcionalidad.duplicar(padre = self)
        return self
    
    def getImpactMax(self, impacto = ''):
        '''
        Clase Servicio
        Devuelve los maximos del impacto
        '''
        impactoMaximo = max([getattr(funcionalidad, '{}Impact'.format(impacto)) for funcionalidad in self.funcionalidades.all()])
        return impactoMaximo
    
#     def getImpactMaxEnergyEfficiency(self, proyecto = None):
#         '''
#         Clase Servicio
#         Cuando es no aplicable no se tiene en cuenta sus valores maximos
#         '''
#         if proyecto:
#             listadoDatos = Dato.objects.filter(proyect = proyecto, 
#                                                    chosenFuncionality__service = self)
#             if listadoDatos:
#                 for dato in listadoDatos:
#                     if dato.chosenFuncionality.description == 'No aplicable':
#                         return 0
#                     else:
#                         return self.impactMaxEnergyEfficiency
#             else:
#                 return self.impactMaxEnergyEfficiency
#         else:
#             return self.impactMaxEnergyEfficiency
#     
#     def getImpactMaxEnergyFlexibility(self, proyecto = None):
#         '''
#         Clase Servicio
#         Cuando es no aplicable no se tiene en cuenta sus valores maximos
#         '''
#         if proyecto:
#             listadoDatos = Dato.objects.filter(proyect = proyecto, 
#                                                    chosenFuncionality__service = self)
#             if listadoDatos:
#                 for dato in listadoDatos:
#                     if dato.chosenFuncionality.description == 'No aplicable':
#                         return 0
#                     else:
#                         return self.impactMaxEnergyFlexibility
#             else:
#                 return self.impactMaxEnergyFlexibility
#         else:
#             return self.impactMaxEnergyFlexibility
#         
#     def getImpactMaxComfort(self, proyecto = None):
#         '''
#         Clase Servicio
#         Cuando es no aplicable no se tiene en cuenta sus valores maximos
#         '''
#         if proyecto:
#             listadoDatos = Dato.objects.filter(proyect = proyecto, 
#                                                    chosenFuncionality__service = self)
#             if listadoDatos:
#                 for dato in listadoDatos:
#                     if dato.chosenFuncionality.description == 'No aplicable':
#                         return 0
#                     else:
#                         return self.impactMaxComfort
#             else:
#                 return self.impactMaxComfort
#         else:
#             return self.impactMaxComfort
#     
#     def getImpactMaxConvenience(self, proyecto = None):
#         '''
#         Clase Servicio
#         Cuando es no aplicable no se tiene en cuenta sus valores maximos
#         '''
#         if proyecto:
#             listadoDatos = Dato.objects.filter(proyect = proyecto, 
#                                                    chosenFuncionality__service = self)
#             if listadoDatos:
#                 for dato in listadoDatos:
#                     if dato.chosenFuncionality.description == 'No aplicable':
#                         return 0
#                     else:
#                         return self.impactMaxConvenience
#             else:
#                 return self.impactMaxConvenience
#         else:
#             return self.impactMaxConvenience
#         
#     def getImpactMaxHealthAccesibility(self, proyecto = None):
#         '''
#         Clase Servicio
#         Cuando es no aplicable no se tiene en cuenta sus valores maximos
#         '''
#         if proyecto:
#             listadoDatos = Dato.objects.filter(proyect = proyecto, 
#                                                    chosenFuncionality__service = self)
#             if listadoDatos:
#                 for dato in listadoDatos:
#                     if dato.chosenFuncionality.description == 'No aplicable':
#                         return 0
#                     else:
#                         return self.impactMaxHealthAccesibility
#             else:
#                 return self.impactMaxHealthAccesibility
#         else:
#             return self.impactMaxHealthAccesibility
#         
#     def getImpactMaxMaintenanceFaultPrediction(self, proyecto = None):
#         '''
#         Clase Servicio
#         Cuando es no aplicable no se tiene en cuenta sus valores maximos
#         '''
#         if proyecto:
#             listadoDatos = Dato.objects.filter(proyect = proyecto, 
#                                                    chosenFuncionality__service = self)
#             if listadoDatos:
#                 for dato in listadoDatos:
#                     if dato.chosenFuncionality.description == 'No aplicable':
#                         return 0
#                     else:
#                         return self.impactMaxMaintenanceFaultPrediction
#             else:
#                 return self.impactMaxMaintenanceFaultPrediction
#         else:
#             return self.impactMaxMaintenanceFaultPrediction
#         
#     def getImpactMaxInformationOccupants(self, proyecto = None):
#         '''
#         Clase Servicio
#         Cuando es no aplicable no se tiene en cuenta sus valores maximos
#         '''
#         if proyecto:
#             listadoDatos = Dato.objects.filter(proyect = proyecto, 
#                                                    chosenFuncionality__service = self)
#             if listadoDatos:
#                 for dato in listadoDatos:
#                     if dato.chosenFuncionality.description == 'No aplicable':
#                         return 0
#                     else:
#                         return self.impactMaxInformationOccupants
#             else:
#                 return self.impactMaxInformationOccupants
#         else:
#             return self.impactMaxInformationOccupants
#             
    @property
    def impactMaxEnergyEfficiency(self):
        ''' 
        Clase Servicio
        
        '''
        if self.funcionalidades.all().count() == 0:
            impactoMaximo = 0 
        else:
            impactoMaximo = max([funcionalidad.energyEfficiencyImpact for funcionalidad in self.funcionalidades.all()])
            
        return impactoMaximo

    @property
    def impactMaxEnergyFlexibility(self):
        ''' 
        Clase Servicio
        
        '''
        if self.funcionalidades.all().count() == 0:
            impactoMaximo = 0
        else:
            impactoMaximo = max([funcionalidad.energyFlexibilityImpact for funcionalidad in self.funcionalidades.all()])
        return impactoMaximo

    @property
    def impactMaxComfort(self):
        ''' 
        Clase Servicio
        
        '''
        if self.funcionalidades.all().count() == 0:
            impactoMaximo = 0
        else:
            impactoMaximo = max([funcionalidad.comfortImpact for funcionalidad in self.funcionalidades.all()])
        
        return impactoMaximo

    @property
    def impactMaxConvenience(self):
        ''' 
        Clase Servicio
        
        '''
        if self.funcionalidades.all().count() == 0:
            impactoMaximo = 0
        else:
            impactoMaximo = max([funcionalidad.convenienceImpact for funcionalidad in self.funcionalidades.all()])
        return impactoMaximo

    @property
    def impactMaxHealthAccesibility(self):
        ''' 
        Clase Servicio
        
        '''
        if self.funcionalidades.all().count() == 0:
            impactoMaximo = 0
        else:
            impactoMaximo = max([funcionalidad.healthAccesibilityImpact for funcionalidad in self.funcionalidades.all()])
        return impactoMaximo

    @property
    def impactMaxMaintenanceFaultPrediction(self):
        ''' 
        Clase Servicio
        
        '''
        if self.funcionalidades.all().count() == 0:
            impactoMaximo = 0
        else:
            impactoMaximo = max([funcionalidad.maintenanceFaultPredictionImpact for funcionalidad in self.funcionalidades.all()])
        return impactoMaximo

    @property
    def impactMaxInformationOccupants(self):
        ''' 
        Clase Servicio
        
        '''
        if self.funcionalidades.all().count() == 0:
            impactoMaximo = 0
        else:
            impactoMaximo = max([funcionalidad.informationOccupantsImpact for funcionalidad in self.funcionalidades.all()])
        return impactoMaximo
        
    @classmethod
    def creaDesdeXML(cls,serviceElement):
        ns = {'d':"http://www.gbxml.org/schema"}
        nuevaInstancia = cls()
        print("\t",serviceElement,serviceElement.attrib)
        description = serviceElement.find('.//d:description',ns)
        id = serviceElement.attrib['id']
        nuevaInstancia.description = description.text
        nuevaInstancia.id = id
        
        return nuevaInstancia

    
class Funcionalidad(Model):
    
    objects = Manager()
    
    service = ForeignKey(Servicio,
                         verbose_name = 'Service',
                         related_name = 'funcionalidades')
    
    description = CharField(default = '',
                            max_length = 1000,
                            verbose_name = "Description")

    reference = CharField(default = '',
                          max_length = 20,
                          verbose_name = "Reference code")        
    
    energyEfficiencyImpact = FloatField(default = 0.0,
                                        verbose_name = 'Energy efficiency')
    
    energyFlexibilityImpact = FloatField(default = 0.0,
                                         verbose_name = 'Energy flexibility and storage')
    
    comfortImpact = FloatField(default = 0.0,
                               verbose_name = 'Comfort')
                               
    convenienceImpact = FloatField(default = 0.0,
                                   verbose_name = 'Convenience')
                                   
    healthAccesibilityImpact = FloatField(default = 0.0,
                                          verbose_name = 'Health, well-being and accessibility')
                                          
    maintenanceFaultPredictionImpact = FloatField(default = 0.0,
                                                  verbose_name = 'Maintenance and fault prediction')
                                          
    informationOccupantsImpact = FloatField(default = 0.0,
                                            verbose_name = 'Information to occupants')
                                          
    en15232Residential = ChoiceField(choices = [('-', '-'),('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')],
                                       verbose_name = u"ISO 52120-1:2021 (Residential)",
                                       default = '-')
                                       
    en15232NonResidential = ChoiceField(choices = [('-', '-'),('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')],
                                       verbose_name = u"ISO 52120-1:2021 (Non-residential)",
                                       default = '-')
                  
    class Meta:
        verbose_name = 'Functionality'
        verbose_name_plural = '4.Functionality'
        ordering = ('id',)

    def __str__(self):
        ''' 
        Clase Funcionalidad
        
        '''
        return 'Id: {} - {} '.format(self.id, self.description)
    
    def duplicar(self, padre = None):
        ''' 
        Clase Funcionalidad
        
        '''
        copyId = copy.deepcopy(self.id)
        

        self.id = None
        self.pk = None

        if (padre != None):
            self.service = padre

        self.save()
        return self
        
    @classmethod
    def creaDesdeXML(cls,funcionalidadElement):
        ns = {'d':"http://www.gbxml.org/schema"}
        nuevaInstancia = cls()
        print("\t",funcionalidadElement,funcionalidadElement.attrib)
        description = funcionalidadElement.find('.//d:description',ns)
        id = funcionalidadElement.attrib['id']
        nuevaInstancia.description = description.text
        nuevaInstancia.id = id
        nuevaInstancia.energyEfficiencyImpact = float(funcionalidadElement.find('.//d:energyEfficiencyImpact',ns).text)
        nuevaInstancia.energyFlexibilityImpact = float(funcionalidadElement.find('.//d:energyFlexibilityImpact',ns).text)
        nuevaInstancia.comfortImpact = float(funcionalidadElement.find('.//d:comfortImpact',ns).text)
        nuevaInstancia.convenienceImpact = float(funcionalidadElement.find('.//d:convenienceImpact',ns).text)
        nuevaInstancia.healthAccesibilityImpact = float(funcionalidadElement.find('.//d:healthAccesibilityImpact',ns).text)
        nuevaInstancia.maintenanceFaultPredictionImpact = float(funcionalidadElement.find('.//d:maintenanceFaultPredictionImpact',ns).text)
        nuevaInstancia.informationOccupantsImpact = float(funcionalidadElement.find('.//d:informationOccupantsImpact',ns).text)
        nuevaInstancia.en15232Residential = funcionalidadElement.find('.//d:en15232Residential',ns).text
        nuevaInstancia.en15232NonResidential = funcionalidadElement.find('.//d:en15232NonResidential',ns).text
        return nuevaInstancia

    
class ImpactWeightings (Model):
    
    objects = Manager()
    
    energyEfficiency = FloatField(verbose_name = 'Energy Efficiency',
                                  default = 0.0)
    
    energyFlexibility = FloatField(verbose_name = 'Energy flexibility and storage',
                                   default = 0.0)
    
    comfort = FloatField(verbose_name = 'Comfort',
                         default = 0.0)
    
    convenience = FloatField(verbose_name = 'Convenience',
                             default = 0.0)
    
    healthAccesibility = FloatField(verbose_name = 'Health, well-being and accessibility',
                                    default = 0.0)
    
    maintenanceFaultPrediction = FloatField(verbose_name = 'Maintenance and fault prediction',
                                            default = 0.0)
    informationOccupants = FloatField(verbose_name = 'Information to occupants',
                                      default = 0.0)
    
    kF1_energyPerformanceAndOperation = FloatField(verbose_name = 'KF1: Energy performance',
                                                   default = 1.0 / 3.0)
    
    kF2_responseToUserNeeds = FloatField(verbose_name = 'KF2: Response to user needs',
                                         default = 1.0 / 3.0)
    
    kF3_energyFlexibility = FloatField(verbose_name = 'KF3: Energy flexibility',
                                       default = 1.0 / 3.0)        
    
    def getLista(self):
        return [self.energyEfficiency,
                self.energyFlexibility,
                self.comfort,
                self.convenience,
                self.healthAccesibility,
                self.maintenanceFaultPrediction,
                self.informationOccupants]

    class Meta:
        verbose_name = 'Impact Weighting'
        verbose_name_plural = '8.Impact Weighting'
        ordering = ('id',)
        
    def duplicar(self, padre = None):
        ''' 
        Clase ImpactWeightings
        
        '''
            
        self.id = None
        self.pk = None
    
        self.save()
        return self

    def __str__(self):
        ''' 
        Clase ImpactWeightings
        
        '''
        return 'Id: {}'.format(self.id)
        
    @classmethod
    def creaDesdeXML(cls, impactWeightingElement):
        ns = {'d':"http://www.gbxml.org/schema"}
        nuevaInstancia = cls()
        print("\t",impactWeightingElement,impactWeightingElement.attrib)
        id = impactWeightingElement.attrib['id']
        nuevaInstancia.id = id
        
        nuevaInstancia.energyEfficiency = float(impactWeightingElement.find('.//d:energyEfficiency',ns).text)
        nuevaInstancia.energyFlexibility = float(impactWeightingElement.find('.//d:energyFlexibility',ns).text)
        nuevaInstancia.comfort = float(impactWeightingElement.find('.//d:comfort',ns).text)
        nuevaInstancia.convenience = float(impactWeightingElement.find('.//d:convenience',ns).text)
        nuevaInstancia.healthAccesibility = float(impactWeightingElement.find('.//d:healthAccesibility',ns).text)
        nuevaInstancia.maintenanceFaultPrediction = float(impactWeightingElement.find('.//d:maintenanceFaultPrediction',ns).text)
        nuevaInstancia.informationOccupants = float(impactWeightingElement.find('.//d:informationOccupants',ns).text)
        nuevaInstancia.kF1_energyPerformanceAndOperation = float(impactWeightingElement.find('.//d:kF1_energyPerformanceAndOperation',ns).text)
        nuevaInstancia.kF2_responseToUserNeeds = float(impactWeightingElement.find('.//d:kF2_responseToUserNeeds',ns).text)
        nuevaInstancia.kF3_energyFlexibility = float(impactWeightingElement.find('.//d:kF3_energyFlexibility',ns).text)
        
        return nuevaInstancia
        
class CustomImpactWeightings(Model):
    
    objects = Manager()
    
    energyEfficiency = FloatField(verbose_name = 'Energy Efficiency',
                                  default = 0.0)
    
    energyFlexibility = FloatField(verbose_name = 'Energy flexibility and storage',
                                   default = 0.0)
    
    comfort = FloatField(verbose_name = 'Comfort',
                         default = 0.0)
    
    convenience = FloatField(verbose_name = 'Convenience',
                             default = 0.0)
    
    healthAccesibility = FloatField(verbose_name = 'Health, well-being and accessibility',
                                    default = 0.0)
    
    maintenanceFaultPrediction = FloatField(verbose_name = 'Maintenance and fault prediction',
                                           default = 0.0)
                                           
    informationOccupants = FloatField(verbose_name = 'Information to occupants',
                                      default = 0.0)
    
    kF1_energyPerformanceAndOperation = FloatField(verbose_name = 'KF1: Energy performance',
                                                   default = 1.0 / 3.0)
    
    kF2_responseToUserNeeds = FloatField(verbose_name = 'KF2: Response to user needs',
                                         default = 1.0 / 3.0)
    
    kF3_energyFlexibility = FloatField(verbose_name = 'KF3: Energy flexibility',
                                       default = 1.0 / 3.0)        
    
    def getLista(self):
        return [self.energyEfficiency,
                self.energyFlexibility,
                self.comfort,
                self.convenience,
                self.healthAccesibility,
                self.maintenanceFaultPrediction,
                self.informationOccupants]

    class Meta:
        verbose_name = 'Custom Impact Weighting'
        verbose_name_plural = '13.Custom Impact Weighting'
        ordering = ('id',)
        
    def duplicar(self, padre = None):
        ''' 
        Clase CustomImpactWeightings
        
        '''
            
        self.id = None
        self.pk = None
    
        self.save()
        return self

    def __str__(self):
        ''' 
        Clase CustomImpactWeightings
        '''
        return 'Id: {}'.format(self.id)

class DomainWeigthing(Model):
    
    objects = Manager()

    name = CharField(default = '',
                              max_length = 1000,
                              verbose_name = "Name")
                              
    country = ForeignKey(Country,
                         verbose_name = 'Countries',
                         related_name = 'domaingWeightings',)
                                     
    catalogo = ForeignKey(Catalogo,
                          verbose_name = 'Catalogue',
                          related_name = 'domaingWeightings',)
    
    climate = ForeignKey(Climate,
                         verbose_name = 'Climates',
                         related_name = 'domaingWeightings',)
    
    impactWeighting = ForeignKey(ImpactWeightings,
                         verbose_name = 'Impact Weightings',
                         related_name = 'impact_weigthing',)
                         
    buildingType = ForeignKey(BuildingType,
                              verbose_name = 'Building Types',
                              related_name = 'domaingWeightings',)
    
    energyEfficiencyHeating = FloatField(verbose_name = 'Energy efficiency heating',
                                         default = 0.0)

    energyFlexibilityHeating = FloatField(verbose_name = 'Energy flexibility heating',
                                         default = 0.0)

    comfortHeating = FloatField(verbose_name = 'Comfort heating',
                                default = 0.0)

    convenienceHeating = FloatField(verbose_name = 'Convenience heating',
                                    default = 0.0)

    healthAccesibilityHeating = FloatField(verbose_name = 'Health, well-being and accessibility heating',
                                           default = 0.0)

    maintenanceFaultPredictionHeating = FloatField(verbose_name = 'Maintenance and fault prediction heating',
                                                   default = 0.0)
    
    informationOccupantsHeating = FloatField(verbose_name = 'Information to occupants heating',
                                             default = 0.0)
    
    energyEfficiencyCooling = FloatField(verbose_name = 'Energy efficiency Cooling',
                                         default = 0.0)

    energyFlexibilityCooling = FloatField(verbose_name = 'Energy flexibility Cooling',
                                          default = 0.0)

    comfortCooling = FloatField(verbose_name = 'Comfort Cooling',
                                default = 0.0)

    convenienceCooling = FloatField(verbose_name = 'Convenience Cooling',
                                    default = 0.0)

    healthAccesibilityCooling = FloatField(verbose_name = 'Health, well-being and accessibility Cooling',
                                           default = 0.0)

    maintenanceFaultPredictionCooling = FloatField(verbose_name = 'Maintenance and fault prediction Cooling',
                                                   default = 0.0)
    
    informationOccupantsCooling = FloatField(verbose_name = 'Information to occupants Cooling',
                                             default = 0.0)
    
    energyEfficiencyDhw = FloatField(verbose_name = 'Energy efficiency DHW',
                                     default = 0.0)

    energyFlexibilityDhw = FloatField(verbose_name = 'Energy flexibility DHW',
                                      default = 0.0)

    comfortDhw = FloatField(verbose_name = 'Comfort DHW',
                           default = 0.0)

    convenienceDhw = FloatField(verbose_name = 'Convenience DHW',
                                  default = 0.0)

    healthAccesibilityDhw = FloatField(verbose_name = 'Health, well-being and accessibility DHW',
                                       default = 0.0)

    maintenanceFaultPredictionDhw = FloatField(verbose_name = 'Maintenance and fault prediction DHW',
                                               default = 0.0)
    
    informationOccupantsDhw = FloatField(verbose_name = 'Information to occupants DHW',
                                         default = 0.0)
    
    energyEfficiencyVentilation = FloatField(verbose_name = 'Energy efficiency Ventilation',
                                             default = 0.0)

    energyFlexibilityVentilation = FloatField(verbose_name = 'Energy flexibility Ventilation',
                                              default = 0.0)

    comfortVentilation = FloatField(verbose_name = 'Comfort Ventilation',
                                    default = 0.0)

    convenienceVentilation = FloatField(verbose_name = 'Convenience Ventilation',
                                       default = 0.0)

    healthAccesibilityVentilation = FloatField(verbose_name = 'Health, well-being and accessibility Ventilation',
                                               default = 0.0)

    maintenanceFaultPredictionVentilation = FloatField(verbose_name = 'Maintenance and fault prediction Ventilation',
                                                       default = 0.0)
    
    informationOccupantsVentilation = FloatField(verbose_name = 'Information to occupants Ventilation',
                                                 default = 0.0)
    
    energyEfficiencyLighting = FloatField(verbose_name = 'Energy efficiency Lighting',
                                          default = 0.0)

    energyFlexibilityLighting = FloatField(verbose_name = 'Energy flexibility Lighting',
                                           default = 0.0)
    comfortLighting = FloatField(verbose_name = 'Comfort Lighting',
                                 default = 0.0)

    convenienceLighting = FloatField(verbose_name = 'Convenience Lighting',
                                     default = 0.0)

    healthAccesibilityLighting = FloatField(verbose_name = 'Health, well-being and accessibility Lighting',
                                            default = 0.0)

    maintenanceFaultPredictionLighting = FloatField(verbose_name = 'Maintenance and fault prediction Lighting',
                                                    default = 0.0)
    
    informationOccupantsLighting = FloatField(verbose_name = 'Information to occupants Lighting',
                                              default = 0.0)
    
    energyEfficiencyElectricity = FloatField(verbose_name = 'Energy efficiency Electricity',
                                             default = 0.0)

    energyFlexibilityElectricity = FloatField(verbose_name = 'Energy flexibility Electricity',
                                              default = 0.0)
    comfortElectricity = FloatField(verbose_name = 'Comfort Electricity',
                                    default = 0.0)

    convenienceElectricity = FloatField(verbose_name = 'Convenience Electricity',
                                       default = 0.0)

    healthAccesibilityElectricity = FloatField(verbose_name = 'Health, well-being and accessibility Electricity',
                                               default = 0.0)

    maintenanceFaultPredictionElectricity = FloatField(verbose_name = 'Maintenance and fault prediction Electricity',
                                                       default = 0.0)
    
    informationOccupantsElectricity = FloatField(verbose_name = 'Information to occupants Electricity',
                                                 default = 0.0)
    
    energyEfficiencyDynamicBuildingEnvelope = FloatField(verbose_name = 'Energy efficiency Dynamic Building Envelope',
                                                         default = 0.0)

    energyFlexibilityDynamicBuildingEnvelope = FloatField(verbose_name = 'Energy flexibility Dynamic Building Envelope',
                                                          default = 0.0)
    comfortDynamicBuildingEnvelope = FloatField(verbose_name = 'Comfort Dynamic Building Envelope',
                                                default = 0.0)

    convenienceDynamicBuildingEnvelope = FloatField(verbose_name = 'Convenience Dynamic Building Envelope',
                                                   default = 0.0)

    healthAccesibilityDynamicBuildingEnvelope = FloatField(verbose_name = 'Health, well-being and accessibility Dynamic Building Envelope',
                                                           default = 0.0)

    maintenanceFaultPredictionDynamicBuildingEnvelope = FloatField(verbose_name = 'Maintenance and fault prediction Dynamic Building Envelope',
                                                                   default = 0.0)
    
    informationOccupantsDynamicBuildingEnvelope = FloatField(verbose_name = 'Information to occupants Dynamic Building Envelope',
                                                             default = 0.0)
    
    energyEfficiencyElectricVehicleCharging = FloatField(verbose_name = 'Energy efficiency Electric Vehicle Charging',
                                                         default = 0.0)

    energyFlexibilityElectricVehicleCharging = FloatField(verbose_name = 'Energy flexibility Electric Vehicle Charging',
                                                          default = 0.0)
    comfortElectricVehicleCharging = FloatField(verbose_name = 'Comfort Electric Vehicle Charging',
                                                default = 0.0)

    convenienceElectricVehicleCharging = FloatField(verbose_name = 'Convenience Electric Vehicle Charging',
                                                    default = 0.0)

    healthAccesibilityElectricVehicleCharging = FloatField(verbose_name = 'Health, well-being and accessibility Electric Vehicle Charging',
                                                           default = 0.0)

    maintenanceFaultPredictionElectricVehicleCharging = FloatField(verbose_name = 'Maintenance and fault prediction Electric Vehicle Charging',
                                                                   default = 0.0)
    
    informationOccupantsElectricVehicleCharging = FloatField(verbose_name = 'Information to occupants Electric Vehicle Charging',
                                                             default = 0.0)
    
    energyEfficiencyMonitoringAndControl = FloatField(verbose_name = 'Energy efficiency Monitoring and Control',
                                                      default = 0.0)

    energyFlexibilityMonitoringAndControl = FloatField(verbose_name = 'Energy flexibility Monitoring and Control',
                                                       default = 0.0)
    comfortMonitoringAndControl = FloatField(verbose_name = 'Comfort Monitoring and Control',
                                             default = 0.0)

    convenienceMonitoringAndControl = FloatField(verbose_name = 'Convenience Monitoring and Control',
                                                 default = 0.0)

    healthAccesibilityMonitoringAndControl = FloatField(verbose_name = 'Health, well-being and accessibility Monitoring and Control',
                                                        default = 0.0)

    maintenanceFaultPredictionMonitoringAndControl = FloatField(verbose_name = 'Maintenance and fault prediction Monitoring and Control',
                                                                default = 0.0)
    
    informationOccupantsMonitoringAndControl = FloatField(verbose_name = 'Information to occupants Monitoring and Control',
                                                          default = 0.0)
                                                          
    
    
    def __str__(self):
        ''' 
        Clase DomainWeigthing
        
        '''
        return 'Id: {} - {} '.format(self.id, self.name)
    
    class Meta:
        verbose_name = 'Domain Weighting'
        verbose_name_plural = '7. Domain Weighting'
        ordering = ('id',)
        
    def duplicar(self, padre = None):
        ''' 
        Clase DomainWeigthing
        
        '''
            
        self.id = None
        self.pk = None
        self.name = self.name + '_copy'
        self.save()
        return self
        
    @classmethod
    def creaDesdeXML(cls,domainWeigthingElement):
        ns = {'d':"http://www.gbxml.org/schema"}
        nuevaInstancia = cls()
        print("\t",domainWeigthingElement,domainWeigthingElement.attrib)
        description = domainWeigthingElement.find('.//d:name',ns)
        id = domainWeigthingElement.attrib['id']
        nuevaInstancia.name = description.text
        nuevaInstancia.id = id
        
        # Para los atributos de Heating en el XML
        instanciaHeating = domainWeigthingElement.find('.//d:Heating',ns)
        nuevaInstancia.energyEfficiencyHeating = float(instanciaHeating.find('.//d:energyEfficiency', ns).text)
        nuevaInstancia.energyFlexibilityHeating = float(instanciaHeating.find('.//d:energyFlexibility', ns).text)
        nuevaInstancia.comfortHeating = float(instanciaHeating.find('.//d:comfort', ns).text)
        nuevaInstancia.convenienceHeating = float(instanciaHeating.find('.//d:convenience', ns).text)
        nuevaInstancia.healthAccesibilityHeating = float(instanciaHeating.find('.//d:healthAccesibility', ns).text)
        nuevaInstancia.maintenanceFaultPredictionHeating = float(instanciaHeating.find('.//d:maintenanceFaultPrediction', ns).text)
        nuevaInstancia.informationOccupantsHeating = float(instanciaHeating.find('.//d:informationOccupants', ns).text)        
        print(instanciaHeating)
        
        # Para los atributos de Heating en el XML
        instanciaCooling = domainWeigthingElement.find('.//d:Cooling',ns)
        nuevaInstancia.energyEfficiencyCooling = float(instanciaCooling.find('.//d:energyEfficiency', ns).text)
        nuevaInstancia.energyFlexibilityCooling = float(instanciaCooling.find('.//d:energyFlexibility', ns).text)
        nuevaInstancia.comfortCooling = float(instanciaCooling.find('.//d:comfort', ns).text)
        nuevaInstancia.convenienceCooling = float(instanciaCooling.find('.//d:convenience', ns).text)
        nuevaInstancia.healthAccesibilityCooling = float(instanciaCooling.find('.//d:healthAccesibility', ns).text)
        nuevaInstancia.maintenanceFaultPredictionCooling = float(instanciaCooling.find('.//d:maintenanceFaultPrediction', ns).text)
        nuevaInstancia.informationOccupantsCooling = float(instanciaCooling.find('.//d:informationOccupants', ns).text)        
        print(instanciaCooling)
        
        # Para los atributos de Heating en el XML
        instanciaDhw = domainWeigthingElement.find('.//d:Dhw',ns)
        nuevaInstancia.energyEfficiencyDhw = float(instanciaDhw.find('.//d:energyEfficiency', ns).text)
        nuevaInstancia.energyFlexibilityDhw = float(instanciaDhw.find('.//d:energyFlexibility', ns).text)
        nuevaInstancia.comfortDhw = float(instanciaDhw.find('.//d:comfort', ns).text)
        nuevaInstancia.convenienceDhw = float(instanciaDhw.find('.//d:convenience', ns).text)
        nuevaInstancia.healthAccesibilityDhw = float(instanciaDhw.find('.//d:healthAccesibility', ns).text)
        nuevaInstancia.maintenanceFaultPredictionDhw = float(instanciaDhw.find('.//d:maintenanceFaultPrediction', ns).text)
        nuevaInstancia.informationOccupantsDhw = float(instanciaDhw.find('.//d:informationOccupants', ns).text)        
        print(instanciaDhw)
        
        # Para los atributos de Heating en el XML
        instanciaVentilation = domainWeigthingElement.find('.//d:Ventilation',ns)
        nuevaInstancia.energyEfficiencyVentilation = float(instanciaVentilation.find('.//d:energyEfficiency', ns).text)
        nuevaInstancia.energyFlexibilityVentilation = float(instanciaVentilation.find('.//d:energyFlexibility', ns).text)
        nuevaInstancia.comfortVentilation = float(instanciaVentilation.find('.//d:comfort', ns).text)
        nuevaInstancia.convenienceVentilation = float(instanciaVentilation.find('.//d:convenience', ns).text)
        nuevaInstancia.healthAccesibilityVentilation = float(instanciaVentilation.find('.//d:healthAccesibility', ns).text)
        nuevaInstancia.maintenanceFaultPredictionVentilation = float(instanciaVentilation.find('.//d:maintenanceFaultPrediction', ns).text)
        nuevaInstancia.informationOccupantsVentilation = float(instanciaVentilation.find('.//d:informationOccupants', ns).text)        
        print(instanciaVentilation)
        
        # Para los atributos de Heating en el XML
        instanciaLighting = domainWeigthingElement.find('.//d:Lighting',ns)
        nuevaInstancia.energyEfficiencyLighting = float(instanciaLighting.find('.//d:energyEfficiency', ns).text)
        nuevaInstancia.energyFlexibilityLighting = float(instanciaLighting.find('.//d:energyFlexibility', ns).text)
        nuevaInstancia.comfortLighting = float(instanciaLighting.find('.//d:comfort', ns).text)
        nuevaInstancia.convenienceLighting = float(instanciaLighting.find('.//d:convenience', ns).text)
        nuevaInstancia.healthAccesibilityLighting = float(instanciaLighting.find('.//d:healthAccesibility', ns).text)
        nuevaInstancia.maintenanceFaultPredictionLighting = float(instanciaLighting.find('.//d:maintenanceFaultPrediction', ns).text)
        nuevaInstancia.informationOccupantsLighting = float(instanciaLighting.find('.//d:informationOccupants', ns).text)        
        print(instanciaLighting)
        
        # Para los atributos de Heating en el XML
        instanciaElectricity = domainWeigthingElement.find('.//d:Electricity',ns)
        nuevaInstancia.energyEfficiencyElectricity = float(instanciaElectricity.find('.//d:energyEfficiency', ns).text)
        nuevaInstancia.energyFlexibilityElectricity = float(instanciaElectricity.find('.//d:energyFlexibility', ns).text)
        nuevaInstancia.comfortElectricity = float(instanciaElectricity.find('.//d:comfort', ns).text)
        nuevaInstancia.convenienceElectricity = float(instanciaElectricity.find('.//d:convenience', ns).text)
        nuevaInstancia.healthAccesibilityElectricity = float(instanciaElectricity.find('.//d:healthAccesibility', ns).text)
        nuevaInstancia.maintenanceFaultPredictionElectricity = float(instanciaElectricity.find('.//d:maintenanceFaultPrediction', ns).text)
        nuevaInstancia.informationOccupantsElectricity = float(instanciaElectricity.find('.//d:informationOccupants', ns).text)        
        print(instanciaElectricity)
        
        # Para los atributos de Heating en el XML
        instanciaDynamicBuildingEnvelope = domainWeigthingElement.find('.//d:DynamicBuildingEnvelope',ns)
        nuevaInstancia.energyEfficiencyDynamicBuildingEnvelope = float(instanciaDynamicBuildingEnvelope.find('.//d:energyEfficiency', ns).text)
        nuevaInstancia.energyFlexibilityDynamicBuildingEnvelope = float(instanciaDynamicBuildingEnvelope.find('.//d:energyFlexibility', ns).text)
        nuevaInstancia.comfortDynamicBuildingEnvelope = float(instanciaDynamicBuildingEnvelope.find('.//d:comfort', ns).text)
        nuevaInstancia.convenienceDynamicBuildingEnvelope = float(instanciaDynamicBuildingEnvelope.find('.//d:convenience', ns).text)
        nuevaInstancia.healthAccesibilityDynamicBuildingEnvelope = float(instanciaDynamicBuildingEnvelope.find('.//d:healthAccesibility', ns).text)
        nuevaInstancia.maintenanceFaultPredictionDynamicBuildingEnvelope = float(instanciaDynamicBuildingEnvelope.find('.//d:maintenanceFaultPrediction', ns).text)
        nuevaInstancia.informationOccupantsDynamicBuildingEnvelope = float(instanciaDynamicBuildingEnvelope.find('.//d:informationOccupants', ns).text)        
        print(instanciaDynamicBuildingEnvelope)
        
        # Para los atributos de Heating en el XML
        instanciaElectricVehicleCharging = domainWeigthingElement.find('.//d:ElectricVehicleCharging',ns)
        nuevaInstancia.energyEfficiencyElectricVehicleCharging = float(instanciaElectricVehicleCharging.find('.//d:energyEfficiency', ns).text)
        nuevaInstancia.energyFlexibilityElectricVehicleCharging = float(instanciaElectricVehicleCharging.find('.//d:energyFlexibility', ns).text)
        nuevaInstancia.comfortElectricVehicleCharging = float(instanciaElectricVehicleCharging.find('.//d:comfort', ns).text)
        nuevaInstancia.convenienceElectricVehicleCharging = float(instanciaElectricVehicleCharging.find('.//d:convenience', ns).text)
        nuevaInstancia.healthAccesibilityElectricVehicleCharging = float(instanciaElectricVehicleCharging.find('.//d:healthAccesibility', ns).text)
        nuevaInstancia.maintenanceFaultPredictionElectricVehicleCharging = float(instanciaElectricVehicleCharging.find('.//d:maintenanceFaultPrediction', ns).text)
        nuevaInstancia.informationOccupantsElectricVehicleCharging = float(instanciaElectricVehicleCharging.find('.//d:informationOccupants', ns).text)        
        print(instanciaElectricVehicleCharging)
        
        # Para los atributos de Heating en el XML
        instanciaMonitoringAndControl = domainWeigthingElement.find('.//d:MonitoringAndControl',ns)
        nuevaInstancia.energyEfficiencyMonitoringAndControl = float(instanciaMonitoringAndControl.find('.//d:energyEfficiency', ns).text)
        nuevaInstancia.energyFlexibilityMonitoringAndControl = float(instanciaMonitoringAndControl.find('.//d:energyFlexibility', ns).text)
        nuevaInstancia.comfortMonitoringAndControl = float(instanciaMonitoringAndControl.find('.//d:comfort', ns).text)
        nuevaInstancia.convenienceMonitoringAndControl = float(instanciaMonitoringAndControl.find('.//d:convenience', ns).text)
        nuevaInstancia.healthAccesibilityMonitoringAndControl = float(instanciaMonitoringAndControl.find('.//d:healthAccesibility', ns).text)
        nuevaInstancia.maintenanceFaultPredictionMonitoringAndControl = float(instanciaMonitoringAndControl.find('.//d:maintenanceFaultPrediction', ns).text)
        nuevaInstancia.informationOccupantsMonitoringAndControl = float(instanciaMonitoringAndControl.find('.//d:informationOccupants', ns).text)        
        print(instanciaMonitoringAndControl)
        
        instanciaImpactWeighting = ImpactWeightings.creaDesdeXML(domainWeigthingElement.find('.//d:ImpactWeighting', ns))
        nuevaInstancia.impactWeighting = instanciaImpactWeighting
        return nuevaInstancia

class CustomDomainWeighting(Model):
    
    objects = Manager()
    
    customImpactWeighting = ForeignKey(CustomImpactWeightings,
                                       verbose_name = 'Custom Impact Weightings',
                                       related_name = 'customDomainWeigthing',)
                         
    user = ForeignKey(User,
                      verbose_name = u"User",
                      related_name = 'customDomainWeigthing',)
        
    name = CharField(default = '',
                     max_length = 1000,
                     verbose_name = "Name")
                              
    country = ForeignKey(Country,
                         verbose_name = 'Countries',
                         related_name = 'customDomainWeigthing',)
    
    climate = ForeignKey(Climate,
                         verbose_name = 'Climates',
                         related_name = 'customDomainWeigthing',)
                         
    buildingType = ForeignKey(BuildingType,
                              verbose_name = 'Building Types',
                              related_name = 'customDomainWeigthing',)
    
    energyEfficiencyHeating = FloatField(verbose_name = 'Energy efficiency heating',)

    energyFlexibilityHeating = FloatField(verbose_name = 'Energy flexibility heating',)

    comfortHeating = FloatField(verbose_name = 'Comfort heating',
                                default = 0.167)

    convenienceHeating = FloatField(verbose_name = 'Convenience heating',
                                    default = 0.111)

    healthAccesibilityHeating = FloatField(verbose_name = 'Health, well-being and accessibility heating',
                                           default = 0.0)

    maintenanceFaultPredictionHeating = FloatField(verbose_name = 'Maintenance and fault prediction heating',)
    
    informationOccupantsHeating = FloatField(verbose_name = 'Information to occupants heating',
                                             default = 0.125)
    
    energyEfficiencyCooling = FloatField(verbose_name = 'Energy efficiency Cooling',)

    energyFlexibilityCooling = FloatField(verbose_name = 'Energy flexibility Cooling',)

    comfortCooling = FloatField(verbose_name = 'Comfort Cooling',
                                default = 0.167)

    convenienceCooling = FloatField(verbose_name = 'Convenience Cooling',
                                    default = 0.111)

    healthAccesibilityCooling = FloatField(verbose_name = 'Health, well-being and accessibility Cooling',
                                           default = 0.0)

    maintenanceFaultPredictionCooling = FloatField(verbose_name = 'Maintenance and fault prediction Cooling',
                                                   )
    
    informationOccupantsCooling = FloatField(verbose_name = 'Information to occupants Cooling',
                                             default = 0.125)
    
    energyEfficiencyDhw = FloatField(verbose_name = 'Energy efficiency DHW',)

    energyFlexibilityDhw = FloatField(verbose_name = 'Energy flexibility DHW',)

    comfortDhw = FloatField(verbose_name = 'Comfort DHW',
                           default = 0.167)

    convenienceDhw = FloatField(verbose_name = 'Convenience DHW',
                                  default = 0.111)

    healthAccesibilityDhw = FloatField(verbose_name = 'Health, well-being and accessibility DHW',
                                       default = 0.0)

    maintenanceFaultPredictionDhw = FloatField(verbose_name = 'Maintenance and fault prediction DHW',)
    
    informationOccupantsDhw = FloatField(verbose_name = 'Information to occupants DHW',
                                         default = 0.0)
    
    energyEfficiencyVentilation = FloatField(verbose_name = 'Energy efficiency Ventilation',
                                             )

    energyFlexibilityVentilation = FloatField(verbose_name = 'Energy flexibility Ventilation',
                                              default = 0.0)

    comfortVentilation = FloatField(verbose_name = 'Comfort Ventilation',
                                    default = 0.167)

    convenienceVentilation = FloatField(verbose_name = 'Convenience Ventilation',
                                       default = 0.111)

    healthAccesibilityVentilation = FloatField(verbose_name = 'Health, well-being and accessibility Ventilation',
                                               default = 0.4)

    maintenanceFaultPredictionVentilation = FloatField(verbose_name = 'Maintenance and fault prediction Ventilation',
                                                       )
    
    informationOccupantsVentilation = FloatField(verbose_name = 'Information to occupants Ventilation',
                                                 default = 0.125)
    
    energyEfficiencyLighting = FloatField(verbose_name = 'Energy efficiency Lighting',)

    energyFlexibilityLighting = FloatField(verbose_name = 'Energy flexibility Lighting',
                                           default = 0.0)
    comfortLighting = FloatField(verbose_name = 'Comfort Lighting',
                                 default = 0.167)

    convenienceLighting = FloatField(verbose_name = 'Convenience Lighting',
                                     default = 0.111)

    healthAccesibilityLighting = FloatField(verbose_name = 'Health, well-being and accessibility Lighting',
                                            default = 0.0)

    maintenanceFaultPredictionLighting = FloatField(verbose_name = 'Maintenance and fault prediction Lighting',)
    
    informationOccupantsLighting = FloatField(verbose_name ='Information to occupants Lighting',
                                              default = 0.0)
    
    energyEfficiencyElectricity = FloatField(verbose_name = 'Energy efficiency Electricity',
                                             default = 0.111)

    energyFlexibilityElectricity = FloatField(verbose_name = 'Energy flexibility Electricity',
                                              default = 0.149)
    comfortElectricity = FloatField(verbose_name = 'Comfort Electricity',
                                    default = 0.0)

    convenienceElectricity = FloatField(verbose_name = 'Convenience Electricity',
                                       default = 0.111)

    healthAccesibilityElectricity = FloatField(verbose_name = 'Health, well-being and accessibility Electricity',
                                               default = 0.0)

    maintenanceFaultPredictionElectricity = FloatField(verbose_name = 'Maintenance and fault prediction Electricity',
                                                       default = 0.113)
    
    informationOccupantsElectricity = FloatField(verbose_name = 'Information to occupants Electricity',
                                                 default = 0.125)
    
    energyEfficiencyDynamicBuildingEnvelope = FloatField(verbose_name = 'Energy efficiency Dynamic Building Envelope',
                                                         default = 0.05)

    energyFlexibilityDynamicBuildingEnvelope = FloatField(verbose_name = 'Energy flexibility Dynamic Building Envelope',
                                                          default = 0.0)
    comfortDynamicBuildingEnvelope = FloatField(verbose_name = 'Comfort Dynamic Building Envelope',
                                                default = 0.167)

    convenienceDynamicBuildingEnvelope = FloatField(verbose_name = 'Convenience Dynamic Building Envelope',
                                                   default = 0.111)

    healthAccesibilityDynamicBuildingEnvelope = FloatField(verbose_name = 'Health, well-being and accessibility Dynamic Building Envelope',
                                                           default = 0.6)

    maintenanceFaultPredictionDynamicBuildingEnvelope = FloatField(verbose_name = 'Maintenance and fault prediction Dynamic Building Envelope',
                                                                   default = 0.05)
    
    informationOccupantsDynamicBuildingEnvelope = FloatField(verbose_name = 'Information to occupants Dynamic Building Envelope',
                                                             default = 0.125)
    
    energyEfficiencyElectricVehicleCharging = FloatField(verbose_name = 'Energy efficiency Electric Vehicle Charging',
                                                         default = 0.0)

    energyFlexibilityElectricVehicleCharging = FloatField(verbose_name = 'Energy flexibility Electric Vehicle Charging',
                                                          default = 0.05)
    comfortElectricVehicleCharging = FloatField(verbose_name = 'Comfort Electric Vehicle Charging',
                                                default = 0.0)

    convenienceElectricVehicleCharging = FloatField(verbose_name = 'Convenience Electric Vehicle Charging',
                                                    default = 0.111)

    healthAccesibilityElectricVehicleCharging = FloatField(verbose_name = 'Health, well-being and accessibility Electric Vehicle Charging',
                                                           default = 0.0)

    maintenanceFaultPredictionElectricVehicleCharging = FloatField(verbose_name = 'Maintenance and fault prediction Electric Vehicle Charging',
                                                                   default = 0.0)
    
    informationOccupantsElectricVehicleCharging = FloatField(verbose_name = 'Information to occupants Electric Vehicle Charging',
                                                             default = 0.125)
    
    energyEfficiencyMonitoringAndControl = FloatField(verbose_name = 'Energy efficiency Monitoring and Control',
                                                      default = 0.2)

    energyFlexibilityMonitoringAndControl = FloatField(verbose_name = 'Energy flexibility Monitoring and Control',                                                       default = 0.2)
    comfortMonitoringAndControl = FloatField(verbose_name = 'Comfort Monitoring and Control',
                                             default = 0.0)

    convenienceMonitoringAndControl = FloatField(verbose_name = 'Convenience Monitoring and Control',
                                                 default = 0.111)

    healthAccesibilityMonitoringAndControl = FloatField(verbose_name = 'Health, well-being and accessibility Monitoring and Control',
                                                        default = 0.0)

    maintenanceFaultPredictionMonitoringAndControl = FloatField(verbose_name = 'Maintenance and fault prediction Monitoring and Control',
                                                                default = 0.2)
    
    informationOccupantsMonitoringAndControl = FloatField(verbose_name = 'Information to occupants Monitoring and Control',
                                                          default = 0.125)
        
    
    class Meta:
        verbose_name = 'Particular Custom Domain Weighting'
        verbose_name_plural = '12. Particular Domain Weighting'
        ordering = ('id',)
        
    def __str__(self):
        ''' 
        Clase CustomDomainWeigthing
        
        '''
        return 'Id: {} - {} '.format(self.id, self.name)
        
    def duplicar(self, padre = None):
        ''' 
        Clase CustomDomainWeigthing
        
        '''
            
        self.id = None
        self.pk = None
        self.name = self.name + '_copy'

        self.save()
        return self
        
class UserDefineDomainWeightings(Model):
    
    objects = Manager()
    
    def __str__(self):
        ''' 
        Clase UserDefineDomainWeightings
        '''
        return 'Id: {} - {} '.format(self.id, self.description)

    class Meta:
        verbose_name = 'User-defined Domain Weightings'
        verbose_name_plural = '11.User-defined Domain Weightings'
        ordering = ('id',)

        
class Proyecto(Model):
    
    objects = Manager()
    
    user = ForeignKey(User,
                      verbose_name = u"User",
                      related_name = 'proyectos')
    
    country = ForeignKey(Country,
                         verbose_name = 'Country',
                         related_name = 'proyectos',)
    
    catalogo = ForeignKey(Catalogo,
                          verbose_name = 'Catalogue',
                          related_name = 'proyectos',)
    
    climate = ForeignKey(Climate,
                         verbose_name = 'Climate',
                         related_name = 'proyectos',)
    
    domainWeigthing = ForeignKey(DomainWeigthing,
                                 verbose_name = 'Default weighting factors',
                                 related_name = 'proyectos',)
                                
    customDomainWeigthings = ForeignKey(CustomDomainWeighting,
                                        verbose_name = 'Custom Domain Weighting',
                                        related_name = 'proyecto',)
                                
    buildingType = ForeignKey(BuildingType,
                              verbose_name = 'Building Type',
                              related_name = 'proyectos',)
      
    name = CharField(default = '',
                     max_length = 1000,
                     verbose_name = "Project-Name")
    
    organisation = CharField(default = '',
                             max_length = 1000,
                             verbose_name = "Organisation")
    
    email = CharField(default = '',
                      max_length = 1000,
                      verbose_name = 'E-mail address')
    
    telephoneNumber = CharField(default = '',
                      max_length = 1000,
                      verbose_name = 'Telephone Number') 
                      
    preference = ChoiceField(choices = [('default', 'default'), ('user defined', 'user defined')],
                                       verbose_name = u"Preference",
                                       default = '')
    
    buildingUsage = ChoiceField(choices = [('', ''),
                                         ('residential - single-family-house', 'residential-single-family-house'),
                                         ('residential - small multi-family-house', 'residential - small multi-family-house'),
                                         ('residential - large multi-family-house', 'residential - large multi-family-house'),
                                         ('residential - other', 'residential - other'),
                                         ('non-residential - office', 'non-residential - office'),
                                         ('non-residential - educational', 'non-residential - educational'),
                                         ('non-residential - healthcare', 'non-residential - healthcare'),                                    
                                         ('non-residential - other', 'non-residential - other')],
                                verbose_name = "Building Usage",
                                default = '')
    
    
    
    netFloorAreaOfTheBuilding = FloatField(verbose_name = 'Net floor area of the building',
                                           default = 0.0)
    
    yearOfConstruction = FloatField(verbose_name = 'Year of construction',
                                    default = 0.0)
    
    buildingState = ChoiceField(choices = [('', ''),
                                         ('Original', 'Original'),
                                         ('Renovated', 'Renovated')],
                                verbose_name = u"Building state",
                                default = '')
    
    assessmentPurpose = ChoiceField(choices = [('Current building state', 'Current building state'),
                                             ('Improvement package', 'Improvement package')],
                                    verbose_name = u"Assessment purpose",
                                    default = 'Current building state')    
    
    energyClass = ChoiceField(choices = [('-', '-'),
                                       ('A','A'),
                                       ('B','B'),
                                       ('C','C'),
                                       ('D','D'),
                                       ('E', 'E'),
                                       ('F', 'F'),
                                       ('G','G'),],
                               verbose_name = u"Energy class",
                               default = '-')  
    
    officialTestPhase = BooleanField(default = False, 
                                     verbose_name = "Official test phase",)      
    
    
    descriptionOfBuilding = CharField(default = '',
                                      max_length = 1000,
                                      verbose_name = 'Description of building')
    
    address = CharField(default = '',
                        max_length = 1000,
                        verbose_name = 'Address')
    
    combinedHVACPower = ChoiceField(choices = [('>= 290 kW', '>= 290 kW'),
                                             ('70 - 290 kW', '70 - 290 kW'),
                                             ('<= 70 kW', '<= 70 kW'),
                                             ('', '')],
                                  verbose_name = u"Effective rated output for HVAC systems",
                                  default = '')    
    
    
    # Almacenamos estos valores para que sirvan de cache en el benchmarking
    totalSriScore = FloatField(verbose_name = 'Total SRI Score',
                               default = 0.0)    
    
    scoreKF1 = FloatField(verbose_name = 'Score KF1',
                          default = 0.0)    

    scoreKF2 = FloatField(verbose_name = 'Score KF2',
                          default = 0.0)    

    scoreKF3 = FloatField(verbose_name = 'Score KF3',
                          default = 0.0)            
    
    
    Heating = BooleanField(default = True, verbose_name = "Heating")
    Dhw = BooleanField(default = True, verbose_name = "DWH")
    Cooling = BooleanField(default = True, verbose_name = "Cooling")
    Ventilation = BooleanField(default = True, verbose_name = "Ventilation")
    Lighting = BooleanField(default = True, verbose_name = "Lighting")
    DynamicBuildingEnvelope = BooleanField(default = True, verbose_name = "Dynamic Building Envelope")
    Electricity = BooleanField(default = True, verbose_name = "Electricity")
    ElectricVehicleCharging = BooleanField(default = True, verbose_name = "Electric Vehicle Charging")
    MonitoringAndControl = BooleanField(default = True, verbose_name = "Monitoring And Control")
    customDomain = BooleanField(default = False, verbose_name = "Custom Domain Weighting")
    
    @classmethod
    def creaDesdeXML(cls,projectElement):
        ns = {'d':"http://www.gbxml.org/schema"}
        nuevaInstancia = cls()
        nameElement = projectElement.find('d:name',ns)
        nuevaInstancia.name = nameElement.text         
        
        print(projectElement,projectElement.attrib)
        nuevaInstancia.country = Country.creaDesdeXML(projectElement)
        nuevaInstancia.user = User.creaDesdeXML(projectElement)
        
        for domainWeigthingElement in projectElement.findall('.//d:DomainWeigthing', ns):
            nuevaInstancia.domainWeigthing = DomainWeigthing.creaDesdeXML(domainWeigthingElement)
            
        
        for catalogueElement in projectElement.findall('.//d:Catalogue',ns):
            print("\t",catalogueElement,catalogueElement.attrib)
            description = catalogueElement.find('.//d:description',ns)
            nuevaInstancia.catalogo = Catalogo.creaDesdeXML(catalogueElement)
            nuevaInstancia.catalogo.country = nuevaInstancia.country
            print("\t\t",description.text)
            for domainElement in catalogueElement.findall('.//d:Domain',ns):
                nuevaInstanciaDominio = Dominio.creaDesdeXML(domainElement)
                nuevaInstanciaDominio.catalogo = nuevaInstancia.catalogo
                print("\t\t\t",domainElement,domainElement.attrib)
                description = domainElement.find('.//d:description',ns)
                print("\t\t\t\t",description.text)
                for serviceElement in domainElement.findall('.//d:Service',ns):
                    nuevaInstanciaService = Servicio.creaDesdeXML(serviceElement)
                    nuevaInstanciaService.dominio = nuevaInstanciaDominio
                    print("\t\t\t",serviceElement,serviceElement.attrib)
                    description = serviceElement.find('.//d:description',ns)
                    print("\t\t\t\t",description.text)
                    for funcionalitiesElement in serviceElement.findall('.//d:Functionality', ns):
                        nuevaInstanciaFunctionality = Funcionalidad.creaDesdeXML(funcionalitiesElement)
                        nuevaInstanciaFunctionality.service = nuevaInstanciaService
                        print("\t\t\t",funcionalitiesElement,funcionalitiesElement.attrib)
                        description = funcionalitiesElement.find('.//d:description',ns)
                        print("\t\t\t\t",description.text)  
        
               
        return nuevaInstancia
    
    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = '10. Project'
        ordering = ('id',)
    
    def __str__(self):
        ''' 
        Clase Proyecto
        
        '''
        return 'Project:' + '{}'.format(self.id) + ' - {}'.format(self.name)
    
    def duplicar(self):
        ''' 
        Clase Proyecto
        
        '''
        
        listaDatos = Dato.objects.filter( proyect = self)
        self.id = None
        self.pk = None
            
        self.name += "_copy"
        
        self.save()
        
        for dato in listaDatos:
            dato.duplicar(padre = self)
            
        return self
    
    # @property
    # def puntuaciónTotal(self): # TODO: Falta de echar un vistazo porque las puntuaciones van ponderadas
    #     total = self.catalogo.impactMaxEnergyEfficiency + self.catalogo.impactMaxEnergyFlexibility + self.catalogo.impactMaxConvenience + self.catalogo.impactMaxComfort + self.catalogo.impactMaxHealthAccesibility + self.catalogo.impactMaxMaintenanceFaultPrediction + self.catalogo.impactMaxInformationOccupants
    #     return total 
    @property
    def iconosPresentes(self):
        listaIconos = [] 
        for dominio in self.catalogo.dominios.all():
            if getattr(self, dominio.nameAttr):
                listaIconos.append(dominio.icono)
        return listaIconos
        
    @property
    def dominiosPresentes(self):
        listaDominios = [] 
        for dominio in self.catalogo.dominios.all():
            if getattr(self, dominio.nameAttr):
                listaDominios.append(dominio)
        return listaDominios
        
    @property
    def listadoNombreImpactos(self):
        return ['energyEfficiency', 'energyFlexibility', 'comfort', 'convenience', 'healthAccesibility',  'maintenanceFaultPrediction','informationOccupants']
        
    @property
    def listadoNombreImpactosMostrar(self):
        return ['Energy Efficiency', 'Energy flexibility and storage', 'Comfort', 'Convenience', 'Health, well-being and accessibility', 'Maintenance and fault prediction', 'Information to occupants',]
    
    @property
    def listadoNombreDominios(self):
        listadoNombreDominios = []
        for dominio in self.catalogo.dominios.all():
            if getattr(self, dominio.nameAttr):
                listadoNombreDominios.append(dominio.description)
        return listadoNombreDominios
        
    @property
    def listadoNombreDominiosMostrar(self):
        listadoNombreDominios = []
        for dominio in self.catalogo.dominios.all():
            if getattr(self, dominio.nameAttr):
                listadoNombreDominios.append(dominio.description)
        return listadoNombreDominios
        
    @property
    def FBacC (self):
        if self.buildingType.id == 2:
            letra = self.getNotaResidentialAndNonResidential(self.calculoMatrizImpacto()) 
            if letra == 'D':
                if  'office' in self.buildingUsage:
                    fBac = 1.44
                elif  'lecture hall' in self.buildingUsage:  
                    fBac = 1.22                    
                elif  'educational' in self.buildingUsage:  
                    fBac = 1.20
                elif 'hospital' in self.buildingUsage:  
                    fBac = 1.31
                elif 'hotel' in self.buildingUsage:  
                    fBac = 1.17    
                elif 'restaurant' in self.buildingUsage:  
                    fBac = 1.21               
                elif 'wholesale and retail' in self.buildingUsage:  
                    fBac = 1.56                                                                    
                else:
                    fBac = None
            elif letra == 'C':
                if  'office' in self.buildingUsage:
                    fBac = 1.0
                elif  'lecture hall' in self.buildingUsage:  
                    fBac = 1.0                    
                elif  'educational' in self.buildingUsage:  
                    fBac = 1.0
                elif 'hospital' in self.buildingUsage:  
                    fBac = 1.0
                elif 'hotel' in self.buildingUsage:  
                    fBac = 1.0    
                elif 'restaurant' in self.buildingUsage:  
                    fBac = 1.0               
                elif 'wholesale and retail' in self.buildingUsage:  
                    fBac = 1.0                                                                    
                else:
                    fBac = 1.0   
            elif letra == 'B':
                if  'office' in self.buildingUsage:
                    fBac = 0.79
                elif  'lecture hall' in self.buildingUsage:  
                    fBac = 0.73                    
                elif  'educational' in self.buildingUsage:  
                    fBac = 0.88
                elif 'hospital' in self.buildingUsage:  
                    fBac = 0.91
                elif 'hotel' in self.buildingUsage:  
                    fBac = 0.85  
                elif 'restaurant' in self.buildingUsage:  
                    fBac = 0.76               
                elif 'wholesale and retail' in self.buildingUsage:  
                    fBac = 0.71                                                                    
                else:
                    fBac = None 
            elif letra == 'A':
                if  'office' in self.buildingUsage:
                    fBac = 0.70
                elif  'lecture hall' in self.buildingUsage:  
                    fBac = 0.3                    
                elif  'educational' in self.buildingUsage:  
                    fBac = 0.8
                elif 'hospital' in self.buildingUsage:  
                    fBac = 0.86
                elif 'hotel' in self.buildingUsage:  
                    fBac = 0.61  
                elif 'restaurant' in self.buildingUsage:  
                    fBac = 0.69               
                elif 'wholesale and retail' in self.buildingUsage:  
                    fBac = 0.46                                                                    
                else:
                    fBac = None 
        else:
            if letra == 'D':
                fBac = 1.09
            elif letra == 'C':
                fBac = 1.0                
            elif letra == 'B':
                fBac = 0.88
            elif letra == 'A':
                fBac = 0.81                                                                                                        
        return fBac
    @property
    def FBacR (self):
        if self.buildingType.id == 2:
            letra = self.getNotaResidentialAndNonResidential(self.calculoMatrizImpacto()) 
            if letra == 'D':
                if  'office' in self.buildingUsage:
                    fBac = 1.58
                elif  'lecture hall' in self.buildingUsage:  
                    fBac = 1.32                    
                elif  'educational' in self.buildingUsage:  
                    fBac = None
                elif 'hospital' in self.buildingUsage:  
                    fBac = None
                elif 'hotel' in self.buildingUsage:  
                    fBac = 1.76 
                elif 'restaurant' in self.buildingUsage:  
                    fBac = 1.39               
                elif 'wholesale and retail' in self.buildingUsage:  
                    fBac = 1.59                                                                    
                else:
                    fBac = None
            elif letra == 'C':
                if  'office' in self.buildingUsage:
                    fBac = 1.0
                elif  'lecture hall' in self.buildingUsage:  
                    fBac = 1.0                    
                elif  'educational' in self.buildingUsage:  
                    fBac = 1.0
                elif 'hospital' in self.buildingUsage:  
                    fBac = 1.0
                elif 'hotel' in self.buildingUsage:  
                    fBac = 1.0    
                elif 'restaurant' in self.buildingUsage:  
                    fBac = 1.0               
                elif 'wholesale and retail' in self.buildingUsage:  
                    fBac = 1.0                                                                    
                else:
                    fBac = 1.0   
            elif letra == 'B':
                if  'office' in self.buildingUsage:
                    fBac = 0.80
                elif  'lecture hall' in self.buildingUsage:  
                    fBac = 0.94                    
                elif  'educational' in self.buildingUsage:  
                    fBac = None
                elif 'hospital' in self.buildingUsage:  
                    fBac = None
                elif 'hotel' in self.buildingUsage:  
                    fBac = 0.79
                elif 'restaurant' in self.buildingUsage:  
                    fBac = 0.94               
                elif 'wholesale and retail' in self.buildingUsage:  
                    fBac = 0.85                                                                    
                else:
                    fBac = None 
            elif letra == 'A':
                if  'office' in self.buildingUsage:
                    fBac = 0.57
                elif  'lecture hall' in self.buildingUsage:  
                    fBac = 0.64                    
                elif  'educational' in self.buildingUsage:  
                    fBac = None
                elif 'hospital' in self.buildingUsage:  
                    fBac = None
                elif 'hotel' in self.buildingUsage:  
                    fBac = 0.76
                elif 'restaurant' in self.buildingUsage:  
                    fBac = 0.60               
                elif 'wholesale and retail' in self.buildingUsage:  
                    fBac = 0.55                                                                    
                else:
                    fBac = None 
        else:
            if letra == 'D':
                fBac = 1.09
            elif letra == 'C':
                fBac = 1.0                
            elif letra == 'B':
                fBac = 0.88
            elif letra == 'A':
                fBac = 0.81                                                                                                        
        return fBac

    @property
    def FBacACS (self):
        if self.buildingType.id == 2:
            letra = self.getNotaResidentialAndNonResidential(self.calculoMatrizImpacto()) 
            if letra == 'D':
                fBac = 1.11
            elif letra == 'C':
                fBac = 1.00  
            elif letra == 'B':
                fBac = 0.90
            elif letra == 'A':
                fBac = 0.80
        else:
            if letra == 'D':
                fBac = 1.11
            elif letra == 'C':
                fBac = 1.00                
            elif letra == 'B':
                fBac = 0.90
            elif letra == 'A':
                fBac = 0.80                                                                                                        
        return fBac    

    @property
    def FBacElL (self):
        if self.buildingType.id == 2:
            letra = self.getNotaResidentialAndNonResidential(self.calculoMatrizImpacto()) 
            if letra == 'D':
                if  'office' in self.buildingUsage:
                    fBac = 1.1
                elif  'lecture hall' in self.buildingUsage:  
                    fBac = 1.1                    
                elif  'educational' in self.buildingUsage:  
                    fBac = 1.1
                elif 'hospital' in self.buildingUsage:  
                    fBac = 1.2
                elif 'hotel' in self.buildingUsage:  
                    fBac = 1.1    
                elif 'restaurant' in self.buildingUsage:  
                    fBac = 1.1               
                elif 'wholesale and retail' in self.buildingUsage:  
                    fBac = 1.1                                                                    
                else:
                    fBac = None
            elif letra == 'C':
                if  'office' in self.buildingUsage:
                    fBac = 1.0
                elif  'lecture hall' in self.buildingUsage:  
                    fBac = 1.0                    
                elif  'educational' in self.buildingUsage:  
                    fBac = 1.0
                elif 'hospital' in self.buildingUsage:  
                    fBac = 1.0
                elif 'hotel' in self.buildingUsage:  
                    fBac = 1.0    
                elif 'restaurant' in self.buildingUsage:  
                    fBac = 1.0               
                elif 'wholesale and retail' in self.buildingUsage:  
                    fBac = 1.0                                                                    
                else:
                    fBac = 1.0   
            elif letra == 'B':
                if  'office' in self.buildingUsage:
                    fBac = 0.85
                elif  'lecture hall' in self.buildingUsage:  
                    fBac = 0.88                    
                elif  'educational' in self.buildingUsage:  
                    fBac = 0.88
                elif 'hospital' in self.buildingUsage:  
                    fBac = 1.0
                elif 'hotel' in self.buildingUsage:  
                    fBac = 0.88  
                elif 'restaurant' in self.buildingUsage:  
                    fBac = 1.0               
                elif 'wholesale and retail' in self.buildingUsage:  
                    fBac = 1.0                                                                    
                else:
                    fBac = None 
            elif letra == 'A':
                if  'office' in self.buildingUsage:
                    fBac = 0.72
                elif  'lecture hall' in self.buildingUsage:  
                    fBac = 0.76                    
                elif  'educational' in self.buildingUsage:  
                    fBac = 0.76
                elif 'hospital' in self.buildingUsage:  
                    fBac = 1.0
                elif 'hotel' in self.buildingUsage:  
                    fBac = 0.76  
                elif 'restaurant' in self.buildingUsage:  
                    fBac = 1.0               
                elif 'wholesale and retail' in self.buildingUsage:  
                    fBac = 1.0                                                                    
                else:
                    fBac = None 
        else:
            fBac = None                                                                                                
        return fBac    

    @property
    def FBacEAux (self):
        if self.buildingType.id == 2:
            letra = self.getNotaResidentialAndNonResidential(self.calculoMatrizImpacto()) 
            if letra == 'D':
                if  'office' in self.buildingUsage:
                    fBac = 1.15
                elif  'lecture hall' in self.buildingUsage:  
                    fBac = 1.11                    
                elif  'educational' in self.buildingUsage:  
                    fBac = 1.12
                elif 'hospital' in self.buildingUsage:  
                    fBac = 1.1
                elif 'hotel' in self.buildingUsage:  
                    fBac = 1.12    
                elif 'restaurant' in self.buildingUsage:  
                    fBac = 1.09               
                elif 'wholesale and retail' in self.buildingUsage:  
                    fBac = 1.13                                                                    
                else:
                    fBac = None
            elif letra == 'C':
                if  'office' in self.buildingUsage:
                    fBac = 1.0
                elif  'lecture hall' in self.buildingUsage:  
                    fBac = 1.0                    
                elif  'educational' in self.buildingUsage:  
                    fBac = 1.0
                elif 'hospital' in self.buildingUsage:  
                    fBac = 1.0
                elif 'hotel' in self.buildingUsage:  
                    fBac = 1.0    
                elif 'restaurant' in self.buildingUsage:  
                    fBac = 1.0               
                elif 'wholesale and retail' in self.buildingUsage:  
                    fBac = 1.0                                                                    
                else:
                    fBac = 1.0   
            elif letra == 'B':
                if  'office' in self.buildingUsage:
                    fBac = 0.86
                elif  'lecture hall' in self.buildingUsage:  
                    fBac = 0.88                    
                elif  'educational' in self.buildingUsage:  
                    fBac = 0.87
                elif 'hospital' in self.buildingUsage:  
                    fBac = 0.98
                elif 'hotel' in self.buildingUsage:  
                    fBac = 0.89  
                elif 'restaurant' in self.buildingUsage:  
                    fBac = 0.96             
                elif 'wholesale and retail' in self.buildingUsage:  
                    fBac = 0.95                                                                  
                else:
                    fBac = None 
            elif letra == 'A':
                if  'office' in self.buildingUsage:
                    fBac = 0.72
                elif  'lecture hall' in self.buildingUsage:  
                    fBac = 0.78                    
                elif  'educational' in self.buildingUsage:  
                    fBac = 0.74
                elif 'hospital' in self.buildingUsage:  
                    fBac = 0.96
                elif 'hotel' in self.buildingUsage:  
                    fBac = 0.78  
                elif 'restaurant' in self.buildingUsage:  
                    fBac = 0.92             
                elif 'wholesale and retail' in self.buildingUsage:  
                    fBac = 0.91                                                                  
                else:
                    fBac = None 
        else:
            fBac = None                                                                                                
        return fBac        
    
    def getPuntuacionPonderadaMaxima(self, matrizFiltrada):
        puntuacionMaximaPonderadaPorDominio = sum([x[3] * x[4] for x in matrizFiltrada])  # Se multiplica la puntación del dominio por el peso.
        return puntuacionMaximaPonderadaPorDominio    
    
    def getPuntuacionPonderada(self, matrizFiltrada):
        puntuacionPonderadaPorDominio = sum([x[2] * x[4] for x in matrizFiltrada])  # Se multiplica la puntación del dominio por el peso.
        return puntuacionPonderadaPorDominio    
        
    def getListaPuntuacionPonderada(self, matriz):
        listaPuntacionesPonderadasPorImpacto = []
        
        for impacto in self.listadoNombreImpactos:
            tablaFiltradaPorImpacto = [x for x in matriz if x[0] == impacto]
            puntuacionPonderadaPorDominio = self.getPuntuacionPonderada(tablaFiltradaPorImpacto)
            listaPuntacionesPonderadasPorImpacto.append(puntuacionPonderadaPorDominio)
            
        return listaPuntacionesPonderadasPorImpacto
        
    def getListaPuntuacionPonderadaMaxima(self, matriz):
        listaPuntacionesMaximasPonderadasPorImpacto = []
        
        for impacto in self.listadoNombreImpactos:
            tablaFiltradaPorImpacto = [x for x in matriz if x[0] == impacto]
            puntuacionMaximaPonderadaPorDominio = self.getPuntuacionPonderadaMaxima(tablaFiltradaPorImpacto)
            listaPuntacionesMaximasPonderadasPorImpacto.append(puntuacionMaximaPonderadaPorDominio)
            
        return listaPuntacionesMaximasPonderadasPorImpacto
    
    def calculoImpactScore(self, matriz):
        impactScores = []
        for impacto in self.listadoNombreImpactos:
            tablaFiltradaPorImpacto = [x for x in matriz if x[0] == impacto]  # Se a�ade a la tabla si x[0] es el mismo impacto
            impactScores.append((self.getPuntuacionPonderada(tablaFiltradaPorImpacto) / self.getPuntuacionPonderadaMaxima(tablaFiltradaPorImpacto) * 100.0) if self.getPuntuacionPonderadaMaxima(tablaFiltradaPorImpacto) or self.getPuntuacionPonderada(tablaFiltradaPorImpacto) else '-')      
        return impactScores
        
    def getEnergyPerformannceKf1(self):
        matrizImpacto = self.calculoMatrizImpacto()
        impactScoreWeighting = [x / y * z if x or y else 0.0 for x, y, z in zip(self.getListaPuntuacionPonderada(matrizImpacto), 
                                                                                                         self.getListaPuntuacionPonderadaMaxima(matrizImpacto), 
                                                                                                         self.impactWeightings)] 
        kf1 = (impactScoreWeighting[0] + impactScoreWeighting[5]) / (self.impactWeightings[0] + self.impactWeightings[5]) * 100.0 # Es por el tema del reordenamiento
        self.scoreKF1 = kf1
        self.save()
        return kf1
        
    def getResponseToUserNeedsKf2(self):
        matrizImpacto = self.calculoMatrizImpacto()
        impactScoreWeighting = [x / y * z if x or y else 0.0  for x, y, z in zip(self.getListaPuntuacionPonderada(matrizImpacto), 
                                                                                                          self.getListaPuntuacionPonderadaMaxima(matrizImpacto), 
                                                                                                          self.impactWeightings)]
        kf2 = (impactScoreWeighting[2] + impactScoreWeighting[3] + impactScoreWeighting[4] + impactScoreWeighting[6]) / (self.impactWeightings[2] + self.impactWeightings[3] + self.impactWeightings[4] + self.impactWeightings[6]) * 100.0
        self.scoreKF2 = kf2
        self.save()
        return kf2
        
    def getEnergyFlexibilityKf3(self):
        impactScore = self.calculoImpactScore(self.calculoMatrizImpacto())
        kf3 = impactScore[1]
        self.scoreKF3 = kf3
        self.save()
        return kf3
        
    def getTotalSRI(self):
        if self.customDomain:
            if self.customDomainWeigthings:
                if self.customDomainWeigthings.customImpactWeighting and self.getEnergyPerformannceKf1(): 
                    totalSriScore = self.customDomainWeigthings.customImpactWeighting.kF1_energyPerformanceAndOperation * self.getEnergyPerformannceKf1()
                else:
                    totalSriScore = 0
                if self.customDomainWeigthings.customImpactWeighting and self.getResponseToUserNeedsKf2(): 
                    totalSriScore += self.customDomainWeigthings.customImpactWeighting.kF2_responseToUserNeeds * self.getResponseToUserNeedsKf2()
                else:  
                    totalSriScore += 0
                if self.customDomainWeigthings.customImpactWeighting and self.getEnergyFlexibilityKf3():
                    totalSriScore += self.customDomainWeigthings.customImpactWeighting.kF3_energyFlexibility * self.getEnergyFlexibilityKf3()
                else:
                    totalSriScore += 0
            else:
                totalSriScore = 0
        else:
            totalSriScore = self.domainWeigthing.impactWeighting.kF1_energyPerformanceAndOperation * self.getEnergyPerformannceKf1()
            totalSriScore += self.domainWeigthing.impactWeighting.kF2_responseToUserNeeds * self.getResponseToUserNeedsKf2()
            totalSriScore += self.domainWeigthing.impactWeighting.kF3_energyFlexibility * self.getEnergyFlexibilityKf3()
        
        totalSriScore = round(totalSriScore, 2)
        self.totalSriScore = totalSriScore
        self.save()
        
        return totalSriScore
    
    def representacionTablaImpactScore (self):
        impactScoreFormateado = []
        for numero in self.calculoImpactScore(self.calculoMatrizImpacto()):
            if type(numero) == float:
                impactScoreFormateado.append("{:0.0f}".format(numero))
            else:
                impactScoreFormateado.append(numero)
        return impactScoreFormateado
    
    def tablaImpactos(self, tablaBruta):
        ''' 
        Clase Proyecto
        Dominios filas
        '''
        # impactos = set([x[0] for x in tablaBruta])
        
        tabla = []
        for dominio in self.listadoNombreDominios:
            fila = []
            for impacto in self.listadoNombreImpactos:
                valor = next((x for x in tablaBruta if x[0] == impacto and x[1] == dominio), None)
                if valor:
                    fila.append(valor[2])
                else:
                    fila.append('-')
            tabla.append(fila)
        return tabla

    def tablaImpactosPD(self, tablaBruta):
        ''' 
        Clase Proyecto
        Dominios filas
        '''
        # impactos = set([x[0] for x in tablaBruta])
        
        tabla = self.tablaImpactos(tablaBruta)
            
        df = pd.DataFrame(tabla, columns = self.listadoNombreImpactosMostrar, index = self.listadoNombreDominiosMostrar)
    
        print(tabulate(df, headers = 'keys', tablefmt = 'psql'))  
        return df    
    
    def getClase(self, totalImpactScore):
        if self.country:
            listadoClases = self.country.domainClassNames.split(',')
            for _ in range(len(listadoClases),7):
                listadoClases.append('-')
                
        else:
            listadoClases = ['A','B','C','D','E','F','G']
             
        if totalImpactScore > 90: return listadoClases[0]
        elif totalImpactScore > 80: return listadoClases[1]
        elif totalImpactScore > 65: return listadoClases[2]
        elif totalImpactScore > 50: return listadoClases[3]
        elif totalImpactScore > 35: return listadoClases[4]
        elif totalImpactScore > 20: return listadoClases[5]
        else: return listadoClases[6]
    def getDicc15232Residential(self, tablaBruta):
        return tablaBruta[0][5]
    
    def getDicc15232NonResidential(self, tablaBruta):
        return tablaBruta[0][6]
        
    def getNotaResidentialAndNonResidential(self, matriz):
        if 'D' in matriz[0][5].values() or 'D' in matriz[0][6].values():
            letra = 'D'
        elif 'C' in matriz[0][5].values() or 'C' in matriz[0][6].values():
            letra = 'C'
        elif 'B' in matriz[0][5].values() or 'B' in matriz[0][6].values():
            letra = 'B'
        else:
            letra = 'A'
        return letra
        
    def tablaImpactosMaximos(self, tablaBruta):
        ''' 
        Clase Proyecto
        Dominios filas
        '''
                
        tabla = []
        for dominio in self.listadoNombreDominios:
            fila = []
            for impacto in self.listadoNombreImpactos:
                valor = next((x for x in tablaBruta if x[0] == impacto and x[1] == dominio), None)  # Añade el valor a la tabla si x[0] es el mismo impacto y x[1] es el mismo dominio
                if valor:
                    fila.append(valor[3])
                else:
                    fila.append('-')
            tabla.append(fila)
        return tabla
        
    def tablaImpactosMaximosPD(self, tablaBruta):
        ''' 
        Clase Proyecto
        Dominios filas
        '''
        tabla = self.tablaImpactosMaximos(tablaBruta)
        df = pd.DataFrame(tabla, columns = self.listadoNombreImpactosMostrar, index = self.listadoNombreDominiosMostrar)
    
        print(tabulate(df, headers = 'keys', tablefmt = 'psql'))
        return df
    
    
    def tablaScoresDetallados(self, tablaBruta):
        ''' 
        Clase Proyecto
        Dominios filas
        '''        
        tabla = []
        for dominio in self.listadoNombreDominios:
            fila = []
            for impacto in self.listadoNombreImpactos:
                valor = next((x for x in tablaBruta if x[0] == impacto and x[1] == dominio), None)
                if valor:
                    fila.append(valor[2] / valor[3] * 100.0 if valor[3] else None)
                else:
                    fila.append(None)
            tabla.append(fila)
        return tabla
        
        # impactScores = []
        
        # listaPuntuacionesPonderadasPorImpacto = []
        # listaPuntacionesMaximasPonderadasPorImpacto = []
        # for impacto in self.listadoNombreImpactos:
        #     tablaFiltradaPorImpacto = [x for x in tablaBruta if x[0] == impacto]  # Se a�ade a la tabla si x[0] es el mismo impacto
        #     puntuacionPonderadaPorDominio = sum([x[2] * x[4] for x in tablaFiltradaPorImpacto])  # Se multiplica la puntaci�n del dominio por el peso.
        #     listaPuntuacionesPonderadasPorImpacto.append(puntuacionPonderadaPorDominio)
        #
        #     puntuacionMaximaPonderadaPorDominio = sum([x[3] * x[4] for x in tablaFiltradaPorImpacto])  # Se multiplica la puntuaci�n m�xima por dominio por el peso.
        #     listaPuntacionesMaximasPonderadasPorImpacto.append(puntuacionMaximaPonderadaPorDominio)
        #
        #     impactScores.append("{:0.0f}".format(puntuacionPonderadaPorDominio / puntuacionMaximaPonderadaPorDominio * 100.0) if puntuacionMaximaPonderadaPorDominio else '-')                   
        
    def tablaScoresDetalladosPD(self, tablaBruta):
        ''' 
        Clase Proyecto
        Dominios filas
        '''        
        print("Detailed scores")
        tabla = self.tablaScoresDetallados(tablaBruta)    
        tablaFormateada = []
        for fila in tabla:
            filaFormateada = []
            sumaPonderada = 0.0
            sumaPesos = 0.0
            for elemento,peso in zip(fila,self.impactWeightings) :
                filaFormateada.append("{:0.0f}%".format(elemento) if elemento != None else '-')
                if elemento != None:
                    sumaPonderada += elemento * peso
                    sumaPesos += peso
            impactoPorDominio = sumaPonderada / sumaPesos if sumaPesos else 0.0
            filaFormateada.append("{:0.0f}%".format(impactoPorDominio) if impactoPorDominio else '-')
                
                    
            tablaFormateada.append(filaFormateada)
        
        df = pd.DataFrame(tablaFormateada, columns = self.listadoNombreImpactosMostrar + ['Domain SRI'], index = self.listadoNombreDominiosMostrar)
        print(tabulate(df, headers = 'keys', tablefmt = 'psql'))
        return df
        
     
    def repAuxialiaryTable(self):
            
        df = pd.DataFrame([self.getListaPuntuacionPonderada(self.calculoMatrizImpacto()),
                            self.getListaPuntuacionPonderadaMaxima(self.calculoMatrizImpacto()),
                            self.impactWeightings], columns = self.listadoNombreImpactosMostrar, index = ['Impact scores weighted by domain', 'Maximum impact scores weighted by domain', 'Impact Weightings'])
        
        print("Auxiliary table with scores weighted by domain")    
        print(tabulate(df, headers = 'keys', tablefmt = 'psql'))
        return df

    def listaAggregatedScores(self):
        
        lista = []
        lista.append(self.getEnergyPerformannceKf1())
        lista.append(self.getResponseToUserNeedsKf2())
        lista.append(self.getEnergyFlexibilityKf3())
        
        return lista
        

        
        
    def calculoMatrizImpacto(self):
        '''
        
        Clase Proyecto
         
        '''
    
        listadoDatos = self.datos.all()
        evaluacionImpactos = {}
        evaluacionImpactosMaximos = {}
        evaluacionPesos = {}
        dicEnResidential15232 = {}
        dicEnNonResidential15232 = {}
        matrizImpactos = []
        for nombreImpacto in self.listadoNombreImpactos:
            # print(f"Impacto: {nombreImpacto}")
            for dominio in self.dominiosPresentes:
                listadoDatosDominio = [x for x in listadoDatos if x.chosenFuncionality.service.dominio == dominio and x.percentage > 0.0]
                listadoPreguntas = []
                listadoMaximos = []
                evaluacionImpactos[nombreImpacto] = [dato.impact(nombreImpacto) for dato in listadoDatosDominio]
                dicEnResidential15232[dominio.description] = ""
                dicEnNonResidential15232[dominio.description] = ""
                for dato in listadoDatosDominio:
                    if dato.chosenFuncionality.en15232Residential != "" and dato.chosenFuncionality.en15232Residential != "-":
                        if dato.chosenFuncionality.en15232Residential == "D":
                            dicEnResidential15232[dominio.description] = dato.chosenFuncionality.en15232Residential
                        elif dato.chosenFuncionality.en15232Residential == "C" and dicEnResidential15232[dominio.description] != "D":
                            dicEnResidential15232[dominio.description] = dato.chosenFuncionality.en15232Residential
                        elif dato.chosenFuncionality.en15232Residential == "B" and dicEnResidential15232[dominio.description] != "C" and dicEnResidential15232[dominio.description] != "D":
                            dicEnResidential15232[dominio.description] = dato.chosenFuncionality.en15232Residential
                        elif dato.chosenFuncionality.en15232Residential == "A" and dicEnResidential15232[dominio.description] != "D" and dicEnResidential15232[dominio.description] != "C" and dicEnResidential15232[dominio.description] != "B":
                            dicEnResidential15232[dominio.description] = dato.chosenFuncionality.en15232Residential
                        else:
                            pass
                            
                    if dato.chosenFuncionality.en15232NonResidential != "" and dato.chosenFuncionality.en15232NonResidential != "-":
                        if dato.chosenFuncionality.en15232NonResidential == "D": 
                            dicEnNonResidential15232[dominio.description] = dato.chosenFuncionality.en15232NonResidential
                        elif dato.chosenFuncionality.en15232NonResidential == "C" and dicEnNonResidential15232[dominio.description] != "D":
                            dicEnNonResidential15232[dominio.description] = dato.chosenFuncionality.en15232NonResidential
                        elif dato.chosenFuncionality.en15232NonResidential == "B" and dicEnNonResidential15232[dominio.description] != "C" and dicEnNonResidential15232[dominio.description] != "D":
                            dicEnNonResidential15232[dominio.description] = dato.chosenFuncionality.en15232NonResidential
                        elif dato.chosenFuncionality.en15232NonResidential == "A" and dicEnNonResidential15232[dominio.description] != "B" and dicEnNonResidential15232[dominio.description] != "C" and dicEnNonResidential15232[dominio.description] != "D":
                            dicEnNonResidential15232[dominio.description] = dato.chosenFuncionality.en15232NonResidential
                        else:
                            pass
                                
                    if dato.chosenFuncionality.service.id not in listadoPreguntas:
                        listadoPreguntas.append(dato.chosenFuncionality.service.id)  
                        listadoMaximos.append(dato.impactoMaximo(nombreImpacto))
                evaluacionImpactosMaximos[nombreImpacto] = listadoMaximos
                # evaluacionImpactosMaximos[nombreImpacto] = [dato.impactoMaximo(nombreImpacto) for dato in listadoDatosDominio]
                evaluacionPesos[nombreImpacto] = [dato.peso(nombreImpacto) for dato in listadoDatosDominio]
                
                puntuacionDominio = sum(evaluacionImpactos[nombreImpacto])
                puntuacionDominioMaxima = sum(evaluacionImpactosMaximos[nombreImpacto])
                
                if len(evaluacionPesos[nombreImpacto]) != 0:
                    
                    peso = evaluacionPesos[nombreImpacto][0]  # Todos tienen el mismo peso
                
                # print("{}: {} / {} = {:0.2f} x {:0.2f}".format(dominio.description,
                #                                                puntuacionDominio,
                #                                                puntuacionDominioMaxima,
                #                                                puntuacionDominio/puntuacionDominioMaxima if puntuacionDominioMaxima else 0.0,peso))
                
                    matrizImpactos.append([nombreImpacto, dominio.description, puntuacionDominio, puntuacionDominioMaxima, peso, dicEnResidential15232, dicEnNonResidential15232])
                    # print(self.FBacTh)
        return matrizImpactos
    
    @property
    def impactWeightings(self):
        if self.customDomain:
            if self.customDomainWeigthings != None:
                impactWeightings = self.customDomainWeigthings.customImpactWeighting.getLista()  
            else:
                impactWeightings = [0.17, 0.33, 0.08, 0.08, 0.08, 0.17, 0.08]
        else:
            impactWeightings = self.domainWeigthing.impactWeighting.getLista()
            
        return impactWeightings
                    
            
    def sri(self):
        matrizImpactos = self.calculoMatrizImpacto()
        calculado = False
        if matrizImpactos:
            tablaImpactosResultado = self.tablaImpactosPD(matrizImpactos)
            tablaImpactoMaximosResultado = self.tablaImpactosMaximosPD(matrizImpactos)
            tablaScores = self.tablaScoresDetalladosPD(matrizImpactos)

            listaImpactScores = self.representacionTablaImpactScore()
            totalSri = self.getTotalSRI()
            tablaAuxiliary = self.repAuxialiaryTable()
            listaAggregatedScores = self.listaAggregatedScores()
            letraCalificacion = self.getClase(totalSri)
            resultadoResidential = self.getNotaResidentialAndNonResidential(matrizImpactos)
            dicc15232Residential = self.getDicc15232Residential(matrizImpactos)
            dicc15232NonResidential = self.getDicc15232NonResidential(matrizImpactos)
            calculado = True       
            return [calculado, tablaImpactosResultado, tablaImpactoMaximosResultado, tablaScores, tablaAuxiliary, listaImpactScores, listaAggregatedScores, totalSri, letraCalificacion, resultadoResidential, dicc15232Residential, dicc15232NonResidential]
        else:
            return [calculado, ]

    
class Dato(Model):
    
    objects = Manager()
    
    chosenFuncionality = ForeignKey(Funcionalidad,
                                    verbose_name = 'Functionality',
                                    related_name = 'datos')
    
    proyect = ForeignKey(Proyecto,
                         verbose_name = 'Project',
                         related_name = 'datos',)
    
    comments = CharField(default = '',
                         max_length = 5000,
                         verbose_name = 'Comment')
    
    justification = CharField(default = '',
                              max_length = 5000,
                              verbose_name = 'Justification') 
    
    percentage = FloatField(verbose_name = 'Percentage',                            
                            default = 100.0,
                            min = 0.0,
                            max = 100)
    
    class Meta:
        verbose_name = 'Datum'
        verbose_name_plural = '5.Data'
        ordering = ('id',)
        
    def __str__(self):
        ''' 
        Clase Dato
        
        '''
        return '{2}: {0}, {3}: {1}'.format(self.proyect.id, self.chosenFuncionality.id, 'Project', 'Functionality')
        
    def duplicar(self, padre = None):
        ''' 
        Clase Dato
        
        '''
            
        self.id = None
        self.pk = None
        if (padre != None):
            self.proyect = padre
        self.save()
        
        return self
    
    def impact(self, impacto = ''):
        resultado = self.percentage * getattr(self.chosenFuncionality, '{}Impact'.format(impacto)) / 100
        return resultado
    
    def impactoMaximo (self, impacto = ''):
        if self.chosenFuncionality.description == 'Not applicable' or self.chosenFuncionality.description.replace(" ","").upper() == 'N/A' or self.chosenFuncionality.description.replace(" ","").upper() == 'N/A' :
            return 0.0
        return self.chosenFuncionality.service.getImpactMax(impacto = impacto)
    
    def peso (self, impacto = ''):
        if self.proyect.customDomain:
            pesos = self.proyect.customDomainWeigthings
        else:
            pesos = self.proyect.domainWeigthing
        dominio = self.chosenFuncionality.service.dominio.nameAttr
        if pesos:
            peso = getattr(pesos, '{}{}'.format(impacto, dominio))
        else:
            peso = 0.0
        return peso
                     
    