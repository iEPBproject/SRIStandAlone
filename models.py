# # -\*- coding: utf-8 -\*-
import copy

from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.fields import , FloatField, BooleanField
from django.utils.translation import gettext_lazy as _
from tabulate import tabulate

import pandas as pd


from librerias.miDjangoModel3.models import Model,CharField


class BuildingType(Model):
    description = CharField(default = '',
                            max_length = 100,
                            verbose_name = _('Description'))
                            
    def __str__(self):
        ''' 
        Clase BuildindgType
        
        '''
        
        return f"{_(self.description)}"
        
    class Meta:
        verbose_name = _('Buiding Type')
        verbose_name_plural = _('11. Buiding Type')

class Country(models.Model):
    name = CharField(default = '',
                       max_length = 1000,
                       verbose_name = _("Name"))
    
    heatingMandatory = BooleanField(default = True, verbose_name = _("Mandatory Heating Domain"), help_text = _("Is heating a mandatory domain?"))
    dhwMandatoryForResidential = BooleanField(default = True, verbose_name = _("Mandatory DWH for residential Domain"), help_text = _("Is DHW  a mandatory domain?"))
    dhwMandatoryForTertiary = BooleanField(default = True, verbose_name = _("Mandatory DWH for tertiary Domain"), help_text = _("Is DHW  a mandatory domain?"))
    CoolingMandatory = BooleanField(default = True, verbose_name = _("Mandatory Cooling Domain"), help_text = _("Is Cooling a mandatory domain?"))
    VentilationMandatory = BooleanField(default = True, verbose_name = _("Mandatory Ventilation Domain"), help_text = _("Is Ventilation  a mandatory domain?"))
    LightingMandatory = BooleanField(default = True, verbose_name = _("Mandatory Lighting Domain"), help_text = _("Is Lighting  a mandatory domain?"))
    DynamicBuildingEnvelopeMandatory = BooleanField(default = True, verbose_name = _("Mandatory Dynamic Building Envelope Domain"), help_text = _("Is Dynamic Building Envelope  a mandatory domain?"))
    ElectricityMandatory = BooleanField(default = True, verbose_name = _("Mandatory Electricity Domain"), help_text = _("Is Electricity a mandatory domain?"))
    ElectricVehicleChargingMandatory = BooleanField(default = True, verbose_name = _("Mandatory Electric Vehicle Charging Domain"), help_text = _("Is Electric Vehicle Charging  a mandatory domain?"))
    MonitoringAndControlMandatory = BooleanField(default = True, verbose_name = _("Mandatory Monitoring And Control Domain"), help_text = _("Is Monitoring and Control  a mandatory domain?"))    
    
    domainClassNames = models.CharField(default = 'A,B,C,D,E,F,G',
                                                        max_length = 1000,
                                                        verbose_name = _("Class names list (separated by comma) with 7 class names"))
    
    
    allowUserDefineDomainWeightings = BooleanField(default = False, verbose_name = _("Allow user defined domain weightings"), )

    def __str__(self):
        ''' 
        Clase Country
        
        '''
        return 'Id: {} - {} '.format(self.id, _(self.name))

    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('6. Country')
        ordering = ('id',)


class Catalogo(models.Model):
    
    description = models.CharField(default = '',
                                  max_length = 1000,
                                  verbose_name = _("Description"))
    
    country = models.ManyToManyField(Country,
                                     blank = True,
                                     verbose_name = _('Country'),
                                     related_name = 'catalogos',
                                     help_text = _('Multiple selection/deselection: use the CTRL key'),)
                                     
    buildingType = models.ManyToManyField(BuildindgType,
                                          blank = True,
                                          verbose_name = _('Building Types'),
                                          related_name = 'catalogos',
                                          help_text = _('Multiple selection/deselection: use the CTRL key'),)
                  
    class Meta:
        verbose_name = _('Catalogue')
        verbose_name_plural = _('1.Catalogue')
        ordering = ('id',)

    def __str__(self):
        ''' 
        Clase Catalogo
        
        '''
        return str(_(self.description))

    @property
    def tieneDatos(self):
        return True
    
    def delete(self, using=None, keep_parents=False):
        if self.tieneDatos:
            return False
        return models.Model.delete(self, using=using, keep_parents=keep_parents)
    def duplicar(self, padre = None): 
        ''' 
        Clase Catalogo
        
        '''         
        copyId = copy.deepcopy(self.id) 
        
        if hasattr(self, 'description'):
            self.description = self.description + _(' copy')
        
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

class Climate(models.Model):
    description = CharField(default = '',
                            max_length = 1000,
                            verbose_name = _("Description"))
    country = models.ManyToManyField(Country,
                                     blank = True,
                                     verbose_name = _('Countries'),
                                     related_name = 'climates',
                                     help_text = _('Multiple selection/deselection: use the CTRL key'),)

    def __str__(self):
        ''' 
        Clase Climate
        
        '''
        return 'Id: {} - {} '.format(self.id, _(self.description))

    class Meta:
        verbose_name = _('Climate')
        verbose_name_plural = _('9. Climate')
        ordering = ('id',)
    
class Dominio(models.Model):
    
    catalogo = models.ForeignKey(Catalogo,
                                  verbose_name = _('Catalogue'),
                                  related_name = 'dominios',
                                  on_delete = models.CASCADE)
    
    description = models.CharField(default = '',
                                  max_length = 1000,
                                  verbose_name = _("Description"))
    
    nameAttr = models.CharField(default = '',  # Este campo se va a utilizar para los getatt() de los campos.
                                max_length = 1000,
                                verbose_name = _("Name Attribute"))
                  
    class Meta:
        verbose_name = _('Domain')
        verbose_name_plural = _('2.Domain')
        ordering = ('id',)

    def __str__(self):
        ''' 
        Clase Dominio
        
        '''
        return f"{_(self.description)}"
    
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
    
    def getForm(self, proyectoId = None):
        '''
        Clase Dominio
        '''
        from sri.forms import DominioForm
        new_fields = {}
        for servicio in self.servicios.all():
            choices1 = [] 
            cont = 0
            for x in servicio.funcionalidades.all(): choices1.append((x.id, _(x.description)))
            listadoDatos = Dato.objects.filter(chosenFuncionality__service__id = servicio.id, proyect = proyectoId)
            porcTotal = 0
            # if len(listadoDatos) == 0:
            new_fields['{0}--{1}--{2}'.format(servicio.id, 'Choice', cont) ] = forms.ChoiceField(label = _(servicio.description),
                                                                                                help_text = _(servicio.description),
                                                                                                choices = choices1)
    
            new_fields['{0}--{1}--{2}'.format(servicio.id, 'Percentage', cont) ] = forms.FloatField(label = _('Percentage'),
                                                                                                   help_text = _(servicio.description),
                                                                                                   initial = 100.0,
                                                                                                   validators=[MinValueValidator(0.0),MaxValueValidator(100.0, u"Please introduce a lower value")])
                
            new_fields['{0}--{1}--{2}'.format(servicio.id, 'Justificacion', cont) ] = forms.CharField(widget = CKEditorUploadingWidget(),
                                                                                                      label = _('Justification'),
                                                                                                      help_text = _(servicio.description),
                                                                                                      required = False)
            
            new_fields['{0}--{1}--{2}'.format(servicio.id, 'Comentario', cont) ] = forms.CharField(widget = CKEditorUploadingWidget(),
                                                                                                   label = _('Comments'),
                                                                                                   help_text = _(servicio.description),
                                                                                                   required = False)
            # else:
                
            for dato in listadoDatos:
                porcTotal += dato.percentage
                if porcTotal < 100.: 
                    cont += 1
                                   
                    new_fields['{0}--{1}--{2}'.format(servicio.id, 'Choice', cont) ] = forms.ChoiceField(label = _(servicio.description),
                                                                         help_text = _(servicio.description),
                                                                         choices = choices1)
                    
                    new_fields['{0}--{1}--{2}'.format(servicio.id, 'Percentage', cont) ] = forms.FloatField(label = _('Percentage'),
                                                                                           help_text = _(servicio.description),
                                                                                           initial = 100 - porcTotal)
                    
                    new_fields['{0}--{1}--{2}'.format(servicio.id, 'Justificacion', cont) ] = forms.CharField(widget = CKEditorUploadingWidget(),
                                                                                            label = _('Justification'),
                                                                                            help_text = _(servicio.description),
                                                                                            required = False)
                    
                    new_fields['{0}--{1}--{2}'.format(servicio.id, 'Comentario', cont) ] = forms.CharField(widget = CKEditorUploadingWidget(),
                                                                                            label = _('Comments'),
                                                                                            help_text = _(servicio.description),
                                                                                            required = False)
        
        DynamicDominionForm = type('DynamicDominionForm', (DominioForm,), new_fields)
        
        return DynamicDominionForm

    
class Servicio(models.Model):
    
    dominio = models.ForeignKey(Dominio,
                              verbose_name = _('Domain'),
                              related_name = 'servicios',
                              on_delete = models.CASCADE)
    
    description = models.CharField(default = '',
                                  max_length = 1000,
                                  verbose_name = _("Description"))

    reference = models.CharField(default = '',
                                  max_length = 20,
                                  verbose_name = _("Reference code"))    
                  
    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('3.Service')
        ordering = ('id',)

    def __str__(self):
        ''' 
        Clase Servicio
        
        '''
        return str(_(self.description))
    
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

    
class Funcionalidad(models.Model):
    
    service = models.ForeignKey(Servicio,
                                verbose_name = _('Service'),
                                related_name = 'funcionalidades',
                                on_delete = models.CASCADE)
    
    description = models.CharField(default = '',
                                  max_length = 1000,
                                  verbose_name = _("Description"))

    reference = models.CharField(default = '',
                                  max_length = 20,
                                  verbose_name = _("Reference code"))        
    
    energyEfficiencyImpact = models.FloatField(default = 0.0,
                                        verbose_name = _('Energy efficiency'))
    
    energyFlexibilityImpact = models.FloatField(default = 0.0,
                                          verbose_name = _('Energy flexibility and storage'))
    
    comfortImpact = models.FloatField(default = 0.0,
                                      verbose_name = _('Comfort'))
    convenienceImpact = models.FloatField(default = 0.0,
                                         verbose_name = _('Convenience'))
    healthAccesibilityImpact = models.FloatField(default = 0.0,
                                          verbose_name = _('Health, well-being and accessibility'))
    maintenanceFaultPredictionImpact = models.FloatField(default = 0.0,
                                          verbose_name = _('Maintenance and fault prediction'))
    informationOccupantsImpact = models.FloatField(default = 0.0,
                                          verbose_name = _('Information to occupants'))
                                          
    en15232Residential = CharField(choices = [('-', '-'),('A', _('A')), ('B', _('B')), ('C', _('C')), ('D', _('D'))],
                                       max_length = 1000,
                                       verbose_name = _(u"ISO 52120-1:2021 (Residential)"),
                                       default = '-')
                                       
    en15232NonResidential = CharField(choices = [('-', '-'),('A', _('A')), ('B', _('B')), ('C', _('C')), ('D', _('D'))],
                                       max_length = 1000,
                                       verbose_name = _(u"ISO 52120-1:2021 (Non-residential)"),
                                       default = '-')
                  
    class Meta:
        verbose_name = _('Functionality')
        verbose_name_plural = _('4.Functionality')
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

    
class ImpactWeightings (models.Model):
    
    energyEfficiency = FloatField(verbose_name = _('Energy Efficiency'),
                                  default = 0.0)
    
    energyFlexibility = FloatField(verbose_name = _('Energy flexibility and storage'),
                                   default = 0.0)
    
    comfort = FloatField(verbose_name = _('Comfort'),
                         default = 0.0)
    
    convenience = FloatField(verbose_name = _('Convenience'),
                             default = 0.0)
    
    healthAccesibility = FloatField(verbose_name = _('Health, well-being and accessibility'),
                                    default = 0.0)
    
    maintenanceFaultPrediction = FloatField(verbose_name = _('Maintenance and fault prediction'),
                                           default = 0.0)
    informationOccupants = FloatField(verbose_name = _('Information to occupants'),
                                      default = 0.0)
    
    kF1_energyPerformanceAndOperation = FloatField(verbose_name = _('KF1: Energy performance'),
                                                                            help_text = "Key functionality 1: Energy performance and operation",
                                                                            default = 1.0 / 3.0)
    
    kF2_responseToUserNeeds = FloatField(verbose_name = _('KF2: Response to user needs'),
                                                                            help_text = "Key functionality 1: Response to user needs",
                                                                            default = 1.0 / 3.0)
    
    kF3_energyFlexibility = FloatField(verbose_name = _('KF3: Energy flexibility'),
                                                                            help_text = "Key functionality 3: Energy flexibility",
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
        verbose_name = _('Impact Weighting')
        verbose_name_plural = _('8.Impact Weighting')
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
        
class CustomImpactWeightings(models.Model):
    
    energyEfficiency = FloatField(verbose_name = _('Energy Efficiency'),
                                  default = 0.0)
    
    energyFlexibility = FloatField(verbose_name = _('Energy flexibility and storage'),
                                   default = 0.0)
    
    comfort = FloatField(verbose_name = _('Comfort'),
                         default = 0.0)
    
    convenience = FloatField(verbose_name = _('Convenience'),
                             default = 0.0)
    
    healthAccesibility = FloatField(verbose_name = _('Health, well-being and accessibility'),
                                    default = 0.0)
    
    maintenanceFaultPrediction = FloatField(verbose_name = _('Maintenance and fault prediction'),
                                           default = 0.0)
    informationOccupants = FloatField(verbose_name = _('Information to occupants'),
                                      default = 0.0)
    
    kF1_energyPerformanceAndOperation = FloatField(verbose_name = _('KF1: Energy performance'),
                                                                            help_text = "Key functionality 1: Energy performance and operation",
                                                                            default = 1.0 / 3.0)
    
    kF2_responseToUserNeeds = FloatField(verbose_name = _('KF2: Response to user needs'),
                                                                            help_text = "Key functionality 1: Response to user needs",
                                                                            default = 1.0 / 3.0)
    
    kF3_energyFlexibility = FloatField(verbose_name = _('KF3: Energy flexibility'),
                                                                            help_text = "Key functionality 3: Energy flexibility",
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
        verbose_name = _('Custom Impact Weighting')
        verbose_name_plural = _('13.Custom Impact Weighting')
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

class DomainWeigthing(models.Model):

    name = models.CharField(default = '',
                              max_length = 1000,
                              verbose_name = _("Name"))
                              
    country = models.ManyToManyField(Country,
                                     blank = True,
                                     verbose_name = _('Countries'),
                                     related_name = 'domaingWeightings',
                                     help_text = _('Multiple selection/deselection: use the CTRL key'),)
                                     
    catalogo = models.ManyToManyField(Catalogo,
                                      blank = True,
                                      verbose_name = _('Catalogue'),
                                      related_name = 'domaingWeightings',
                                      help_text = _('Multiple selection/deselection: use the CTRL key'),)
    
    climate = models.ManyToManyField(Climate,
                                   blank = True,
                                   verbose_name = _('Climates'),
                                   related_name = 'domaingWeightings',
                                   help_text = _('Multiple selection/deselection: use the CTRL key'),)
    
    impactWeighting = models.ForeignKey(ImpactWeightings,
                         verbose_name = _('Impact Weightings'),
                         related_name = 'impact_weigthing',
                         blank = True,
                         null = True,
                         on_delete = models.DO_NOTHING)
                         
    buildingType = models.ManyToManyField(BuildindgType,
                                          blank = True,
                                          verbose_name = _('Building Types'),
                                          related_name = 'domaingWeightings',
                                          help_text = _('Multiple selection/deselection: use the CTRL key'),)
    
    energyEfficiencyHeating = FloatField(verbose_name = _('Energy efficiency heating'),
                                         default = 0.0)

    energyFlexibilityHeating = FloatField(verbose_name = _('Energy flexibility heating'),
                                         default = 0.0)

    comfortHeating = FloatField(verbose_name = _('Comfort heating'),
                                default = 0.0)

    convenienceHeating = FloatField(verbose_name = _('Convenience heating'),
                                    default = 0.0)

    healthAccesibilityHeating = FloatField(verbose_name = _('Health, well-being and accessibility heating'),
                                           default = 0.0)

    maintenanceFaultPredictionHeating = FloatField(verbose_name = _('Maintenance and fault prediction heating'),
                                                   default = 0.0)
    
    informationOccupantsHeating = FloatField(verbose_name = _('Information to occupants heating'),
                                             default = 0.0)
    
    energyEfficiencyCooling = FloatField(verbose_name = _('Energy efficiency Cooling'),
                                         default = 0.0)

    energyFlexibilityCooling = FloatField(verbose_name = _('Energy flexibility Cooling'),
                                          default = 0.0)

    comfortCooling = FloatField(verbose_name = _('Comfort Cooling'),
                                default = 0.0)

    convenienceCooling = FloatField(verbose_name = _('Convenience Cooling'),
                                    default = 0.0)

    healthAccesibilityCooling = FloatField(verbose_name = _('Health, well-being and accessibility Cooling'),
                                           default = 0.0)

    maintenanceFaultPredictionCooling = FloatField(verbose_name = _('Maintenance and fault prediction Cooling'),
                                                   default = 0.0)
    
    informationOccupantsCooling = FloatField(verbose_name = _('Information to occupants Cooling'),
                                             default = 0.0)
    
    energyEfficiencyDhw = FloatField(verbose_name = _('Energy efficiency DHW'),
                                     default = 0.0)

    energyFlexibilityDhw = FloatField(verbose_name = _('Energy flexibility DHW'),
                                      default = 0.0)

    comfortDhw = FloatField(verbose_name = _('Comfort DHW'),
                           default = 0.0)

    convenienceDhw = FloatField(verbose_name = _('Convenience DHW'),
                                  default = 0.0)

    healthAccesibilityDhw = FloatField(verbose_name = _('Health, well-being and accessibility DHW'),
                                       default = 0.0)

    maintenanceFaultPredictionDhw = FloatField(verbose_name = _('Maintenance and fault prediction DHW'),
                                               default = 0.0)
    
    informationOccupantsDhw = FloatField(verbose_name = _('Information to occupants DHW'),
                                         default = 0.0)
    
    energyEfficiencyVentilation = FloatField(verbose_name = _('Energy efficiency Ventilation'),
                                             default = 0.0)

    energyFlexibilityVentilation = FloatField(verbose_name = _('Energy flexibility Ventilation'),
                                              default = 0.0)

    comfortVentilation = FloatField(verbose_name = _('Comfort Ventilation'),
                                    default = 0.0)

    convenienceVentilation = FloatField(verbose_name = _('Convenience Ventilation'),
                                       default = 0.0)

    healthAccesibilityVentilation = FloatField(verbose_name = _('Health, well-being and accessibility Ventilation'),
                                               default = 0.0)

    maintenanceFaultPredictionVentilation = FloatField(verbose_name = _('Maintenance and fault prediction Ventilation'),
                                                       default = 0.0)
    
    informationOccupantsVentilation = FloatField(verbose_name = _('Information to occupants Ventilation'),
                                                 default = 0.0)
    
    energyEfficiencyLighting = FloatField(verbose_name = _('Energy efficiency Lighting'),
                                          default = 0.0)

    energyFlexibilityLighting = FloatField(verbose_name = _('Energy flexibility Lighting'),
                                           default = 0.0)
    comfortLighting = FloatField(verbose_name = _('Comfort Lighting'),
                                 default = 0.0)

    convenienceLighting = FloatField(verbose_name = _('Convenience Lighting'),
                                     default = 0.0)

    healthAccesibilityLighting = FloatField(verbose_name = _('Health, well-being and accessibility Lighting'),
                                            default = 0.0)

    maintenanceFaultPredictionLighting = FloatField(verbose_name = _('Maintenance and fault prediction Lighting'),
                                                    default = 0.0)
    
    informationOccupantsLighting = FloatField(verbose_name = _('Information to occupants Lighting'),
                                              default = 0.0)
    
    energyEfficiencyElectricity = FloatField(verbose_name = _('Energy efficiency Electricity'),
                                             default = 0.0)

    energyFlexibilityElectricity = FloatField(verbose_name = _('Energy flexibility Electricity'),
                                              default = 0.0)
    comfortElectricity = FloatField(verbose_name = _('Comfort Electricity'),
                                    default = 0.0)

    convenienceElectricity = FloatField(verbose_name = _('Convenience Electricity'),
                                       default = 0.0)

    healthAccesibilityElectricity = FloatField(verbose_name = _('Health, well-being and accessibility Electricity'),
                                               default = 0.0)

    maintenanceFaultPredictionElectricity = FloatField(verbose_name = _('Maintenance and fault prediction Electricity'),
                                                       default = 0.0)
    
    informationOccupantsElectricity = FloatField(verbose_name = _('Information to occupants Electricity'),
                                                 default = 0.0)
    
    energyEfficiencyDynamicBuildingEnvelope = FloatField(verbose_name = _('Energy efficiency Dynamic Building Envelope'),
                                                         default = 0.0)

    energyFlexibilityDynamicBuildingEnvelope = FloatField(verbose_name = _('Energy flexibility Dynamic Building Envelope'),
                                                          default = 0.0)
    comfortDynamicBuildingEnvelope = FloatField(verbose_name = _('Comfort Dynamic Building Envelope'),
                                                default = 0.0)

    convenienceDynamicBuildingEnvelope = FloatField(verbose_name = _('Convenience Dynamic Building Envelope'),
                                                   default = 0.0)

    healthAccesibilityDynamicBuildingEnvelope = FloatField(verbose_name = _('Health, well-being and accessibility Dynamic Building Envelope'),
                                                           default = 0.0)

    maintenanceFaultPredictionDynamicBuildingEnvelope = FloatField(verbose_name = _('Maintenance and fault prediction Dynamic Building Envelope'),
                                                                   default = 0.0)
    
    informationOccupantsDynamicBuildingEnvelope = FloatField(verbose_name = _('Information to occupants Dynamic Building Envelope'),
                                                             default = 0.0)
    
    energyEfficiencyElectricVehicleCharging = FloatField(verbose_name = _('Energy efficiency Electric Vehicle Charging'),
                                                         default = 0.0)

    energyFlexibilityElectricVehicleCharging = FloatField(verbose_name = _('Energy flexibility Electric Vehicle Charging'),
                                                          default = 0.0)
    comfortElectricVehicleCharging = FloatField(verbose_name = _('Comfort Electric Vehicle Charging'),
                                                default = 0.0)

    convenienceElectricVehicleCharging = FloatField(verbose_name = _('Convenience Electric Vehicle Charging'),
                                                    default = 0.0)

    healthAccesibilityElectricVehicleCharging = FloatField(verbose_name = _('Health, well-being and accessibility Electric Vehicle Charging'),
                                                           default = 0.0)

    maintenanceFaultPredictionElectricVehicleCharging = FloatField(verbose_name = _('Maintenance and fault prediction Electric Vehicle Charging'),
                                                                   default = 0.0)
    
    informationOccupantsElectricVehicleCharging = FloatField(verbose_name = _('Information to occupants Electric Vehicle Charging'),
                                                             default = 0.0)
    
    energyEfficiencyMonitoringAndControl = FloatField(verbose_name = _('Energy efficiency Monitoring and Control'),
                                                      default = 0.0)

    energyFlexibilityMonitoringAndControl = FloatField(verbose_name = _('Energy flexibility Monitoring and Control'),
                                                       default = 0.0)
    comfortMonitoringAndControl = FloatField(verbose_name = _('Comfort Monitoring and Control'),
                                             default = 0.0)

    convenienceMonitoringAndControl = FloatField(verbose_name = _('Convenience Monitoring and Control'),
                                                 default = 0.0)

    healthAccesibilityMonitoringAndControl = FloatField(verbose_name = _('Health, well-being and accessibility Monitoring and Control'),
                                                        default = 0.0)

    maintenanceFaultPredictionMonitoringAndControl = FloatField(verbose_name = _('Maintenance and fault prediction Monitoring and Control'),
                                                                default = 0.0)
    
    informationOccupantsMonitoringAndControl = FloatField(verbose_name = _('Information to occupants Monitoring and Control'),
                                                          default = 0.0)
    
    def __str__(self):
        ''' 
        Clase DomainWeigthing
        
        '''
        return 'Id: {} - {} '.format(self.id, _(self.name))
    
    class Meta:
        verbose_name = _('Domain Weighting')
        verbose_name_plural = _('7. Domain Weighting')
        ordering = ('id',)
        
    def duplicar(self, padre = None):
        ''' 
        Clase DomainWeigthing
        
        '''
            
        self.id = None
        self.pk = None
        self.name = self.name + _('_copy')

        self.save()
        return self

class CustomDomainWeighting(models.Model):
    
    customImpactWeighting = models.ForeignKey(CustomImpactWeightings,
                         verbose_name = _('Custom Impact Weightings'),
                         related_name = 'customDomainWeigthing',
                         blank = True,
                         null = True,
                         on_delete = models.DO_NOTHING)
                         
    user = models.ForeignKey(User,
                             verbose_name = _(u"User"),
                             related_name = 'customDomainWeigthing',
                             blank = True,
                             null = True,
                             on_delete = models.DO_NOTHING)
        
    name = models.CharField(default = '',
                              max_length = 1000,
                              verbose_name = _("Name"))
                              
    country = models.ManyToManyField(Country,
                                     blank = True,
                                     verbose_name = _('Countries'),
                                     related_name = 'customDomainWeigthing',
                                     help_text = _('Multiple selection/deselection: use the CTRL key'),)
    
    climate = models.ManyToManyField(Climate,
                                   blank = True,
                                   verbose_name = _('Climates'),
                                   related_name = 'customDomainWeigthing',
                                   help_text = _('Multiple selection/deselection: use the CTRL key'),)
                         
    buildingType = models.ManyToManyField(BuildindgType,
                                          blank = True,
                                          verbose_name = _('Building Types'),
                                          related_name = 'customDomainWeigthing',
                                          help_text = _('Multiple selection/unselection: use the CTRL key'),)
    
    energyEfficiencyHeating = FloatField(verbose_name = _('Energy efficiency heating'),
                                         )

    energyFlexibilityHeating = FloatField(verbose_name = _('Energy flexibility heating'),
                                          )

    comfortHeating = FloatField(verbose_name = _('Comfort heating'),
                                default = 0.167)

    convenienceHeating = FloatField(verbose_name = _('Convenience heating'),
                                    default = 0.111)

    healthAccesibilityHeating = FloatField(verbose_name = _('Health, well-being and accessibility heating'),
                                           default = 0.0)

    maintenanceFaultPredictionHeating = FloatField(verbose_name = _('Maintenance and fault prediction heating'),
                                                   )
    
    informationOccupantsHeating = FloatField(verbose_name = _('Information to occupants heating'),
                                             default = 0.125)
    
    energyEfficiencyCooling = FloatField(verbose_name = _('Energy efficiency Cooling'),
                                         )

    energyFlexibilityCooling = FloatField(verbose_name = _('Energy flexibility Cooling'),
                                          )

    comfortCooling = FloatField(verbose_name = _('Comfort Cooling'),
                                default = 0.167)

    convenienceCooling = FloatField(verbose_name = _('Convenience Cooling'),
                                    default = 0.111)

    healthAccesibilityCooling = FloatField(verbose_name = _('Health, well-being and accessibility Cooling'),
                                           default = 0.0)

    maintenanceFaultPredictionCooling = FloatField(verbose_name = _('Maintenance and fault prediction Cooling'),
                                                   )
    
    informationOccupantsCooling = FloatField(verbose_name = _('Information to occupants Cooling'),
                                             default = 0.125)
    
    energyEfficiencyDhw = FloatField(verbose_name = _('Energy efficiency DHW'),
                                     )

    energyFlexibilityDhw = FloatField(verbose_name = _('Energy flexibility DHW'),
                                      )

    comfortDhw = FloatField(verbose_name = _('Comfort DHW'),
                           default = 0.167)

    convenienceDhw = FloatField(verbose_name = _('Convenience DHW'),
                                  default = 0.111)

    healthAccesibilityDhw = FloatField(verbose_name = _('Health, well-being and accessibility DHW'),
                                       default = 0.0)

    maintenanceFaultPredictionDhw = FloatField(verbose_name = _('Maintenance and fault prediction DHW'),
                                               )
    
    informationOccupantsDhw = FloatField(verbose_name = _('Information to occupants DHW'),
                                         default = 0.0)
    
    energyEfficiencyVentilation = FloatField(verbose_name = _('Energy efficiency Ventilation'),
                                             )

    energyFlexibilityVentilation = FloatField(verbose_name = _('Energy flexibility Ventilation'),
                                              default = 0.0)

    comfortVentilation = FloatField(verbose_name = _('Comfort Ventilation'),
                                    default = 0.167)

    convenienceVentilation = FloatField(verbose_name = _('Convenience Ventilation'),
                                       default = 0.111)

    healthAccesibilityVentilation = FloatField(verbose_name = _('Health, well-being and accessibility Ventilation'),
                                               default = 0.4)

    maintenanceFaultPredictionVentilation = FloatField(verbose_name = _('Maintenance and fault prediction Ventilation'),
                                                       )
    
    informationOccupantsVentilation = FloatField(verbose_name = _('Information to occupants Ventilation'),
                                                 default = 0.125)
    
    energyEfficiencyLighting = FloatField(verbose_name = _('Energy efficiency Lighting'),
                                          )

    energyFlexibilityLighting = FloatField(verbose_name = _('Energy flexibility Lighting'),
                                           default = 0.0)
    comfortLighting = FloatField(verbose_name = _('Comfort Lighting'),
                                 default = 0.167)

    convenienceLighting = FloatField(verbose_name = _('Convenience Lighting'),
                                     default = 0.111)

    healthAccesibilityLighting = FloatField(verbose_name = _('Health, well-being and accessibility Lighting'),
                                            default = 0.0)

    maintenanceFaultPredictionLighting = FloatField(verbose_name = _('Maintenance and fault prediction Lighting'),
                                                    )
    
    informationOccupantsLighting = FloatField(verbose_name = _('Information to occupants Lighting'),
                                              default = 0.0)
    
    energyEfficiencyElectricity = FloatField(verbose_name = _('Energy efficiency Electricity'),
                                             default = 0.111)

    energyFlexibilityElectricity = FloatField(verbose_name = _('Energy flexibility Electricity'),
                                              default = 0.149)
    comfortElectricity = FloatField(verbose_name = _('Comfort Electricity'),
                                    default = 0.0)

    convenienceElectricity = FloatField(verbose_name = _('Convenience Electricity'),
                                       default = 0.111)

    healthAccesibilityElectricity = FloatField(verbose_name = _('Health, well-being and accessibility Electricity'),
                                               default = 0.0)

    maintenanceFaultPredictionElectricity = FloatField(verbose_name = _('Maintenance and fault prediction Electricity'),
                                                       default = 0.113)
    
    informationOccupantsElectricity = FloatField(verbose_name = _('Information to occupants Electricity'),
                                                 default = 0.125)
    
    energyEfficiencyDynamicBuildingEnvelope = FloatField(verbose_name = _('Energy efficiency Dynamic Building Envelope'),
                                                         default = 0.05)

    energyFlexibilityDynamicBuildingEnvelope = FloatField(verbose_name = _('Energy flexibility Dynamic Building Envelope'),
                                                          default = 0.0)
    comfortDynamicBuildingEnvelope = FloatField(verbose_name = _('Comfort Dynamic Building Envelope'),
                                                default = 0.167)

    convenienceDynamicBuildingEnvelope = FloatField(verbose_name = _('Convenience Dynamic Building Envelope'),
                                                   default = 0.111)

    healthAccesibilityDynamicBuildingEnvelope = FloatField(verbose_name = _('Health, well-being and accessibility Dynamic Building Envelope'),
                                                           default = 0.6)

    maintenanceFaultPredictionDynamicBuildingEnvelope = FloatField(verbose_name = _('Maintenance and fault prediction Dynamic Building Envelope'),
                                                                   default = 0.05)
    
    informationOccupantsDynamicBuildingEnvelope = FloatField(verbose_name = _('Information to occupants Dynamic Building Envelope'),
                                                             default = 0.125)
    
    energyEfficiencyElectricVehicleCharging = FloatField(verbose_name = _('Energy efficiency Electric Vehicle Charging'),
                                                         default = 0.0)

    energyFlexibilityElectricVehicleCharging = FloatField(verbose_name = _('Energy flexibility Electric Vehicle Charging'),
                                                          default = 0.05)
    comfortElectricVehicleCharging = FloatField(verbose_name = _('Comfort Electric Vehicle Charging'),
                                                default = 0.0)

    convenienceElectricVehicleCharging = FloatField(verbose_name = _('Convenience Electric Vehicle Charging'),
                                                    default = 0.111)

    healthAccesibilityElectricVehicleCharging = FloatField(verbose_name = _('Health, well-being and accessibility Electric Vehicle Charging'),
                                                           default = 0.0)

    maintenanceFaultPredictionElectricVehicleCharging = FloatField(verbose_name = _('Maintenance and fault prediction Electric Vehicle Charging'),
                                                                   default = 0.0)
    
    informationOccupantsElectricVehicleCharging = FloatField(verbose_name = _('Information to occupants Electric Vehicle Charging'),
                                                             default = 0.125)
    
    energyEfficiencyMonitoringAndControl = FloatField(verbose_name = _('Energy efficiency Monitoring and Control'),
                                                      default = 0.2)

    energyFlexibilityMonitoringAndControl = FloatField(verbose_name = _('Energy flexibility Monitoring and Control'),
                                                       default = 0.2)
    comfortMonitoringAndControl = FloatField(verbose_name = _('Comfort Monitoring and Control'),
                                             default = 0.0)

    convenienceMonitoringAndControl = FloatField(verbose_name = _('Convenience Monitoring and Control'),
                                                 default = 0.111)

    healthAccesibilityMonitoringAndControl = FloatField(verbose_name = _('Health, well-being and accessibility Monitoring and Control'),
                                                        default = 0.0)

    maintenanceFaultPredictionMonitoringAndControl = FloatField(verbose_name = _('Maintenance and fault prediction Monitoring and Control'),
                                                                default = 0.2)
    
    informationOccupantsMonitoringAndControl = FloatField(verbose_name = _('Information to occupants Monitoring and Control'),
                                                          default = 0.125)
        
    
    class Meta:
        verbose_name = _('Particular Custom Domain Weighting')
        verbose_name_plural = _('12. Particular Domain Weighting')
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
        self.name = self.name + _('_copy')

        self.save()
        return self
        
class UserDefineDomainWeightings(models.Model):
    
    def __str__(self):
        ''' 
        Clase UserDefineDomainWeightings
        '''
        return 'Id: {} - {} '.format(self.id, self.description)

    class Meta:
        verbose_name = _('User-defined Domain Weightings')
        verbose_name_plural = _('11.User-defined Domain Weightings')
        ordering = ('id',)

        
class Proyecto(models.Model):
    
    user = models.ForeignKey(User,
                                    verbose_name = _(u"User"),
                                    related_name = 'proyectos',
                                    on_delete = models.DO_NOTHING)
    
    country = models.ForeignKey(Country,
                                verbose_name = _('Country'),
                                related_name = 'proyectos',
                                blank = True,
                                null = True,
                                on_delete = models.DO_NOTHING)
    
    catalogo = models.ForeignKey(Catalogo,
                                 verbose_name = _('Catalogue'),
                                 related_name = 'proyectos',
                                 blank = True,
                                null = True,
                                 on_delete = models.DO_NOTHING)
    
    climate = models.ForeignKey(Climate,
                                verbose_name = _('Climate'),
                                related_name = 'proyectos',
                                blank = True,
                                null = True,
                                on_delete = models.DO_NOTHING)
    
    domainWeigthing = models.ForeignKey(DomainWeigthing,
                                verbose_name = _('Default weighting factors'),
                                related_name = 'proyectos',
                                blank = True,
                                null = True,
                                on_delete = models.DO_NOTHING)
                                
    customDomainWeigthings = models.ForeignKey(CustomDomainWeighting,
                                verbose_name = _('Custom Domain Weighting'),
                                related_name = 'proyecto',
                                blank = True,
                                null = True,
                                on_delete = models.DO_NOTHING)
                                
    buildingType = models.ForeignKey(BuildindgType,
                                verbose_name = _('Building Type'),
                                related_name = 'proyectos',
                                blank = True,
                                null = True,
                                on_delete = models.DO_NOTHING)
      
    name = CharField(default = '',
                     max_length = 1000,
                     verbose_name = _("Project-Name"))
    
    organisation = CharField(default = '',
                             max_length = 1000,
                             verbose_name = _("Organisation"))
    
    email = CharField(default = '',
                      max_length = 1000,
                      verbose_name = _('E-mail address'))
    
    telephoneNumber = CharField(default = '',
                      max_length = 1000,
                      verbose_name = _('Telephone Number')) 
                      
    preference = CharField(choices = [('default', _('default')), ('user defined', _('user defined'))],
                                       max_length = 1000,
                                       verbose_name = _(u"Preference"),
                                       default = '')
    
    buildingUsage = CharField(choices = [('', ''),
                                         ('residential - single-family-house', _('residential-single-family-house')),
                                         ('residential - small multi-family-house', _('residential - small multi-family-house')),
                                         ('residential - large multi-family-house', _('residential - large multi-family-house')),
                                         ('residential - other', _('residential - other')),
                                         ('non-residential - office', _('non-residential - office')),
                                         ('non-residential - educational', _('non-residential - educational')),
                                         ('non-residential - healthcare', _('non-residential - healthcare')),                                    
                                         ('non-residential - other', _('non-residential - other'))],                                         
                              max_length = 1000,
                              verbose_name = _("Building Usage"),
                              default = '')
    
    
    
    netFloorAreaOfTheBuilding = FloatField(null = True,
                                           blank = True,
                                           verbose_name = _('Net floor area of the building'),
                                           default = 0.0)
    
    yearOfConstruction = FloatField(null = True,
                                    blank = True,
                                    verbose_name = _('Year of construction'),
                                    default = 0.0)
    
    buildingState = CharField(choices = [('', ''),
                                         ('Original', _('Original')),
                                         ('Renovated', _('Renovated'))],                                         
                              max_length = 1000,
                              verbose_name = _(u"Building state"),
                              default = '')
    
    assessmentPurpose = CharField(choices = [('Current building state', _('Current building state')),
                                         ('Improvement package', _('Improvement package'))],                                         
                              max_length = 1000,
                              verbose_name = _(u"Assessment purpose"),
                              help_text = _(u"Data presented in this assessment reflects the current state of the building or a package of measures/recommendations for updating the BACS"),
                              default = 'Current building state')    
    
    energyClass = CharField(choices = [('-', '-'),
                                         ('A','A'),
                                         ('B','B'),
                                         ('C','C'),
                                         ('D','D'),
                                         ('E', 'E'),
                                         ('F', 'F'),
                                         ('G','G'),],                                         
                              max_length = 2,
                              verbose_name = _(u"Energy class"),
                              help_text = _(u"Energy Performance Certificate (EPC) label/class"),
                              default = '-')  
    
    officialTestPhase = BooleanField(default = False, 
                                                   verbose_name = _("Official test phase"), 
                                                   help_text = _("Click if this assessment is part of an official Member State test"))      
    
    
    descriptionOfBuilding = CharField(default = '',
                                      max_length = 1000,
                                      verbose_name = _('Description of building'))
    
    address = CharField(default = '',
                        max_length = 1000,
                        verbose_name = _('Address'))
    
    combinedHVACPower = CharField(choices = [('>= 290 kW', _('>= 290 kW')),
                                                                      ('70 - 290 kW', _('70 - 290 kW')),
                                                                       ('<= 70 kW', _('<= 70 kW')),
                                                                       ('', '')],
                                         
                              max_length = 1000,
                              verbose_name = _(u"Effective rated output for HVAC systems"),
                              default = '')    
    
    
    # Almacenamos estos valores para que sirvan de cache en el benchmarking
    totalSriScore = FloatField(null = True,
                                    blank = True,
                                    verbose_name = _('Total SRI Score'),
                                    default = 0.0)    
    
    scoreKF1 = FloatField(null = True,
                                    blank = True,
                                    verbose_name = _('Score KF1'),
                                    default = 0.0)    

    scoreKF2 = FloatField(null = True,
                                    blank = True,
                                    verbose_name = _('Score KF2'),
                                    default = 0.0)    

    scoreKF3 = FloatField(null = True,
                                    blank = True,
                                    verbose_name = _('Score KF3'),
                                    default = 0.0)            
    
    
    Heating = BooleanField(default = True, verbose_name = _("Heating"), help_text = _("Is Heating domain assessable?"))
    Dhw = BooleanField(default = True, verbose_name = _("DWH"), help_text = _("Is DHW domain assessable?"))
    Cooling = BooleanField(default = True, verbose_name = _("Cooling"), help_text = _("Is Cooling domain assessable?"))
    Ventilation = BooleanField(default = True, verbose_name = _("Ventilation"), help_text = _("Is Ventilation domain assessable?"))
    Lighting = BooleanField(default = True, verbose_name = _("Lighting"), help_text = _("Is Lighting domain assessable?"))
    DynamicBuildingEnvelope = BooleanField(default = True, verbose_name = _("Dynamic Building Envelope"), help_text = _("Is Dynamic Building Envelope domain assessable?"))
    Electricity = BooleanField(default = True, verbose_name = _("Electricity"), help_text = _("Is Electricity domain assessable?"))
    ElectricVehicleCharging = BooleanField(default = True, verbose_name = _("Electric Vehicle Charging"), help_text = _("Is Electric Vehicle Charging domain assessable?"))
    MonitoringAndControl = BooleanField(default = True, verbose_name = _("Monitoring And Control"), help_text = _("Is Monitoring and Control domain assessable?"))
    customDomain = BooleanField(default = False, verbose_name = _("Custom Domain Weighting"), help_text = _("Prefer to customize domain weightings?"))
    
    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('10. Project')
        ordering = ('id',)
    
    def __str__(self):
        ''' 
        Clase Proyecto
        
        '''
        return _('Project:') + '{}'.format(self.id) + ' - {}'.format(self.name)
    
    def duplicar(self):
        ''' 
        Clase Proyecto
        
        '''
        
        listaDatos = Dato.objects.filter( proyect = self)
        self.id = None
        self.pk = None
            
        self.name += _("_copy")
        
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
        return [_('Energy Efficiency'), _('Energy flexibility and storage'), _('Comfort'), _('Convenience'), _('Health, well-being and accessibility'), _('Maintenance and fault prediction'), _('Information to occupants'),]
    
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
                listadoNombreDominios.append(_(dominio.description))
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
        
        df = pd.DataFrame(tablaFormateada, columns = self.listadoNombreImpactosMostrar + [_('Domain SRI')], index = self.listadoNombreDominiosMostrar)
        print(tabulate(df, headers = 'keys', tablefmt = 'psql'))
        return df
        
     
    def repAuxialiaryTable(self):
            
        df = pd.DataFrame([self.getListaPuntuacionPonderada(self.calculoMatrizImpacto()),
                            self.getListaPuntuacionPonderadaMaxima(self.calculoMatrizImpacto()),
                            self.impactWeightings], columns = self.listadoNombreImpactosMostrar, index = [_('Impact scores weighted by domain'), _('Maximum impact scores weighted by domain'), _('Impact Weightings')])
        
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

    
class Dato(models.Model):
    
    chosenFuncionality = models.ForeignKey(Funcionalidad,
                                             verbose_name = _('Functionality'),
                                             related_name = 'datos',
                                             on_delete = models.CASCADE)
    
    proyect = models.ForeignKey(Proyecto,
                                verbose_name = _('Project'),
                                related_name = 'datos',
                                null = True,
                                blank = True,
                                on_delete = models.CASCADE)
    
    comments = RichTextUploadingField(verbose_name = _("Comment"),
                             blank = True,
                             default = '')
    
    justification = RichTextUploadingField(verbose_name = _("Justification"),
                                  blank = True,
                                  default = '')
    
    percentage = FloatField(verbose_name = _('Percentage'),                            
                                       default = 100.0,
                                       validators = [MinValueValidator(0.0),MaxValueValidator(100)])
    
    class Meta:
        verbose_name = _('Datum')
        verbose_name_plural = _('5.Data')
        ordering = ('id',)
        
    def __str__(self):
        ''' 
        Clase Dato
        
        '''
        return '{2}: {0}, {3}: {1}'.format(self.proyect.id, self.chosenFuncionality.id, _('Project'), _('Functionality'))
        
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
        if _(self.chosenFuncionality.description) == _('Not applicable') or _(self.chosenFuncionality.description.replace(" ","").upper()) == _('N/A') or self.chosenFuncionality.description.replace(" ","").upper() == 'N/A' :
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
    
