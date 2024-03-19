'''
Created on 19 mar 2024

@author: Efinovatic
'''
import xml.etree.ElementTree as ET


if __name__ == '__main__':
    tree = ET.parse('ejemplos/test.iEPBXML')
    root = tree.getroot()
    print(root.findall('.//Project'))
    # print(root)
    ns = {'d':"http://www.gbxml.org/schema"}
    for projectElement in root.findall('.//d:Project',ns):
        print(projectElement,projectElement.attrib)
        for catalogueElement in projectElement.findall('.//d:Catalogue',ns):
            print("\t",catalogueElement,catalogueElement.attrib)
            description = catalogueElement.find('.//d:description',ns)
            print("\t\t",description.text)
            for domainElement in catalogueElement.findall('.//d:Domain',ns):
                print("\t\t\t",domainElement,domainElement.attrib)
                description = domainElement.find('.//d:description',ns)
                print("\t\t\t\t",description.text)
                
                
            
            