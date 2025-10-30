<h1 align="center" style="color:#00FF00;">LICEO AERONÁUTICO MILITAR</h1>
<h2 align="center" style="color:#00FF00;">PROMOCIÓN 46</h2>
<p align="center">
  <b>GRUPO:</b> CAD II AÑO Cicolini, CAD II AÑO Franchi, CAD II AÑO Méndez y CAD II AÑO Santacroce
</p>

<p align="center">
  <img src="/img/images.png" alt="Insignia FAA" style="height:120px; width:auto; margin-right:30px;">
  <img src="/img/Flag_of_Argentina.svg.png" alt="Bandera Argentina" style="height:120px; width:auto; margin:0 30px;">
  <img src="/img/LAM_Cuerpo_de_Cadetes_1982_FAA_parche.png" alt="Escudo LAM" style="height:120px; width:auto; margin-left:30px;">
</p>


---

### GRUPO DE TRABAJO  
**CAD II Año Cicolini, CAD II Año Franchi, CAD II Año Méndez y CAD II Año Santacroce**

---

## Descripción del Proyecto

El **Proyecto SONAR** es una iniciativa académica desarrollada en el marco de la **Promoción 46 del Liceo Aeronáutico Militar (LAM)**, orientada a la **visualización de distancias y detección de objetos en tiempo real** mediante el uso de un sensor ultrasónico **HC-SR04**, un **servo SG90** y una interfaz gráfica desarrollada en **Python**.

El sistema realiza un **barrido angular de 0° a 180°**, midiendo distancias con precisión y generando un **radar visual** con sonido e interfaz gráfica, que representa los ecos detectados con puntos en movimiento.

---

## Componentes Utilizados

| Componente | Descripción |
|-------------|--------------|
| **Arduino UNO** | Microcontrolador principal encargado de controlar el servo y leer las distancias del sensor. |
| **Sensor ultrasónico HC-SR04** | Mide la distancia al objeto mediante pulsos de sonido. |
| **Servo SG90** | Gira el sensor entre 0° y 180° para realizar el barrido. |
| **Python (Matplotlib + PySerial)** | Programa que recibe los datos del Arduino y muestra el radar en tiempo real. |

---

## Esquema de Funcionamiento

```text
HC-SR04 → mide distancia
↓
Arduino → envía “ángulo,distancia” por COM3
↓
Python (sonar_realtime.py) → muestra radar + sonidos
↓
Servo → sincronizado con el barrido visual
```

- Lee los datos reales del Arduino vía PySerial.

- Renderiza el radar con Matplotlib y sonidos tipo sonar.

- Muestra en pantalla la interfaz del LAM SONAR – REALTIME con insignias e información del grupo.

##Conexiones Básicas
- Elemento	Pin Arduino UNO
- Servo (naranja)	D3 (señal PWM)
- Servo (rojo)	5V
- Servo (marrón)	GND
- HC-SR04 TRIG	D9
- HC-SR04 ECHO	D10
- LED	D7
- Buzzer	D6

##Captura de la Interfaz

**Ejecución**
1. Subir el sketch al Arduino

2. Ejecutar el radar desde consola
```bash
python sonar_realtime.py
```
3️. Resultado esperado

- Línea verde de barrido activo
- Puntos rojos indicando detecciones
- Sonidos de eco al detectar obstáculos
- Información lateral con rango y bearing



<h2 align="center">Video de Demostración</h2>

<p align="center">
  <a href="https://youtu.be/TNBWvrjQFEQ">
    <img src="https://img.youtube.com/vi/TNBWvrjQFEQ/0.jpg" alt="Video del radar LAM" width="600">
  </a>
</p>

<p align="center">
  - <a href="https://youtu.be/TNBWvrjQFEQ" target="_blank" rel="noopener noreferrer">
  Ver en YouTube en pantalla completa
  </a>
</p>





## Créditos
Proyecto educativo del Liceo Aeronáutico Militar – Promoción 46
Desarrollado con fines académicos y de divulgación técnica.

Docente guía: Profesor Emiliano Juan
Materia: Tecnología II Año – LAM 2025

## Licencia
Este proyecto es de uso educativo y libre distribución bajo licencia MIT.
