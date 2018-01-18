# DjangoApp

0. Would be best if you went through all the below points after installing the newest Pycharm IDE version

====== CONFIGURE PYTHON AND DJANGO ======
1. Install python3 interpreter or set the virtualenv python interpreter to inherit from python 3
  + File/Settings/Project:ImgApp/ProjectInterpreter// GearWheel Icon -> Create VirtualEnv
2. In Pycharm Add Django to the packages list, then hit Install Package or install Django directly on your server
  + after this process is complete, go to Terminal in PyCharm or your server's terminal and type: django-admin --version

====== UNIT TESTING ======
3. Add UnitTests with xml-reporting:
  + install xml-reporting package:
    - File/Settings/Project:ToDoApp/Project Interpreter/'Plus icon'/unittest-xml-reporting/ Install Package

====== GRAPHIC LIBRARY ======
4. + install Pillow:
    - File/Settings/Project:ToDoApp/Project Interpreter/'Plus icon'/Pillow/ Install Package

====== Vision API ======
5. Get your API key from: https://azure.microsoft.com/en-us/try/cognitive-services/?api=face-api
  + No CreditCard required, 30days Trial available after e.g. GitHub account synchronisation
  + Replace ImgApp/lib/visionapi.py's subscription_key variable with your key
