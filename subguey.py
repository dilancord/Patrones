import tkinter as tk
from tkinter import ttk, messagebox
# patrón Decorator Subguey


#Objeto o como Interface que define la estructura minina del componente seria Icomponent
class ISandwich:
    def obtener_descripcion(self):
        pass
    
    def obtener_precio(self):
        pass





# Implementación básica de sándwich, que seria ConcretComponent
class SandwichBasico(ISandwich):
    def __init__(self, tipo_sandwich, tamano):
        self.tipo = tipo_sandwich
        self.tamano = tamano
        self.precios_15cm = {
            "Pavo": 12, "Italiano": 9, "Beef": 10, 
            "Veggie": 8, "Atún": 11, "Pollo": 12
        }
        self.precios_30cm = {
            "Pavo": 18, "Italiano": 16, "Beef": 16, 
            "Veggie": 14, "Atún": 17, "Pollo": 18
        }
    
    def obtener_descripcion(self):
        return f"{self.tipo} de {self.tamano} cm"
    
    def obtener_precio(self):
        if self.tamano == 15:
            return self.precios_15cm.get(self.tipo, 0)
        else:
            return self.precios_30cm.get(self.tipo, 0)

# Clase abstracta para decoradores 
class AdicionalDecorador(ISandwich):
    def __init__(self, sandwich, tipo_adicional):
        self.sandwich = sandwich
        self.tipo_adicional = tipo_adicional
        self.precios = {
            "Aguacate": {15: 1.5, 30: 2.5},
            "Doble proteína": {15: 4.5, 30: 8},
            "Hongos": {15: 0.85, 30: 1.45},
            "Refresco": {15: 1, 30: 1},
            "Sopa": {15: 4.2, 30: 4.2},
            "Postre": {15: 3.5, 30: 3.5},
            
        }
    
    def obtener_descripcion(self):
        return f"{self.sandwich.obtener_descripcion()} + {self.tipo_adicional}"
    
    def obtener_precio(self):
        tamano = self.sandwich.tamano if hasattr(self.sandwich, 'tamano') else 15
        precio_adicional = self.precios.get(self.tipo_adicional, {}).get(tamano, 0)
        return self.sandwich.obtener_precio() + precio_adicional

# Decoradores especificos
class AguacateDecorador(AdicionalDecorador):
    def __init__(self, sandwich):
        super().__init__(sandwich, "Aguacate")

class DobleProteinaDecorador(AdicionalDecorador):
    def __init__(self, sandwich):
        super().__init__(sandwich, "Doble proteína")
        
class HongosDecorador(AdicionalDecorador):
    def __init__(self, sandwich):
        super().__init__(sandwich, "Hongos")
class RefrescoDecorador(AdicionalDecorador):
    def __init__(self, sandwich):
        super().__init__(sandwich, "Refresco")
class SopaDecorador(AdicionalDecorador):
    def __init__(self, sandwich):
        super().__init__(sandwich, "Sopa")
class PostreDecorador(AdicionalDecorador):
    def __init__(self, sandwich):
        super().__init__(sandwich, "Postre")


# Clase principal de la aplicación
class AplicacionSandwich:
    def __init__(self, root):
        self.root = root
        self.root.title("Subguey")
        #definir color ventana
        self.root.configure(bg="#266820")
        
        self.orden_actual = []
        self.sandwich_actual = None
        self.adicionales_actuales = []
        
        self.crear_widgets()
    
    def crear_widgets(self):
        # Frame selección de sándwich
        frame_sandwich = ttk.LabelFrame(self.root, text="Seleccione su sándwich")
        frame_sandwich.pack(padx=10, pady=5, fill="x")
        
        ttk.Label(frame_sandwich, text="Tipo:").grid(row=0, column=0, padx=5, pady=5)
        self.tipo_sandwich = ttk.Combobox(frame_sandwich, values=[
            "Pavo", "Italiano", "Beef", "Veggie", "Atún", "Pollo"
        ], state="readonly")
        self.tipo_sandwich.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame_sandwich, text="Tamaño:").grid(row=0, column=2, padx=5, pady=5)
        self.tamano_sandwich = ttk.Combobox(frame_sandwich, values=[15, 30], state="readonly")
        self.tamano_sandwich.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Button(frame_sandwich, text="Crear Sándwich", 
                  command=self.crear_sandwich).grid(row=0, column=4, padx=5, pady=5)
        
        # Frame adicionales
        frame_adicionales = ttk.LabelFrame(self.root, text="Agregar adicionales")
        frame_adicionales.pack(padx=10, pady=5, fill="x")
        
        self.var_adicionales = tk.StringVar(value=[
            "Aguacate", "Doble proteína", "Hongos", "Refresco", "Sopa", "Postre"
        ])
        self.lista_adicionales = tk.Listbox(frame_adicionales, listvariable=self.var_adicionales, 
                                        selectmode="multiple", height=6)
        self.lista_adicionales.pack(padx=5, pady=5, fill="x")
        
        ttk.Button(frame_adicionales, text="Agregar Adicionales Seleccionados", 
                  command=self.agregar_adicionales).pack(padx=5, pady=5)
        
        # Frame orden actual
        frame_orden = ttk.LabelFrame(self.root, text="Orden Actual")
        frame_orden.pack(padx=10, pady=5, fill="both", expand=True)
        
        self.texto_orden = tk.Text(frame_orden, height=10, state="disabled")
        self.texto_orden.pack(padx=5, pady=5, fill="both", expand=True)
        
        # Botones finales
        frame_botones = ttk.Frame(self.root)
        frame_botones.pack(padx=10, pady=5, fill="x")
        
        ttk.Button(frame_botones, text="Agregar a Orden", command=self.agregar_a_orden).pack(side="left", padx=5)
        ttk.Button(frame_botones, text="Finalizar Orden", command=self.finalizar_orden).pack(side="right", padx=5)
        ttk.Button(frame_botones, text="Nuevo Sándwich", command=self.nuevo_sandwich).pack(side="right", padx=5)
    
    def crear_sandwich(self):
        tipo = self.tipo_sandwich.get()
        tamano = int(self.tamano_sandwich.get())
        
        if not tipo or not tamano:
            messagebox.showerror("Error", "Seleccione tipo y tamaño de sándwich")
            return
        
        self.sandwich_actual = SandwichBasico(tipo, tamano)
        self.adicionales_actuales = []
        self.actualizar_orden()
    
    def agregar_adicionales(self):
        if not self.sandwich_actual:
            messagebox.showerror("Error", "Primero cree un sándwich")
            return
        
        seleccionados = [self.lista_adicionales.get(i) for i in self.lista_adicionales.curselection()]
        
        for adicional in seleccionados:
            self.sandwich_actual = AdicionalDecorador(self.sandwich_actual, adicional)
            self.adicionales_actuales.append(adicional)
        
        self.actualizar_orden()
    
    def actualizar_orden(self):
        self.texto_orden.config(state="normal")
        self.texto_orden.delete(1.0, tk.END)
        
        if self.sandwich_actual:
            desc = self.sandwich_actual.obtener_descripcion()
            precio = self.sandwich_actual.obtener_precio()
            self.texto_orden.insert(tk.END, f"{desc} PRECIO: ${precio:.2f}\n\n")
        
        self.texto_orden.insert(tk.END, "Orden completa:\n")
        self.texto_orden.insert(tk.END, "="*50 + "\n")
        
        total = 0
        for item in self.orden_actual:
            self.texto_orden.insert(tk.END, f"{item.obtener_descripcion()} PRECIO: ${item.obtener_precio():.2f}\n")
            total += item.obtener_precio()
        
        if self.orden_actual:
            self.texto_orden.insert(tk.END, "="*50 + "\n")
            self.texto_orden.insert(tk.END, f"TOTAL PARCIAL: ${total:.2f}\n")
        
        self.texto_orden.config(state="disabled")
    
    def agregar_a_orden(self):
        if not self.sandwich_actual:
            messagebox.showerror("Error", "No hay sándwich para agregar")
            return
        
        self.orden_actual.append(self.sandwich_actual)
        self.sandwich_actual = None
        self.adicionales_actuales = []
        self.actualizar_orden()
    
    def nuevo_sandwich(self):
        self.sandwich_actual = None
        self.adicionales_actuales = []
        self.actualizar_orden()
    
    def finalizar_orden(self):
        if not self.orden_actual:
            messagebox.showerror("Error", "La orden está vacía")
            return
        
        recibo = "="*50 + "\n"
        total = 0
        
        for item in self.orden_actual:
            recibo += f"{item.obtener_descripcion()} PRECIO: ${item.obtener_precio():.2f}\n"
            total += item.obtener_precio()
        
        recibo += "="*50 + "\n"
        recibo += f"TOTAL: ${total:.2f}\n"
        recibo += "="*50
        
        messagebox.showinfo("Recibo Final", recibo)
        self.orden_actual = []
        self.actualizar_orden()

# Iniciar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionSandwich(root)
    root.mainloop()
