import streamlit as st
import requests
from io import BytesIO
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
st.set_page_config(layout="wide")

# --- URLs públicas de GitHub ---
GIF_URL = "https://raw.githubusercontent.com/thewhediaz/SAT/main/media/CURRENT_2H_colores_windy/animacion.gif"
MP4_URL = "https://raw.githubusercontent.com/thewhediaz/SAT/main/media/CURRENT_2H_colores_windy/animacion.mp4"

# --- Mostrar GIF animado ---
st.image(GIF_URL, use_column_width=True)

# --- Descargar MP4 ---
mp4_bytes = requests.get(MP4_URL).content
st.download_button(
    label="Descargar animación MP4",
    data=mp4_bytes,
    file_name="animacion.mp4",
    mime="video/mp4"
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


