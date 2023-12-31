# Script for patching file webui.py for Fooocus
# Author: AlekPet
# Github: https://github.com/AlekPet/Fooocus_Extensions_AlekPet

import os
import shutil

DIR_FOOOCUS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Fooocus")
PATH_TO_WEBUI = os.path.join(DIR_FOOOCUS, "webui.py")

PATH_OBJ_DATA_PROMPT_TRANSLATE = [
["from modules.auth import auth_enabled, check_auth\n", "from modules.module_translate import translate, GoogleTranslator\n"],
["    execution_start_time = time.perf_counter()", """
    # Prompt translate AlekPet
    argsList = list(args)
    toT = argsList.pop() 
    srT = argsList.pop() 
    trans_automate = argsList.pop() 
    trans_enable = argsList.pop() 
    
    if trans_enable:      
        if trans_automate:
            positive, negative = translate(argsList[0], argsList[1], srT, toT)            
            argsList[0] = positive
            argsList[1] = negative
            
    args = tuple(argsList)
    # ---\n"""],
["            desc_tab.select(lambda: 'desc', outputs=current_tab, queue=False, _js=down_js, show_progress=False)\n","""

            # [start] Prompt trasnlate AlekPet
            with gr.Row(elem_classes='translate_row'):
                    langs_sup = GoogleTranslator().get_supported_languages(as_dict=True)
                    langs_sup = list(langs_sup.values())

                    def change_lang(src, dest):
                            if src != 'auto' and src != dest:
                                return [src, dest]
                            return ['en','auto']
                        
                    def show_viewtrans(checkbox):
                        return {viewstrans: gr.update(visible=checkbox)} 
                    
                    with gr.Accordion('Prompt Translate', open=False):
                        with gr.Row():
                            translate_enabled = gr.Checkbox(label='Enable translate', value=False, elem_id='translate_enabled_el')
                            translate_automate = gr.Checkbox(label='Auto translate "Prompt and Negative prompt" before Generate', value=True, interactive=True, elem_id='translate_enabled_el')
                            
                        with gr.Row():
                            gtrans = gr.Button(value="Translate")        

                            srcTrans = gr.Dropdown(['auto']+langs_sup, value='auto', label='From', interactive=True)
                            toTrans = gr.Dropdown(langs_sup, value='en', label='To', interactive=True)
                            change_src_to = gr.Button(value="🔃")
                            
                        with gr.Row():
                            adv_trans = gr.Checkbox(label='See translated prompts after click Generate', value=False)          
                            
                        with gr.Box(visible=False) as viewstrans:
                            gr.Markdown('Tranlsated prompt & negative prompt')
                            with gr.Row():
                                p_tr = gr.Textbox(label='Prompt translate', show_label=False, value='', lines=2, placeholder='Translated text prompt')

                            with gr.Row():            
                                p_n_tr = gr.Textbox(label='Negative Translate', show_label=False, value='', lines=2, placeholder='Translated negative text prompt')             
                        
            # [end] Prompt trasnlate AlekPet\n"""],
["            .then(fn=lambda: None, _js='refresh_grid_delayed', queue=False, show_progress=False)\n","""
        # [start] Prompt translate AlekPet
        def seeTranlateAfterClick(adv_trans, prompt, negative_prompt="", srcTrans="auto", toTrans="en"):
            if(adv_trans):
                positive, negative = translate(prompt, negative_prompt, srcTrans, toTrans)
                return [positive, negative]   
            return ["", ""]
        
        gtrans.click(translate, inputs=[prompt, negative_prompt, srcTrans, toTrans], outputs=[prompt, negative_prompt])
        gtrans.click(translate, inputs=[prompt, negative_prompt, srcTrans, toTrans], outputs=[p_tr, p_n_tr])
        
        change_src_to.click(change_lang, inputs=[srcTrans,toTrans], outputs=[toTrans,srcTrans])
        adv_trans.change(show_viewtrans, inputs=adv_trans, outputs=[viewstrans])
        # [end] Prompt translate AlekPet\n"""],
["        ctrls += ip_ctrls\n", "        ctrls += [translate_enabled, translate_automate, srcTrans, toTrans]\n"],
["            .then(fn=generate_clicked, inputs=ctrls, outputs=[progress_html, progress_window, progress_gallery, gallery]) \\\n","""            .then(fn=seeTranlateAfterClick, inputs=[adv_trans, prompt, negative_prompt, srcTrans, toTrans], outputs=[p_tr, p_n_tr]) \\\n"""]
    ]


def search_and_path():
    isOk = 0
    pathesLen = len(PATH_OBJ_DATA_PROMPT_TRANSLATE)
    patchedFileName = os.path.join(DIR_FOOOCUS, "webui_patched.py")
    
    with open(PATH_TO_WEBUI, 'r+', encoding='utf-8') as f:
        lines = f.readlines()
        len_lines = len(lines)

        if not len_lines:
            print(f"File '{PATH_TO_WEBUI}' is empty!\n")
            return

        if PATH_OBJ_DATA_PROMPT_TRANSLATE[0][1] in lines:
            return "Already"

        pathed = 0
        pathSteps = 100 / pathesLen
        
        patchedFile = open(patchedFileName, 'w+', encoding='utf-8')

        for line in lines:            
            for linepath in PATH_OBJ_DATA_PROMPT_TRANSLATE:
                if line.startswith(linepath[0]):             
                    line = line + linepath[1]
                    isOk = isOk + 1
                    
                    pathed += pathSteps
                    print('Patches applied to file {0} of {1} [{2:1.1f}%)]'.format(isOk, pathesLen, pathed), end='\r', flush=True)
                    
            patchedFile.write(line)
            
        patchedFile.close()

        pathResult = isOk == pathesLen

        if not pathResult:
            # Remove tmp file
            os.remove(patchedFileName)
        else:
            # Rename to webui.py and backup original
            if not os.path.exists(os.path.join(DIR_FOOOCUS, "webui_original.py")):
                shutil.copy(PATH_TO_WEBUI, os.path.join(DIR_FOOOCUS, "webui_original.py"))
                
            shutil.move(patchedFileName, PATH_TO_WEBUI)
        
    return "Ok" if pathResult else "Error"

def start_path():
    print("""=== Script for patching file webui.py for Fooocus ===
> Extension: 'Prompt Translate'
> Author: AlekPet
> Github: https://github.com/AlekPet/Fooocus_Extensions_AlekPet
=== ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ===""")
    
    isOk = search_and_path()
    if isOk == "Ok":
        print("\nPatched successfully!")
        
    elif isOk == "Already":
        print("\nPath already appied!")
        
    else:
        print("\nError path data incorrect!")

start_path()
