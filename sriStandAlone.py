'''
Created on 2 abr 2024

@author: efinovatic
'''
import sys, getopt
import argparse
from modulos.operacionesXML import importarSriStandAlone, imprimirTodosResultadosSri,\
    escribirXML, imprimirResultadoSRI, imprimirResultadoKf1, imprimirResultadoKf2, imprimirResultadoKf3, \
    extraerArchivos




def main(argv):
    inputfile = ''
    outputfile = ''
    # try:
    #     opts, args = getopt.getopt(argv,"hi:o:p",["ifile=","ofile=","pfile="])
    # except getopt.GetoptError:
    #     print ('Las opciones admitidas son las siguientes --> -i <inputfile> -o <outputfile>')
    #     sys.exit(2)
    # for opt, arg in opts:
    #     if opt == '-h':
    #         print('Las unicas opciones disponibles son: -i <inputfile> -o <outputfile> -p <file>')
    #         sys.exit()
    #     elif opt in ("-i", "--ifile"):
    #         inputfile = arg
    #         importarSriStandAlone(inputfile)
    #         print ('El archivo XML ha sido importado correctamente')
    #     elif opt in ("-o", "--ofile"):
    #         outputfile = arg
    #         escribirXML(inputfile, outputfile)
    #         print ('El archivo XML se ha mostrado correctamente en --> {}'.format(outputfile))
    #     elif opt in ("-p", "--pfile"):
    #         print ('Estos son los resultados que se han encontrado')
    #         escribirResultadosSri(inputfile)
    
    parser = argparse.ArgumentParser(description = 'SRI Stand Alone Applicationl')
    parser.add_argument('-i','--import_file', type=str, help="Input file", required=True)
    parser.add_argument('-o','--output_file', type=str, help="Output file")
    parser.add_argument('-p','--result_file', type=str, help="Print results", nargs='?')
    parser.add_argument('-s','--result_SRI', type=str, help="Print main result only", nargs='?')
    parser.add_argument('-kf1','--result_Kf1', type=str, help="Print Kf1 result", nargs='?')
    parser.add_argument('-kf2','--result_Kf2', type=str, help="Print Kf2 result", nargs='?')
    parser.add_argument('-kf3','--result_Kf3', type=str, help="Print Kf3 result", nargs='?')
    parser.add_argument('-x','--extract_files', type=str, help="Extract xml and gbXML from iEPB file", nargs='?')
    
    args = parser.parse_args()
    
    if args.output_file and '-o' in argv:
        inputfile = args.import_file
        outputfile = args.output_file
        importarSriStandAlone(inputfile)
        print ('iEPB loaded')
        escribirXML(inputfile, outputfile)
        
    elif args.result_file:
        if args.import_file != args.result_file:
            importarSriStandAlone(args.import_file)
            print ('iEPB loaded')
            print('Error: Input and result files should be the same')
            sys.exit()
        else:
            importarSriStandAlone(args.import_file)
            print ('iEPB loaded')
            inputfile = args.result_file
            imprimirTodosResultadosSri(inputfile)
    elif not args.result_file and '-p' in argv:
        args.result_file = args.import_file
        importarSriStandAlone(args.import_file)
        print ('iEPB loaded')
        inputfile = args.import_file
        imprimirTodosResultadosSri(inputfile)
        
    elif args.result_SRI:
        if args.import_file != args.result_SRI:
            importarSriStandAlone(args.import_file)
            print('Error: Input and result files should be the same')
            sys.exit()
        else:
            importarSriStandAlone(args.import_file)
            inputfile = args.result_SRI
            imprimirResultadoSRI(inputfile)
    elif not args.result_SRI and '-s' in argv:
        args.result_SRI = args.import_file
        importarSriStandAlone(args.import_file)
        inputfile = args.result_SRI
        imprimirResultadoSRI(inputfile)
         
    elif args.result_Kf1:
        if args.import_file != args.result_Kf1:
            importarSriStandAlone(args.import_file)
            print('Error: Error: Input and result files should be the same')
            sys.exit()
        else:
            importarSriStandAlone(args.import_file)
            inputfile = args.result_Kf1
            imprimirResultadoKf1(inputfile)
    elif not args.result_Kf1 and '-kf1' in argv:
        args.result_Kf1 = args.import_file
        importarSriStandAlone(args.import_file)
        inputfile = args.result_Kf1
        imprimirResultadoKf1(inputfile)
        
    elif args.result_Kf2:
        if args.import_file != args.result_Kf2:
            importarSriStandAlone(args.import_file)
            print('Error: Error: Input and result files should be the same')
            sys.exit()
        else:
            importarSriStandAlone(args.import_file)
            inputfile = args.result_Kf2
            imprimirResultadoKf2(inputfile)
    elif not args.result_Kf2 and '-kf2' in argv:
        args.result_Kf2 = args.import_file
        importarSriStandAlone(args.import_file)
        inputfile = args.result_Kf2
        imprimirResultadoKf2(inputfile)
        
    elif args.result_Kf3:
        if args.import_file != args.result_Kf3:
            importarSriStandAlone(args.import_file)
            print('Error: Error: Input and result files should be the same')
            sys.exit()
        else:
            importarSriStandAlone(args.import_file)
            inputfile = args.result_Kf3
            imprimirResultadoKf3(inputfile)
    elif not args.result_Kf3 and '-kf3' in argv:
        args.result_Kf3 = args.import_file
        importarSriStandAlone(args.import_file)
        inputfile = args.result_Kf3
        imprimirResultadoKf3(inputfile)
    
    elif args.extract_files:
        importarSriStandAlone(args.import_file)
        extraerArchivos(args.import_file, args.extract_files)
    elif not args.extract_files and '-x' in argv:
        importarSriStandAlone(args.import_file)
        args.extract_files = args.import_file
        extraerArchivos(args.extract_files)
    else:
        importarSriStandAlone(args.import_file)
        print ('iEPB loaded') 
        
    # else:
    #     inputfile = args.import_file
    #     importarSriStandAlone(inputfile)
    #     print ('El archivo XML ha sido importado correctamente')
    
if __name__ == "__main__":
    # print("Hello sriStandAlone")
    # print(sys.argv[:1])
    # sys.argv.append(r'C:\temp\test.iEPBXML -o')
    # print(sys.argv[1:])
    main(sys.argv[1:])
    # main(r'C:\temp\test.iEPBXML -o')