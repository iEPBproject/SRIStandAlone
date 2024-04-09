# -\*- coding: utf-8 -\*-
'''
Created on 28 oct. 2018

@author: mapas
'''


import string
import random
def random_string(length):
    return ''.join(random.choice(string.ascii_letters) for m in xrange(length))

class CharField(object):
    
    def __init__(self, 
                 default = None, 
                 verbose_name = None, 
                 max_length = None,
                 required = False):
        self.val = default
        self.verbose_name = verbose_name 
        self.max_length = max_length 
        self.required = required 
        
    def snoop_name(self, owner):
        for attr in dir(owner):
            if getattr(owner, attr) is self:
                return attr

    def __get__(self, instance, owner):  
        ''' 
        '''       
        print "entremos en __get__"
        if instance is None:
            return self
        name = self.snoop_name(owner)
        if hasattr(instance, '_'+name):
            return getattr(instance,'_'+name)
        else:
            return self.val
    
    def __set__(self, instance, val):    
        ''' Al hacer set, vamos a inyectar el valor a las instancias de MyClass (m1 ó m2). El nombre del
            atributo a inyectar será _x ó _y (el nombre al que estamos asignado el descriptor). El valor queda almacenado
            en _x ó _y y no se puede almacenar directamente en x e y porque se produciría un bucle infinito de recursividad 
        '''
        
        name = self.snoop_name(type(instance))
        print "entremos en __set__ de {0}".format(name)
        setattr(instance,  '_'+name,val)
class RevealAccess(object):
    """A data descriptor that sets and returns values
       normally and prints a message logging their access.
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
#         print "entremos en __get__"
        if instance is None:
            return self
        name = self.snoop_name(owner)
        return getattr(instance,'_'+name)
    
    def __set__(self, instance, val):    
        ''' Al hacer set, vamos a inyectar el valor a las instancias de MyClass (m1 ó m2). El nombre del
            atributo a inyectar será _x ó _y (el nombre al que estamos asignado el descriptor). El valor queda almacenado
            en _x ó _y y no se puede almacenar directamente en x e y porque se produciría un bucle infinito de recursividad 
        '''
        name = self.snoop_name(type(instance))
        print "entremos en __set__ de {0}".format(name)
        setattr(instance,  '_'+name,val)

class MyClass(object):
    x = RevealAccess(10, 'var "x"')
    y = RevealAccess(20, 'var "y"' )
    z = RevealAccess() 
    soyGuay = CharField(default = 'hola')


if __name__ == '__main__':
    m1 = MyClass()
    m1.x = 10
    m1.y = 11
    m1.z = 12
#     m1.soyGuay = "muy guay"
    print "m1.x",m1.x
    print "m1.y",m1.y
    print "m1.z",m1.z
    print "m1.soyGuay",m1.soyGuay
    
#     m2 = MyClass()
#     m2.x = 20
#     m2.y = 21 
#     print "m2.x",m2.x    
#     print "m2.y",m2.y
#     
#     print "m1.x",m1.x
#     print "m1.y",m1.y
    