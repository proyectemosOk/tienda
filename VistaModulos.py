import customtkinter as ctk

class VistaModulos():
    def __init__(self, verFrameModulos):
       
        # Colores y estilos
        self.colors = {
            "Fondo": "#FFFFFF",
            "FondoResalto": "#4C7EC1",
            "BordeResalto": "#04376B",
            "Borde": "#E0E0E0",
            "Texto": "#333333",
            "TextoResalto": "#FFFFFF"
        }
        # Etiquetas 
        self.Etiquetas = [
            "Ventas",
            "Inventario",
            "Gastos",
            "####",
            "####",
            "####",
            "####",
            "####"
        ]
        self.Ventana = verFrameModulos
        
        # Configuración Ventana
        self.Ventana.title("Vista Modulos")  
        self.Ventana.columnconfigure((0,1,2), weight = 1)   
        self.Ventana.rowconfigure((0,1,2), weight = 1)  
        self.Ventana.geometry(None)
        self.Ventana.resizable(False, False)
        # Frames de modulos
        self.Frames = []
        self.Frame_Modulos(4, 2) 
 

    def Frame_Modulos(self, columnas, filas):
       index = 0
       for i in range(filas):
          for j in range(columnas):
                frame_modulo = ctk.CTkFrame(
                    master=self.Ventana,
                    corner_radius = 90,
                    fg_color = self.colors["Fondo"],
                    border_color = self.colors["Borde"],
                    border_width = 1
                )
                Etiqueta = self.AsignarEtiquetas(frame_modulo, self.Etiquetas[index])
                frame_modulo.configure(width = 200, height = 200)
                frame_modulo.grid(row= i, column= j, padx=10, pady=10)  # Corrección de posicionamiento
                self.Frames.append((frame_modulo, Etiqueta)) 
                frame_modulo.bind("<Enter>", lambda event, idx = index: self.Resalto(idx) )
                frame_modulo.bind("<Leave>", lambda event, idx = index: self.QuitarResalto(idx))
                index += 1 
    # Asignar Etiquetas Frames
    def AsignarEtiquetas(self, frame, texto):
        Etiqueta = ctk.CTkLabel(master = frame, text = texto, text_color = self.colors["Texto"], font = ("Arial", 12 ) )
        Etiqueta.place(relx = 0.5, rely = 0.9, anchor = "s")
        return Etiqueta
    # Resaltar el frame con evento 
    def Resalto(self, index):
        frame, Etiqueta = self.Frames[index]
        frame.configure(cursor = "hand2")
        frame.configure(fg_color = self.colors["FondoResalto"], 
                        border_color = self.colors["BordeResalto"],
                        )
        Etiqueta.configure(text_color=self.colors["TextoResalto"])
    def QuitarResalto(self, index):
        frame, Etiqueta = self.Frames[index]
        frame.configure(cursor = "")
        frame.configure(fg_color = self.colors["Fondo"],
                        border_color = self.colors["Borde"],
                        )
        Etiqueta.configure(text_color = self.colors["Texto"])               
if __name__ == "__main__":
    root = ctk.CTk() 
    app = VistaModulos(root)
    root.mainloop()