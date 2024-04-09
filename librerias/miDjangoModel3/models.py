# -*- coding: cp1252 -*-
'''
Si los atributos son obligatorios hay que meterlos en listaAtributosObligatorios.
A los atributos se les puede definir m�todo clean para la comprobacion

En descriptores primero se mira si tienen un m�todo clean propio.
En caso contrario, se hace la comprobacion de sus errores propios.

la explicaci�n del funcionamiento de los descriptores FloatField, CharField,... est� en pruebas.pruebas.py
'''
import copy
import datetime
import inspect
import json


                    
import imp
import os
import sys
from inspect import ismethod  
from types import NoneType                    



class Manager(object):
    ''' Clase para implementar el manager de las otras (objects)
    '''
    def __init__(self):
        self.listadoObjetos = []
        
        self.model = None
        
    def all(self):
        return self.listadoObjetos
    
    def first(self):
        try:
            return self.listadoObjetos[0]
        except IndexError:
            return None
            
    def count(self):
        return len(self.listadoObjetos)

    def last(self):
        return self.listadoObjetos[-1]
    
    def filter(self,**kwargs):
        listadoObjetosEncontrados = self.listadoObjetos
        for k in kwargs:
            if kwargs[k].__class__ == str:
                argumento =  str(kwargs[k],'cp1252',errors='ignore')
            else:
                argumento = kwargs[k]
            listadoObjetosEncontrados = [x for x in listadoObjetosEncontrados if getattr(x, k) == argumento]
    
        # Lo devolvemos ordenado por id
        if hasattr(self, u'id'):
            listadoObjetosEncontrados.sort(key = lambda x: int(x.id))
        return listadoObjetosEncontrados    
    

    
    def get(self,**kwargs):
        listadoObjetosEncontrados = self.filter(**kwargs)
        if len(listadoObjetosEncontrados) > 1:
            raise Exception (u"Se han encontrado m�ltiples objetos")
            
        elif len(listadoObjetosEncontrados) == 0:
            return None
        
        return listadoObjetosEncontrados[0]
    
    

        

class Model(object):
    ''' 
    Clase para replicar el models.Model de django
    '''    
    listaAtributosObligatorios = []
    
    rutaBaseDatos = None
    
    nombreTabla = None
    
    duplicarDescendientes = True
    
    
    @property
    def nombreTablaSqlite(self):
        
        if self.nombreTabla:
            return self.nombreTabla
        else:
            return u'{nombreModulo}_{nombreClase}'.format(nombreModulo = self.__module__.replace(".","_"),
                                                      nombreClase = self.__class__.__name__)
        
        
    def esCorrecto(self, 
                   getErroresInstanciasRelacionadas = False,
                   **kwargs):
        '''
        class: Model
        '''
        diccErrores = self.getDiccErrores(getErroresInstanciasRelacionadas, **kwargs)
        if diccErrores == {}:
            return True
        else: 
            return False

    
    @classmethod 
    def getClaseBaseDescriptor(cls, nombreDescriptor = u''):
        '''
        class: Model
        Devuelve la clase a la que pertenece el descriptor dado. 
        Puede ser la clase en la que estamos o alguna de las que hereda 
        Si no existe el descriptor en ninguna de ellas, devuelve None
        '''  
        listadoClasesBase = cls.__mro__
        for claseBase in listadoClasesBase:
            if nombreDescriptor in claseBase.__dict__.keys():
                return claseBase
        return None
    
    
    @property
    def diccionarioTablaSqlite(self):
        '''
        class: Model
        Devuelve un diccionario con la informaci�n necesaria para grabar en la base de datos
        '''
        
        diccionario = {}
        
        diccionarioInstanciasDescriptores = self.getDiccionarioValoresDescriptores()
        
        for nombreDescriptor in diccionarioInstanciasDescriptores.keys():
            valorDescriptor = diccionarioInstanciasDescriptores[nombreDescriptor]
            
            if (valorDescriptor == None) or (valorDescriptor == u''):
                valorDescriptor = 'NULL'
            
            
            diccionario[nombreDescriptor] = valorDescriptor 
                                 
        return diccionario
            

        
    def getDiccionarioValoresDescriptores(self):
        '''
        class Model
        Devuelve un listado con todos los valores de los descriptores que hay en una instanacia
        Por ejemplo: de material: devuelve espesor (1.), densidad (200.), etc...
        '''
        diccInstancias = {}
        listaNombresDescriptores = self.getNombresDescriptoresInstancia()
        for nombre in listaNombresDescriptores:
            instancia = self.getInstanciaDescriptor(nombreDescriptor = nombre)
            if instancia.__class__ ==  BooleanField:
                if getattr(self,nombre) == True:
                    diccInstancias[nombre] = '1'
                elif getattr(self,nombre) == False:
                    diccInstancias[nombre] = '0'
                else:
                    diccInstancias[nombre] =  getattr(self,nombre)
                 
            elif instancia.__class__ not in [ForeignKey,OneToOneField]:
                diccInstancias[nombre] = getattr(self,nombre)

        return diccInstancias
        
            
    def getInstanciaDescriptor(self, nombreDescriptor = u''):
        '''
        class: Model
        Devuelve la instancia del descriptor. Si no existe, es None
        '''   
        try:
            instancia = self.__class__.getClaseBaseDescriptor(nombreDescriptor).__dict__[nombreDescriptor]
        except AttributeError:
            instancia = None
            
        return instancia
    
    def getNombreInstanciaDescriptor(self, nombreDescriptor = u''):
        try:
            claseInstancia = self.getInstanciaDescriptor(nombreDescriptor = nombreDescriptor).__class__.__name__
        except Exception as e:
            print(e)
            claseInstancia = u''
            
        return claseInstancia
    
    def getListaErroresDeDescriptor(self, nombreDescriptor = u'', **kwargs): 
        '''
        class: Model
        Devuelve el listado de errores de un descriptor que pertenece al modelo o a alguna de las clases de las que hereda
        Si no existe el descriptor, devuelve vac�o
        En kwargs arguments pueden ir un  diccionario cuyas keys ser�n el nombre del atributo que queremos modificar y como valor el nuevo valor que va a tomar. Ejemplo required = True 
        '''   
        instancia = self.getInstanciaDescriptor(nombreDescriptor)
        for key in kwargs:
            if hasattr(instancia, key): 
                setattr(instancia, key, kwargs[key]) 
        if instancia != None:
            listaErrores = instancia.getListaErrores(getattr(self, nombreDescriptor))
        else:
            listaErrores = []
        return listaErrores
        
    def getDiccErrores(self, 
                       getErroresInstanciasRelacionadas = False, 
                       **kwargs):
        '''
        class: Model
        Devuelve diccionario con todos los errores encontrados.
        dicc[nombre del atributo o del descriptor] = {'verbose_name: xxx, 'error': []}
        getErroresInstanciasRelacionadas = True: mira tb los errores de las instancias OTO o FK relacionadas
        '''
        diccErrores = {}
        diccErrorCampo = {}
        for atributo in self.getNombresAtributosInstancia():
            error = self.getErroresDelAtributo(atributo, **kwargs)
            if error != []:
                diccErrorCampo = {'error': error,
                                  'verbose_name': atributo}
                diccErrores[atributo] = diccErrorCampo
            

        for nombreDescriptor in self.getNombresDescriptoresInstancia():
            if nombreDescriptor != 'listaAtributosObligatorios':
                error = self.getErroresDelDescriptor(nombreDescriptor, **kwargs) #lo hago siempre para comprobar x ej. si es required
                if error != []:
                    listadoClasesBase = self.__class__.__mro__
                    for claseBase in listadoClasesBase:
                        if nombreDescriptor in claseBase.__dict__.keys():
                            verbose_name = claseBase.__dict__[nombreDescriptor].verbose_name #si no hay un verbose_name, le paso el nombre del descriptor
                            break
                    if verbose_name == None:
                        verbose_name = nombreDescriptor
                    diccErrorCampo = {'error': error,
                                      'verbose_name': verbose_name}
                    diccErrores[nombreDescriptor] = diccErrorCampo
                
                #si es un OneToOne o un ForeingKey, el nombreDescriptor
                instanciaApuntada = getattr(self, nombreDescriptor)
                if hasattr(instanciaApuntada,'getDiccErrores') and getErroresInstanciasRelacionadas: #si lo que se guarda en el atributo es una instancia, tiene errorres
                    #devuelve un diccionario
                    for key in instanciaApuntada.getDiccErrores():
                        diccErrorCampo = {'error': instanciaApuntada.getDiccErrores()[key]['error'],
                                          'verbose_name': instanciaApuntada.getDiccErrores()[key]['verbose_name']} #de momento no se usa verbose_name en OTO o FK
                                            
                        diccErrores[u'{nombreDescriptor}_{nombreKey}'.format(nombreDescriptor = nombreDescriptor,
                                                                             nombreKey = key)] = diccErrorCampo
                    
        return diccErrores
    

        
    def getErroresDelDescriptor(self, nombreDescriptor, **kwargs):
        '''
        class: Model
        Devuelve un listado con los errores relacionados del descriptor
        '''
        error = []
        #damos prioridad a si se ha escrito un m�todo clean en la comprobacion del campo
        
        #comprobamos si se ha definido un clean para el descriptor.
        if hasattr(self, 'validador_{0}'.format(nombreDescriptor)):
            error = getattr(self, 'validador_{0}'.format(nombreDescriptor))(**kwargs)
            return error
            
        else:  
            try:
                # Hay que comprobar si el descriptor esta definidio en la clase actual o en las clases bases
                listadoDeClasesBase = self.__class__.__mro__
                for claseBase in listadoDeClasesBase:
                    if nombreDescriptor in claseBase.__dict__.keys():
                        error += claseBase.__dict__[nombreDescriptor].getListaErrores(getattr(self,nombreDescriptor))
                        
                        # Hacemos la comprobacion del campo unico
                        if hasattr(claseBase.__dict__[nombreDescriptor], 'unico'):
                            if claseBase.__dict__[nombreDescriptor].unico:
                                valoresYaUtilizados = [getattr(x,nombreDescriptor) for x in claseBase.objects.all()]
                                valorAComprobar = getattr(self,nombreDescriptor)
                                if valoresYaUtilizados.count(valorAComprobar) > 1:
                                    error.append(u"El atributo '{0}' con el valor '{1}'se encuentra repetido {2} veces".format(nombreDescriptor,valorAComprobar,valoresYaUtilizados.count(valorAComprobar)))
                        
                        break 
            except KeyError:
                print("El descriptor <{0}> no esta definido en las clases base: {1}".format(nombreDescriptor,listadoDeClasesBase))
            
            except:
                pass
#                 print "El descriptor <{0}> no tiene el m�todo errores".format(nombreDescriptor)
                          
            return error
        

    def getErroresDelAtributo(self, atributo, **kwargs):
        '''
        class: Model
        Devuelve un listado con los errores relacionados del atributo
        '''
        error = []
        erroresObtenidosDelClean = []
        #comprobamos si el atributo tiene un valor si este es obligatorio
        valor = getattr(self, atributo)
        if atributo in self.listaAtributosObligatorios:
            if type(valor) == type(None):
                error.append(u"El campo es obligatorio")
            elif (type(valor) == str or type(valor) == unicode) and  valor == '':
                error.append(u"El campo es obligatorio")      
                
        #comprobamos otros posibles errores: que tome el valor que es necesario, etc...  
        if hasattr(self, 'validador_{0}'.format(atributo)):
            erroresObtenidosDelClean = getattr(self, 'validador_{0}'.format(atributo))(**kwargs)
        return error + erroresObtenidosDelClean
        
    def getListaErrores(self, 
                        getErroresInstanciasRelacionadas = False,
                        **kwargs):
        '''
        class: Model
        Devuelve una lista con los errores para mostrar
        '''
        lista = []
        diccErrores = self.getDiccErrores(getErroresInstanciasRelacionadas, 
                                          **kwargs)
        for key in diccErrores:
            errorTexto = u''
            for error in diccErrores[key]['error']:
                errorTexto += u'{error}. '.format(error = error)
            lista.append(u'{verbose_name}: {error}'.format(verbose_name = diccErrores[key]['verbose_name'],
                                                           error = errorTexto))
        return lista        
        
    def __init__(self,**kwargs):
        ''' 
        Class: Model
        '''  
        
        if self.objects.listadoObjetos == []:
            nuevoId  = 1
        else:
            nuevoId = max([objecto.id for objecto in self.objects.listadoObjetos])+1 
        self.id = nuevoId
        
        if self not in self.objects.listadoObjetos:
            self.objects.listadoObjetos.append(self)

            
        self.inicializaDescriptoresANone()
        
        
        for clave,valor in kwargs.items():
            setattr(self,clave,valor)
        

        
    
    def inicializaDescriptoresANone(self):
        ''' 
        Class: Model
        Clase para replicar el models.Model de django
        '''          
        if self.__class__ == ForeignKey or self.__class__ == OneToOneField:
            return 
        listadoCamposDescriptores = self.getCamposDescriptores()
        for descriptor in listadoCamposDescriptores:
            setattr(self,"instanciaPadre{0}".format(descriptor.model.__name__),None)
        return listadoCamposDescriptores
    
    @classmethod
    def reset(self):
        self.objects.listadoObjetos = [] 
        
               
    def save(self):
        ''' 
        Class: Model
        Molaria implementar la grabacion de cada instancia aqui
        '''
        pass
    
    def delete(self,claseExclusionAscendente=None):
        ''' 
        Class: Model
        Hace lo siguiente:
                - Borra la instancia del listado de objetos de la clase
                - Objetos padre: (por ejemplo, para cerramiento proyecto), actualiza los �ndices de los padres (borra la instancia de los listados de los objetos padre)
                - Objetos hijo: (por ejemplo, para cerramiento huecos), borra los objetos hijos que cuelgan (si borramos el cerramiento, borra tambi�n los huecos)

            El par�metro claseExclusionAscendente es de uso interno, sirve para evitar la recursividad. Por ejemplo, borramos un cerramiento y por lo tanto se
            llama a la funci�n delete de los huecos, como cada hueco tiene como padre el cerramiento que estamos borrando se forma un bucle que se evita con este 
            par�metro
        '''
        #TODO: REVISAR CON MA. NOS DA ERROR CD POR LO QUE SEA NO ESTA EN LISTADO. POR EJEMPLO, SI SE HA CREADO CON UN COPY.DEEPCOPY
        if self in self.objects.listadoObjetos:
            self.objects.listadoObjetos.remove(self)
        
        # borrado aguas abajo
        for atributo in self.getNombresAtributosInstancia():
            posibleLista = getattr(self,atributo)
            if type(posibleLista) == type([]):
                if self.__class__.duplicarDescendientes: # si los descendientes se pueden duplicar, tambi�n se deben borrar
                    for elementoInLista in posibleLista:
                        if hasattr(elementoInLista,'delete'):
                            metodoBorrado = getattr(elementoInLista, 'delete')
                            result = metodoBorrado(claseExclusionAscendente=self.__class__)        
                    setattr(self,atributo,[])
        
        # eliminar la referencia al objeto aguas arriba
        for atributo in self.getNombresDescriptoresInstancia():
            if hasattr(self, atributo):
                try:

                    if getattr(self,atributo).__class__ != claseExclusionAscendente:
                        # eval("del self.{}".format(atributo))
                        delattr(self,atributo)
                except AttributeError as error: # Si no se ha definido no tiene __delete__
                    pass
                
        
        return True



    def duplicar(self, **kwargs):
        ''' 
        Class: Model
        Duplica de la siguiente forma:
                - Las nuevas instancias creadas mantienen el mismo padre
                - Todos los hijos se duplican
                - En instanciaAscendente le pasamos la instancia de la clase padre de un FK. 
                Ej: si estamos creando un hueco, le pasamos el cerramiento al que pertenece

        '''
        if kwargs :
            listadoAtributosAscendentes = kwargs.keys()
            nombreAtributoInstanciaAscendente = kwargs.keys()[0]
            instanciaAscendente = kwargs.values()[0]
        else:
            listadoAtributosAscendentes = [] 
        
        nuevaInstancia = self.__class__() #al poner los parentesis crea una copia de la instancia
        
        for atributo in self.getNombresAtributosInstancia():
            valorAtributo = getattr(self,atributo)
            if type(valorAtributo) == type([]):
                lista = valorAtributo
                setattr(nuevaInstancia,atributo,[])
                for elementoEnLista in lista:
                    if self.__class__.duplicarDescendientes:
                        if hasattr(elementoEnLista,'duplicar'):                        
                            metodoDuplicar = getattr(elementoEnLista, 'duplicar')
                            try:
                                result = metodoDuplicar(**kwargs)
                            except:
                                print (u"Problemas aplicando el m�todo duplicar a:  {0}".format(elementoEnLista.__class__))   
                        else:
                            #El elemento de la lista no es un obj de django model. Copiamos y lo a�adimos en lista de nueva instancia
                            listaEnLaNuevaInstancia = getattr(nuevaInstancia,atributo)
                            listaEnLaNuevaInstancia.append(copy.deepcopy(elementoEnLista))
            else:
                if hasattr(valorAtributo,'duplicar'):
                    if self.__class__.duplicarDescendientes:
                            metodoDuplicar = getattr(valorAtributo, 'duplicar')
                            result = metodoDuplicar(instanciaAscendente = nuevaInstancia)
                            setattr(nuevaInstancia, atributo,  result)
                    else:
                        setattr(nuevaInstancia, atributo,  valorAtributo)
                            

                else:  
                    valorAtributo = getattr(self, atributo)
                    if valorAtributo.__class__ in [float,str,unicode,NoneType]:
                        nuevoValor = valorAtributo
                    else:
                        nuevoValor = copy.deepcopy(valorAtributo)
                    setattr(nuevaInstancia, atributo, nuevoValor)
                            
        

            
        
        
        for atributo in self.getNombresDescriptoresInstancia():
            if atributo in listadoAtributosAscendentes:
                #miro en instancia antigua el tipo del atributo que estoy asignando. Si coincide con el tipo de la instanciaAscendente, se la asigno
                setattr(nuevaInstancia, atributo, kwargs[atributo])
                
            else: 
                valorAtributo = getattr(self, atributo)
                if valorAtributo.__class__ in [float,str,unicode,NoneType]:
                    nuevoValor = valorAtributo
                else:
                    nuevoValor = copy.deepcopy(valorAtributo)
                setattr(nuevaInstancia, atributo, nuevoValor)
                
        return nuevaInstancia
            
    @classmethod
    def listaDescriptoresClase(cls):
        '''
        Class: Model
        '''
        nombresAtributos = inspect.getmembers(cls, lambda a:(not inspect.isroutine(a) and not inspect.isdatadescriptor(a)))
        nombresAtributos = [a[0] for a in nombresAtributos if not(a[0].startswith('__') and a[0].endswith('__')) and a[0] != 'objects']
        
        lista = []
        for nombre in nombresAtributos:
            tipo = cls.__dict__[nombre].__class__.__name__
            modelo = cls.__dict__[nombre].model.__name__
            lista.append([nombre,tipo,modelo])
        return lista
        
    
    def getNombresDescriptoresInstancia(self):
        '''
        Class: Model
        '''
#         nombresAtributos = inspect.getmembers(self.__class__, lambda a:(not inspect.isroutine(a) and not inspect.isdatadescriptor(a)))
#         nombresAtributos = [a[0] for a in nombresAtributos if not(a[0].startswith('__') and a[0].endswith('__')) and a[0] != 'objects']
        nombresAtributos = []
        busquedaDeAtributos = []
#         busquedaDeAtributos = [inspect.getmembers(self.__class__, lambda a:(not inspect.isroutine(a) and not inspect.isdatadescriptor(a)))[1][1]]
        # __mro__: method resolution order
        # sirve para cuando hay herencias multiples, nos determina el orden de prioridad de los m�todos. 
        for claseBase in self.__class__.__mro__ :
            busquedaDeAtributos.append(inspect.getmembers(claseBase, lambda a:(not inspect.isroutine(a) and not inspect.isdatadescriptor(a)))[1][1])
            
        
        listaTiposDeDescriptor = ["CharField","FloatField","BooleanField","ChoiceField","ListField","ForeignKey","OneToOneField","DateField"]
        for diccionarioProxy in [x for x in busquedaDeAtributos if type(x) == dict ]:
            for posibleAtributo in diccionarioProxy.keys():
                if diccionarioProxy[posibleAtributo].__class__.__name__ in listaTiposDeDescriptor:
                    nombresAtributos.append(posibleAtributo)
               
          
        
        return nombresAtributos
        
    def getNombresAtributosInstancia(self):
        '''
        Class: Model
        '''
#         listadoDeMiembros = inspect.getmembers(self,lambda a: (not inspect.isroutine(a)))
#         listadoDeMiembrosFiltrado = []
#         for miembro in self.__dict__.values():
#             nombreDelAtributo = miembro#[0]
#             if hasattr(self.__class__,nombreDelAtributo):
#                 if type(getattr(self.__class__,nombreDelAtributo)) != property :
#                     listadoDeMiembrosFiltrado.append(miembro)
#             else:
#                 listadoDeMiembrosFiltrado.append(miembro)
        listadoDeMiembros = self.__dict__.keys()
        nombresAtributos = [a for a in listadoDeMiembros if not(a.startswith('__') and a.endswith('__')) and a != 'objects']
        nombresAtributos = [x for x in nombresAtributos if "instanciaPadre" not in x and x != "id"] # filtramos campos nombre padre e id
        atributosDescriptores = self.getNombresDescriptoresInstancia()
        nombresAtributos = [x for x in nombresAtributos if x not in atributosDescriptores and x != ''] # Filtramos descriptores      
        return nombresAtributos        
       
    def getCamposDescriptores(self):
        '''
        Class: Model
        '''
        listado = [x for x in self.__class__.__dict__.values() if x.__class__ == ForeignKey or  x.__class__ == OneToOneField]
        return listado
    
    @classmethod
    def getOrCreate(cls,**kwargs):
        listadoInstanciasExistentes = cls.objects.filter(**kwargs)
        if len(listadoInstanciasExistentes) == 1:
            return listadoInstanciasExistentes[0]
        elif len(listadoInstanciasExistentes) == 0:
            nuevaInstancia = cls(**kwargs)
            return nuevaInstancia
        else:
            raise Exception(msg = u'Multiples intancias encontradas.')
    
    @classmethod
    def imprimeInstanciasClase(cls,separador = '\t'):
        '''
        Class: Model
        '''
        primeraInstancia = cls.objects.first()
        if primeraInstancia != None:
            listadoAtributos = primeraInstancia.getNombresAtributosInstancia()
            print (separador.join(listadoAtributos))
            for instancia in cls.objects.all():
                print (separador.join([str(getattr(instancia,atributo)) for atributo in listadoAtributos if atributo != '' and hasattr(instancia,atributo)]))
        else:
            print (u"{0}: Tabla vac�a".format(cls.__name__))
            

    
    @classmethod
    def crearTablaSqlite(cls):
        '''
        Class: Model
        '''
        import sqlite3

        #crear conexion
        conexion = sqlite3.connect(cls.rutaBaseDatos)    
        #crear cursor
        cursor = conexion.cursor()

        #crear tabla
        primeraInstancia = cls.objects.first()
        if primeraInstancia == None:
            primeraInstancia = cls()

        listado = []
        listado.append(u'id')

        listadoDescriptores = listado + primeraInstancia.getNombresDescriptoresInstancia()
    
        stringCreate = u"CREATE TABLE if not exists {nombreTabla} (".format(nombreTabla = primeraInstancia.nombreTablaSqlite)   
        cont = 1

        for atributo in listadoDescriptores:
            if atributo == u'id':
                stringCreate = stringCreate + str(atributo)+u" INTEGER PRIMARY KEY, "
            else:
                nombreClaseDescriptor = primeraInstancia.getNombreInstanciaDescriptor(nombreDescriptor = atributo)
                
                if nombreClaseDescriptor == u'FloatField':
                    stringCreate = stringCreate+str(atributo)+u" REAL, "
                    
                if nombreClaseDescriptor == u'CharField' or nombreClaseDescriptor == u'ChoiceField' or \
                nombreClaseDescriptor == u'ListField' or nombreClaseDescriptor == u'DateField' or  nombreClaseDescriptor == u'BooleanField':
                    stringCreate = stringCreate+str(atributo)+u" TEXT, " 
                    
            cont = cont +1  
                  
        if stringCreate[-2:-1]==',':
            stringCreate=stringCreate[:-2]
        stringCreate = stringCreate + u");"
        cursor.execute(stringCreate)
         
        #desconexion
        conexion.close()
        

       
    @classmethod 
    def rellenarTablaSqlite(cls, *args):
        '''
        Class: Model
        kwargs: lista de variables que no pueden estar repetidas en la tabla. 
        Por ejemplo nombre y conductividad, si los materiales no pueden tener ese valor repetido
        Si args est� vac�o, coge el listado de descriptores
        '''
        
        for i in cls.objects.all():
            if args != ():
                for nombreVariable in args:
                    dicc = {nombreVariable : getattr(i, nombreVariable) }
            else: 
                dicc = i.diccionarioTablaSqlite
            i.crearOActualizarInstanciaEnTablaSqlite(**dicc)
        
         
    @classmethod 
    def leerTablaSqlite(cls):
        '''
        Class: Model
        '''
        if not cls.existeTablaSqlite():
            return []
        
        import sqlite3
  
        #crear conexion
        conexion = sqlite3.connect(cls.rutaBaseDatos)   
        #crear cursor
        cursor = conexion.cursor()  
        
        primeraInstancia = cls.objects.first()
        if primeraInstancia == None:
            primeraInstancia = cls()
        
        cursor.execute(u"SELECT * FROM "+ primeraInstancia.nombreTablaSqlite+";")
        #mostramos los datos
        datos = cursor.fetchall()
        #desconexion
        conexion.close()
        
        return datos 
    
    @classmethod
    def informacionColumnasBaseDeDatos(cls):
        import sqlite3
        c=sqlite3.connect(cls.rutaBaseDatos)
        cursor1 = c.cursor()
        cursor1.execute("""PRAGMA table_info(%s)"""%cls.nombreTablaSqlite)
        col = cursor1.fetchall()
        return col
    
    @classmethod
    def generarInstanciasDesdeLaBaseDeDatos(cls):
        datosEnFilas = cls.leerTablaSqlite()
        informacionColumnas = cls.informacionColumnasBaseDeDatos()
        

        for fila in datosEnFilas:
            diccionarioContenido={}
            for columna,key,tipo,_,_,_ in informacionColumnas:
                if fila[columna] == 'NULL':
                    diccionarioContenido[key] = None
                elif tipo == 'INTEGER':
                    diccionarioContenido[key] = int(fila[columna])
                elif tipo == 'REAL':
                    diccionarioContenido[key] = float(fila[columna])
                elif tipo == 'TEXT':
                    diccionarioContenido[key] = fila[columna]
            
            cls(diccionarioContenido)
                
                
        
        
        
    
    def existeInstanciaEnTablaSqlite(self,
                                     **kwargs):
        '''
        Class: Model
        Devuelve True o False si encuenta o no un elemento o con los par�metros dados
        '''
        lista = self.leerInstanciaEnTablaSqlite(**kwargs) #si no existe la tabla, devuelve []
        if lista == []:
            return False
        else:
            return True
        
        
    def leerInstanciaEnTablaSqlite(self, 
                                   **kwargs):
        '''
        Class: Model
        '''
        if not self.existeTablaSqlite():
            return []
            
            
        import sqlite3

        if 'diccAtributoABuscar'  in kwargs.keys():
            kwargs = kwargs['diccAtributoABuscar']
        #crear conexion
        conexion = sqlite3.connect(self.rutaBaseDatos)   
        conexion.text_factory = str
        #crear cursor
        cursor = conexion.cursor()  
        
        sql = u"SELECT * FROM {nombreTabla} WHERE ".format(nombreTabla = self.nombreTablaSqlite)
        
        contador = 0
        nuevoDicc = {}
        for nombreVariable in kwargs:
            valorVariable =  kwargs[nombreVariable]
            if valorVariable:
                nuevoDicc[nombreVariable] = valorVariable
        for nombreVariable in nuevoDicc:
            valorVariable =  nuevoDicc[nombreVariable]
            if valorVariable.__class__ == str:
                valorVariable = str(valorVariable,self.encoding)
            elif valorVariable.__class__ == bool:
                if valorVariable:
                    valorVariable = '1'
                else:
                    valorVariable = '0'
            sql += u"{nombreVariable}".format(nombreVariable=nombreVariable)+u"="+ u'''"{valorVariable}"'''.format(valorVariable = valorVariable)

            contador += 1
        
            if contador < len(nuevoDicc):
                sql += u' AND '
            
        cursor.execute(sql.encode(self.encoding))
       
        #mostramos los datos
        datos = cursor.fetchall()
        #desconexion
        conexion.close()
        
        return datos 
    
    
    
    @classmethod
    def existeTablaSqlite(cls):   
        '''
        Class: Model
        '''
        import sqlite3 
  
        #crear conexion
        conexion = sqlite3.connect(cls.rutaBaseDatos)  
        #crear cursor
        cursor = conexion.cursor()      
        
        primeraInstancia = cls.objects.first()
        if primeraInstancia == None:
            primeraInstancia = cls()
        
        tb_exists = u"SELECT name FROM sqlite_master WHERE type='table' AND name='{nombreTabla}'".format(nombreTabla = primeraInstancia.nombreTablaSqlite)
        laCogemos = cursor.execute(tb_exists).fetchone()
        existe = True if laCogemos != None else False
        
        #guardar cambios
        return existe  
        
    
    def crearInstanciaEnTablaSqlite(self,**kwargs):
        '''
        Class: Model
        '''
        if not self.existeTablaSqlite():
            self.crearTablaSqlite()
            
        import sqlite3
        
        #crear conexion
        conexion = sqlite3.connect(self.rutaBaseDatos)  
        #crear cursor
        cursor = conexion.cursor()
                
        sql = "INSERT INTO {nombreTabla} ".format(nombreTabla = self.nombreTablaSqlite)
        
        sqlNombresCampos = '('
        sqlValoresCampos = 'VALUES ('
        
        if kwargs:
            diccionarioTablaSqlite = kwargs
        else:
            diccionarioTablaSqlite = self.diccionarioTablaSqlite
        listaKeys = diccionarioTablaSqlite.keys()
        
        while listaKeys != []:
            key = listaKeys[0]
            valorCampo = diccionarioTablaSqlite[key]
            if valorCampo.__class__ == str:
                valorCampo = str(valorCampo,'cp1252')
            
            sqlNombresCampos += '{nombreCampo}'.format(nombreCampo = key)
            
            if isinstance(valorCampo, basestring): 
                sqlValoresCampos += '''"{valorCampo}"'''.format(valorCampo = valorCampo)
            elif isinstance(valorCampo, bool):
                sqlValoresCampos += "{valorCampo}".format(valorCampo = 1 if valorCampo else 0)                
            else:
                sqlValoresCampos += "{valorCampo}".format(valorCampo = valorCampo)                
        
            listaKeys.remove(key)
            if len(listaKeys) >= 1: #si hay uno, ya no tiene que poner la coma
                sqlNombresCampos += ', '
                sqlValoresCampos += ', '
            else: 
                sqlNombresCampos += ')'
                sqlValoresCampos += ')'

        sql += sqlNombresCampos
        sql += sqlValoresCampos
        
        cursor.execute(sql.encode('cp1252'))
 
        #guardar cambios
        conexion.commit()

        conexion.close()
    
    
    def crearOActualizarInstanciaEnTablaSqlite(self, **kwargs):
        '''
        Class:Model
        Si existe instancia con par�metros dados, se actualiza, sino, se crea nueva
        Si no se pasan par�metros en kwargs, coge todos los que descriptores
        '''
        if kwargs == {}:
            kwargs = self.diccionarioTablaSqlite
            
        if self.existeInstanciaEnTablaSqlite(**kwargs):
            self.actualizarInstanciaEnTablaSqlite(**kwargs)
            
        else: 
            self.crearInstanciaEnTablaSqlite(**kwargs)
            
            
         
    def actualizarInstanciaEnTablaSqlite(self, **kwargs):   
        '''
        Class: Model
        Actualiza en la tabla Sqlite los valores de la instancia
        '''
        import sqlite3 
   
        #crear conexion 
        conexion = sqlite3.connect(self.rutaBaseDatos)  
        #crear cursor
        cursor = conexion.cursor()    
        
        if kwargs:
            diccionarioTablaSqlite =  kwargs
        else:
            diccionarioTablaSqlite = self.diccionarioTablaSqlite
         
        #creamos el string que ejecutamos en la base de datos
        sql = '''UPDATE {nombreTabla} SET '''.format(nombreTabla = self.nombreTablaSqlite)
        
        listaKeys = diccionarioTablaSqlite.keys()
        
        while listaKeys != []:
            key = listaKeys[0]
            valorCampo = diccionarioTablaSqlite[key]
            if valorCampo.__class__ == str:
                valorCampo = str(valorCampo,'cp1252')            
            
            if isinstance(valorCampo, basestring):
                sql += '''{nombreCampo} = "{valorCampo}" '''.format(nombreCampo = key,
                                                               valorCampo = valorCampo)
            else:
                sql += '''{nombreCampo} = {valorCampo} '''.format(nombreCampo = key,
                                                               valorCampo = valorCampo)                
        
            listaKeys.remove(key)
            if len(listaKeys) >= 1: #si hay uno, ya no tiene que poner la coma
                sql += ''', '''
                
        sql += " WHERE "
        
        contador = 0
        for nombreVariable in kwargs:
            sql += '''{nombreVariable} = "{valorVariable}"'''.format(nombreVariable = nombreVariable,
                                                                  valorVariable = kwargs[nombreVariable])
            contador += 1
            
            if contador < len(kwargs):
                sql += ''' AND '''
                
        cursor.execute(sql.encode('cp1252'))
 
        #guardar cambios
        conexion.commit()

        conexion.close()

        
        
    @classmethod
    def eliminarTablaSqlite(cls):
        '''
        Class: Model
        '''
        import sqlite3
  
        #crear conexion
        conexion = sqlite3.connect(cls.rutaBaseDatos)  
        #crear cursor
        cursor = conexion.cursor()   
        
        primeraInstancia = cls.objects.first()
        if primeraInstancia == None:
            primeraInstancia = cls()

        #borrar tabla
        cursor.execute(u"DROP TABLE if exists {nombreTabla};".format(nombreTabla = primeraInstancia.nombreTablaSqlite))
        
        #guardar cambios
        conexion.commit()
        
    @classmethod
    def limpiarTablaSqlite(cls):
        '''
        Class: Model
        '''
        
        if not cls.existeTablaSqlite():
            return 
        
        import sqlite3
        
        #crear conexion
        conexion = sqlite3.connect(cls.rutaBaseDatos)  
        #crear cursor
        cursor = conexion.cursor()   
        
        primeraInstancia = cls.objects.first()
        if primeraInstancia == None:
            primeraInstancia = cls()
        
        #borrar tabla
        cursor.execute(u"DELETE FROM {nombreTabla};".format(nombreTabla = primeraInstancia.nombreTablaSqlite))
        
        #guardar cambios
        conexion.commit()
        
    
    def borrarInstanciaEnTablaSqlite(self, 
                                     **kwargs):
        '''
        Class: Model
        **kwargs: si le paso argumentos, borra los elementos que cumplan la condicion dada, 
        Sino, coge los argumentos de diccionarioTAblaSqlite, es decir, todos los descriptores
        '''
        if not self.existeTablaSqlite():
            return 
        
        if kwargs == {}:
            kwargs = self.diccionarioTablaSqlite
            
        import sqlite3
          
        #crear conexion
        conexion = sqlite3.connect(self.rutaBaseDatos)   
        #crear cursor
        cursor = conexion.cursor()   
        #borrar tabla

        sql = u"DELETE FROM {nombreTabla} WHERE ".format(nombreTabla = self.nombreTablaSqlite)
        
        contador = 0
        for nombreVariable in kwargs:
            sql += u"{nombreVariable} = '{valorVariable}'".format(nombreVariable = nombreVariable,
                                                                  valorVariable = kwargs[nombreVariable])
            contador += 1
            
            if contador < len(kwargs):
                sql += u' AND '
                
        cursor.execute(sql)
                
        
        #guardar cambios
        conexion.commit()

        
        
    def serializarInstanciaJson(self):
        '''
        Class: Model
        Crea un diccionario json con la info de la instancia y de todas las relacionadas aguas abajo.
        Nunca aguas arriba
        '''

        #para atributos
        nuevoDiccionario = {}
        nuevoDiccionario[u'className'] = self.__class__.__name__
        nuevoDiccionario[u'classModuleName'] = self.__module__
        
        for nombreAtributo in self.getNombresAtributosInstancia():
            if nombreAtributo[0] == '_': 
                continue
            
            if nombreAtributo == u'datosOriginalCex':
                continue
            
            valorAtributo = getattr(self,nombreAtributo)
            
            if valorAtributo.__class__ == list and valorAtributo != []: #si es un related_name es un listado de instancias que son objetos
                #es una lista de instancias, por lo tanto es un FK
                #comprobamos que el tipo del primer elemento que encuentra en la lista y vemos si es instance o  no
                if valorAtributo[0].__class__ not in [NoneType, str, tuple, float, int, 
                                               list, bool, dict]:
                    #es un ForeignKey
                    listadoDiccionariosRelatedName = []
                    for instance in valorAtributo:
                        dicc = instance.serializarInstanciaJson()
                        listadoDiccionariosRelatedName.append(dicc)
                    nuevoDiccionario[nombreAtributo] = listadoDiccionariosRelatedName
                    
                else:
                    #es una lista de atributos normales 
                    atributoIsInstance = False
                    nuevoDiccionario[nombreAtributo] = valorAtributo
                    
            elif valorAtributo.__class__ in [NoneType, str, tuple, float, int, 
                                               list, bool, dict]:
                nuevoDiccionario[nombreAtributo] = valorAtributo
                
                
            else: 
                #es un OTO
                if hasattr(valorAtributo, 'serializarInstanciaJson') and ismethod(getattr(valorAtributo, 'serializarInstanciaJson')):
                    try:
                        jsonOTO = valorAtributo.serializarInstanciaJson() #es una instancia
                        nuevoDiccionario[nombreAtributo] = jsonOTO
                    except Exception as e:
                        print(e)
                        

        for nombreDescriptor in self.getNombresDescriptoresInstancia():
            valorDescriptor = getattr(self,nombreDescriptor)

            if valorDescriptor.__class__ not in [NoneType, str, tuple, float, int, 
                                               list, bool, dict]:
                 
                descriptorIsInstance = True
            else: 
                descriptorIsInstance = False
                 
            if descriptorIsInstance: #xa evitar recursividad.  Nunca serializamos aguas arriba, solo aguas abajo. 
                pass
                 
            else:
                nuevoDiccionario[nombreDescriptor] = valorDescriptor
                            
        stringJson = json.dumps(nuevoDiccionario,ensure_ascii=False)
        
        return stringJson
    
        
        
    def loadDesdeJson(self, string):
        '''
        class: Model
        Crea la instancia a partir de un diccionario json
        En caso de que haya relaciones aguas abajo de FK o OTO las crear� y establecer� las relaciones.
        Nunca aguas arriba
        '''
        diccionario = json.loads(string)
                
        for key in diccionario.keys():
            value = diccionario[key]
            
            if key[0] == '_' or key == u'className' or key == u'classModuleName': 
                continue
            
            elif self.getInstanciaDescriptor(key) != None: #Est� entre los Fields del Models: FloatField, BooleanField, etc...
                setattr(self, key, value)
                
            else:
                if type(value) == list: #es un listado de diccionarios - un FK
                    #esto ocurre cuando se encuentra un related_name
                    #el value es una lista de json, con la informaci�n para crear las instancias relaciondas
                     
                    try: 
                        diccionarioString = json.loads(value[0]) #si se puede hacer esto es que es una lista de ForeignKeys
                        
                        for stringLista in value:
                            #para cada elemento de la lista, creamos la instancia
                            diccionarioString = json.loads(stringLista)
                            module = sys.modules[diccionarioString[u'classModuleName']]
                            instancia = getattr(module, diccionarioString[u'className'])() #creamos la instancia - cerramiento
                            
                            #le cargamos a la instancia toda la informaci�n
                            instancia.loadDesdeJson(stringLista)
        
                            #ahora, a la instancia le decimos qu� relaci�n tiene con self
                            #por ejemplo: self = Proyecto. la instancia = Cerramiento. Tenemos que hacer cerramiento.proyecto = self
                            
                            #Recorremos todos los descriptores de la instancia (cerramiento) y buscamos si hay alguno tipo FK o OTO
                            #Una vez encontrado alguno, comprobamos que su modelo asociado es el mismo que self. ForeignKey(model = Proyecto)
                            #en ese caso,a la instancia creada le asociamos self, al descriptor correspondiente. instancia.proyecto = Proyecto
                            for nombreDescriptor in instancia.getNombresDescriptoresInstancia():
                                instanciaDescriptor = instancia.getInstanciaDescriptor(nombreDescriptor)
                                
                                if isinstance(instanciaDescriptor, ForeignKey):
                                    if instanciaDescriptor.model.__name__ == self.__class__.__name__: #si el modelo asociado al descriptor es el mismo que self, se asigna
                                        setattr(instancia, nombreDescriptor, self)
                        
                        
                    except: #no es un json lo que llega 
                        setattr(self, key, value)
                        
                                    
                else:
                    try: 
                        #es un OTO
                        diccionarioString = json.loads(value) #es un Json y corresponde a una relaci�n OTO
                        module = sys.modules[diccionarioString[u'classModuleName']]
                             
                        instancia = getattr(module, diccionarioString[u'className'])() #creamos la instancia - cerramiento
                         
                        #le cargamos a la instancia toda la informaci�n
                        instancia.loadDesdeJson(value)
                         
                        #Recorremos todos los descriptores de la instancia (cliente) y buscamos si hay alguno tipo OTO
                        #Una vez encontrado alguno, comprobamos que su modelo asociado es el mismo que self. OTO(model = Proyecto)
                        #en ese caso,a la instancia creada le asociamos self, al descriptor correspondiente. instancia.proyecto = Proyecto
                        for nombreDescriptor in instancia.getNombresDescriptoresInstancia():
                            instanciaDescriptor = instancia.getInstanciaDescriptor(nombreDescriptor)
                             
                            if isinstance(instanciaDescriptor, OneToOneField):
                                if instanciaDescriptor.model.__name__ == self.__class__.__name__: #si el modelo asociado al descriptor es el mismo que self, se asigna
                                    setattr(instancia, nombreDescriptor, self)       
                                    
                    except: #es un campo cualuqiera, que no es in ForeignKey, ni OTO, ni FloatField, ni nada
                        setattr(self, key, value)             


class Descriptor(Model):
    """
    """
    def snoop_name(self, owner):
        for attr in dir(owner):
            if getattr(owner, attr) is self:
                return attr
 
    def __init__(self, default=None, name='var'):
        self.val = default
        self.name = name
 
    def __get__(self, instance, owner):  
        ''' 
        '''       
        if instance is None:
            return self
        name = self.snoop_name(owner)
        if hasattr(instance, '_'+name):
            return getattr(instance,'_'+name)
        else:
            return self.val
    
    def __set__(self, instance, val):    
        ''' Al hacer set, vamos a inyectar el valor a las instancias de MyClass (m1 � m2). El nombre del
            atributo a inyectar ser� _x � _y (el nombre al que estamos asignado el descriptor). El valor queda almacenado
            en _x � _y y no se puede almacenar directamente en x e y porque se producir�a un bucle infinito de recursividad 
        '''
        
        name = self.snoop_name(type(instance))
        setattr(instance,  '_'+name,val)         
         
class FloatField(Descriptor):
    
    def __init__(self, 
                 default = None, 
                 verbose_name = None,
                 min = None,
                 max = None,
                 minNoPuedeSerIgual = None,
                 maxNoPuedeSerIgual = None, 
                 required = False):
        self.val = default
        self.verbose_name = verbose_name  
        self.min = min
        self.max = max 
        self.minNoPuedeSerIgual = minNoPuedeSerIgual
        self.maxNoPuedeSerIgual = maxNoPuedeSerIgual
        self.required = required 
        



    def getListaErrores(self,val):
        '''
        Class: FloatField
        '''
        listaErrores = []
        
        if val == None: 
            if not self.required:
                return listaErrores
            
            elif self.required:
                listaErrores.append(u'El campo es obligatorio')
                return listaErrores
        
        else:
            if type(val) != float:
                listaErrores.append(u'El campo tiene que ser un n�mero decimal')
                return listaErrores
            
            # Minimos: el valor no puede ser inferior pero s� igual
            if self.min != None:
                if val < self.min :
                    listaErrores.append(u'El valor debe ser superior o igual a {0}'.format(self.min))
            
            if self.max != None:
                if val > self.max :
                    listaErrores.append(u'El valor debe ser inferior o igual a {0}'.format(self.max))
                    
            # Minimos: el valor tiene que ser menor obligatoriamente, no puede ser igual
            if self.minNoPuedeSerIgual != None:
                if val <= self.minNoPuedeSerIgual :
                    listaErrores.append(u'El valor debe ser superior a {0}'.format(self.minNoPuedeSerIgual))
            
            if self.maxNoPuedeSerIgual != None:
                if val >= self.maxNoPuedeSerIgual :
                    listaErrores.append(u'El valor debe ser inferior a {0}'.format(self.maxNoPuedeSerIgual))                
                    
            return listaErrores
                
#     @property                 
#     def esCorrecto(self):
#         '''
#         Class: FloatField
#         Creo que no lo estamos usando
#         '''
#         if self.errores == []:
#             return True
#         else:
#             return False



class CharField(Descriptor):
    
    def __init__(self, 
                 default = None, 
                 verbose_name = None, 
                 max_length = None,
                 required = False,
                 unico = False):
        self.val = default
        self.verbose_name = verbose_name 
        self.max_length = max_length 
        self.required = required 
        self.unico = unico
        
    
        
    def getListaErrores(self,val):
        '''
        Class: CharField
        '''
        listaErrores = []
        
        if val == None:
            if not self.required: #es correcto, no es requerido y no se ha indicado nada
                return listaErrores
            
            elif self.required:
                listaErrores.append(u'El campo es obligatorio')
                return listaErrores
            
        else:
            # if type(val) != UnicodeType:
            #     listaErrores.append(u'El campo tiene que ser unicode')
            #     return listaErrores
            
            if val == u'' and self.required:
                listaErrores.append(u'El campo es obligatorio')
                return listaErrores
                
            
            if self.max_length != None and type(self.max_length) == int:
                if len(val) > self.max_length:
                    listaErrores.append(u'El campo no puede tener m�s de {numeroCaracteres} caracteres'.format(numeroCaracteres = self.max_length))
                    
            return listaErrores
                
                
class BooleanField(Descriptor):
    
    def __init__(self, 
                 default = None, 
                 verbose_name = None, 
                 required = False):
        self.val = default
        self.verbose_name = verbose_name  
        self.required = required 
        
        
        

    def getListaErrores(self,val):
        '''
        Class: BooleanField
        '''
        listaErrores = []
        
        if val == None:
            if not self.required: #es correcto, no es requerido y no se ha indicado nada
                return listaErrores
            
            elif self.required:
                listaErrores.append(u'El campo es obligatorio')
                return listaErrores
        
        else:
            if type(val) != bool:
                listaErrores.append(u'El campo tiene que ser de tipo boolean')
                return listaErrores             
                    
            return listaErrores
                
                                
class ListField(Descriptor):
    
    def __init__(self, 
                 default = None, 
                 verbose_name = None, 
                 max_length = None,
                 required = False):
        self.val = default
        self.verbose_name = verbose_name 
        self.max_length = max_length 
        self.required = required 
        

        
        
    def getListaErrores(self,val):
        '''
        Class: ListField
        '''
        listaErrores = []
        
        if val == None:
            if not self.required: #es correcto, no es requerido y no se ha indicado nada
                return listaErrores
            
            elif self.required:
                listaErrores.append(u'El campo es obligatorio')
                return listaErrores
        
        else:
            if type(val) != list:
                listaErrores.append(u'El campo tiene que ser de tipo una lista')
                return listaErrores   
            
            if val == [] and self.required:
                listaErrores.append(u'El campo es obligatorio')
                return listaErrores            


            if self.max_length != None:
                if len(val) > self.max_length:
                    listaErrores.append(u'La lista no puede tener m�s de {longitudMaxima} elementos'.format(longitudMaxima = self.max_length))
                
            return listaErrores
                
                

class ChoiceField(Descriptor):
    
    def __init__(self, 
                 default = None, 
                 verbose_name = None, 
                 choices = None,
                 required = False):
        self.val = default
        self.verbose_name = verbose_name 
        self.choices = choices 
        self.required = required 
        
        
        
    def getListaErrores(self,val):
        '''
        Class: ChoiceField
        '''
        listaErrores = []
        
        if val == None:
            if not self.required: #es correcto, no es requerido y no se ha indicado nada
                return listaErrores
            
            elif self.required:
                listaErrores.append(u'El campo es obligatorio')
                return listaErrores
        
        else:
            if self.choices != None:
                if val not in self.choices:
                    listaErrores.append(u'El campo no es v�lido')
                    return listaErrores   

            return listaErrores
                               
        
class ForeignKey(Model):
    objects = Manager()
    def __init__(self,
                 model = None,
                 verbose_name = None,
                 related_name = u'',
                 required = False):
        self.model = model
        self.related_name = related_name
        self.verbose_name = verbose_name #de momento no lo usamos para nada, pero se pone para tratarlo igual que FloatField o Charfield
        
        super(ForeignKey, self).__init__()    
    
    def __get__( self, instance, owner ):    
        '''
        Class: ForeignKey
        '''
        if hasattr(instance, 'instanciaPadre' + self.model.__name__+"_{0}".format(self.id)):
            return getattr(instance, 'instanciaPadre' + self.model.__name__+"_{0}".format(self.id))
        else:
            return None    
    
    def __set__( self, instance, instanciaPadre ):
        '''
        Class: ForeignKey
        '''
        setattr(instance, 'instanciaPadre' + self.model.__name__+"_{0}".format(self.id), instanciaPadre)  
        
        if instanciaPadre != None:
        
            # Creamos el atributo en la clase padre con el nombre indicado en related_name
            if not hasattr(instanciaPadre,self.related_name):
                setattr(instanciaPadre,self.related_name,[])
            
            listadoInstanciasReferenciadas = getattr(instanciaPadre,self.related_name)
            if not instance in listadoInstanciasReferenciadas:
                listadoInstanciasReferenciadas.append(instance)
                setattr(instanciaPadre,self.related_name,listadoInstanciasReferenciadas)
    
    
    def __delete__(self,instancia):
        '''
        Class: ForeignKey
        '''
        
        if hasattr(instancia,"instanciaPadre{}_{}".format(self.model.__name__,self.id)):
            instanciaPadre = getattr(instancia,"instanciaPadre{}_{}".format(self.model.__name__,self.id))
            listadoRelacionados = getattr(instanciaPadre,self.related_name)
            listadoRelacionados.remove(instancia)
            
          
class OneToOneField(Model):
    objects = Manager()
    def __init__(self,
                 model = None,
                 related_name = None,
                 verbose_name = None,
                 required = False):
        
        self.model = model
        self.related_name = related_name
        self.required = required
        self.verbose_name = verbose_name #de momento no lo usamos para nada, pero se pone para tratarlo igual que FloatField o Charfield
        #si hay related_name, se relacionan as�, sino coge el nombre en minusculas
        super(OneToOneField, self).__init__()    
    
    def __get__( self, instance, owner ):
        '''
        Class: OneToOneField
        '''
        if hasattr(instance, 'instanciaPadre' + self.model.__name__):
            return getattr(instance, 'instanciaPadre' + self.model.__name__)
        else:
            return None
    
    
    def __set__( self, instance, instanciaPadre ):
        '''
        Class: OneToOneField
        '''
        setattr(instance, 'instanciaPadre' + self.model.__name__, instanciaPadre)
        
        if self.related_name != None:
            related_name = self.related_name
            
        else:
            related_name = instance.__class__.__name__.lower()
        
        if instanciaPadre != None:
            instance.instanciaPadre = instanciaPadre    
            
            # Creamos el atributo en la clase padre con el nombre indicado en related_name
            if not hasattr(instanciaPadre, related_name):
                setattr(instanciaPadre, related_name, None)
                

            setattr(instanciaPadre, related_name, instance)    
            
            
    def __delete__(self,instancia):
        '''
        Class: OneToOneField
        '''
        if hasattr(instancia,"instanciaPadre{0}".format(self.model.__name__)):
            instanciaPadre = getattr(instancia,"instanciaPadre{0}".format(self.model.__name__))
            setattr(instanciaPadre,self.related_name,None)
            
    
    def getListaErrores(self):
        '''
        Class: OneToOneField
        comentario
        '''
        listaErrores = []
        existeLaRelacion = hasattr(self.__dict__['model'], self.__dict__['related_name'])
        
        if self.required and not existeLaRelacion: #TODO: COMPROBAR SI ESTO ESTA BIEN
            listaErrores.append(u'El campo es obligatorio')
        return listaErrores
                
                
class DateField(Descriptor):    
    def __init__(self, 
                 default = None, 
                 verbose_name = None, 
                 min = None,
                 max = None,
                 required = False):
        self.val = default
        self.verbose_name = verbose_name 
        self.required = required 
        self.min = min
        self.max = max
        
    
    def __set__(self, instance, val):    
        ''' Almacenamos un objecto en formato date
        '''
        
        name = self.snoop_name(type(instance))
        
        if val.__class__ == datetime.date:
            setattr(instance,  '_'+name,val)            
        elif val != None:
            fechaEnFormatoDate = datetime.datetime.strptime(val, "%d/%m/%Y").date()
            setattr(instance,  '_'+name,fechaEnFormatoDate)       
        else:
            setattr(instance,  '_'+name,None)    
    
    def getListaErrores(self,val):
        
        '''
        Class: CharField
        '''
        listaErrores = []
        
        if val == None:
            if not self.required: #es correcto, no es requerido y no se ha indicado nada
                return listaErrores
            
            elif self.required:
                listaErrores.append(u'El campo es obligatorio')
                return listaErrores
            
        else:
            if type(val) != datetime.date:
                listaErrores.append(u'El campo tiene que ser datetime.date')
                return listaErrores
            
            if val == u'' and self.required:
                listaErrores.append(u'El campo es obligatorio')
                return listaErrores
                
            if self.min != None:
                if val < self.min:
                    listaErrores.append(u'La fecha no puede ser anterior a {:%d/%m/%Y}'.format(self.min))
                    
            if self.max != None:
                if val > self.max:
                    listaErrores.append(u'La fecha no puede ser posterior a {:%d/%m/%Y}'.format(self.max))                
                    
            return listaErrores                