# gui/main_app.py
import tkinter as tk
from tkinter import ttk, messagebox

# Capa de datos / dominio
from repository.contacto_repository import ContactoRepository
from services.db_services import init_schema


class ContactosApp(tk.Tk):
    """
    Ventana principal del ABM de contactos.
    - Inicializa el esquema de BD (CREATE TABLE IF NOT EXISTS...).
    - Muestra un Treeview con los contactos.
    - Permite Alta, Edición y Borrado (vía ContactoRepository).
    """

    def __init__(self):
        super().__init__()

        # --- Metadatos de ventana ---
        self.title("ABM de Contactos")
        self.geometry("900x520")   # ancho x alto
        self.minsize(820, 480)

        # --- Repositorio de datos (CRUD) ---
        # No recibe parámetros; gestiona la conexión internamente.
        self.repo = ContactoRepository()

        # --- Inicialización de esquema ---
        try:
            # Ejecuta el DDL de schema.sql (ruta resuelta adentro de services).
            init_schema()
        except Exception as e:
            messagebox.showerror(
                "Error de base de datos",
                f"No se pudo inicializar el esquema.\n\n{e}",
                parent=self
            )
            self.destroy()
            return

        # --- Estilos (opcional) ---
        self._configurar_estilos()

        # --- Construcción de UI ---
        self._construir_barra_superior()   # crea los botones
        self._construir_treeview()         # crea la grilla + scrollbars

        # Estado inicial de botones (sin selección)
        self._set_btn_states(False)

        # --- Carga inicial de datos ---
        self._refrescar_grilla()

    # ---------------------------------------------------------------------
    # Estilos
    # ---------------------------------------------------------------------
    def _configurar_estilos(self):
        """Define estilos ttk para una apariencia más prolija."""
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), padding=6)
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=26)
        style.configure("TButton", font=("Segoe UI", 10), padding=6)
        style.configure("TLabel", font=("Segoe UI", 10))

    # ---------------------------------------------------------------------
    # Barra superior (botonera)
    # ---------------------------------------------------------------------
    def _construir_barra_superior(self):
        """Crea la barra de botones superior."""
        barra = ttk.Frame(self, padding=(10, 10))
        barra.pack(fill=tk.X, side=tk.TOP)

        # Refrescar → vuelve a leer la BD y repinta la grilla
        ttk.Button(barra, text="Refrescar", command=self._refrescar_grilla)\
            .pack(side=tk.LEFT, padx=(0, 8))

        # Alta → abre diálogo de nuevo contacto
        self.btn_alta = ttk.Button(barra, text="Nuevo contacto", command=self._abrir_dialogo_nuevo)
        self.btn_alta.pack(side=tk.LEFT, padx=(0, 8))

        # Editar → abre diálogo con datos de la fila seleccionada
        self.btn_editar = ttk.Button(barra, text="Editar", command=self._abrir_dialogo_editar)
        self.btn_editar.pack(side=tk.LEFT, padx=(0, 8))

        # Borrar → elimina la fila seleccionada (con confirmación)
        self.btn_borrar = ttk.Button(barra, text="Borrar", command=self._borrar_seleccionado)
        self.btn_borrar.pack(side=tk.LEFT, padx=(0, 8))

        # Estados iniciales: deshabilitados hasta que haya selección
        self.btn_editar.state(["disabled"])
        self.btn_borrar.state(["disabled"])

        # Label informativo a la derecha
        ttk.Label(barra, text="Listado / Alta / Edición / Borrar").pack(side=tk.RIGHT)

    # ---------------------------------------------------------------------
    # Grilla (Treeview + Scrollbars)
    # ---------------------------------------------------------------------
    def _construir_treeview(self):
        """
        Construye la grilla principal para mostrar contactos.
        """
        self.frame_tree = ttk.Frame(self, padding=(10, 0, 10, 10))
        self.frame_tree.pack(fill=tk.BOTH, expand=True)

        columnas = ("id", "nombre", "apellido", "telefono", "email")
        self.tree = ttk.Treeview(
            self.frame_tree,
            columns=columnas,
            show="headings",
            selectmode="browse"
        )

        # Encabezados
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("apellido", text="Apellido")
        self.tree.heading("telefono", text="Teléfono")
        self.tree.heading("email", text="Email")

        # Anchos / alineación
        self.tree.column("id", width=60, anchor=tk.W, stretch=False)
        self.tree.column("nombre", width=160, anchor=tk.W)
        self.tree.column("apellido", width=160, anchor=tk.W)
        self.tree.column("telefono", width=160, anchor=tk.W)
        self.tree.column("email", width=240, anchor=tk.W)

        # Scrollbars
        vsb = ttk.Scrollbar(self.frame_tree, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(self.frame_tree, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # Layout
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        self.frame_tree.rowconfigure(0, weight=1)
        self.frame_tree.columnconfigure(0, weight=1)

        # Eventos
        self.tree.bind("<Double-1>", self._on_doble_click_row)               # doble click => editar
        self.tree.bind("<<TreeviewSelect>>", self._on_tree_selection_change) # habilita/inhabilita botones
        # (Opcional) tecla Supr/Del para borrar:
        # self.tree.bind("<Delete>", lambda e: self._borrar_seleccionado())

    # ---------------------------------------------------------------------
    # Helpers de estado de botones
    # ---------------------------------------------------------------------
    def _set_btn_states(self, hay_sel: bool):
        """
        Habilita/Deshabilita botones según haya selección.
        Usa ttk.state; si falla en algún theme, cae a .configure(state=...).
        """
        try:
            if hay_sel:
                self.btn_editar.state(["!disabled"])
                self.btn_borrar.state(["!disabled"])
            else:
                self.btn_editar.state(["disabled"])
                self.btn_borrar.state(["disabled"])
        except Exception:
            # Fallback por si algún theme no soporta .state()
            self.btn_editar.configure(state=(tk.NORMAL if hay_sel else tk.DISABLED))
            self.btn_borrar.configure(state=(tk.NORMAL if hay_sel else tk.DISABLED))

    # ---------------------------------------------------------------------
    # Cargar/Refrescar datos
    # ---------------------------------------------------------------------
    def _refrescar_grilla(self):
        """Vuelve a leer desde la base y repinta la grilla completa."""
        # Limpiar filas actuales
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            # obtener_todos()
            contactos = self.repo.obtener_todos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron leer los contactos.\n\n{e}", parent=self)
            return

        # Insertar filas (en el mismo orden que las columnas)
        for c in contactos:
            self.tree.insert("", tk.END, values=(c.id, c.nombre, c.apellido, c.telefono, c.email))

        # Tras refrescar, no hay selección activa
        self._set_btn_states(False)

    # ---------------------------------------------------------------------
    # Hooks / Eventos
    # ---------------------------------------------------------------------
    def _on_tree_selection_change(self, event=None):
        """Habilita/Deshabilita botones según haya fila seleccionada."""
        sels = self.tree.selection()
        # print("[DEBUG] <<TreeviewSelect>> ->", sels)  # útil para diagnosticar
        self._set_btn_states(bool(sels))

    def _on_doble_click_row(self, event):
        """Abrir edición con doble click."""
        self._abrir_dialogo_editar()

    # ---------------------------------------------------------------------
    # Alta (Nuevo contacto)
    # ---------------------------------------------------------------------
    def _abrir_dialogo_nuevo(self):
        """
        Abre el diálogo de alta.
        Flujo:
          - El usuario completa nombre/apellido/telefono/email.
          - Al guardar: se valida y se construye models.Contacto.
          - Se llama repo.agregar(contacto).
          - Se refresca la grilla y se informa resultado.
        """
        dlg = AddContactDialog(self)  # parent=self para modal y centrado
        self.wait_window(dlg)         # bloquea hasta que cierran el diálogo
        if dlg.result is None:
            return  # cancelado

        try:
            # agregar(contacto) puede devolver el ID (int) o None (según tu repo)
            new_id = self.repo.agregar(dlg.result)
            self._refrescar_grilla()
            msg = f"Contacto creado (ID={new_id})." if new_id is not None else "Contacto creado."
            messagebox.showinfo("Éxito", msg, parent=self)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear el contacto.\n\n{e}", parent=self)

    # ---------------------------------------------------------------------
    # Edición
    # ---------------------------------------------------------------------
    def _abrir_dialogo_editar(self):
        """
        Abre el diálogo de edición sobre la fila seleccionada.
        Usa los datos visibles en la grilla como pre-fill y al confirmar
        llama repo.actualizar(contacto) (UPDATE por ID).
        """
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccioná un contacto para editar.", parent=self)
            return

        item_id = sel[0]
        values = self.tree.item(item_id, "values")  # (id, nombre, apellido, telefono, email)

        try:
            contacto_id = int(values[0])
        except Exception:
            messagebox.showerror("Error", "ID seleccionado inválido.", parent=self)
            return

        # Prellenamos desde la grilla
        from models.contacto import Contacto
        contacto = Contacto(
            id=contacto_id,
            nombre=values[1],
            apellido=values[2],
            telefono=values[3],
            email=values[4],
        )

        dlg = EditContactDialog(self, contacto)
        self.wait_window(dlg)
        if dlg.result is None:
            return  # cancelado

        try:
            ok = self.repo.actualizar(dlg.result)  # bool o rowcount>0
            if ok:
                self._refrescar_grilla()
                messagebox.showinfo("Éxito", "Contacto actualizado.", parent=self)
            else:
                messagebox.showwarning("Atención", "No se actualizó ninguna fila (¿ID inexistente?).", parent=self)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el contacto.\n\n{e}", parent=self)

    # ---------------------------------------------------------------------
    # Borrado
    # ---------------------------------------------------------------------
    def _borrar_seleccionado(self):
        """
        Elimina la fila seleccionada.
        Soporta repos con API:
        - eliminar_por_id(id: int) -> bool/int
        - eliminar(contacto: Contacto) -> bool/int
        - eliminar(id: int) -> bool/int
        """
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccioná un contacto para borrar.", parent=self)
            return

        item_id = sel[0]
        values = self.tree.item(item_id, "values")  # (id, nombre, apellido, telefono, email)

        try:
            contacto_id = int(values[0])
        except Exception:
            messagebox.showerror("Error", "ID seleccionado inválido.", parent=self)
            return

        nombre, apellido = values[1], values[2]
        if not messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Eliminar a {nombre} {apellido} (ID={contacto_id})?",
            parent=self
        ):
            return

        try:
            ok = None

            # 1) Si existe eliminar_por_id
            if hasattr(self.repo, "eliminar_por_id"):
                ok = self.repo.eliminar_por_id(contacto_id)

            else:
                # 2) Intento por id directamente
                try:
                    ok = self.repo.eliminar(contacto_id)
                except Exception as e:
                    # 3) Si el repo esperaba un Contacto (error típico: "'int' object has no attribute 'id'")
                    if "has no attribute 'id'" in str(e):
                        from models.contacto import Contacto
                        dummy = Contacto(id=contacto_id, nombre="", apellido="", telefono="", email="")
                        ok = self.repo.eliminar(dummy)
                    else:
                        raise  # otro error real: lo dejamos subir

            # Normalizar truthiness (rowcount o bool)
            if ok:
                self._refrescar_grilla()
                messagebox.showinfo("Éxito", "Contacto eliminado.", parent=self)
            else:
                messagebox.showwarning("Atención", "No se eliminó ninguna fila (¿ID inexistente?).", parent=self)

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el contacto.\n\n{e}", parent=self)



# =====================================================================
# Diálogo de ALTA
# =====================================================================
class AddContactDialog(tk.Toplevel):
    """
    Diálogo MODAL para crear un contacto.
    Retorna en self.result un models.Contacto o None si cancelan.
    """
    def __init__(self, parent: tk.Tk):
        """
        Args:
            parent: ventana padre para modalidad y centrado.
        """
        super().__init__(parent)
        self.title("Nuevo contacto")
        self.resizable(False, False)

        # Modal sobre la ventana principal
        self.transient(parent)
        self.grab_set()

        # Vars de formulario
        self.var_nombre = tk.StringVar()
        self.var_apellido = tk.StringVar()
        self.var_telefono = tk.StringVar()
        self.var_email = tk.StringVar()
        self.result = None  # se setea al confirmar

        # --- UI ---
        frm = ttk.Frame(self, padding=12)
        frm.grid(row=0, column=0)

        ttk.Label(frm, text="Nombre").grid(row=0, column=0, sticky="w", pady=4)
        ttk.Entry(frm, textvariable=self.var_nombre, width=30).grid(row=0, column=1, sticky="w")

        ttk.Label(frm, text="Apellido").grid(row=1, column=0, sticky="w", pady=4)
        ttk.Entry(frm, textvariable=self.var_apellido, width=30).grid(row=1, column=1, sticky="w")

        ttk.Label(frm, text="Teléfono").grid(row=2, column=0, sticky="w", pady=4)
        ttk.Entry(frm, textvariable=self.var_telefono, width=30).grid(row=2, column=1, sticky="w")

        ttk.Label(frm, text="Email").grid(row=3, column=0, sticky="w", pady=4)
        ttk.Entry(frm, textvariable=self.var_email, width=30).grid(row=3, column=1, sticky="w")

        btns = ttk.Frame(frm)
        btns.grid(row=4, column=0, columnspan=2, pady=(10, 0))
        ttk.Button(btns, text="Cancelar", command=self._on_cancel).pack(side=tk.RIGHT, padx=6)
        ttk.Button(btns, text="Guardar", command=self._on_ok).pack(side=tk.RIGHT)

        # Centrar sobre la ventana padre
        self.update_idletasks()
        x = parent.winfo_rootx() + (parent.winfo_width() - self.winfo_width()) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{max(x,0)}+{max(y,0)}")

    def _on_cancel(self):
        """Cierra el diálogo sin devolver datos (result=None)."""
        self.result = None
        self.destroy()

    def _on_ok(self):
        """
        Valida y devuelve Contacto.
        Reglas:
          - nombre/apellido: 2..60 chars
          - teléfono: 6..20 (dígitos, +, -, (), espacios)
          - email: patrón básico user@dominio.tld
        """
        import re
        from tkinter import messagebox
        from models.contacto import Contacto  # import local para evitar ciclos

        nombre = self.var_nombre.get().strip()
        apellido = self.var_apellido.get().strip()
        telefono = self.var_telefono.get().strip()
        email = self.var_email.get().strip()

        if not (2 <= len(nombre) <= 60):
            messagebox.showerror("Validación", "Nombre: 2 a 60 caracteres.", parent=self); return
        if not (2 <= len(apellido) <= 60):
            messagebox.showerror("Validación", "Apellido: 2 a 60 caracteres.", parent=self); return
        if not re.match(r"^[\d+\-\(\)\s]{6,20}$", telefono):
            messagebox.showerror("Validación", "Teléfono inválido (6–20, dígitos + () - y espacios).", parent=self); return
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            messagebox.showerror("Validación", "Email inválido.", parent=self); return

        c = Contacto(nombre=nombre, apellido=apellido, telefono=telefono, email=email)

        # Si el modelo tiene validar(), la usamos
        if hasattr(c, "validar"):
            ok, msg = c.validar()
            if not ok:
                messagebox.showerror("Validación", msg or "Datos inválidos.", parent=self); return

        self.result = c
        self.destroy()


# =====================================================================
# Diálogo de EDICIÓN
# =====================================================================
class EditContactDialog(tk.Toplevel):
    """
    Diálogo modal para EDITAR un contacto existente.
    Recibe un Contacto con 'id' + datos actuales y devuelve en result otro Contacto con los cambios.
    """
    def __init__(self, parent: tk.Tk, contacto):
        """
        Args:
            parent: ventana padre.
            contacto: models.Contacto con id + nombre + apellido + telefono + email (valores actuales).
        """
        super().__init__(parent)
        self.title("Editar contacto")
        self.resizable(False, False)

        # Modal sobre la ventana principal
        self.transient(parent)
        self.grab_set()

        # Guardamos el ID del contacto a editar (clave primaria para UPDATE)
        self.contacto_id = contacto.id

        # Variables pre-cargadas
        self.var_nombre = tk.StringVar(value=contacto.nombre)
        self.var_apellido = tk.StringVar(value=contacto.apellido)
        self.var_telefono = tk.StringVar(value=contacto.telefono)
        self.var_email = tk.StringVar(value=contacto.email)
        self.result = None  # se setea al confirmar

        # --- UI ---
        frm = ttk.Frame(self, padding=12)
        frm.grid(row=0, column=0)

        ttk.Label(frm, text=f"ID: {self.contacto_id}").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

        ttk.Label(frm, text="Nombre").grid(row=1, column=0, sticky="w", pady=4)
        ttk.Entry(frm, textvariable=self.var_nombre, width=30).grid(row=1, column=1, sticky="w")

        ttk.Label(frm, text="Apellido").grid(row=2, column=0, sticky="w", pady=4)
        ttk.Entry(frm, textvariable=self.var_apellido, width=30).grid(row=2, column=1, sticky="w")

        ttk.Label(frm, text="Teléfono").grid(row=3, column=0, sticky="w", pady=4)
        ttk.Entry(frm, textvariable=self.var_telefono, width=30).grid(row=3, column=1, sticky="w")

        ttk.Label(frm, text="Email").grid(row=4, column=0, sticky="w", pady=4)
        ttk.Entry(frm, textvariable=self.var_email, width=30).grid(row=4, column=1, sticky="w")

        btns = ttk.Frame(frm)
        btns.grid(row=5, column=0, columnspan=2, pady=(10, 0))
        ttk.Button(btns, text="Cancelar", command=self._on_cancel).pack(side=tk.RIGHT, padx=6)
        ttk.Button(btns, text="Guardar", command=self._on_ok).pack(side=tk.RIGHT)

        # Centrar sobre la ventana padre
        self.update_idletasks()
        x = parent.winfo_rootx() + (parent.winfo_width() - self.winfo_width()) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{max(x,0)}+{max(y,0)}")

    def _on_cancel(self):
        """Cierra el diálogo sin devolver cambios."""
        self.result = None
        self.destroy()

    def _on_ok(self):
        """
        Valida y construye el Contacto modificado (con el mismo ID).
        Validaciones:
          - nombre/apellido: 2..60
          - teléfono: 6..20 (dígitos, +, -, (), espacios)
          - email: patrón user@dominio.tld
        """
        import re
        from tkinter import messagebox
        from models.contacto import Contacto  # import local para evitar ciclos

        nombre = self.var_nombre.get().strip()
        apellido = self.var_apellido.get().strip()
        telefono = self.var_telefono.get().strip()
        email = self.var_email.get().strip()

        if not (2 <= len(nombre) <= 60):
            messagebox.showerror("Validación", "Nombre: 2 a 60 caracteres.", parent=self); return
        if not (2 <= len(apellido) <= 60):
            messagebox.showerror("Validación", "Apellido: 2 a 60 caracteres.", parent=self); return
        if not re.match(r"^[\d+\-\(\)\s]{6,20}$", telefono):
            messagebox.showerror("Validación", "Teléfono inválido (6–20, dígitos + () - y espacios).", parent=self); return
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            messagebox.showerror("Validación", "Email inválido.", parent=self); return

        c = Contacto(id=self.contacto_id, nombre=nombre, apellido=apellido, telefono=telefono, email=email)

        if hasattr(c, "validar"):
            ok, msg = c.validar()
            if not ok:
                messagebox.showerror("Validación", msg or "Datos inválidos.", parent=self); return

        self.result = c
        self.destroy()


# -------------------------------------------------------------------------
# Entry point
# -------------------------------------------------------------------------
if __name__ == "__main__":
    app = ContactosApp()
    app.mainloop()
