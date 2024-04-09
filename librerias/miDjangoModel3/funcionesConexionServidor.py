## -*- coding: cp1252 -*-
import json
import logging
import urllib2


def comprobarVersionActualComplemento(versionActual = u'',
                                      nombreComplemento = u'', 
                                      server = u''):
    '''
    Comprueba si la versión del complemento es la actual. 
    Devuelve True o False y direccion url en caso de que haya nueva version
    '''
    direccionUrl = 'http://%s/controlUsoComplemento/comprobarVersion/%s/%s'%(server, nombreComplemento, versionActual)
    try: 
        url = urllib2.urlopen(direccionUrl)
        dicc_string = url.read()
        dicc = json.loads(dicc_string)
        esVersionActual = dicc[u'esVersionActual']
        urlDescargaNuevaVersion = dicc[u'urlVersionActual']
        
        return esVersionActual, urlDescargaNuevaVersion

    except urllib2.URLError: #no hay conexion a internet para ver si es la version actual, plq se supone que si para que siga adelante
        logging.warning(u'Exception', exc_info=True)
        esVersionActual = True
        return esVersionActual, u''
     

    except: #ha habido un error y no se ha podido comprobar si es la version actual, plq se supone que si para que siga adelante
        logging.warning(u'Exception', exc_info=True)
        esVersionActual = True   
        return esVersionActual, u''

def descargaDatosEnJSONDelServidor(server = '', funcionURL = ''):
    direccionUrl = '%s/%s'%(server,funcionURL)
    
    url = urllib2.urlopen(direccionUrl)
    html = url.read()
   
    try:
        json_data = json.loads(html)
    except:
        json_data = []
    return json_data
