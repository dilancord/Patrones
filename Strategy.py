import tkinter as tk
from tkinter import messagebox
import random
import os  # rutas de archivo


# Clases de Lógica

class Golpe:
    def __init__(self, nombre, poder, efecto_curacion=0, daño_extra=0):
        self.nombre = nombre
        self.poder = poder  # Daño base
        self.efecto_curacion = efecto_curacion  # Cantidad para curar
        self.daño_extra = daño_extra  # Daño extra

    def aplicar_efecto(self, atacante, oponente):
        daño_infligido = self.poder + self.daño_extra
        oponente.vida -= daño_infligido
        atacante.vida += self.efecto_curacion

        # Devolver información para el registro
        partes_registro = []
        partes_registro.append(
            {"texto": f"{atacante.nombre} usa {self.nombre} en {oponente.nombre}, infligiendo ", "etiqueta": None})
        partes_registro.append({"texto": f"{daño_infligido} de daño.", "etiqueta": "daño_rojo"})

        if self.efecto_curacion > 0:
            partes_registro.append({"texto": f" {atacante.nombre} se cura por ", "etiqueta": None})
            partes_registro.append({"texto": f"{self.efecto_curacion}.", "etiqueta": "curacion_verde"})
        if self.daño_extra > 0:
            partes_registro.append(
                {"texto": f" (¡Se aplicó {self.daño_extra} de daño extra!)", "etiqueta": "daño_extra_naranja"})

        return partes_registro


class ArteMarcial:
    def __init__(self, nombre, golpes):
        self.nombre = nombre
        self.golpes = golpes  # Lista de objetos Golpe

    def obtener_golpes_aleatorios(self, num_golpes):
        if len(self.golpes) < num_golpes:
            return random.sample(self.golpes, len(self.golpes))
        return random.sample(self.golpes, num_golpes)

    def __str__(self):
        return self.nombre



class Taekwondo(ArteMarcial):
    def __init__(self):
        super().__init__("Taekwondo", [
            Golpe("Dollyo Chagi", 20),
            Golpe("Ap Chagi", 10),
            Golpe("Yop Chagi", 35, daño_extra=5)
        ])


class Wushu(ArteMarcial):
    def __init__(self):
        super().__init__("Wushu", [
            Golpe("Patada de Tornado", 15),
            Golpe("Puño Directo", 10),
            Golpe("Barrido de Dragón", 25, efecto_curacion=5)
        ])


class Sumo(ArteMarcial):
    def __init__(self):
        super().__init__("Sumo", [
            Golpe("Oshi-dashi", 25),
            Golpe("Kimedashi", 35),
            Golpe("Yorikiri", 40, daño_extra=10)
        ])


class KungFu(ArteMarcial):
    def __init__(self):
        super().__init__("Kung Fu", [
            Golpe("Ch'ien", 10),
            Golpe("Kuan Tsu", 22, efecto_curacion=5, daño_extra=5),
            Golpe("Pai Tsu", 40)
        ])


class Aikido(ArteMarcial):
    def __init__(self):
        super().__init__("Aikido", [
            Golpe("Irimi Nage", 12),
            Golpe("Kote Gaeshi", 18),
            Golpe("Tenkan", 8, efecto_curacion=15)
        ])


class Sambo(ArteMarcial):
    def __init__(self):
        super().__init__("Sambo", [
            Golpe("Agarre de Brazo", 15),
            Golpe("Lanzamiento de Cadera", 25),
            Golpe("Bloqueo de Pierna", 30)
        ])


class Judo(ArteMarcial):
    def __init__(self):
        super().__init__("Judo", [
            Golpe("Tai-Otoshi", 8),
            Golpe("Koshi-guruma", 18),
            Golpe("O-soto-gari", 13)
        ])


class Boxeo(ArteMarcial):
    def __init__(self):
        super().__init__("Boxeo", [
            Golpe("Jab", 5),
            Golpe("Gancho", 15),
            Golpe("Uppercut", 40)
        ])


class Karate(ArteMarcial):
    def __init__(self):
        super().__init__("Karate", [
            Golpe("Mae Geri", 10),
            Golpe("Yoko Geri", 25, efecto_curacion=10),
            Golpe("Mawashi Geri", 30)
        ])


class Capoeira(ArteMarcial):
    def __init__(self):
        super().__init__("Capoeira", [
            Golpe("Armada", 10),
            Golpe("Martillo", 28),
            Golpe("Ponteira", 13, daño_extra=5)
        ])


class Iaido(ArteMarcial):
    def __init__(self):
        super().__init__("Iaido", [
            Golpe("Nukitsuke", 20),
            Golpe("Kirioroshi", 45),
            Golpe("Chiburui", 10, daño_extra=15)
        ])


class BitacoraAtaques:
    def __init__(self):
        self.entradas = []

    def añadir_entrada(self, partes):
        self.entradas.append(partes)
        if len(self.entradas) > 15:
            self.entradas.pop(0)

    def obtener_partes_registro(self):
        return self.entradas


class Jugador:
    def __init__(self, nombre, todas_artes_marciales):
        self.nombre = nombre
        self.vida = 200
        self.todas_artes_marciales = todas_artes_marciales
        self.artes_marciales_actuales = []
        self.bitacora_ataques = BitacoraAtaques()
        self.arte_marcial_seleccionada = None
        self.golpes_combo_actual = []

        self.re_asignar_artes_marciales()

    def re_asignar_artes_marciales(self):
        self.artes_marciales_actuales = random.sample(self.todas_artes_marciales, 3)
        self.arte_marcial_seleccionada = None
        self.golpes_combo_actual = []

    def generar_combo(self, arte_marcial):
        num_golpes = random.randint(3, 6)
        self.golpes_combo_actual = arte_marcial.obtener_golpes_aleatorios(num_golpes)
        nombres_combo = [golpe.nombre for golpe in self.golpes_combo_actual]
        return f"{arte_marcial.nombre} -- {' + '.join(nombres_combo)}"

    def realizar_ataque(self, oponente):
        if not self.golpes_combo_actual:
            return [{"texto": "No se generó ningún combo.Genere un combo primero.", "etiqueta": None}]

        daño_total_este_turno = 0

        for golpe in self.golpes_combo_actual:
            partes_efecto = golpe.aplicar_efecto(self, oponente)
            daño_total_este_turno += (golpe.poder + golpe.daño_extra)
            self.bitacora_ataques.añadir_entrada(partes_efecto)

        partes_resumen = []
        partes_resumen.append(
            {"texto": f"{self.arte_marcial_seleccionada.nombre if self.arte_marcial_seleccionada else 'Aleatorio'}: "
                      f"{' + '.join([g.nombre for g in self.golpes_combo_actual])} -> Daño Total: ", "etiqueta": None})
        partes_resumen.append({"texto": f"{daño_total_este_turno}", "etiqueta": "daño_rojo"})

        partes_resumen.append({"texto": f" (Vida de {oponente.nombre}: ", "etiqueta": None})
        partes_resumen.append({"texto": f"{max(0, oponente.vida)}",
                               "etiqueta": "vida_jugador2" if oponente.nombre == "Jugador 2" else "vida_jugador1"})
        partes_resumen.append({"texto": f", Vida de {self.nombre}: ", "etiqueta": None})
        partes_resumen.append({"texto": f"{max(0, self.vida)})",
                               "etiqueta": "vida_jugador1" if self.nombre == "Jugador 1" else "vida_jugador2"})

        self.bitacora_ataques.añadir_entrada(partes_resumen)
        self.golpes_combo_actual = []
        return partes_resumen

    # GUI con Tkinter


class JuegoArtesMarcialesGUI:
    def __init__(self, master):
        self.master = master
        master.title("Batalla de Artes Marciales")

        # tamaño mínimo para la ventana
        master.minsize(width=900, height=700)

        self.todas_artes_marciales = [
            Taekwondo(), Wushu(), Sumo(), KungFu(), Aikido(),
            Sambo(), Judo(), Boxeo(), Karate(), Capoeira(), Iaido()
        ]
        self.jugador1 = Jugador("Jugador 1", self.todas_artes_marciales)
        self.jugador2 = Jugador("Jugador 2", self.todas_artes_marciales)
        self.turno_jugador_actual = self.jugador1

        master.configure(bg="#F0F0F0")
        self.fuente_grande = ("Arial", 16, "bold")
        self.fuente_mediana = ("Arial", 12, "bold")
        self.fuente_pequeña = ("Arial", 10)

        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=0)
        master.grid_columnconfigure(2, weight=1)
        master.grid_rowconfigure(0, weight=1)
        master.grid_rowconfigure(1, weight=1)

        self.marco_jugador1 = tk.LabelFrame(master, text="Jugador 1", bg="#D4E6F1", padx=10, pady=10, bd=2,
                                            relief="groove", font=self.fuente_grande)
        self.marco_jugador1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.configurar_gui_jugador(self.marco_jugador1, self.jugador1, num_jugador=1)

        self.marco_central = tk.Frame(master, bg="#F0F0F0", padx=10, pady=10)
        self.marco_central.grid(row=0, column=1, padx=5, pady=10, sticky="ns")

        self.boton_atacar_central = tk.Button(self.marco_central, text="Atacarse", command=self.procesar_turno_ataque,
                                              bg="#E74C3C", fg="white", font=self.fuente_mediana, width=10, height=2)
        self.boton_atacar_central.pack(pady=10)

        self.boton_reasignar_j1 = tk.Button(self.marco_central, text="J1 Re Asignar",
                                            command=lambda: self.reasignar_y_actualizar(self.jugador1), bg="#F39C12",
                                            fg="white", font=self.fuente_mediana, width=15)
        self.boton_reasignar_j1.pack(pady=5)

        self.boton_reasignar_j2 = tk.Button(self.marco_central, text="J2 Re Asignar",
                                            command=lambda: self.reasignar_y_actualizar(self.jugador2), bg="#F39C12",
                                            fg="white", font=self.fuente_mediana, width=15)
        self.boton_reasignar_j2.pack(pady=5)

        self.marco_jugador2 = tk.LabelFrame(master, text="Jugador 2", bg="#D4F1E6", padx=10, pady=10, bd=2,
                                            relief="groove", font=self.fuente_grande)
        self.marco_jugador2.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        self.configurar_gui_jugador(self.marco_jugador2, self.jugador2, num_jugador=2)

        self.marco_registro_j1 = tk.LabelFrame(master, text="Bitácora Jugador 1", bg="#F8F9F9", padx=5, pady=5, bd=1,
                                               relief="solid")
        self.marco_registro_j1.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        self.texto_registro_j1 = tk.Text(self.marco_registro_j1, height=8, width=40, font=self.fuente_pequeña,
                                         state='disabled')
        self.texto_registro_j1.pack(expand=True, fill="both")
        self.definir_etiquetas_texto(self.texto_registro_j1)

        self.marco_registro_j2 = tk.LabelFrame(master, text="Bitácora Jugador 2", bg="#F8F9F9", padx=5, pady=5, bd=1,
                                               relief="solid")
        self.marco_registro_j2.grid(row=1, column=2, padx=10, pady=5, sticky="nsew")
        self.texto_registro_j2 = tk.Text(self.marco_registro_j2, height=8, width=40, font=self.fuente_pequeña,
                                         state='disabled')
        self.texto_registro_j2.pack(expand=True, fill="both")
        self.definir_etiquetas_texto(self.texto_registro_j2)

        self.actualizar_gui()
        self.establecer_controles_jugador_activo()

    def definir_etiquetas_texto(self, widget_texto):
        widget_texto.tag_configure("daño_rojo", foreground="red", font=("Arial", 10, "bold"))
        widget_texto.tag_configure("curacion_verde", foreground="green", font=("Arial", 10, "bold"))
        widget_texto.tag_configure("daño_extra_naranja", foreground="orange", font=("Arial", 10, "italic"))
        widget_texto.tag_configure("vida_jugador1", foreground="blue", font=("Arial", 10, "bold"))
        widget_texto.tag_configure("vida_jugador2", foreground="red", font=("Arial", 10, "bold"))

    def configurar_gui_jugador(self, marco_padre, jugador, num_jugador):
        etiqueta_vida = tk.Label(marco_padre, text=f"Vida: {jugador.vida}/200", bg=marco_padre['bg'],
                                 font=self.fuente_mediana)
        etiqueta_vida.pack(pady=5)
        setattr(self, f'etiqueta_vida_j{num_jugador}', etiqueta_vida)

        marco_botones_arte = tk.Frame(marco_padre, bg=marco_padre['bg'])
        marco_botones_arte.pack(pady=10)
        setattr(self, f'marco_botones_arte_j{num_jugador}', marco_botones_arte)

        etiqueta_info_arte = tk.Label(marco_padre, text="Arte marcial seleccionado para ataque", bg="#F0F0F0",
                                      relief="sunken", font=self.fuente_pequeña)
        etiqueta_info_arte.pack(pady=10)
        setattr(self, f'etiqueta_info_arte_j{num_jugador}', etiqueta_info_arte)  # Renombré el atributo

        if num_jugador == 1:
            boton_generar_combo = tk.Button(marco_padre, text="Generar combo de 3-6 golpes",
                                            command=lambda: self.generar_combo_j1(), bg="#3498DB", fg="white",
                                            font=self.fuente_pequeña)
            boton_generar_combo.pack(pady=5)
            setattr(self, f'boton_generar_combo_j{num_jugador}', boton_generar_combo)

            self.mostrar_combo_j1 = tk.Label(marco_padre, text="Combo: ", bg=marco_padre['bg'],
                                             font=self.fuente_pequeña, wraplength=250)
            self.mostrar_combo_j1.pack(pady=2)

            boton_atacar = tk.Button(marco_padre, text="Atacar", command=lambda: self.atacar_j1(), bg="#2ECC71",
                                     fg="white", font=self.fuente_mediana)
            boton_atacar.pack(pady=5)
            setattr(self, f'boton_atacar_j{num_jugador}', boton_atacar)

        else:
            self.mostrar_combo_j2 = tk.Label(marco_padre, text="Combo J2: ", bg=marco_padre['bg'],
                                             font=self.fuente_pequeña, wraplength=250)
            self.mostrar_combo_j2.pack(pady=2)

            boton_atacar = tk.Button(marco_padre, text="Atacar (Aleatorio)", command=lambda: self.atacar_j2(),
                                     bg="#2ECC71", fg="white", font=self.fuente_mediana)
            boton_atacar.pack(pady=5)
            setattr(self, f'boton_atacar_j{num_jugador}', boton_atacar)

        boton_actualizar = tk.Button(marco_padre, text="Actualizar vidas y golpes", command=self.actualizar_gui,
                                     bg="#9B59B6", fg="white", font=self.fuente_pequeña)
        boton_actualizar.pack(pady=5)

        self.actualizar_botones_arte(jugador, num_jugador)

    def actualizar_botones_arte(self, jugador, num_jugador):
        marco_botones_arte = getattr(self, f'marco_botones_arte_j{num_jugador}')
        for widget in marco_botones_arte.winfo_children():
            widget.destroy()

        for i, arte in enumerate(jugador.artes_marciales_actuales):
            if num_jugador == 1:
                btn = tk.Button(marco_botones_arte, text=arte.nombre,
                                command=lambda a=arte: self.seleccionar_arte_marcial_j1(a),
                                bg="#5DADE2", fg="white", font=self.fuente_pequeña, width=12)
            else:
                btn = tk.Label(marco_botones_arte, text=arte.nombre, bg="#AED6F1", fg="black", font=self.fuente_pequeña,
                               width=12, relief="ridge")
            btn.grid(row=0, column=i, padx=2, pady=2)

    def actualizar_gui(self):
        self.etiqueta_vida_j1.config(text=f"Vida: {max(0, self.jugador1.vida)}/200")
        self.etiqueta_vida_j2.config(text=f"Vida: {max(0, self.jugador2.vida)}/200")

        self._actualizar_widget_texto_registro(self.texto_registro_j1,
                                               self.jugador1.bitacora_ataques.obtener_partes_registro())
        self._actualizar_widget_texto_registro(self.texto_registro_j2,
                                               self.jugador2.bitacora_ataques.obtener_partes_registro())

        if self.jugador1.golpes_combo_actual:
            combo_str = "Combo J1: " + ' + '.join([g.nombre for g in self.jugador1.golpes_combo_actual])
            self.mostrar_combo_j1.config(text=combo_str)
        else:
            self.mostrar_combo_j1.config(text="Combo J1: (No hay combo generado)")

        if self.jugador2.golpes_combo_actual:
            combo_str = "Combo J2: " + ' + '.join([g.nombre for g in self.jugador2.golpes_combo_actual])
            self.mostrar_combo_j2.config(text=combo_str)
        else:
            self.mostrar_combo_j2.config(text="Combo J2: (No hay combo generado)")

        self.verificar_fin_juego()
        self.establecer_controles_jugador_activo()

    def _actualizar_widget_texto_registro(self, widget_texto, entradas_registro_partes):
        widget_texto.config(state='normal')
        widget_texto.delete('1.0', tk.END)

        for partes_entrada in entradas_registro_partes:
            for parte in partes_entrada:
                texto = parte["texto"]
                etiqueta = parte.get("etiqueta")
                if etiqueta:
                    widget_texto.insert(tk.END, texto, etiqueta)
                else:
                    widget_texto.insert(tk.END, texto)
            widget_texto.insert(tk.END, "\n")

        widget_texto.config(state='disabled')
        widget_texto.see(tk.END)

    def establecer_controles_jugador_activo(self):
        if self.turno_jugador_actual == self.jugador1:
            self.habilitar_controles_jugador(self.marco_jugador1, self.jugador1)
            self.deshabilitar_controles_jugador(self.marco_jugador2, self.jugador2)
            self.boton_reasignar_j1.config(state='normal')
            self.boton_reasignar_j2.config(state='disabled')
        else:
            self.habilitar_controles_jugador(self.marco_jugador2, self.jugador2)
            self.deshabilitar_controles_jugador(self.marco_jugador1, self.jugador1)
            self.boton_reasignar_j1.config(state='disabled')
            self.boton_reasignar_j2.config(state='normal')

        self.boton_atacar_central.config(state='normal')

    def habilitar_controles_jugador(self, marco, jugador):
        for widget in marco.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(state='normal')

        if jugador == self.jugador1:
            marco_botones_arte = getattr(self, 'marco_botones_arte_j1')
            for widget in marco_botones_arte.winfo_children():
                if isinstance(widget, tk.Button):
                    widget.config(state='normal')

            if not self.jugador1.golpes_combo_actual:
                self.boton_atacar_j1.config(state='disabled')
            if not self.jugador1.arte_marcial_seleccionada:
                self.boton_generar_combo_j1.config(state='disabled')
                # Actualiza la info de arte marcial
                self.etiqueta_info_arte_j1.config(text="Selecciona un arte marcial para ver su info")
            else:
                self.boton_generar_combo_j1.config(state='normal')
                # Da el nombre del arte marcial seleccionado
                self.etiqueta_info_arte_j1.config(
                    text=f"Arte seleccionado: {self.jugador1.arte_marcial_seleccionada.nombre}")

        if jugador == self.jugador2:
            self.boton_atacar_j2.config(state='normal')
            self.etiqueta_info_arte_j2.config(text="Arte marcial del ataque (se elige al atacar)")

    def deshabilitar_controles_jugador(self, marco, jugador):
        for widget in marco.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(state='disabled')

        if jugador == self.jugador1:
            marco_botones_arte = getattr(self, 'marco_botones_arte_j1')
            for widget in marco_botones_arte.winfo_children():
                if isinstance(widget, tk.Button):
                    widget.config(state='disabled')
            self.etiqueta_info_arte_j1.config(text="Arte marcial seleccionado para ataque")

        if jugador == self.jugador2:
            self.etiqueta_info_arte_j2.config(text="Arte marcial del ataque (se elige al atacar)")

    def seleccionar_arte_marcial_j1(self, arte_marcial):
        self.jugador1.arte_marcial_seleccionada = arte_marcial

        self.etiqueta_info_arte_j1.config(text=f"Arte seleccionado: {arte_marcial.nombre}")

        self.boton_generar_combo_j1.config(state='normal')
        self.boton_atacar_j1.config(state='disabled')
        self.mostrar_combo_j1.config(text="Combo J1: (Generar para atacar)")

    def generar_combo_j1(self):
        if not self.jugador1.arte_marcial_seleccionada:
            messagebox.showwarning("Error", "Jugador 1: Por favor, selecciona un arte marcial primero.")
            return

        info_combo = self.jugador1.generar_combo(self.jugador1.arte_marcial_seleccionada)
        self.mostrar_combo_j1.config(text=info_combo)
        self.boton_atacar_j1.config(state='normal')
        messagebox.showinfo("Combo Generado", f"Jugador 1: {info_combo}")

    def atacar_j1(self):
        if not self.jugador1.golpes_combo_actual:
            messagebox.showwarning("Error", "Jugador 1: Por favor, genera un combo antes de atacar.")
            return

        partes_resumen_ataque = self.jugador1.realizar_ataque(self.jugador2)

        texto_resumen = "".join(parte["texto"] for parte in partes_resumen_ataque)
        messagebox.showinfo("Ataque del Jugador 1", texto_resumen)

        self.actualizar_gui()
        self.siguiente_turno()

    def atacar_j2(self):
        arte_aleatorio = random.choice(self.jugador2.artes_marciales_actuales)
        self.jugador2.arte_marcial_seleccionada = arte_aleatorio
        info_combo = self.jugador2.generar_combo(arte_aleatorio)
        self.mostrar_combo_j2.config(text=info_combo)

        self.etiqueta_info_arte_j2.config(text=f"Arte elegido: {arte_aleatorio.nombre}")

        partes_resumen_ataque = self.jugador2.realizar_ataque(self.jugador1)

        texto_resumen = "".join(parte["texto"] for parte in partes_resumen_ataque)
        messagebox.showinfo("Ataque del Jugador 2", texto_resumen)

        self.actualizar_gui()
        self.siguiente_turno()

    def reasignar_y_actualizar(self, jugador):
        jugador.re_asignar_artes_marciales()
        self.actualizar_botones_arte(jugador, 1 if jugador == self.jugador1 else 2)
        messagebox.showinfo("Reasignación", f"{jugador.nombre} ha reasignado sus artes marciales.")
        self.actualizar_gui()

        if jugador == self.jugador1:
            self.etiqueta_info_arte_j1.config(text="Arte marcial seleccionado para ataque")
        else:
            self.etiqueta_info_arte_j2.config(text="Arte marcial del ataque (se elige al atacar)")

    def procesar_turno_ataque(self):
        if self.turno_jugador_actual == self.jugador1:
            messagebox.showinfo("Turno",
                                "Turno del Jugador 1. Selecciona un arte marcial y genera un combo para atacar.")
        else:
            messagebox.showinfo("Turno",
                                "Turno del Jugador 2. Haz clic en 'Atacar (Aleatorio)' en el lado del Jugador 2.")

    def siguiente_turno(self):
        if self.turno_jugador_actual == self.jugador1:
            self.turno_jugador_actual = self.jugador2
            messagebox.showinfo("Turno", "¡Turno del Jugador 2!")
        else:
            self.turno_jugador_actual = self.jugador1
            messagebox.showinfo("Turno", "¡Turno del Jugador 1!")
        self.actualizar_gui()

    def verificar_fin_juego(self):
        if self.jugador1.vida <= 0:
            messagebox.showinfo("Juego Terminado",
                                f"¡{self.jugador2.nombre} Gana! {self.jugador1.nombre} ha sido derrotado.")
            self.master.destroy()
            return True
        if self.jugador2.vida <= 0:
            messagebox.showinfo("Juego Terminado",
                                f"¡{self.jugador1.nombre} Gana! {self.jugador2.nombre} ha sido derrotado.")
            self.master.destroy()
            return True
        return False


if __name__ == "__main__":
    root = tk.Tk()
    app = JuegoArtesMarcialesGUI(root)
    root.mainloop()