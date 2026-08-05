

# Extensiones de Fooocus por AlekPet

> Github Fooocus: [ir a fooocus](https://github.com/lllyasviel/Fooocus)

**[Patcher webui.py](#patcher-webuipy)** instala automáticamente las extensiones después de actualizar Fooocus.

# Historial de cambios:

> 2024.05.23 - [Prompt translate] Se han añadido otros servicios de traducción (¡edita **modules/config.json** para configurarlo!) ([Nota config.json](https://github.com/AlekPet/Fooocus_Extensions_AlekPet/tree/main/prompt_translate#note-settings))

## Lista de extensiones:

| Nombre               |                      Descripción                      |                                                                                            Enlace |
| :----------------- | :---------------------------------------------------: | ----------------------------------------------------------------------------------------------: |
| _Prompt translate_ | Traduce el prompt positivo y negativo al inglés | [Enlace al git](https://github.com/AlekPet/Fooocus_Extensions_AlekPet/tree/main/prompt_translate) |

## Patcher webui.py

## Restablecer el último webui.py original

1. Instala git en tu sistema.
2. Abre tu Shell (cmd, bash ...)
3. Introduce el comando:

```bash
git restore --source origin/master PATH_TO_WEBUI_PY\webui.py
```

o

```bash
git restore PATH_TO_WEBUI_PY\webui.py
```

**Ejemplo:** _git restore --source origin/master E:\Fooocus\Fooocus\webui.py_

Instalación:

1. Coloca **patcher_webui.py** en el mismo directorio que **run.bat, run_anime.bat, run_realistic.bat**, las carpetas **Fooocus** y **python_embeded**.
2. Agrega esta línea a los archivos bat **run.bat, run_anime.bat, run_realistic.bat**:
   **Ejemplo de run.bat (en mi fooocus uso el tema oscuro ^\_^):**

Ejemplo de run.bat:

```cmd
.\python_embeded\python.exe -s patcher_webui.py
.\python_embeded\python.exe -s Fooocus\entry_with_update.py --theme dark
pause
```

3. Coloca la carpeta **modules** (dentro de la carpeta prompt_translate) en la carpeta raíz de Fooocus y ¡reemplázala!
4. Ejecuta run.bat

> Nota: Después de aplicar los parches a webui.py, se crea automáticamente una copia de seguridad llamada webui_original.py
