El DEIS pone a disposición datos en su página https://deis.minsal.cl/ .

El objetivo de este módulo es leer todos esos datos y revisar su actualización.

La página muestra 2.242 documentos a descargar (fecha 2024-01-30).

La tabla se construye en base a un json API del mismo mensual de la url:

https://deis.minsal.cl/deisajax?action=wp_ajax_ninja_tables_public_action&table_id=2736&target_action=get-all-data&default_sorting=manual_sort&skip_rows=0&limit_rows=0&chunk_number=1&ninja_table_public_nonce=ebeeef3d63

El cual tiene la información de todos los documentos en un formato

```json

{
    "options": {
        "classes": "ninja_table_row_5240 nt_row_id_23151"
    },
    "value": {
        "estadistica": "Atenciones Sector Privado",
        "filtro_1": "2008",
        "filtro_2": "Atenciones Odontol\u00f3gicas",
        "filtro_3": "",
        "filtro_4": "",
        "filtro_5": "",
        "formato": "html",
        "nombre": "Atenciones odontol\u00f3gicas por actividad y grupo de edad \u2013 ANEXO 2008",
        "ver": "https:\/\/reportesdeis.minsal.cl\/REMSAS\/2008_publica\/Remsas_2008_ODONTOLOGICA_ANEXO_2\/Remsas_2008_ODONTOLOGICA_ANEXO.aspx",
        "___id___": 23151
    }
}
```

## Scraping

la url indicada arriba que trae un json con todos los datos tiene una especie de seguridad para evitar robots, por lo que se debe asegurar que el request se haga con headers reales que asemejen un navegador.

# Proceso

Se compara el listado de datos disponibles en la página del DEIS con la útlima información y se buscan nuevos archivos:

- se revisa si hay un archivo nuevo.
- se revisa que los archivos tengan el mismo nombre
- **No** se está revisando si un archivo que existía ya no aparece

