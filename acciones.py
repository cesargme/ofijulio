from util import audio_processing, gpt
from pathlib import Path
import FreeSimpleGUI as sg
import os
import shutil

def seleccionar_archivo_mkv(func):
    def wrapper(*args, **kwargs):
        layout = [
            [sg.Text("Selecciona el archivo .mkv")],
            [sg.Input(), sg.FileBrowse(file_types=(("MKV Files", "*.mkv"),))],
            [sg.OK(), sg.Cancel()]
        ]

        window = sg.Window("Seleccionar Archivo", layout)
        
        event, values = window.read()
        window.close()

        if event == "OK":
            ruta_mkv = values[0]
            if ruta_mkv.endswith('.mkv'):
                return func(ruta_mkv, *args, **kwargs)
            else:
                sg.popup_error("Debe seleccionar un archivo .mkv")
        else:
            sg.popup("Operación cancelada")
    
    return wrapper

@seleccionar_archivo_mkv #TODO, que sea en el mismo explorador, seleccionándolo ahí mismito
def transcribir_reunión(ruta_mkv):
    ruta_mkv_str= ruta_mkv
    ruta_mkv = Path(ruta_mkv)

    audio_processing.convertir_mkv_a_mp3(ruta_mkv_str, "temp_audio.mp3")
    audio_processing.dividir_audio_en_chunks("temp_audio.mp3", duracion_minutos=10, carpeta_salida="reu")
    gpt.transcribir_y_unificar_chunks("reu",ruta_mkv.parent / (ruta_mkv.stem + ".txt") )
    shutil.rmtree("reu")