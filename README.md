# SRIStandAlone
<!-- TABLA DE CONTENIDOS -->
<details>
  <summary>TABLA DE CONTENIDOS</summary>
  <ol>
    <li>
      <a href="#sobre-el-sristandalone">Sobre el SRIStandAlone</a>
      <ul>
        <li><a href="#programas-utilizados">Construido con</a></li>
      </ul>
    </li>
    <li>
      <a href="#iniciación">Iniciación</a>
      <ul>
        <li><a href="#prerequisitos">Prerequisitos</a></li>
        <li><a href="#instalación">Instalación</a></li>
      </ul>
    </li>
      <li><a href="#uso">Uso</a></li>
    <li><a href="#contribuciones">Contribuciones</a></li>
    <li><a href="#licencia">Licencia</a></li>
    <li><a href="#Contacto">Contacto</a></li>
  </ol>
</details>

<!-- SOBRE EL SRIStandAlone -->
## Sobre el SRIStandAlone
Es un programa que complementará al la página del SRI2Market, con el cual podremos hacer varias acciones: 
  <ul>
    <li>Cácular del proyecto e imprimir los resultados (del total del SRI, Kf1, Kf2, Kf3) por pantalla.</li> 
    <li>Exportar los xml del archivo iEPB previamente descargados de la página del SRI2Market.</li> 
    <li>Generar un nuevo iEPB con nuevos xml con los cambios realizados.</li>
    <li>Ver la versión del programa.</li>
  </ul>

<!-- PROGRAMAS UTILIZADOS -->
## Programas utilizados
Estos son los programas que con su ayuda hemos podido desarrollar el software para el funcionamiento del SRIStandAlone.
* [![Python][Python.py]][Python-url]
* [![Django][Django.dj]][Django-url]

<!-- PRIMEROS PASOS PARA LA UTILIZACIÓN DEL SRIStandAlone -->
## Iniciación
### Prerequisitos
Lo primero tendrás que tener descargado el software en el sitio habilitado para la distribución del producto.
### Instalación
Hay que dirigirse a la página "poner nombre de la página" para descargarlo o utilizar el siguiente para la descarga "poner link de descarga".
Cuando lo descargues te creará una carpeta llamada SRI/SRIStandAlone en el cual se encuentra el ejecutable para poder iniciar el programa.

<!-- USO DEL SRIStandAlone -->
## USO
En este apartado vamos a explicar el manejo del programa ya que este tiene una serie de opciones. 
Para poder inicializar el programa tendremos que dirijirnos a la ubiccación del del ejecutable en el explorador de archivos, 
cuando nos encontremos ya en el sitio en en la barra de url escribiremos <i>cmd</i> (para abrirnos una consola de comando en la misma ubicación del ejecutable).
Dentro de la consola tendremos que escribir el nombre del ejecutable <i>sriStandAlone.exe</i>, y seguido puede escribir las siguientes opciones:
* Opción <b>-h</b> o <b>--help</b>: Con esta opción nos desplegará una ayuda con las opciones disponibles del programa y una explicación breve de cada opción.
   ```cmd
   sriStandAlone.exe -h
   ```
* Opción <b>-i</b> o <b>--import_file</b>: Con dicho argumento importaremos los datos del proyecto que aportamos. Este argumento es obligatorio ponerlo con todas las opciones a excepción del la opción <i>-v</i>
   ```cmd
   sriStandAlone.exe -i <inputfile>
   ```
* Opción <b>-o</b> o <b>--output_file</b>: Con esta opcion exportamos otro archivo iEPB calculado en la ruta que el usuario indique.
  ```cmd
   sriStandAlone.exe -i <inputfile> -o <outputfile>
   ```
* Opción <b>-p</b> o <b>--result_file</b>: En esta opción se imprimen todos los resultados por pantalla, además no es obligatorio pasarle ningun archivo
  ```cmd
   sriStandAlone.exe -i <inputfile> -p
   ```
* Opción <b>-s</b> o <b>--result_SRI</b>: Aqui se muestra el resultado total del proyecto (SRI) por pantalla. No es necesario pasarle archivo.
  ```cmd
   sriStandAlone.exe -i <inputfile> -s
   ```
* Opción <b>-kf1</b> o <b>--result_Kf1</b>: Imprime por pantalla el resultado total del Energy Performance And Operation (Kf1). No es necesario pasarle archivo.
  ```cmd
   sriStandAlone.exe -i <inputfile> -kf1
   ```
* Opción <b>-kf2</b> o <b>--result_Kf2</b>: Imprime por pantalla el resultado total del Response To User Needs (Kf2). No es necesario pasarle archivo.
  ```cmd
   sriStandAlone.exe -i <inputfile> -kf2
   ```
* Opción <b>-kf3</b> o <b>--result_Kf3</b>: Imprime por pantalla el resultado total del Energy Flexibility (Kf3). No es necesario pasarle archivo.
  ```cmd
   sriStandAlone.exe -i <inputfile> -kf3
   ```
* Opción <b>-x</b> o <b>--extract_files</b>: Con este argumento se extraen los xml que se pasan en el argumento <i>-i</i>, el usuario puede pasarle una ubicación, si no la pasa se guardan en el mismo sitio que en el fichero de la opción <i>-i</i>
  ```cmd
   sriStandAlone.exe -i <inputfile> -x <route_new-file>
   ```
* Opción <b>-v</b> o <b>--show_version</b>: Con esta opción se imprime por pantalla la versión del programa. No hay que pasarle ningún fichero.
  ```cmd
   sriStandAlone.exe -x
   ```
<!-- CONTRIBUCIONES -->
## Contribuciones
<!--Revisar este apartado para reformular o no -->
Las unicas contribuciones que que se han aportado para desarrollar el programa han sido dos empreses Efinovatic y Cener
<!-- Licencia -->
## Licencia
<!--Revisar este apartado para reformular o no -->
Poner dueño de la licencia
<!-- Contacto -->
## Contacto
El contacto de la disponible para posibles errores o dudas que surjan son los siguientes:
* Efinovatic:
  - Teléfono: 948 31 68 29
  - E-mail: info@efinovatic.es
* Cener:
    - Teléfono: 948 25 28 00
    - Email: info@cener.com


<!-- REFERENCIA A LAS URLS E IMAGENES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[Python.py]: https://img.shields.io/badge/python-000000?style=for-the-badge&logo=pypi&logoColor=white
[Python-url]: https://www.python.org/downloads/
[Django.dj]: https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white
[Django-url]: https://www.djangoproject.com/download/



