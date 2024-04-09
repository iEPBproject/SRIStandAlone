# -\*- coding: utf-8 -\*-
'''
Created on 6 may 2022

@author: mapas
'''
from miDjangoModel.models import Model, FloatField, Manager


class Prueba(Model):
    objects = Manager()
    a = FloatField()
    
    def __init__(self, **kwargs):
        Model.__init__(self, **kwargs)
if __name__ == '__main__':
    p = Prueba()
    p.a = 10000.2565566556541212
    
    
    print p.a.asTxt()