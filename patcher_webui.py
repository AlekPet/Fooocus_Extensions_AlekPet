# Script for patching file webui.py for Fooocus
# Author: AlekPet
# Version: for Fooocus v2.5.2
# Github: https://github.com/AlekPet/Fooocus_Extensions_AlekPet

import os
import datetime
import shutil

DEBUG = False
DIR_FOOOCUS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Fooocus")
PATH_TO_WEBUI = os.path.join(DIR_FOOOCUS, "webui.py")

PATCH_OBJ_DATA_PROMPT_TRANSLATE = [
    [
        "from modules.util import is_json\n",
        "from modules.module_translate import PromptTranslate # Prompt translate AlekPet\n",
    ],
    [
        "def get_task(*args):\n",
        """    # [start] Prompt translate AlekPet
    argsList = list(args)
    toT = argsList.pop() 
    srT = argsList.pop() 
    trans_enable = argsList.pop()

    trans_service = argsList.pop()
    trans_proxy_enabled = argsList.pop()
    trans_proxy = argsList.pop()
    trans_auth_data = argsList.pop()

    if trans_enable:      
        positive, negative, detected_lang = promptTranslate.deep_translate_text(srT, toT, trans_proxy_enabled, trans_proxy, trans_auth_data, trans_service,  argsList[2], argsList[3])
        argsList[2] = positive
        argsList[3] = negative
        promptTranslate.translated_prompts = [positive, negative, detected_lang]
        
    args = tuple(argsList)
    # [end] Prompt trasnlate AlekPet\n
""",
    ],
    [
        "reload_javascript()\n",
        "\n# [start] Prompt translate AlekPet\npromptTranslate = PromptTranslate()\n# [end] Prompt trasnlate AlekPet\n",
    ],
    [
        "            describe_tab.select(lambda: 'desc', outputs=current_tab, queue=False, _js=down_js, show_progress=False)\n",
        """
            # [start] Prompt trasnlate AlekPet
            dom, translate_enabled, translate_service, gtrans, srcTrans, toTrans, change_src_to, adv_trans, p_tr, p_n_tr, translate_proxy_enabled, translate_proxy, translate_auth_data, viewstrans, proxy_settings = promptTranslate.createElements()
            # [end] Prompt trasnlate AlekPet
\n""",
    ],
    [
        "            .then(fn=lambda: None, _js='refresh_grid_delayed', queue=False, show_progress=False)\n",
        """\n        # [start] Prompt translate AlekPet 
        translate_service.change(promptTranslate.setComboBoxesSrcTo, inputs=translate_service, outputs=[srcTrans, toTrans, translate_proxy, translate_auth_data])

        gtrans.click(promptTranslate.translateByClick, inputs=[srcTrans, toTrans, translate_proxy_enabled, translate_proxy, translate_auth_data, translate_service, prompt, negative_prompt], outputs=[prompt, negative_prompt,p_tr, p_n_tr, srcTrans])

        change_src_to.click(promptTranslate.change_lang, inputs=[srcTrans,toTrans], outputs=[srcTrans,toTrans])
        adv_trans.change(lambda x: gr.update(visible=x), inputs=adv_trans, outputs=viewstrans, queue=False, show_progress=False, _js=switch_js)
        translate_proxy_enabled.change(lambda x: gr.update(visible=x), inputs=translate_proxy_enabled, outputs=proxy_settings, queue=False, show_progress=False, _js=switch_js)
        # [end] Prompt translate AlekPet\n""",
    ],
    [
        "        ctrls += enhance_ctrls\n",
        """\n        # [start] Prompt translate AlekPet\n        ctrls += [translate_auth_data, translate_proxy, translate_proxy_enabled, translate_service, translate_enabled, srcTrans, toTrans]\n        # [end] Prompt translate AlekPet\n""",
    ],
    [
        "            .then(fn=generate_clicked, inputs=currentTask, outputs=[progress_html, progress_window, progress_gallery, gallery]) \\\n",
        "            .then(fn=lambda: promptTranslate.translated_prompts[2], inputs=[], outputs=[srcTrans]) \\\n            .then(fn=lambda adv: (promptTranslate.translated_prompts if adv else ['', '']), inputs=[adv_trans], outputs=[p_tr, p_n_tr]) \\\n",
    ],
]


def search_and_patch():
    isOk = 0
    patchLen = len(PATCH_OBJ_DATA_PROMPT_TRANSLATE)
    patchedFileName = os.path.join(DIR_FOOOCUS, "webui_patched.py")

    with open(PATH_TO_WEBUI, "r+", encoding="utf-8") as f:
        lines = f.readlines()
        len_lines = len(lines)

        if not len_lines:
            print(f"File '{PATH_TO_WEBUI}' is empty!\n")
            return

        if (
            "from modules.module_translate import translate, GoogleTranslator\n"
            in lines
        ):
            return "Old version"

        if PATCH_OBJ_DATA_PROMPT_TRANSLATE[0][1] in lines:
            return "Already"

        patched = 0
        patchSteps = 100 / patchLen

        patchedFile = open(patchedFileName, "w+", encoding="utf-8")

        for line in lines:
            for patch_num, linepatch in enumerate(PATCH_OBJ_DATA_PROMPT_TRANSLATE):
                if line.startswith(linepatch[0]):
                    line = line + linepatch[1]
                    isOk = isOk + 1

                    patched += patchSteps
                    print(
                        "Patches applied to file {0} of {1} [{2:1.1f}%)]".format(
                            isOk, patchLen, patched
                        ),
                        end="\r",
                        flush=True,
                    )

            patchedFile.write(line)

        patchedFile.close()

        patchResult = isOk == patchLen

        if not patchResult:
            # Remove tmp file
            os.remove(patchedFileName)
        else:
            # Rename to webui.py and backup original
            if not os.path.exists(os.path.join(DIR_FOOOCUS, "webui_original.py")):
                shutil.copy(
                    PATH_TO_WEBUI, os.path.join(DIR_FOOOCUS, "webui_original.py")
                )
            else:
                currentDateTime = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
                shutil.copy(
                    PATH_TO_WEBUI,
                    os.path.join(DIR_FOOOCUS, f"webui_original_{currentDateTime}.py"),
                )

            shutil.move(patchedFileName, PATH_TO_WEBUI)

    if DEBUG and not patchResult:
        not_patched = map(
            PATCH_OBJ_DATA_PROMPT_TRANSLATE.index,
            filter(lambda l: l[0] not in lines, PATCH_OBJ_DATA_PROMPT_TRANSLATE),
        )
        print(
            "\n[WARNING] Not pathced lines:\n",
            "\n".join(
                map(
                    lambda p: (f"line {p}: {PATCH_OBJ_DATA_PROMPT_TRANSLATE[p][0]}"),
                    not_patched,
                )
            ),
            end="\r",
            flush=True,
        )

    return "Ok" if patchResult else "Error"


def restore_file(file_path, commit_hash=None):
    import pygit2

    """
    Restore file Git  repository concrete commit.

    Args:
        repo_path (str): Path to Git.
        file_path (str): Path to file from git directory.
        commit_hash (str, optional): Hash commit restore.
                                    If not enter, used HEAD.
    """
    repo = pygit2.Repository(DIR_FOOOCUS)

    # Get commit
    if commit_hash is None:
        commit = repo.head.peel()
    else:
        commit = repo[commit_hash]

    # Get tree commit
    tree = commit.tree

    # Find file in tree commit
    try:
        tree_entry = tree[file_path]
    except KeyError:
        raise FileNotFoundError(
            f"File '{file_path}' not found in the commit {commit.hex}"
        )

    # Get content file from commit
    blob = repo[tree_entry.id]
    file_content = blob.data

    # Write file
    with open(os.path.join(DIR_FOOOCUS, file_path), "wb") as f:
        f.write(file_content)


def start_patch(showTitle=True):
    if showTitle:
        print(
            """=== Script for patching file webui.py for Fooocus ===
    > Extension: 'Prompt Translate'
    > Author: AlekPet
    > Github: https://github.com/AlekPet/Fooocus_Extensions_AlekPet

    > Reset original webui.py:
    https://github.com/AlekPet/Fooocus_Extensions_AlekPet/?tab=readme-ov-file#reset-last-original-webuipy
    === ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ==="""
        )

    status = search_and_patch()
    if status == "Ok":
        print("\nPatched successfully!")

    elif status == "Already":
        print("\nPatches already appieds!")

    elif status == "Old version":
        print("\n>>>> Used old version patches! Restore original webui.py ...\n")
        restore_file("webui.py")
        print(">>> File webui.py restored!\n")
        start_patch(False)
    else:
        print("\n[ERROR] File patch failed, invalid data!")


start_patch()
