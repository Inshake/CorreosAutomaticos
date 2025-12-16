from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import smtplib
from email.message import EmailMessage
import re
from io import BytesIO

app = Flask(__name__)

EMAIL_RE = re.compile(r"^[^@]+@[^@]+\.[^@]+$") # Patrón para validar correos 

COLUMNAS_ESPERADAS = ["email", "nombre", "apellido", "link"] # Da el orden de las columnas esperadas
NOMBRE_COL = {
    "email": "correo electrónico",
    "nombre": "nombre",
    "apellido": "apellido",
    "link": "link del certificado"
}

@app.route("/")
def index():
    return render_template("index.html", error=None, success=None)

@app.route("/send", methods=["GET", "POST"])
def send():
    if request.method == "GET":
        return redirect(url_for("index"))

    asunto = request.form.get("asunto", "").strip()
    texto = request.form.get("texto", "").strip()
    correo = request.form.get("correo", "").strip()
    contraseniaSec = request.form.get("contraseniaSec", "").strip()
    archivo = request.files.get("archivo")

    if not asunto or not texto or not correo or not contraseniaSec: # Verifica que los campos no estén vacíos
        return render_template("index.html", error="Faltan completar campos del formulario.", success=None)

    if not archivo or archivo.filename == "":
        return render_template("index.html", error="No se recibió archivo Excel.", success=None)

    if not (archivo.filename.endswith(".xlsx") or archivo.filename.endswith(".xls")):
        return render_template("index.html", error="El archivo debe ser Excel (.xlsx o .xls).", success=None)

    try: # Lee el archivo Excel
        contenido = archivo.read()
        excel = BytesIO(contenido)
        df = pd.read_excel(excel, header=1, usecols=[1, 2, 3, 4])
    except Exception:
        return render_template("index.html", error="Error al leer el archivo Excel.", success=None)

    if list(df.columns) != COLUMNAS_ESPERADAS: # Verifica que las columnas sean las esperadas
        return render_template(
            "index.html",
            error="Formato incorrecto del Excel. Columnas esperadas: email, nombre, apellido, link.",
            success=None
        )

    errores = [] # Creamos una lista para almacenar errores de validación

    if df.empty:
        errores.append("El Excel no contiene filas de datos.")

    for i, row in df.iterrows(): # Validamos cada fila
        fila = i + 3

        for col in COLUMNAS_ESPERADAS:
            valor = row[col]
            valor_str = "" if pd.isna(valor) else str(valor).strip()

            if not valor_str:
                errores.append(f"Fila {fila}, {NOMBRE_COL[col]} está vacío.")
                continue

            if col == "email" and not EMAIL_RE.match(valor_str):
                errores.append(f"Fila {fila}, correo electrónico inválido: {valor_str}")

            if col == "link" and not valor_str.startswith(("http://", "https://")):
                errores.append(f"Fila {fila}, link inválido: {valor_str}")

    if errores:
        return render_template("index.html", error=" | ".join(errores), success=None)

    enviados = 0
    errores_envio = []

    try: # Configuramos el servidor SMTP y enviamos los correos
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(correo, contraseniaSec)

            for i, row in df.iterrows(): 
                destinatario = str(row["email"]).strip()
                nombre = str(row["nombre"]).strip()
                apellido = str(row["apellido"]).strip()
                link = str(row["link"]).strip()

                asunto_personalizado = (
                    asunto
                    .replace("{nombre}", nombre)
                    .replace("{apellido}", apellido)
                )

                texto_personalizado = (
                    texto
                    .replace("{nombre}", nombre)
                    .replace("{apellido}", apellido)
                    .replace("{enlace}", link)
                )

                msg = EmailMessage()
                msg["From"] = correo
                msg["To"] = destinatario
                msg["Subject"] = asunto_personalizado
                msg.set_content(texto_personalizado)

                try:  # Enviamos el correo
                    smtp.send_message(msg)
                    enviados += 1
                except Exception as e:
                    errores_envio.append(f"{destinatario}: {e}")

    except Exception as e:
        return render_template("index.html", error=f"Error SMTP: {e}", success=None)

    if errores_envio:
        mensaje = f"Enviados: {enviados}. Errores: " + " | ".join(errores_envio)
        return render_template("index.html", error=mensaje, success=None)
    else:
        mensaje = f"Correos enviados correctamente. Total enviados: {enviados}."
        return render_template("index.html", error=None, success=mensaje)

if __name__ == "__main__":
    app.run(debug=True)
