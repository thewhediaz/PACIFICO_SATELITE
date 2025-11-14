import streamlit as st
try:
    import requests
    import imageio.v2 as imageio
    from io import BytesIO
    import tempfile
    
    # --- Configuración ---
    GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
    HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}
    URL = "https://api.github.com/repos/thewhediaz/SAT/contents/media/CURRENT_3H"
    
    st.set_page_config(layout="wide")
    
    # --- Obtener archivos PNG desde GitHub ---
    response = requests.get(URL, headers=HEADERS)
    files = response.json()
    png_files = sorted([f["download_url"] for f in files if f["name"].endswith(".png")])
    
    if not png_files:
        st.stop()  # No mostrar nada si no hay imágenes
    
    # --- Leer imágenes ---
    images = []
    for png_url in png_files:
        r = requests.get(png_url)
        img = imageio.imread(BytesIO(r.content))
        images.append(img)
    
    # --- Crear GIF temporal (bucle infinito) ---
    temp_gif = tempfile.NamedTemporaryFile(suffix=".gif", delete=False)
    imageio.mimsave(temp_gif.name, images, format="GIF", fps=5, loop=0)
    
    # --- Mostrar GIF ajustado al ancho ---
    st.image(temp_gif.name, use_column_width=True)
    
    # --- Crear MP4 temporal ---
    temp_mp4 = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
    imageio.mimsave(temp_mp4.name, images, format="FFMPEG", fps=4)
    
    # --- Botón para descargar MP4 ---
    with open(temp_mp4.name, "rb") as f:
        mp4_bytes = f.read()
    st.download_button(
        label="Descargar animación MP4",
        data=mp4_bytes,
        file_name="animacion.mp4",
        mime="video/mp4"
    )
    
    # --- Botón para descargar última imagen ---
    last_img_bytes = BytesIO()
    imageio.imwrite(last_img_bytes, images[-1], format="PNG")
    last_img_bytes.seek(0)
    st.download_button(
        label="Descargar última imagen",
        data=last_img_bytes,
        file_name="ultima_imagen.png",
        mime="image/png"
    )
    
    from datetime import datetime
    from streamlit_autorefresh import st_autorefresh
    
    # Minutos objetivo
    target_minutes = [2, 12, 22, 32, 42, 52]
    
    now = datetime.now()
    minute = now.minute
    second = now.second
    
    # Buscar el próximo minuto objetivo
    for m in target_minutes:
        if m > minute or (m == minute and second == 0):
            next_target = m
            break
    else:
        next_target = target_minutes[0]  # siguiente hora
    
    # Calcular segundos hasta el próximo refresh
    delta_seconds = (next_target - minute) * 60 - second
    if delta_seconds < 0:
        delta_seconds += 3600  # pasar a la siguiente hora si es necesario
    
    # Activar autorefresh
    st_autorefresh(interval=delta_seconds*1000, key="autorefresh")
    
    
    
    
except:
    pass
