# Prompt translate

# Changelog:

> 2024.05.23 - [Prompt translate] Added other translation services and update patcher (edit **modules/config.json** for setting!) ([Note config.json](https://github.com/AlekPet/Fooocus_Extensions_AlekPet/tree/main/prompt_translate#note-settings))

![Prompt translate image ](https://raw.githubusercontent.com/AlekPet/Fooocus_Extensions_AlekPet/main/assets/images/image_prompt_translate.jpg)
![Prompt translate image 2 new version](https://raw.githubusercontent.com/AlekPet/Fooocus_Extensions_AlekPet/main/assets/images/image_prompt_translate_2.jpg)

### Description:

The extension for translating promts into English (possibly into other languages) supports the following services (not all is free):

- DeeplTranslator
- QcriTranslator
- LingueeTranslator
- PonsTranslator
- PapagoTranslator
- BaiduTranslator
- MyMemoryTranslator
- GoogleTranslator
- YandexTranslator
- ChatGptTranslator
- LingueeTranslator
- MicrosoftTranslator

### Installation:

1. Backup one file in the Fooocus, **webui.py** in the root Fooocus direcory.
2. Download files as zip file
3. Extract the data from the archive and copy or move it from the **prompt_translate** folder to, where install **Fooocus** , and confirm replace all.
4. Run Fooocus.

### Note settings:

By default, in the **config.json** file, the option to show services without api is disabled (option **"show_services_no_check_api = false"**), which have **free_api = false** and do not specify **api_key** and other authorization values ​​(depending on the translation service). If you set the value of **show_services_no_check_api: true**, then all services with the value **show_service: true** will be shown.
