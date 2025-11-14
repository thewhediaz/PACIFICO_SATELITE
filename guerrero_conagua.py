import streamlit as st
import requests

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

