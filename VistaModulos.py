import customtkinter as ctk

class VistaModulos():
    def __init__(self, verFrameModulos):
       
        # Colores y estilos
        self.colors = {
            "fondo": "#FFFFFF",
            "borde": "#E0E0E0",
            "texto": "#333333",
            "descripcion": "#666666",
            "stock": "#CC4444",
            "precio": "#1A73E8",
            "boton": "#4CAF50",
            "boton_hover": "#45A049",
            "borde_hover": "#1A73E8",
        }
        self.Ventana = verFrameModulos
        
        # Configuración Ventana
        self.Ventana.title("Vista Modulos")  
        self.Ventana.columnconfigure((0,1,2), weight=0)  # Corrección de "weigth"
        self.Ventana.rowconfigure((0,1,2), weight=0)  
        self.Ventana.geometry(None)
        self.Ventana.resizable(False, False)
        # Frames de modulos
        self.Frame_Modulos(4, 2)  

    def Frame_Modulos(self, columnas, filas):
       for i in range(filas):
          for j in range(columnas):
                frame_modulo = ctk.CTkFrame(
                    master=self.Ventana,
                    corner_radius=20
                )
                frame_modulo.configure(width=80, height=100)
                frame_modulo.grid(row= i, column= j, padx=10, pady=10)  # Corrección de posicionamiento
                
               
if __name__ == "__main__":
    root = ctk.CTk() 
    app = VistaModulos(root)
    root.mainloop()