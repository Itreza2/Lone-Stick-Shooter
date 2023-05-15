# Lone-Stick-Shooter

Crédits assets :  
-https://cainos.itch.io/pixel-art-top-down-basic Par "Cainos"  
-https://demching.itch.io/dino-family (v1.0.0) Par "DemChing"  
-https://gg-undroid-games.itch.io/pixel-art-guns-with-firing-animations Par "GG Undroid Games"  
  
------------------------------------------------------------------------------------------------  
  
Instructions pour la compilation du programme :  
/! un executable windows est également disponible, ce processus n'est pas obligatoire/  
-La lecture et la compilation de ce programme nécessitent un interpréteur python ainsi que les librairies  
 Pillow (et cx-Freeze, pour la compilation uniquement), installables via pip :  
  ->pip install Pillow  
  ->pip install cx_Freeze  
-Documentation officielle de cx_Freeze : https://cx-freeze.readthedocs.io/en/latest/  
  
-Script "setup.py" :  
  
  import sys  
  from cx_Freeze import setup, Executable  
  base = None  
  if(sys.platform == "win32"):  
        base = "Win32GUI"  
  if(sys.platform == "win64"):  
        base = "Win64GUI"  
  setup(name="Lone Stick Shooter", executables=[Executable(script="arcade.py", base=base)])  
