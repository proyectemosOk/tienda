import tkinter as tk
import customtkinter as ctk

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("400x300")

# Usamos un Canvas tradicional de tkinter (más flexible para gráficos)
canvas = tk.Canvas(app, width=400, height=300, highlightthickness=0, bg="#f0f0f0")
canvas.pack(fill="both", expand=True)

# Dibujamos una "sombra" como un rectángulo gris claro
shadow = canvas.create_rectangle(103, 103, 303, 203, fill="#c0c0c0", outline="")

# Luego colocamos un CTkFrame justo encima de la sombra
frame = ctk.CTkFrame(master=canvas, width=200, height=100, corner_radius=15, fg_color="#ffffff")
# Agregamos el frame al canvas como ventana
canvas.create_window(100, 100, anchor="nw", window=frame)

app.mainloop()
