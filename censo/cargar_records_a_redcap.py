"""
Archivo para cargar los archivos de censo 2017 a redcap. 
Esta función sólo se debería utilizar una vez, para la carga inicial
"""

import os
import csv
import json
import requests

from dotenv import load_dotenv

load_dotenv()  # carga variables del archivo .env


class Lectura:
    url = "https://redcap.cibm.cl/api/"

    token = os.environ.get("token")

    def fetch_records(self):
        # Traer todos los recorsd y obtener último id
        fields = {"token": self.token, "content": "record", "format": "json", "returnFormat": "json"}
        resp = requests.post(self.url, data=fields)
        self.data_json = json.loads(resp.text)

        with open("respuesta.json", "w") as file:
            json.dump(self.data_json, file, indent=4)

        redcap_repeat_instrument = ""
        self.ultimo_id = int(self.data_json[-1].get("id_level_1"))
        self.name_level_1_existentes = [d.get("name_level_1") for d in self.data_json if d.get("redcap_repeat_instrument") == redcap_repeat_instrument]

    def obtener_rows_columns(self, ubicacion):
        """para un archivo csv dado (guardado en ubicación), se obtiene el número de columnas y filas."""
        f = open(ubicacion, "r")
        reader = csv.reader(f, delimiter=";")
        numero_columnas = len(next(reader))
        f.seek(0)
        numero_filas = 0
        for row in reader:
            numero_filas += 1

        return numero_columnas, numero_filas

    def actualizar_todos(self):
        """actualiza todos los records de la api de redcap"""
        self.fetch_records()

        # f = []
        # layer = 1
        w = os.walk("descargas/")
        for dirpath, dirnames, filenames in w:
            if dirpath.find("csv-identificación-geográfica-censo-2017") < 0:
                continue
            for filename in filenames:
                if filename.find(".csv") < 0:
                    continue

                numero_columnas, numero_filas = self.obtener_rows_columns(f"{dirpath}/{filename}")

                name_level_1 = f"Identificación geográfica Censo 2017 - {filename}"

                # se crea el record.

                if name_level_1 in self.name_level_1_existentes:
                    # en caso de que exista, se obtiene el record y  se modicfican los campos que se quieran updatear
                    record = [d for d in self.data_json if d.get("name_level_1") == name_level_1][0]

                else:
                    # en caso de que no exista, se busca el último id y se le suma 1 correlativo
                    # y se hacen los cambios que se quieran
                    self.fetch_records()  # Asegura que se obtenga el último ID
                    record = {
                        "id_level_1": self.ultimo_id + 1,
                        "name_level_1": name_level_1,
                        "origin": "2",  # que es esto?
                        "acquisition": "4",  # que es esto?
                        "date_download": "2024-01-18 12:53:00",
                        "download_url": "https://www.ine.gob.cl/estadisticas/sociales/censos-de-poblacion-y-vivienda/censo-de-poblacion-y-vivienda",
                        "download_screenshot": "Screenshot 2024-01-18 at 12.53.22.png",
                        "format_original": "1",  # que es esto?
                        "granularity": "1",  # que es esto?
                        "granularity_itemized_level": "3",  # que es esto?
                        "columns": numero_columnas,
                        "rows": numero_filas - 1,
                    }

                # cambios que se quieran aplicar a todos los records
                record["file_original"] = "http://pordefinir.cl"

                # para crear o updatear se ocupa el mismo endpoint
                fields = {
                    "token": self.token,
                    "content": "record",
                    "format": "json",
                    "type": "flat",
                    "data": json.dumps([record]),
                }

                resp = requests.post(self.url, data=fields, timeout=20)

                print("respuesta", resp.text)


Lectura().actualizar_todos()
