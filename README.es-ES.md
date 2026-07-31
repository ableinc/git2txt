

# git2txt

Convierte todos los archivos de un repositorio de git en archivos .txt. Esto es útil para entrenar LLMs con tu base de código.

## Cómo utilizarlo

1. Crea un nuevo archivo .env copiando example.env
```shell
cp example.env .env
```
2. Agrega los campos necesarios. Los campos predeterminados son un buen punto de partida.
```bash
GIT_PROJECT_DIRECTORY=/path/to/git/repo
IGNORE_FILES=.env,package-lock.json
IGNORE_DIRS=.git,.vscode,node_modules
SAVE_DIRECTORY=training_data
SKIP_EMPTY_FILES=true
```
3. Instala las dependencias. Se recomienda usar un entorno virtual.
```shell
python -m pip install -r requirements.txt
```
4. Ejecuta el programa
```shell
python main.py
```
5. Verás tus archivos de datos en el directorio ```training_data/```. Esto cambiará si modificaste la ruta mediante ```SAVE_DIRECTORY``` en el archivo ```.env``.


## Notas
- Este programa requiere Python versión 3.6 o posterior. Utiliza la técnica de formato f-string introducida en Python 3.6.
