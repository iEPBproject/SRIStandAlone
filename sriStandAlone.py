'''
Created on 2 abr 2024

@author: efinovatic
'''
import sys, getopt
from exportarXML import exportarSri2Market
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
        elif opt in ("-o", "--ofile"):
            outputfile = arg
            exportarSri2Market()
    print ('Input file is {}'.format(inputfile))
    print ('Output file is {}'.format(outputfile))
    
if __name__ == "__main__":
    # print(sys.argv[:1])
    # sys.argv.append(r'C:\temp\test.iEPBXML -o')
    # print(sys.argv[1:])
    # main(sys.argv[1:])
    main(sys.argv[1:])
    # main(r'C:\temp\test.iEPBXML -o')