import streamlit as st
import os
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

st.set_page_config(layout="wide")

# --- Ruta local de los archivos ---
LOCAL_FOLDER = "media/CURRENT_2H_colores_windy"  # ajusta a tu carpeta

# --- Listar archivos ---
all_files = os.listdir(LOCAL_FOLDER)

# Buscar GIF y MP4 por nombre fijo
gif_file = os.path.join(LOCAL_FOLDER, "animacion.gif") if "animacion.gif" in all_files else None
mp4_file = os.path.join(LOCAL_FOLDER, "animacion.mp4") if "animacion.mp4" in all_files else None

# Buscar PNGs y tomar la última por fecha de modificación
png_files = [f for f in all_files if f.endswith(".png")]
if png_files:
    png_files = sorted(
        png_files,
        key=lambda f: os.path.getmtime(os.path.join(LOCAL_FOLDER, f))
    )
    last_png_file = os.path.join(LOCAL_FOLDER, png_files[-1])
else:
    last_png_file = None

# Si no hay GIF o MP4 o última imagen → no mostrar nada
if not gif_file or not mp4_file or not last_png_file:
    st.stop()

# --- Mostrar GIF animado ---
st.image(gif_file, width='stretch')

# --- Botón descargar MP4 ---
with open(mp4_file, "rb") as f:
    mp4_bytes = f.read()

st.download_button(
    label="Descargar animación MP4",
    data=mp4_bytes,
    file_name="animacion.mp4",
    mime="video/mp4"
)

# --- Botón descargar última imagen PNG ---
with open(last_png_file, "rb") as f:
    last_png_bytes = f.read()

st.download_button(
    label="Descargar última imagen",
    data=last_png_bytes,
    file_name="ultima_imagen.png",
    mime="image/png"
)

# --- AUTOREFRESH EN MINUTOS ESPECÍFICOS ---
target_minutes = [2, 7, 12, 17, 22, 27, 32, 37, 42, 47, 52, 57]

now = datetime.now()
minute = now.minute
second = now.second

# Buscar el próximo minuto objetivo
for m in target_minutes:
    if m > minute or (m == minute and second == 0):
        next_target = m
        break
else:
    next_target = target_minutes[0]

# Segundos hasta el refresh
delta_seconds = (next_target - minute) * 60 - second
if delta_seconds < 0:
    delta_seconds += 3600

st_autorefresh(interval=delta_seconds * 1000, key="autorefresh")

