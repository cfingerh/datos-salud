"""
Script que revisa la página del censo, descarga los archivos y obtiene screenshots.
Dependiendo de la velocidad de internet, puede que no alcance a descargar todos los archivos: modificar el tiempo de espera en ese caso.

"""

import os
import shutil
import time
from datetime import datetime
import rarfile

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

tiempo_de_espera_minutos = 5

folder_descargas = os.getcwd() + "/" f"descargas_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
os.mkdir(folder_descargas)

options = Options()
profile = webdriver.FirefoxProfile()
profile.set_preference("browser.download.folderList", 2)
profile.set_preference("browser.download.manager.showWhenStarting", False)
profile.set_preference("browser.download.dir", folder_descargas)
profile.set_preference("general.warnOnAboutConfig", False)
profile.update_preferences()

driver = webdriver.Firefox(options=options, firefox_profile=profile)


driver.maximize_window()
driver.get("https://www.ine.gob.cl/estadisticas/sociales/censos-de-poblacion-y-vivienda/censo-de-poblacion-y-vivienda")
driver.get_screenshot_as_file(f"{folder_descargas}/pagina_inicial.png")
driver.find_element(By.CSS_SELECTOR, ".fas.fa-database").click()
time.sleep(2)
driver.find_element(By.CSS_SELECTOR, ".categoriaDescarga.bloqueCatDes").click()
time.sleep(2)
driver.find_element(By.XPATH, "//div[text()[contains(.,'CSV')]]").click()

driver.get_screenshot_as_file(f"{folder_descargas}/pagina_datos.png")

# descarga los archivos
driver.find_element(By.XPATH, "//span[text()[contains(.,'CSV Identificación geográfica Censo 2017')]]").click()
driver.find_element(By.XPATH, "//span[text()[contains(.,'CSV Viviendas Censo 2017')]]").click()
driver.find_element(By.XPATH, "//span[text()[contains(.,'CSV Hogares Censo 2017')]]").click()
driver.find_element(By.XPATH, "//span[text()[contains(.,'CSV Personas Censo 2017')]]").click()
driver.find_element(By.XPATH, "//span[text()[contains(.,'CSV Manzana - entidad Censo 2017')]]").click()


completo = [False, False, False, False, False]

for k in range(tiempo_de_espera_minutos * 60 / 10):
    archivos = [
        {"nombre": "csv-hogares-censo-2017.rar", "size": 15526894},
        {"nombre": "csv-identificación-geográfica-censo-2017.rar", "size": 453852},
        {"nombre": "csv-manzana---entidad-censo-2017.rar", "size": 7641516},
        {"nombre": "csv-personas-censo-2017.rar", "size": 240286217},
        {"nombre": "csv-viviendas-censo-2017.rar", "size": 29656653},
    ]

    for count, archivo in enumerate(archivos):
        file_stats = os.stat(folder_descargas + "/" + archivo["nombre"])
        completo[count] = file_stats.st_size == archivo["size"]

    print(completo)
    time.sleep(10)
    if all(completo):
        break
driver.quit()


if not all(completo):
    print("No se descargaron todos los archivos con los tamaños esperados")
else:
    # copia la versión descargad a la capreta descargar y descomprime
    print("Se descargaron todos los archivos con los tamaños esperados")

    # borra la carpeta descargas si existe
    if os.path.exists("descargas") and os.path.isdir("descargas"):
        shutil.rmtree("descargas")

    shutil.copytree(folder_descargas, "descargas")

    # descomprimir
    for archivo in archivos:
        r = rarfile.RarFile(folder_descargas + "/" + archivo["nombre"])
        r.extractall(path="descargas/" + archivo["nombre"].replace(".rar", ""))
        r.close()
