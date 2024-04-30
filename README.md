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
      <li><a href="#Use-of-the-SRIStanAlone-application">Uso</a></li>
    <li><a href="#contributions">Contribuciones</a></li>
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
First download the software from the site enabled for distribution. 
### Installation
To download just double click on release and save it in the location of your choice.

<!-- USO DEL SRIStandAlone -->
## Use of the SRIStanAlone application
This section explains how to use the program and its options. 
In order to initialize the program we will have to go to the location of the executable in the file explorer, 
when we are already in the site in the url bar we will write <i>cmd</i> (to open a command console in the same location of the executable).
Inside the console we will have to type the name of the executable <i>sriStandAlone.exe</i>, and then you can type the following options:
* Option <b>-h</b> o <b>--help</b>: With this option a help will be displayed with the available options of the program and a brief explanation of each option.
   ```cmd
   sriStandAlone.exe -h
   ```
* Option <b>-i</b> o <b>--import_file</b>: This argument is used to import the project data provided. This argument is mandatory with all the options except the <i>-v</i> option.
   ```cmd
   sriStandAlone.exe -i <inputfile>
   ```
* Option <b>-o</b> o <b>--output_file</b>: With this option another calculated iEPB file will be exported to the path specified by the user.
  ```cmd
   sriStandAlone.exe -i <inputfile> -o <outputfile>
   ```
* Option <b>-p</b> o <b>--result_file</b>: This option prints all the results on the screen, also it is not mandatory to provide any file to it.
  ```cmd
   sriStandAlone.exe -i <inputfile> -p
   ```
* Option <b>-s</b> o <b>--result_SRI</b>: Displays the total result of the project (SRI) on the screen. It is not necessary to provide a file.
  ```cmd
   sriStandAlone.exe -i <inputfile> -s
   ```
* Option <b>-kf1</b> o <b>--result_Kf1</b>: Prints the total 'Energy performance and operation' (Kf1) result on screen. It is not necessary to provide a file.
  ```cmd
   sriStandAlone.exe -i <inputfile> -kf1
   ```
* Option <b>-kf2</b> o <b>--result_Kf2</b>: Prints the total result of the 'Response to user needs' (Kf2). It is not necessary to provide a file.
  ```cmd
   sriStandAlone.exe -i <inputfile> -kf2
   ```
* Option <b>-kf3</b> o <b>--result_Kf3</b>: Prints the total result of the 'Energy flexibility' (Kf3). It is not necessary to provide a file.
  ```cmd
   sriStandAlone.exe -i <inputfile> -kf3
   ```
* Option <b>-x</b> o <b>--extract_files</b>: With this argument the xml that are given in the <i>-i</i> argument are extracted, the user can provide a location, if not, they are saved in the same place as in the file of the <i>-i</i> option.
  ```cmd
   sriStandAlone.exe -i <inputfile> -x <route_new-file>
   ```
* Option <b>-v</b> o <b>--show_version</b>: Prints the program version on the screen. No file has to be provided.
  ```cmd
   sriStandAlone.exe -v
   ```
<!-- Contacto -->
## Contact
The following contacts are available for any errors or questions that may arise:
* Efinovatic:
  - Phone number: 948 31 68 29
  - E-mail: info@efinovatic.es
* Cener:
  - Phone number: 948 25 28 00
  <!-- - Email: info@cener.com -->


<!-- REFERENCIA A LAS URLS E IMAGENES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[Python.py]: https://img.shields.io/badge/python-000000?style=for-the-badge&logo=pypi&logoColor=white
[Python-url]: https://www.python.org/downloads/



