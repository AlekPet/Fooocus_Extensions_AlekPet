# Fooocus extensions by AlekPet

> Github Fooocus: [go to fooocus](https://github.com/lllyasviel/Fooocus)

**[Patcher webui.py](#patcher-webuipy)** automatic install extensions after update Fooocus.

## List extensions:

| Name               |                      Description                      |                                                                                            Link |
| :----------------- | :---------------------------------------------------: | ----------------------------------------------------------------------------------------------: |
| _Prompt translate_ | Translate prompt positive and negative to the Englsih | [Link to git](https://github.com/AlekPet/Fooocus_Extensions_AlekPet/tree/main/prompt_translate) |

## Patcher webui.py

## Reset last original webui.py

1. Install git in your system.
2. Open in the your Shell (cmd, bash ...)
3. Input command: git restore --source origin/master PATH_TO_WEBUI_PY\webui.py

**Example:** _git restore --source origin/master E:\Fooocus\Fooocus\webui.py_

Install:

1. Placed **patcher_webui.py** where they are **run.bat, run_anime.bat, run_realistic.bat, folders Fooocus and python_embeded**
2. Add this line to the bat files **run.bat, run_anime.bat, run_realistic.bat**:
   **Example run.bat (in my fooocus i'am used dark theme ^\_^):**

Example run.bat:

```cmd
.\python_embeded\python.exe -s patcher_webui.py
.\python_embeded\python.exe -s Fooocus\entry_with_update.py --theme dark
pause
```

3. Run run.bat

> Note: After applied patches to the webui.py, automatic make backup webui.py named webui_original.py
