# <div align="center">Azure Cognitive Services en archivos de video</div>
<p>
   <a align="left" href="https://azure.microsoft.com/es-es/services/cognitive-services/" target="_blank">
   <img width="850" src="https://techcommunity.microsoft.com/t5/image/serverpage/image-id/179918i6FC3178F079DE32D/image-size/large?v=v2&px=999"></a>
</p>
<p>

## <div>Desarrollado por:</div>

<ul>
   <li type="circle"> <a href=https://github.com/mererr20> Merelyn Rodríguez Rojas </a> </li>
   <li type="circle"> <a href=https://github.com/mendez-jfer> Fernando Méndez Hurtado </a> </li>
   <li type="circle"> <a href=https://github.com/LDVargas> Daniel Vargas Gómez </a> </li>
</ul>

</p>

# <div align="center">Introducción</div>
<p>
Azure Cognitive es una IA desarrollada por Microsoft y que pusieron al alcance de desarrolladores y científicos de datos. Los modelos brindados por ellos permiten incorporar la capacidad de ver, escuchar, hablar, buscar, comprender y acelerar la toma de decisiones avanzadas en las aplicaciones unicamente llamando el API desde el proyecto que se está desarrollando.
  
En este proyecto se utilizó esta herramienta para dos tareas. Una es el analizar una persona en generada a partir de un video y obtener las emociones, el género y objetos que este cargando. La segunda tarea es un análisis del audio de un video para detectar el uso de mal vocabulario.
</p>
<br>

</div>

# <div align="center">Cómo iniciar</div>

<details open>
<summary>Instalación</summary>

Se requiere [**Python>=3.6.0**](https://www.python.org/) y los requerimientos especificados en [requirements.txt](https://github.com/mererr20/Azure-Project/blob/main/requirements.txt).

```bash
$ git clone https://github.com/mererr20/Azure-Project.git
$ cd Azure-Project
$ pip install -r requirements.txt
$ pip install azure-appconfiguration
$ pip install azure-cognitiveservices-speech
$ pip install azure-cognitiveservices-vision-face   
$ pip install audio
$ pip install futures
$ pip install moviepy  
$ pip install pydub
```
Importante también el ingresar en [*AzureConfig.py*](https://github.com/mererr20/Azure-Project/blob/main/AzureConfig.py) en la línea [*4*](https://github.com/mererr20/Azure-Project/blob/c14c1edd3f3107c17885bcb55a71c4d5524d64c1/AzureConfig.py#L4) y la [*5*](https://github.com/mererr20/Azure-Project/blob/c14c1edd3f3107c17885bcb55a71c4d5524d64c1/AzureConfig.py#L5) las credenciales de Azure. 
  
   
Una vez tenemos todo lo necesario, debemos ejecutar el [main.py](https://github.com/mererr20/Azure-Project/blob/main/main.py)
   
En el [main.py](https://github.com/mererr20/Yolo-Project/main.py) se debe enviar por parámetros en el método main cuál será la carpeta a analizar (tomando en cuenta que se debe enviar la ruta de dicha carpeta, por ejemplo 'C:\User\...'), por defectos se indica la carpeta [videos](https://github.com/mererr20/Azure-Project/tree/main/videos) que se encuentra en la raíz de dicho proyecto.

</details>

<br><br>
# <div align="center">Explicación/Ejecución</div>

A continuación, explicamos cómo se implementó la solución realizada y su ejecución.



Para empezar, la función [*main(routeDirectory)*](https://github.com/mererr20/Azure-Project/blob/9767120c04e99028ba824d49ee3b8625673a9cb4/main.py#L154) es la función principal, la cual será la encargada de llamar las demás funciones para una correcta ejecución, además, la encargada de recibir por parámetro la ruta de la carpeta a analizar,<a href="#cómo-iniciar"> como se mencionó anteriormente.</a>

Primero, se llama la función [*extraction*](https://github.com/mererr20/Azure-Project/blob/9767120c04e99028ba824d49ee3b8625673a9cb4/main.py#L76) que es la que permite la extracción tanto de los frames de los videos cada 1 segundo así como el audio para después partirlo en 2. Para guardar todo lo que se extrajo se crean las carpeta Data y dentro de ella subcarpetas con los nombres de los videos. Dentro de estas subcarpetas se almacenan los frames y los audios extraídos.

Ya con todo esto preparado se llama  la función [*distribution*](https://github.com/mererr20/Azure-Project/blob/7fd30b7a280ba3e98886020c0b640847a3dcfa84/main.py#L120) encargada de organizar las carpetas. Desde esta función se llama a [*distribution*](https://github.com/mererr20/Azure-Project/blob/7fd30b7a280ba3e98886020c0b640847a3dcfa84/main.py#L96). Esta segunda función lo que hace es invocar la clase [*analizer.py*](https://github.com/mererr20/Azure-Project/blob/main/analyzer.py) que es donde se hace la conección con la API de Azure Cognitive Services.

Al final, se llama la función [*results*](https://github.com/mererr20/Azure-Project/blob/7fd30b7a280ba3e98886020c0b640847a3dcfa84/main.py#L141) en donde los resultados generados se guardan en un archivo llamado (*scenes.txt*) que se incluye un rango de las edades de las personas detectdas, una descripción de los escenarios de los frames, si hay contenido adulto, la cantidad de escenas y los tiempos de duración. Además, se muestran gráficos generados a partir de la misma información

<br><br>
# <div align="center">Resultados</div>
Para los resultados presentados a continuación, se utilizó el video llamado "DailyRoutine" que tiene una duración aproximada de 6 minutos , de el cual se obtuvo lo siguiente:

<p>
   <div align="center">
   <img width="550" src="https://github.com/mererr20/Azure-Project/blob/main/resources/emotions.jpg"></a>
   </div>
</p>


<p>
   <div align="center">
   <img width="550" src="https://github.com/mererr20/Azure-Project/blob/main/resources/feeling.jpg"></a>
   </div>
</p>

<p>
   <div align="center">
   <img width="550" src="https://github.com/mererr20/Azure-Project/blob/main/resources/gender.jpg"></a>
   </div>
</p>

El archivo scenes.txt se ve así:

<p>
   <div align="center">
      <img width="550" src="https://github.com/mererr20/Azure-Project/blob/main/resources/resultScenes.png"></a>
   </div>
</p>

