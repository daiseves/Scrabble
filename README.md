# ScrabbleAR.py 🎲
_Seminario de Lenguajes Python - Trabajo Final._

## Información 📝
ScrabbleAR es un juego de palabrar basado en el Scrabble, en el cual se intenta ganar puntos mediante la formación de palabras sobre un tablero.

## Tener en cuenta ⚠️
  * La configuración del nivel modifica el tamaño del tablero. (Fácil: tablero de 15x15: - Medio: tablero de 17x17 - Difícil: tablero de 19x19). Cambian además las casillas de       bonus con el fin de aumentarle la complejidad al armado de palabras. 
  * En el nivel FÁCIL, se aceptan sustantivos, adjetivos y verbos.
  * En el nivel MEDIO, se aceptan sustantivos y adjetivos.
  * En el nivel DIFÍCIL, se aceptan sólo verbos.
  * El nivel por defecto es 'Fácil'.
  * Se pone una ficha aleatoria en el centro del tablero al comienzo del juego
  * La segunda ficha ingresada debe estar al lado de la primer ficha dispuesta, tanto al inicio del juego  (válido tanto para la Pc como para el jugador) como al inicio de cada     ronda
  * El juego termina cuando se presiona el botón 'Terminar juego', cuando ya terminó el tiempo o cuando ya no hay más fichas en la bolsa. En estos casos, se calcula el puntaje       de cada jugador y se nombra al ganador.
  * Las casillas -2 y -3 restan ese puntaje a la letra.
  * Las casillas x2 y x3 multiplican el valor de la letra.
  * La casilla 'bomba' resta 4 puntos a la palabra.
  * La casilla 'estrella' suma 5 puntos a la palabra.
  * Las palabras se pueden acomodar sólo vertical u horizontalmente.
  * Las palabras no pueden superponerse. 
  * La PC sólo forma combinaciones de palabras con tres letras (indicado dentro del código cómo cambiarlo).
  * El usuario debe armar palabras de dos letras o más.
  
## Ejecución 💻
  * Descargar el repositorio
  * Descomprimir el contenido
  * Ejecutar el archivo ScrabbleAR.py

### Necesario para su correcta ejecución
 * [Python 3.6.8](https://www.python.org/downloads/release/python-368/)
 * [PySimpleGUI](https://github.com/PySimpleGUI/PySimpleGUI/) 
 * [Pattern](https://github.com/clips/pattern/)

## Integrantes del proyecto 👧
  * [Maria Lara Remorini]
  
## Licencia 🔓
  GNU General Public License v3.0

