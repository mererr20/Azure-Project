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
Azure Cognitive es una IA desarrollada por Microsoft para el alcance de desarrolladores y científicos de datos. Los modelos brindados por ellos permiten incorporar la capacidad de ver, escuchar, hablar, buscar, comprender y acelerar la toma de decisiones avanzadas en las aplicaciones unicamente llamando el API desde el proyecto que se está desarrollando.
  
En este proyecto se utilizó esta herramienta para 4 tareas. Una es el analizar las caras de la personas para obtener las emociones, el género, edad, con el API Face. Otra api utiliza fue SPEECH, la cual nos ayuda para extraer el audio de un vídeo, para posterior enviar el texto a Text Analitics, otra api para analizar el sentimiento del mismo. Y por último, Computer Vision, para analizar la escena de la imagen para poder detectar las actividades realizadas o si contiene contenido de adultos.
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
```
Importante también el ingresar en [*AzureConfig.py*](https://github.com/mererr20/Azure-Project/blob/main/AzureConfig.py) en la línea [*4*](https://github.com/mererr20/Azure-Project/blob/c14c1edd3f3107c17885bcb55a71c4d5524d64c1/AzureConfig.py#L4) y la [*5*](https://github.com/mererr20/Azure-Project/blob/c14c1edd3f3107c17885bcb55a71c4d5524d64c1/AzureConfig.py#L5) las credenciales de Azure. Estas se pueden conseguir al crear un recuerso en [*Azure*](https://portal.azure.com/#create/hub) de tipo Cognitive Services, y en el apartado de *Manage keys* se podrá visualizar una ventana como la siguiente:

<p>
   <div align="center">
   <img width="550" src="https://github.com/mererr20/Azure-Project/blob/main/resources/azure.jpg"></a>
   </div>
</p>

Solamente copiamos y pegamos en la lista indicada con anterioridad.

Una vez tenemos todo lo necesario, debemos ejecutar el [main.py](https://github.com/mererr20/Azure-Project/blob/main/main.py)
   
En el [main.py](https://github.com/mererr20/Yolo-Project/main.py) se debe enviar por parámetros cuál será la carpeta a analizar (tomando en cuenta que se debe enviar la ruta de dicha carpeta, por ejemplo 'C:\User\...'), por defectos se indica la carpeta [videos](https://github.com/mererr20/Azure-Project/tree/main/videos) que se encuentra en la raíz de dicho proyecto.

</details>

<br><br>
# <div align="center">Explicación/Ejecución</div>

A continuación, explicamos cómo se implementó la solución realizada y su ejecución.



Para empezar, la función [*main(routeDirectory)*](https://github.com/mererr20/Azure-Project/blob/9767120c04e99028ba824d49ee3b8625673a9cb4/main.py#L246) es la función principal, la cual será la encargada de llamar las demás funciones para una correcta ejecución, además, la encargada de recibir por parámetro la ruta de la carpeta a analizar,<a href="#cómo-iniciar"> como se mencionó anteriormente.</a>

Primero, se llama la función [*extraction*](https://github.com/mererr20/Azure-Project/blob/9767120c04e99028ba824d49ee3b8625673a9cb4/main.py#L72) que es la que permite la extracción tanto de los fotogramas de los videos cada 5 segundos, así como el audio para después dividirlo en 2. Para guardar todo lo que se extrajo se crea la carpeta Data, dentro de ella subcarpetas con los nombres de los videos. Dentro de estas subcarpetas se almacenan los frames y los audios extraídos en una carpeta respectivamente.

Ya con todo esto preparado se llama  la función [*distribution*](https://github.com/mererr20/Azure-Project/blob/7fd30b7a280ba3e98886020c0b640847a3dcfa84/main.py#L114) encargada de dividir el total de carpetas en 2. En esta función se llama a [*analyzer*](https://github.com/mererr20/Azure-Project/blob/7fd30b7a280ba3e98886020c0b640847a3dcfa84/main.py#L91). Esta segunda función lo que hace es invocar diferentes métodos de la clase [*analizer.py*](https://github.com/mererr20/Azure-Project/blob/main/analyzer.py) que es donde se hace la conección con la API de Azure Cognitive Services.

Al final, se llama la función [*results*](https://github.com/mererr20/Azure-Project/blob/7fd30b7a280ba3e98886020c0b640847a3dcfa84/main.py#L135) en donde los resultados generados se guardan en un archivo llamado (*scenes.txt*) que se incluye un rango de las edades de las personas detectdas, una descripción de los escenarios de los frames, si hay contenido adulto, la cantidad de escenas y los tiempos de duración. Además, se muestran gráficos donde se pueden visualizar el mayor género detectado, el sentimiento del audio y por último una gráfica con las distintas emociones.

Para el proyecto se generan diferentes procesos en paralelo para una respuesta más rápida. Con el vídeo testeado se consiguió una respuesta de 62% más rápida que la ejecución secuencial.

<br><br>
# <div align="center">Resultados</div>
Para los resultados presentados a continuación, se utilizó el video llamado "DailyRoutine" que tiene una duración aproximada de 6 minutos , del cual se obtuvo lo siguiente:

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
   <img width="550" src="https://github.com/mererr20/Azure-Project/blob/main/resources/gender.png"></a>
   </div>
</p>

El archivo scenes.txt se ve así:

<p>
   <div align="center">
      <img width="550" src="https://github.com/mererr20/Azure-Project/blob/main/resources/resultScenes.png"></a>
   </div>
</p>

En la carpeta [Data](https://github.com/mererr20/Yolo-Project/Data) se pueden visualizar otros resultados obtenidos de otro vídeo testeado.
