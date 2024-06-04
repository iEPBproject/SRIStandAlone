# SRIStandAlone application
<!-- TABLA DE CONTENIDOS -->
<details>
  <summary>TABLE OF CONTENTS</summary>
  <ol>
    <li>
      <a href="#About-SRIStandAlone-application">About SRIStandAlone application</a>
      <ul>
        <li><a href="#Built-with">Built with</a></li>
      </ul>
    </li>
    <li>
      <a href="#Get-started-with-the-SRIStandAlone-application">Get started with the SRIStandAlone application</a>
      <ul>
        <li><a href="#Prerequisites">Prerequisites</a></li>
        <li><a href="#Installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#Use-of-the-SRIStanAlone-application">Use of the SRIStanAlone application</a></li>
    <li><a href="#Troubleshooting-&-FAQ">Troubleshooting & FAQ</a></li>
    <li><a href="#contributions">Contributions</a></li>
    <li><a href="#Licence">Licence</a></li>
    <li><a href="#Contact">Contact</a></li>
  </ol>
</details>

<!-- SOBRE LA SRIStandAlone APP-->
## About SRIStandAlone application
The SRIStandalone APP is a tool developed within the framework of the iEPB project (co-funded by the European Union, project number 101120690) with which the following actions can be executed: 
  <ul>
    <li>Calculation of the SRI Total Score and the three key functionalities (Kf1, Kf2, Kf3) results and printing them on the screen.</li> 
    <li>Export the xml files of the SRI assessment, previously downloaded from the SRI2Market application, to the iEPB file.</li> 
    <li>Generate a new element in the iEPB file including the data of the changes made.</li>
    <li>Check the version of the tool.</li>
  </ul>
The SRIStandalone is a tool that will complement the SRI2Market application.

<!-- PROGRAMAS UTILIZADOS -->
## Built with
The software for the operation of the SRIStandAlone application has been developed with the help of the following tools.
* [![Python][Python.py]][Python-url]

<!-- PRIMEROS PASOS PARA LA UTILIZACIÓN DEL SRIStandAlone -->
## Get started with the SRIStandAlone application
### Prerequisites
First download the software from the site enabled for distribution. To download just double click on release and save it in the location of your choice.
### Installation
After running the setupSRIStandAlone1.2.exe file, the application will be installed on your computer in the default path C:\Program Files\SriStandAlone. A folder called "examples" will also be created in the same path where the 12.iEPB file is included (file of the new iEPB format with an example of the SRI assessment included to be read and calculated by the SRIStandAlone app).

<!-- USO DEL SRIStandAlone -->
## Use of the SRIStanAlone application
This section explains how to use the program and its options. 
In order to initialize the program we will have to go to the location of the executable in the file explorer, 
when we are already in the site in the url bar we will write <i>cmd</i> (to open a command console in the same location of the executable).
Inside the console we will have to type the name of the executable <i>sriStandAlone.exe</i>, and then you can type the following options:
* Option <b>-h</b> or <b>--help</b>: With this option a help will be displayed with the available options of the program and a brief explanation of each option.
   ```cmd
   sriStandAlone.exe -h
   ```
* Option <b>-i</b> or <b>--import_file</b>: This argument is used to import the project data provided. This argument is mandatory with all the options except the <i>-v</i> option.
   ```cmd
   sriStandAlone.exe -i <inputfile>
   ```
* Option <b>-o</b> or <b>--output_file</b>: With this option, the SRI calculated of the iEPB file will be recalculated and exported to the path specified by the user.
  ```cmd
   sriStandAlone.exe -i <inputfile> -o <outputfile>
   ```
* Option <b>-p</b> or <b>--result_file</b>: This option prints all the results on the screen, also it is not mandatory to provide any file to it.
  ```cmd
   sriStandAlone.exe -i <inputfile> -p
   ```
* Option <b>-s</b> or <b>--result_SRI</b>: Displays the total result of the project (SRI) on the screen. It is not necessary to provide a file.
  ```cmd
   sriStandAlone.exe -i <inputfile> -s
   ```
* Option <b>-kf1</b> or <b>--result_Kf1</b>: Prints the total 'Energy performance and operation' (Kf1) result on screen. It is not necessary to provide a file.
  ```cmd
   sriStandAlone.exe -i <inputfile> -kf1
   ```
* Option <b>-kf2</b> or <b>--result_Kf2</b>: Prints the total result of the 'Response to user needs' (Kf2). It is not necessary to provide a file.
  ```cmd
   sriStandAlone.exe -i <inputfile> -kf2
   ```
* Option <b>-kf3</b> or <b>--result_Kf3</b>: Prints the total result of the 'Energy flexibility' (Kf3). It is not necessary to provide a file.
  ```cmd
   sriStandAlone.exe -i <inputfile> -kf3
   ```
* Option <b>-x</b> or <b>--extract_files</b>: With this argument the xml that are given in the <i>-i</i> argument are extracted, the user can provide a location, if not, they are saved in the same place as in the file of the <i>-i</i> option.
  ```cmd
   sriStandAlone.exe -i <inputfile> -x <route_new-file>
   ```
* Option <b>-e</b> or <b>--package_files</b>: This option creates a new iEPB file that includes the files defined in the -e section (xml and gbMXL). The option -o is used to define the output file name. If the -o option is not used, the output file name will be like the first input file name, but with the extension renamed to .iepb.
  ```cmd
   sriStandAlone.exe -o <outputfile> -e <xmlfile> <gbxmlfile>
   ```
* Option <b>-v</b> or <b>--show_version</b>: Prints the program version on the screen. No file has to be provided.
  ```cmd
   sriStandAlone.exe -v
   ```
<!-- Solución de problemas y FAQ del SRIStandAlone -->
## Troubleshooting & FAQ
* Remember that you are running the application on the MS-DOS subsystem and therefore you have to follow its rules, so if any folder in the path you enter consists of two words, e.g. Program Files, the path must be written in quotation marks.
    (Right) C:\Program Files\SriStandAlone>sristandalone.exe -i "C:\Example Files" -e "C:\Example Files\12.xml" "C:\Example Files\12_gbXML.xml” 
    (Wrong) C:\Program Files\SriStandAlone>sristandalone.exe -i C:\Example Files -e C:\Example Files\12.xml C:\Example Files\12_gbXML.xml 

* For those tool options that integrate file saving (-o, -x, -e ) the new path where the file is to be saved must be free and have write permissions.

<!-- Contacto -->
## Contact
The following contacts are available for any errors or questions that may arise:
* Efinovatic:
  - E-mail: info@efinovatic.es
  <!-- - Email: info@cener.com -->


<!-- REFERENCIA A LAS URLS E IMAGENES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[Python.py]: https://img.shields.io/badge/python-000000?style=for-the-badge&logo=pypi&logoColor=white
[Python-url]: https://www.python.org/downloads/



