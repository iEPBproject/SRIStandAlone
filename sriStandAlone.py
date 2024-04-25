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
    
    parser = argparse.ArgumentParser(description = 'Importa proyectos sri para mostrar los calculos en pantalla o crear nuevos xml')
    parser.add_argument('-i','--import_file', type=str, help="Importa proyectos", required=True)
    parser.add_argument('-o','--output_file', type=str, help="Exporta proyectos")
    parser.add_argument('-p','--result_file', type=str, help="Imprime todos los resultados del proyectos", nargs='?')
    parser.add_argument('-s','--result_SRI', type=str, help="Imprime el resultado SRI del proyecto", nargs='?')
    parser.add_argument('-e','--result_Kf1', type=str, help="Imprime el resultado Kf1 del proyecto", nargs='?')
    parser.add_argument('-n','--result_Kf2', type=str, help="Imprime el resultado Kf2 del proyecto", nargs='?')
    parser.add_argument('-f','--result_Kf3', type=str, help="Imprime el resultado Kf3 del proyecto", nargs='?')
    parser.add_argument('-x','--extract_files', type=str, help="Extrae los xml y los guarda en el mismo sitio o en la ruta introducida", nargs='?')
    
    args = parser.parse_args()
    
    if args.output_file and '-o' in argv:
        inputfile = args.import_file
        outputfile = args.output_file
        importarSriStandAlone(inputfile)
        print ('El archivo XML ha sido importado correctamente')
        escribirXML(inputfile, outputfile)
        
    elif args.result_file:
        if args.import_file != args.result_file:
            importarSriStandAlone(args.import_file)
            print ('El archivo XML ha sido importado correctamente')
            print('Error: El archivo importado y el archivo para imprimir resultados deben ser el mismo')
            sys.exit()
        else:
            importarSriStandAlone(args.import_file)
            print ('El archivo XML ha sido importado correctamente')
            inputfile = args.result_file
            imprimirTodosResultadosSri(inputfile)
    elif not args.result_file and '-p' in argv:
        args.result_file = args.import_file
        importarSriStandAlone(args.import_file)
        print ('El archivo XML ha sido importado correctamente')
        inputfile = args.import_file
        imprimirTodosResultadosSri(inputfile)
        
    elif args.result_SRI:
        if args.import_file != args.result_SRI:
            importarSriStandAlone(args.import_file)
            print ('El archivo XML ha sido importado correctamente')
            print('Error: El archivo importado y el archivo para imprimir resultado del SRI deben ser el mismo')
            sys.exit()
        else:
            importarSriStandAlone(args.import_file)
            print ('El archivo XML ha sido importado correctamente')
            inputfile = args.result_SRI
            imprimirResultadoSRI(inputfile)
    elif not args.result_SRI and '-s' in argv:
        args.result_SRI = args.import_file
        importarSriStandAlone(args.import_file)
        print ('El archivo XML ha sido importado correctamente')
        inputfile = args.result_SRI
        imprimirResultadoSRI(inputfile)
         
    elif args.result_Kf1:
        if args.import_file != args.result_Kf1:
            importarSriStandAlone(args.import_file)
            print ('El archivo XML ha sido importado correctamente')
            print('Error: El archivo importado y el archivo para imprimir resultado total de Energy Perfomance (Kf1) deben ser el mismo')
            sys.exit()
        else:
            importarSriStandAlone(args.import_file)
            print ('El archivo XML ha sido importado correctamente')
            inputfile = args.result_Kf1
            imprimirResultadoKf1(inputfile)
    elif not args.result_Kf1 and '-e' in argv:
        args.result_Kf1 = args.import_file
        importarSriStandAlone(args.import_file)
        print ('El archivo XML ha sido importado correctamente')
        inputfile = args.result_Kf1
        imprimirResultadoKf1(inputfile)
        
    elif args.result_Kf2:
        if args.import_file != args.result_Kf2:
            importarSriStandAlone(args.import_file)
            print ('El archivo XML ha sido importado correctamente')
            print('Error: El archivo importado y el archivo para imprimir resultado total de Response To User Needs (Kf2) deben ser el mismo')
            sys.exit()
        else:
            importarSriStandAlone(args.import_file)
            print ('El archivo XML ha sido importado correctamente')
            inputfile = args.result_Kf2
            imprimirResultadoKf2(inputfile)
    elif not args.result_Kf2 and '-n' in argv:
        args.result_Kf2 = args.import_file
        importarSriStandAlone(args.import_file)
        print ('El archivo XML ha sido importado correctamente')
        inputfile = args.result_Kf2
        imprimirResultadoKf2(inputfile)
        
    elif args.result_Kf3:
        if args.import_file != args.result_Kf3:
            importarSriStandAlone(args.import_file)
            print ('El archivo XML ha sido importado correctamente')
            print('Error: El archivo importado y el archivo para imprimir resultado total de Energy Flexibility (Kf3) deben ser el mismo')
            sys.exit()
        else:
            importarSriStandAlone(args.import_file)
            print ('El archivo XML ha sido importado correctamente')
            inputfile = args.result_Kf3
            imprimirResultadoKf3(inputfile)
    elif not args.result_Kf3 and '-f' in argv:
        args.result_Kf3 = args.import_file
        importarSriStandAlone(args.import_file)
        print ('El archivo XML ha sido importado correctamente')
        inputfile = args.result_Kf3
        imprimirResultadoKf3(inputfile)
    
    elif args.extract_files:
        importarSriStandAlone(args.import_file)
        print ('El archivo XML ha sido importado correctamente')
        extraerArchivos(args.import_file, args.extract_files)
    elif not args.extract_files and '-x' in argv:
        importarSriStandAlone(args.import_file)
        print ('El archivo XML ha sido importado correctamente')
        args.extract_files = args.import_file
        extraerArchivos(args.extract_files)
    else:
        importarSriStandAlone(args.import_file)
        print ('El archivo XML ha sido importado correctamente') 
        
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