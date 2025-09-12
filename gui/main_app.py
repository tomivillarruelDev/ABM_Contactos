import tkinter as tk

# Crear ventana principal
root = tk.Tk()
root.title("Mi primera ventana")
root.geometry("300x200")  # ancho x alto

# Etiqueta de texto
label = tk.Label(root, text="Hola, Tkinter!")
label.pack(pady=20)  # se coloca en la ventana

# Botón
def saludar():
    label.config(text="¡Hola desde el botón!")

btn = tk.Button(root, text="Saludar", command=saludar)
btn.pack()

# Iniciar loop de la app
root.mainloop()
