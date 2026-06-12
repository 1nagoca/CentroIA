import tkinter as tk
from tkinter import messagebox
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# =====================================
# MODELO 1 - PREDICCION DE CASAS
# =====================================

datos = pd.read_csv("casas.csv")

X = datos[["metros"]]
y = datos["precio"]

modelo_casas = LinearRegression()
modelo_casas.fit(X, y)

# =====================================
# MODELO 2 - DETECTOR DE SPAM
# =====================================

mensajes = [
    "ganaste dinero",
    "reclama tu premio",
    "haz clic aqui",
    "oferta limitada",
    "gana un iphone",
    "hola profesor",
    "nos vemos mañana",
    "adjunto la tarea",
    "reunion a las 8",
    "gracias por tu ayuda"
]

etiquetas = [
    "SPAM",
    "SPAM",
    "SPAM",
    "SPAM",
    "SPAM",
    "NO SPAM",
    "NO SPAM",
    "NO SPAM",
    "NO SPAM",
    "NO SPAM"
]

vectorizador = CountVectorizer()

X_texto = vectorizador.fit_transform(mensajes)

modelo_spam = MultinomialNB()
modelo_spam.fit(X_texto, etiquetas)

# =====================================
# FUNCION CASAS
# =====================================

def abrir_casas():

    ventana = tk.Toplevel()
    ventana.title("Predicción de Casas")
    ventana.geometry("650x500")
    ventana.configure(bg="#f4f6f9")

    def predecir():

        try:

            metros = float(txt_metros.get())

            precio = modelo_casas.predict([[metros]])[0]

            if precio < 180:
                categoria = "BAJO"
            elif precio < 250:
                categoria = "MEDIO"
            else:
                categoria = "ALTO"

            lbl_resultado.config(
                text=f"Precio estimado: ${precio:.2f} millones"
            )

            lbl_categoria.config(
                text=f"Categoría: {categoria}"
            )

            historial.insert(
                tk.END,
                f"{metros:.0f} m² → ${precio:.2f} millones"
            )

        except:

            messagebox.showerror(
                "Error",
                "Ingrese un número válido"
            )

    def limpiar():

        txt_metros.delete(0, tk.END)

        lbl_resultado.config(text="")
        lbl_categoria.config(text="")

    titulo = tk.Label(
        ventana,
        text="🏠 IA PREDICTORA DE CASAS",
        font=("Arial", 18, "bold"),
        bg="#f4f6f9"
    )

    titulo.pack(pady=15)

    tk.Label(
        ventana,
        text="Ingrese los metros cuadrados",
        bg="#f4f6f9"
    ).pack()

    txt_metros = tk.Entry(
        ventana,
        font=("Arial", 14)
    )

    txt_metros.pack(pady=10)

    frame = tk.Frame(
        ventana,
        bg="#f4f6f9"
    )

    frame.pack()

    tk.Button(
        frame,
        text="Predecir",
        width=12,
        command=predecir
    ).grid(row=0, column=0, padx=10)

    tk.Button(
        frame,
        text="Limpiar",
        width=12,
        command=limpiar
    ).grid(row=0, column=1, padx=10)

    lbl_resultado = tk.Label(
        ventana,
        text="",
        font=("Arial", 14, "bold"),
        bg="#f4f6f9"
    )

    lbl_resultado.pack(pady=15)

    lbl_categoria = tk.Label(
        ventana,
        text="",
        font=("Arial", 12, "bold"),
        bg="#f4f6f9"
    )

    lbl_categoria.pack()

    tk.Label(
        ventana,
        text="Historial",
        font=("Arial", 12, "bold"),
        bg="#f4f6f9"
    ).pack(pady=10)

    historial = tk.Listbox(
        ventana,
        width=50,
        height=10
    )

    historial.pack()


# =====================================
# FUNCION SPAM
# =====================================

def abrir_spam():

    ventana = tk.Toplevel()

    ventana.title("Detector de Spam")

    ventana.geometry("650x500")

    ventana.configure(bg="#f4f6f9")

    def analizar():

        texto = txt_mensaje.get("1.0", tk.END).strip()

        if texto == "":
            return

        texto_transformado = vectorizador.transform([texto])

        resultado = modelo_spam.predict(
            texto_transformado
        )[0]

        lbl_resultado.config(
            text=f"Resultado: {resultado}"
        )

        historial.insert(
            tk.END,
            f"{texto[:40]} -> {resultado}"
        )

    titulo = tk.Label(
        ventana,
        text="📧 DETECTOR DE SPAM",
        font=("Arial", 18, "bold"),
        bg="#f4f6f9"
    )

    titulo.pack(pady=15)

    tk.Label(
        ventana,
        text="Escriba un mensaje:",
        bg="#f4f6f9"
    ).pack()

    txt_mensaje = tk.Text(
        ventana,
        width=50,
        height=6
    )

    txt_mensaje.pack(pady=10)

    tk.Button(
        ventana,
        text="Analizar",
        width=15,
        command=analizar
    ).pack()

    lbl_resultado = tk.Label(
        ventana,
        text="",
        font=("Arial", 14, "bold"),
        bg="#f4f6f9"
    )

    lbl_resultado.pack(pady=15)

    tk.Label(
        ventana,
        text="Historial",
        font=("Arial", 12, "bold"),
        bg="#f4f6f9"
    ).pack()

    historial = tk.Listbox(
        ventana,
        width=60,
        height=10
    )

    historial.pack(pady=10)


# =====================================
# VENTANA PRINCIPAL
# =====================================

root = tk.Tk()

root.title("Centro de IA")

root.geometry("500x400")

root.configure(bg="#e8eef5")

titulo = tk.Label(
    root,
    text="🤖 CENTRO DE IA",
    font=("Arial", 24, "bold"),
    bg="#e8eef5"
)

titulo.pack(pady=30)

tk.Button(
    root,
    text="🏠 Predicción de Casas",
    font=("Arial", 14),
    width=25,
    height=2,
    command=abrir_casas
).pack(pady=15)

tk.Button(
    root,
    text="📧 Detector de Spam",
    font=("Arial", 14),
    width=25,
    height=2,
    command=abrir_spam
).pack(pady=15)

tk.Label(
    root,
    text="Aplicación de Machine Learning",
    font=("Arial", 10),
    bg="#e8eef5"
).pack(side="bottom", pady=20)

root.mainloop()