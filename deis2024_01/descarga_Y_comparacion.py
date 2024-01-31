"""

"""

import json
import requests

import os
import shutil
import time
from datetime import datetime
import rarfile

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


url = "https://deis.minsal.cl/deisajax?action=wp_ajax_ninja_tables_public_action&table_id=2736&target_action=get-all-data&default_sorting=manual_sort&skip_rows=0&limit_rows=0&chunk_number=1&ninja_table_public_nonce=ebeeef3d63"
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}
resp = requests.get(url, headers=headers)

datas_json_descargada = json.loads(resp.text)

# Este código sólo debe ejecutarse cuando se quiera actualizar los datos base del archivo "data_base.json"
# INICIO CODIGO TEMPORAL
# dasta_json_descargada_campos_seleccionados=[{
#         "estadistica":d["value"]["estadistica"],
#         "filtro_2":d["value"]["filtro_2"],
#         "nombre":d["value"]["nombre"],
#         "ver":d["value"]["ver"],
#         "___id___":d["value"]["___id___"],
#     } for d in data_json_descargada]
# with open('data_base.json', 'w', encoding='utf-8') as f:
#   s  json.dump(data_json_descargada_campos_seleccionados, f, ensure_ascii=False, indent=4)
# FIN CODIGO TEMPORAL


# Carga los datos base
datas_base = json.load(open("data_base.json"))
datas_base_ids = [d["___id___"] for d in datas_base]

# compara que los datos base sean los mismos que los descargados
for data_json_descargada in datas_json_descargada:
    if data_json_descargada["value"]["___id___"] not in datas_base_ids:
        print(f'El dato descargado con ___id___ {data_json_descargada["value"]["___id___"]} no está en la base de referencia')
        continue

    data_base_id_equivalente = [d for d in datas_base if d["___id___"] == data_json_descargada["value"]["___id___"]][0]
    if data_base_id_equivalente["estadistica"] != data_json_descargada["value"]["estadistica"]
    and data_base_id_equivalente["filtro_2"] != data_json_descargada["value"]["filtro_2"]
    and data_base_id_equivalente["nombre"] != data_json_descargada["value"]["nombre"]
    and data_base_id_equivalente["ver"] != data_json_descargada["value"]["ver"]:
        print(f'El dato descargado con ___id___ {data_json_descargada["value"]["___id___"]} no es igual al de la base de referencia')
        continue
    

# El siguiente código saca screenshots de todas las páginas de la tabla.
# INICIO
folder_descargas = os.getcwd() + "/" f"descargas_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
os.mkdir(folder_descargas)

opts = Options()
opts.set_preference("browser.link.open_newwindow.restriction", 0)
opts.set_preference("browser.link.open_newwindow", 3)
driver = webdriver.Firefox(options=opts)
driver.maximize_window()
driver.get("https://deis.minsal.cl/")
time.sleep(3)
driver.get_screenshot_as_file(f"{folder_descargas}/pagina_inicial.png")

driver.find_element(By.XPATH, "//a[text()[contains(.,'1)]]").click()
paginas_faltantes = True
pagina = 1

while paginas_faltantes:
    time.sleep(0.5)
    d=driver.get_screenshot_as_file(f"{folder_descargas}/pagina_datos_{pagina}.png")
    if driver.find_element(By.CSS_SELECTOR, 'li[data-page="next"]').get_attribute("class").find("disabled") > 0:
        break
    driver.find_element(By.CSS_SELECTOR, 'li[data-page="next"]>a').click()
    pagina += 1

#Termino


# El siguiente código descarga los archivos y los compara
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
