'''
Created on 2 abr 2024

@author: efinovatic
'''
import sys, getopt
from modulos.operacionesXML import importarSriStandAlone, escribirResultadosSri,\
    escribirXML




def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:p",["ifile=","ofile=","pfile="])
    except getopt.GetoptError:
        print ('Las opciones admitidas son las siguientes --> -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('Las unicas opciones disponibles son: -i <inputfile> -o <outputfile> -p <file>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
            importarSriStandAlone(inputfile)
            print ('El archivo XML ha sido importado correctamente')
        elif opt in ("-o", "--ofile"):
            outputfile = arg
            escribirXML(inputfile, outputfile)
            print ('El archivo XML se ha mostrado correctamente en --> {}'.format(outputfile))
        elif opt in ("-p", "--pfile"):
            print ('Estos son los resultados que se han encontrado')
            escribirResultadosSri(inputfile)
    # print ('Input file is {}'.format(inputfile))
    # print ('Output file is {}'.format(outputfile))
    
if __name__ == "__main__":
    # print("Hello sriStandAlone")
    # print(sys.argv[:1])
    # sys.argv.append(r'C:\temp\test.iEPBXML -o')
    # print(sys.argv[1:])
    main(sys.argv[1:])
    # main(r'C:\temp\test.iEPBXML -o')