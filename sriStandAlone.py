'''
Created on 2 abr 2024

@author: efinovatic
'''
import sys, getopt
from importarXML import importarSriStandAlone

def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print ('Las opciones admitidas son las siguientes --> -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('Las unicas opciones disponibles son: -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
            importarSriStandAlone()
            print ('El archivo XML ha sido importado correctamente')
        elif opt in ("-o", "--ofile"):
            outputfile = arg
            print ('El archivo XML ha sido exportado correctamente')
    print ('Input file is {}'.format(inputfile))
    print ('Output file is {}'.format(outputfile))
    
if __name__ == "__main__":
    # print(sys.argv[:1])
    # sys.argv.append(r'C:\temp\test.iEPBXML -o')
    # print(sys.argv[1:])
    # main(sys.argv[1:])
    main(sys.argv[1:])
    # main(r'C:\temp\test.iEPBXML -o')