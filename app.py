from flask import Flask, render_template, request
import pandas as pd  # Para leer el Excel
import smtplib       # Para enviar correos
from email.message import EmailMessage  # Para crear el mensaje

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/send", methods=["POST"])
def send():

    # Datos del formulario
    asunto = request.form.get("asunto")
    texto = request.form.get("texto")
    correo = request.form.get("correo")
    contraseniaSec = request.form.get("contraseniaSec")

    # Archivo Excel
    archivo = request.files.get("archivo")

    print("\n--- Datos recibidos ---")
    print("Asunto:", asunto)
    print("Texto:", texto)
    print("Correo remitente:", correo)
    print("App Password:", contraseniaSec)
    print("Archivo:", archivo.filename if archivo else "No llegó archivo")

    # Leer Excel
    excel_data = pd.read_excel(archivo)
    print("\n--- Primeras filas del Excel ---")
    print(excel_data.head())

    # Obtener primer email para prueba
    destinatario = excel_data["email"][0]

    # Obtener link del Excel
    link_certificado = excel_data["link"][0]   
    print("\nLink para este destinatario:", link_certificado)

    # Acá creamos el contenido del correo y le el certificado.
    contenido_final = f"""{texto}

🔗 Aquí tienes tu certificado:
{link_certificado}
"""

    msg = EmailMessage()
    msg["From"] = correo
    msg["To"] = destinatario
    msg["Subject"] = asunto
    msg.set_content(contenido_final)

    # Esta parte de código manda el correo, con la libería smtplib
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            print("Intentando login con:", correo)
            print("Longitud password:", len(contraseniaSec))
            smtp.login(correo, contraseniaSec)
            smtp.send_message(msg)

        print("Correo enviado correctamente.")

    except Exception as e:
        print("Error al enviar correo:", e)

    return "Correo de prueba enviado (si falla debería mostrarme en consola el error)."

if __name__ == "__main__":
    app.run(debug=True)
