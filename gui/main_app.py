# gui/main_app.py
import tkinter as tk
from tkinter import ttk, messagebox

# Importás tu capa de dominio/datos:
from repository.contacto_repository import ContactoRepository
from services.db_services import init_schema

class ContactosApp(tk.Tk):
    """
    Ventana principal del ABM de contactos (Iteración 1: solo lectura).
    - Crea el esquema si no existe.
    - Muestra un Treeview con los contactos.
    - Deja ganchos (botones deshabilitados) para las siguientes iteraciones: Alta/Editar/Borrar.
    """

    def __init__(self):
        # Inicialización estándar de Tkinter:
        super().__init__()

        # --- Metadatos de ventana ---
        self.title("ABM de Contactos — Iteración 1")
        self.geometry("900x520")  # (ancho x alto) en píxeles
        self.minsize(820, 480)    # tamaño mínimo para que no se rompa el layout

        # --- Repositorio de datos ---
        # Instanciamos la capa de acceso a datos (CRUD). No recibe parámetros.
        self.repo = ContactoRepository()

        # --- Bootstrap de esquema ---
        # Ejecuta el DDL (CREATE TABLE IF NOT EXISTS ...) desde services.
        # Parámetros:
        #   schema_path (str, opcional): ruta al archivo .sql. Por defecto "database/schema.sql"
        try:
            init_schema()
        except Exception as e:
            # messagebox muestra un cuadro de error modal. parent=self lo ancla a esta ventana.
            messagebox.showerror("Error de base de datos", f"No se pudo inicializar el esquema.\n\n{e}", parent=self)
            # Si falla el esquema, no tiene sentido seguir.
            self.destroy()
            return

        # --- Estilos (opcionales) ---
        self._configurar_estilos()

        # --- Construcción de UI ---
        self._construir_barra_superior()
        self._construir_treeview()

        # --- Carga inicial de datos ---
        self._refrescar_grilla()

    # ---------------------------------------------------------------------
    # Estilos
    # ---------------------------------------------------------------------
    def _configurar_estilos(self):
        """
        Define estilos ttk para lograr una apariencia más prolija.
        No requiere parámetros. Modifica estilos globales del tema activo.
        """
        style = ttk.Style(self)

        # Intenta elegir un tema 'clam' (suele verse mejor que 'default' nativo)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        # Estilo para encabezados de Treeview
        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold"),
            padding=6
        )

        # Estilo para filas de Treeview
        style.configure(
            "Treeview",
            font=("Segoe UI", 10),
            rowheight=26
        )

        # Estilo para botones
        style.configure(
            "TButton",
            font=("Segoe UI", 10),
            padding=6
        )

        # Estilo para frames y labels
        style.configure(
            "TLabel",
            font=("Segoe UI", 10)
        )

    # ---------------------------------------------------------------------
    # Barra superior (botonera placeholder)
    # ---------------------------------------------------------------------
    def _construir_barra_superior(self):
        """
        Crea una barra con botones. En esta iteración los dejamos como placeholders
        o deshabilitados, y en la próxima iteración les daremos funcionalidad real.
        """
        barra = ttk.Frame(self, padding=(10, 10))
        barra.pack(fill=tk.X, side=tk.TOP)

        # Botón para refrescar la grilla:
        #   command=self._refrescar_grilla -> callback a ejecutar al click.
        btn_refrescar = ttk.Button(barra, text="Refrescar", command=self._refrescar_grilla)
        btn_refrescar.pack(side=tk.LEFT, padx=(0, 8))

        # Placeholders de próximas iteraciones:
        self.btn_alta = ttk.Button(barra, text="Nuevo contacto (próx. iteración)", state=tk.DISABLED)
        self.btn_alta.pack(side=tk.LEFT, padx=(0, 8))

        self.btn_editar = ttk.Button(barra, text="Editar (próx. iteración)", state=tk.DISABLED)
        self.btn_editar.pack(side=tk.LEFT, padx=(0, 8))

        self.btn_borrar = ttk.Button(barra, text="Borrar (próx. iteración)", state=tk.DISABLED)
        self.btn_borrar.pack(side=tk.LEFT, padx=(0, 8))

        # Espaciador flexible para “tirar” el siguiente label a la derecha
        barra.grid_columnconfigure(99, weight=1)

        # Un label informativo alineado a derecha
        lbl_info = ttk.Label(barra, text="Iteración 1: Listado en modo lectura")
        lbl_info.pack(side=tk.RIGHT)

    # ---------------------------------------------------------------------
    # Grilla (Treeview + Scrollbars)
    # ---------------------------------------------------------------------
    def _construir_treeview(self):
        """
        Construye el Treeview para mostrar contactos.
        - columns: tuplas con los identificadores lógicos de columnas.
        - show="headings": oculta la primera columna “#0” para usar solo nuestras columnas.
        - selectmode="browse": selección de a una fila.
        """
        contenedor = ttk.Frame(self, padding=(10, 0, 10, 10))
        contenedor.pack(fill=tk.BOTH, expand=True)

        columnas = ("id", "nombre", "apellido", "telefono", "email")
        self.tree = ttk.Treeview(
            contenedor,
            columns=columnas,
            show="headings",
            selectmode="browse"
        )

        # Configuración de encabezados y ancho de columnas
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("apellido", text="Apellido")
        self.tree.heading("telefono", text="Teléfono")
        self.tree.heading("email", text="Email")

        self.tree.column("id", width=60, anchor=tk.W, stretch=False)
        self.tree.column("nombre", width=160, anchor=tk.W)
        self.tree.column("apellido", width=160, anchor=tk.W)
        self.tree.column("telefono", width=160, anchor=tk.W)
        self.tree.column("email", width=240, anchor=tk.W)

        # Scrollbars vertical y horizontal
        vsb = ttk.Scrollbar(contenedor, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(contenedor, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # Layout: Treeview “grande” y scrollbars a los costados
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        # Que el tree se expanda con el contenedor
        contenedor.rowconfigure(0, weight=1)
        contenedor.columnconfigure(0, weight=1)

        # (Opcional) Evento de doble-click para inspección futura (edición)
        # En esta iteración no hace nada, solo está el hook
        self.tree.bind("<Double-1>", self._on_doble_click_row)

    # ---------------------------------------------------------------------
    # Cargar/Refrescar datos
    # ---------------------------------------------------------------------
    def _refrescar_grilla(self):
        """
        Borra todas las filas de la grilla y vuelve a llenar desde la base.
        No recibe parámetros, usa self.repo.listar() (que no recibe argumentos).
        """
        # Limpiar filas actuales
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            contactos = self.repo.listar()  # List[Contacto]
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron leer los contactos.\n\n{e}", parent=self)
            return

        # Insertar fila por fila
        for c in contactos:
            # values: deben estar en el mismo orden que las columnas declaradas
            self.tree.insert("", tk.END, values=(c.id, c.nombre, c.apellido, c.telefono, c.email))

    # ---------------------------------------------------------------------
    # Hooks / Eventos
    # ---------------------------------------------------------------------
    def _on_doble_click_row(self, event):
        """
        Hook de doble click sobre una fila.
        Próxima iteración: abrir diálogo de Edición con los datos seleccionados.
        """
        seleccion = self.tree.selection()
        if not seleccion:
            return
        item_id = seleccion[0]
        fila = self.tree.item(item_id, "values")  # tupla (id, nombre, apellido, telefono, email)
        # Por ahora solo informativo:
        messagebox.showinfo("Fila seleccionada", f"Seleccionaste ID={fila[0]} — {fila[1]} {fila[2]}", parent=self)

# -------------------------------------------------------------------------
# Entry point
# -------------------------------------------------------------------------
if __name__ == "__main__":
    app = ContactosApp()
    app.mainloop()
