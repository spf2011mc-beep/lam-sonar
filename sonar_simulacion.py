import matplotlib.pyplot as plt
import numpy as np
import matplotlib.image as mpimg
import sounddevice as sd
from datetime import datetime


# --- FUNCIONES DE SONIDO ---
fs = 44100

def sonar_ping(frecuencia=1000, duracion=0.08, volumen=0.5):
    """Ping agudo corto estilo radar USAF"""
    try:
        t = np.linspace(0, duracion, int(fs * duracion), False)
        onda = np.sin(frecuencia * 2 * np.pi * t) * volumen
        sd.play(onda, fs, blocking=False)  # 👈 no bloquea el loop
    except Exception as e:
        print("⚠️ Error en sonar_ping:", e)


def beep_objeto(frecuencia=1400, duracion=0.2, volumen=0.8):
    """Beep fuerte estilo contacto radar"""
    t = np.linspace(0, duracion, int(fs * duracion), False)
    onda = np.sin(frecuencia * 2 * np.pi * t) * volumen
    sd.play(onda, fs, blocking=True)

def timestamp_militar():
    """Devuelve timestamp en formato militar (DTG)."""
    ahora = datetime.utcnow()
    return ahora.strftime("%d%H%MZ %b %y").upper()

# --- FIGURA ---
fig = plt.figure(figsize=(18, 12), facecolor="black")
fig.canvas.manager.set_window_title("LAM SONAR")

# --- RADAR (gigante, hasta el header) ---
ax = fig.add_axes([0.05, 0.05, 0.9, 0.7], polar=True)

ax.set_theta_offset(0)
ax.set_theta_direction(1)
ax.set_thetamin(0)
ax.set_thetamax(180)
ax.set_rlim(0, 200)

ax.set_facecolor("black")
ax.set_xticks([])
ax.set_yticks([])
ax.grid(False)

# --- GRILLA ---
for r in np.linspace(40, 200, 5):
    ax.plot(np.linspace(0, np.pi, 300), [r]*300, color="lime", linestyle="--", linewidth=0.5)
for angle in np.linspace(0, np.pi, 9):
    ax.plot([angle, angle], [0, 200], color="lime", linestyle="--", linewidth=0.5)

# --- HEADER COMPLETO ARRIBA ---
plt.figtext(0.5, 0.97, "LICEO AERONÁUTICO MILITAR",
            ha="center", va="top", fontsize=24,
            color="lime", fontweight="bold")

# (↓ Bajamos un poco más para simular líneas en blanco)
plt.figtext(0.5, 0.94, " ", ha="center", va="top")  # 1 línea en blanco
plt.figtext(0.5, 0.93, " ", ha="center", va="top")  # 2 líneas en blanco

plt.figtext(0.5, 0.92, "PROMOCIÓN 46",
            ha="center", va="top", fontsize=18, color="lime")

# Otra separación antes de la lista de cadetes
plt.figtext(0.5, 0.90, " ", ha="center", va="top")
plt.figtext(0.5, 0.89, " ", ha="center", va="top")

plt.figtext(0.5, 0.88,
            "GRUPO: CAD II AÑO Cicolini, CAD II AÑO Franchi, CAD II Méndez y CAD II AÑO Santacroce",
            ha="center", va="top", fontsize=12, color="lime")

# Ahora dejamos 3 líneas en blanco antes de las imágenes
plt.figtext(0.5, 0.85, " ", ha="center", va="top")
plt.figtext(0.5, 0.84, " ", ha="center", va="top")
plt.figtext(0.5, 0.83, " ", ha="center", va="top")


# --- IMÁGENES centradas en fila ---
imagenes = [
    "images.png",
    "Flag_of_Argentina.svg.png",
    "LAM_Cuerpo_de_Cadetes_1982_FAA_parche.png"
]
posiciones = [0.33, 0.5, 0.70]

for img_path, pos in zip(imagenes, posiciones):
    img = mpimg.imread(img_path)
    ax_img = fig.add_axes([pos - 0.08, 0.70, 0.16, 0.1])
    ax_img.imshow(img)
    ax_img.axis("off")

# --- PANEL DE CONTACTOS (parte inferior derecha, alineado al radar) ---
ax_panel = fig.add_axes([0.80, 0.02, 0.23, 0.7])
ax_panel.set_facecolor("black")
ax_panel.axis("off")

texto_titulo = ax_panel.text(0, 1.0, "CONTACTOS: 0",
                             ha="left", va="top",
                             fontsize=14, color="lime",
                             family="monospace")

texto_log = ax_panel.text(0, 0.95, "",
                          ha="left", va="top",
                          fontsize=10, color="lime",
                          family="monospace")

# --- RADAR ---
linea_barrido = None
rastros = []
max_rastro = 80

# Lista para historial
log_contactos = []

# Objetos simulados
objetos = [
    (np.pi/6, 100),
    (np.pi/3, 150),
    (2*np.pi/3, 80)
]

# --- LOOP PRINCIPAL ---
while True:
    for sweep in [np.linspace(0, np.pi, 180),
                  np.linspace(np.pi, 0, 180)]:

        contactos_en_paso = 0
        log_contactos.append(f"{timestamp_militar()} | INICIO BARRIDO")
        if len(log_contactos) > 40:
            log_contactos.pop(0)
        texto_log.set_text("\n".join(log_contactos))
        sonar_ping()  # sonar submarino al inicio de cada barrido

        for i, angle in enumerate(sweep):
            if i % 10 == 0:  # cada 10 pasos de barrido
                sonar_ping()
            if linea_barrido:
                linea_barrido.remove()

            # Línea barrido
            linea_barrido, = ax.plot([angle, angle], [0, 200],
                                     color="lime", linewidth=2, alpha=0.6)

            # Rastro
            rastro = ax.fill_between([angle-0.02, angle], 0, 200,
                                     color="lime", alpha=0.1)
            rastros.append(rastro)
            if len(rastros) > max_rastro:
                rastros[0].remove()
                rastros.pop(0)

            # Detecciones
            for (theta, dist) in objetos:
                ax.plot(theta, dist, 'ro', markersize=8)
                if abs(angle - theta) < 0.05:
                    contactos_en_paso += 1
                    grados = int(np.degrees(theta))
                    registro = f"{timestamp_militar()} | BRG {grados:03d}° RNG {dist}cm"
                    log_contactos.append(registro)

                    if len(log_contactos) > 40:  # límite panel
                        log_contactos.pop(0)

                    beep_objeto()

            # Actualizar panel
            texto_titulo.set_text(f"CONTACTOS: {contactos_en_paso}")
            texto_log.set_text("\n".join(log_contactos))

            plt.pause(0.01)
