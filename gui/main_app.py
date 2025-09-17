# gui/main_app.py
import sys
import os

# Añadir el directorio raíz del proyecto al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import ttk, messagebox, font

# Capa de datos / dominio
from repository.contacto_repository import ContactoRepository
from services.db_services import init_schema


class ContactosApp(tk.Tk):
    """
    Ventana principal del ABM de contactos con diseño moderno.
    - Inicializa el esquema de BD (CREATE TABLE IF NOT EXISTS...).
    - Muestra un Treeview con los contactos.
    - Permite Alta, Edición y Borrado (vía ContactoRepository).
    """

    def __init__(self):
        super().__init__()

        self.colors = {
            "bg": "#f8fafc",  # Fondo principal más suave
            "sidebar": "#e2e8f0",  # Fondo de sidebar más elegante
            "primary": "#3b82f6",  # Azul más moderno
            "secondary": "#6366f1",  # Índigo
            "success": "#10b981",  # Verde más vibrante
            "danger": "#ef4444",  # Rojo más suave
            "warning": "#f59e0b",  # Ámbar
            "info": "#06b6d4",  # Cyan
            "text": "#1e293b",  # Texto principal más suave
            "text_muted": "#64748b",  # Texto secundario
            "border": "#e2e8f0",  # Bordes suaves
            "white": "#ffffff",  # Blanco puro
            "hover": "#e0f2fe",  # Hover más sutil
            "card": "#ffffff",  # Fondo de tarjetas
            "accent": "#8b5cf6",  # Púrpura accent
            "gradient_start": "#667eea",  # Gradiente inicio
            "gradient_end": "#764ba2",  # Gradiente fin
        }

        # --- Metadatos de ventana ---
        self.title("🌟 Gestión de Contactos - Sistema Profesional 2025")
        self.geometry("1300x750")
        self.minsize(1100, 650)
        self.configure(bg=self.colors["bg"])

        # --- Repositorio de datos (CRUD) ---
        self.repo = ContactoRepository()

        # --- Inicialización de esquema ---
        try:
            init_schema()
        except Exception as e:
            messagebox.showerror(
                "❌ Error de base de datos",
                f"No se pudo inicializar el esquema.\n\n{e}",
                parent=self,
            )
            self.destroy()
            return

        # --- Configurar estilos modernos ---
        self._configurar_estilos_modernos()

        # --- Construcción de UI moderna ---
        self._construir_header()  # Header con título y info
        self._construir_barra_superior()  # Toolbar moderna
        self._construir_contenido()  # Área principal con tabla
        self._construir_barra_estado()  # Barra de estado

        # Estado inicial de botones
        self._set_btn_states(False)

        # --- Carga inicial de datos ---
        self._refrescar_grilla()

        # --- Efectos de ventana ---
        self._aplicar_efectos_ventana()

    # ---------------------------------------------------------------------
    # Estilos modernos
    # ---------------------------------------------------------------------
    def _configurar_estilos_modernos(self):
        """Configura estilos ttk para una apariencia moderna y profesional."""
        style = ttk.Style(self)

        # Usar tema base y personalizarlo
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        # --- Configurar fuentes ---
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(family="Segoe UI", size=10)

        title_font = font.Font(family="Segoe UI", size=22, weight="bold")
        header_font = font.Font(family="Segoe UI", size=16, weight="bold")
        subheader_font = font.Font(family="Segoe UI", size=12, weight="bold")
        button_font = font.Font(family="Segoe UI", size=10, weight="normal")
        tree_font = font.Font(
            family="Segoe UI", size=10
        )  # Más grande para mejor lectura
        tree_header_font = font.Font(family="Segoe UI", size=11, weight="bold")
        small_font = font.Font(family="Segoe UI", size=9)
        tiny_font = font.Font(family="Segoe UI", size=8)

        # --- Estilos para botones con mejor estado disabled ---
        style.configure(
            "Modern.TButton",
            font=button_font,
            padding=(12, 8),
            background=self.colors["primary"],
            foreground="white",
            borderwidth=0,
            focuscolor="none",
        )

        style.map(
            "Modern.TButton",
            background=[
                ("active", "#0b5ed7"),
                ("pressed", "#0a58ca"),
                ("disabled", "#9ca3af"),
            ],
            foreground=[("disabled", "#6b7280")],
        )

        style.configure(
            "Success.TButton",
            font=button_font,
            padding=(12, 8),
            background=self.colors["success"],
            foreground="white",
            borderwidth=0,
            focuscolor="none",
        )

        style.map(
            "Success.TButton",
            background=[
                ("active", "#157347"),
                ("pressed", "#146c43"),
                ("disabled", "#9ca3af"),
            ],
            foreground=[("disabled", "#6b7280")],
        )

        style.configure(
            "Danger.TButton",
            font=button_font,
            padding=(12, 8),
            background=self.colors["danger"],
            foreground="white",
            borderwidth=0,
            focuscolor="none",
        )

        style.map(
            "Danger.TButton",
            background=[
                ("active", "#bb2d3b"),
                ("pressed", "#b02a37"),
                ("disabled", "#9ca3af"),
            ],
            foreground=[("disabled", "#6b7280")],
        )

        style.configure(
            "Warning.TButton",
            font=button_font,
            padding=(12, 8),
            background=self.colors["warning"],
            foreground="white",
            borderwidth=0,
            focuscolor="none",
        )

        style.map(
            "Warning.TButton",
            background=[
                ("active", "#fd7e14"),
                ("pressed", "#e8681a"),
                ("disabled", "#9ca3af"),
            ],
            foreground=[("disabled", "#6b7280")],
        )

        # --- Estilos para Treeview con fuentes mejoradas ---
        style.configure(
            "Modern.Treeview.Heading",
            font=tree_header_font,
            background="#1e293b",
            foreground="white",
            padding=(12, 10),
            relief="flat",
        )

        # Map para hover en headers - mejor contraste
        style.map(
            "Modern.Treeview.Heading",
            background=[
                ("active", "#374151"),  # Gris más oscuro
                ("pressed", "#111827"),
            ],  # Gris muy oscuro
            foreground=[("active", "#ffffff"), ("pressed", "#f9fafb")],  # Blanco puro
        )  # Blanco casi puro

        style.configure(
            "Modern.Treeview",
            font=tree_font,
            background="white",  # Fondo base blanco para mejor contraste
            foreground="#212529",  # Texto oscuro
            rowheight=40,  # Más altura para mejor legibilidad
            fieldbackground="white",  # Fondo de campo blanco
            borderwidth=1,
            relief="solid",
            selectbackground=self.colors["primary"],
            selectforeground="white",
        )

        style.map(
            "Modern.Treeview",
            background=[
                ("selected", self.colors["primary"]),
            ],
            foreground=[
                ("selected", "white"),
            ],
        )

        # --- Estilos para Labels ---
        style.configure(
            "Header.TLabel",
            font=header_font,
            background=self.colors["bg"],
            foreground=self.colors["text"],
        )

        style.configure(
            "Modern.TLabel",
            font=button_font,
            background=self.colors["bg"],
            foreground=self.colors["text"],
        )

        style.configure(
            "Muted.TLabel",
            font=("Segoe UI", 9),
            background=self.colors["bg"],
            foreground=self.colors["text_muted"],
        )

        # --- Estilos para Frames ---
        style.configure(
            "Card.TFrame",
            background=self.colors["white"],
            relief="flat",
            borderwidth=1,
            lightcolor=self.colors["border"],
            darkcolor=self.colors["border"],
        )

        style.configure(
            "Toolbar.TFrame", background=self.colors["sidebar"], relief="flat"
        )

        # --- Estilos para Scrollbars modernos ---
        style.configure(
            "Modern.Vertical.TScrollbar",
            background=self.colors["sidebar"],
            troughcolor=self.colors["bg"],
            bordercolor=self.colors["border"],
            arrowcolor=self.colors["text_muted"],
            darkcolor=self.colors["border"],
            lightcolor=self.colors["white"],
            borderwidth=1,
            relief="flat",
        )

        style.map(
            "Modern.Vertical.TScrollbar",
            background=[
                ("active", self.colors["primary"]),
                ("pressed", self.colors["secondary"]),
            ],
        )

        style.configure(
            "Modern.Horizontal.TScrollbar",
            background=self.colors["sidebar"],
            troughcolor=self.colors["bg"],
            bordercolor=self.colors["border"],
            arrowcolor=self.colors["text_muted"],
            darkcolor=self.colors["border"],
            lightcolor=self.colors["white"],
            borderwidth=1,
            relief="flat",
        )

        style.map(
            "Modern.Horizontal.TScrollbar",
            background=[
                ("active", self.colors["primary"]),
                ("pressed", self.colors["secondary"]),
            ],
        )

    def _construir_header(self):
        """Construye el header."""
        header_frame = ttk.Frame(self, style="Card.TFrame", padding=(25, 20))
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 0))

        title_frame = ttk.Frame(header_frame, style="Card.TFrame")
        title_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Título principal
        title_label = ttk.Label(
            title_frame,
            text="🌟 Gestión de Contactos",
            font=("Segoe UI", 22, "bold"),
            foreground=self.colors["primary"],
            background=self.colors["card"],
        )
        title_label.pack(side=tk.TOP, anchor="w")

        subtitle_label = ttk.Label(
            title_frame,
            text="Sistema Profesional 2025 ✨",
            font=("Segoe UI", 12),
            foreground=self.colors["text_muted"],
            background=self.colors["card"],
        )
        subtitle_label.pack(side=tk.TOP, anchor="w", pady=(3, 0))

        info_panel = ttk.Frame(header_frame, style="Card.TFrame")
        info_panel.pack(side=tk.RIGHT, fill=tk.Y)

        metrics_frame = ttk.Frame(info_panel, style="Card.TFrame")
        metrics_frame.pack(side=tk.TOP, anchor="e")

        # Estado del sistema
        status_icon = ttk.Label(
            metrics_frame,
            text="🟢 Sistema Activo",
            font=("Segoe UI", 11, "bold"),
            foreground=self.colors["success"],
            background=self.colors["card"],
        )
        status_icon.pack(side=tk.TOP, anchor="e", pady=(0, 5))

        self.contador_label = ttk.Label(
            metrics_frame,
            text="📊 0 contactos",
            font=("Segoe UI", 14, "bold"),
            foreground=self.colors["accent"],
            background=self.colors["card"],
        )
        self.contador_label.pack(side=tk.TOP, anchor="e")

    def _construir_barra_superior(self):
        """Crea la barra de herramientas moderna con iconos y efectos."""
        toolbar = ttk.Frame(self, style="Toolbar.TFrame", padding=(20, 15))
        toolbar.pack(fill=tk.X, padx=15, pady=(10, 0))

        # Frame izquierdo para botones principales
        left_frame = ttk.Frame(toolbar, style="Toolbar.TFrame")
        left_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Botón Refrescar
        self.btn_refrescar = ttk.Button(
            left_frame,
            text="🔄 Refrescar",
            command=self._refrescar_grilla,
            style="Modern.TButton",
        )
        self.btn_refrescar.pack(side=tk.LEFT, padx=(0, 10))

        # Botón Nuevo Contacto
        self.btn_alta = ttk.Button(
            left_frame,
            text="➕ Nuevo Contacto",
            command=self._abrir_dialogo_nuevo,
            style="Success.TButton",
        )
        self.btn_alta.pack(side=tk.LEFT, padx=(0, 10))

        # Separador visual
        separator = ttk.Separator(left_frame, orient="vertical")
        separator.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        # Botón Editar
        self.btn_editar = ttk.Button(
            left_frame,
            text="✏️ Editar",
            command=self._abrir_dialogo_editar,
            style="Warning.TButton",
        )
        self.btn_editar.pack(side=tk.LEFT, padx=(0, 10))

        # Botón Dar de Baja
        self.btn_borrar = ttk.Button(
            left_frame,
            text="⬇️ Dar de Baja",
            command=self._borrar_seleccionado,
            style="Danger.TButton",
        )
        self.btn_borrar.pack(side=tk.LEFT, padx=(0, 10))

        # Frame derecho para información y ayuda
        right_frame = ttk.Frame(toolbar, style="Toolbar.TFrame")
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Panel de ayuda con mejor diseño
        help_frame = ttk.Frame(right_frame, style="Toolbar.TFrame")
        help_frame.pack(side=tk.RIGHT)

        # Información de ayuda
        help_label = ttk.Label(
            help_frame,
            text="✨ Doble clic para editar",
            font=("Segoe UI", 9, "italic"),
            foreground=self.colors["text_muted"],
            background=self.colors["sidebar"],
        )
        help_label.pack(side=tk.TOP, anchor="e")

        # Indicador de modo
        mode_label = ttk.Label(
            help_frame,
            text="🚀 Modo Profesional",
            font=("Segoe UI", 8, "bold"),
            foreground=self.colors["accent"],
            background=self.colors["sidebar"],
        )
        mode_label.pack(side=tk.TOP, anchor="e", pady=(2, 0))

        # Estados iniciales
        self.btn_editar.state(["disabled"])
        self.btn_borrar.state(["disabled"])

    # ---------------------------------------------------------------------
    # Contenido principal
    # ---------------------------------------------------------------------
    def _construir_contenido(self):
        """Construye el área principal con la tabla de contactos."""
        # Frame contenedor con estilo de card
        content_frame = ttk.Frame(self, style="Card.TFrame", padding=0)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(10, 0))

        # Construir tabla dentro del frame
        self._construir_treeview_moderno(content_frame)

    def _construir_treeview_moderno(self, parent):
        """Construye la tabla moderna para mostrar contactos."""
        self.frame_tree = ttk.Frame(parent)
        self.frame_tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Configurar columnas
        columnas = ("id", "nombre", "apellido", "telefono", "email")
        self.tree = ttk.Treeview(
            self.frame_tree,
            columns=columnas,
            show="headings",
            selectmode="browse",
            style="Modern.Treeview",
        )

        # Encabezados con iconos (alineados con sus columnas)
        self.tree.heading("id", text="🆔", anchor=tk.CENTER)
        self.tree.heading("nombre", text="👤 Nombre", anchor=tk.W)
        self.tree.heading("apellido", text="👨 Apellido", anchor=tk.W)
        self.tree.heading("telefono", text="📞 Teléfono", anchor=tk.W)
        self.tree.heading("email", text="📧 Email", anchor=tk.W)

        # Configurar columnas con mejor ancho y alineación
        self.tree.column("id", width=90, minwidth=80, anchor=tk.CENTER, stretch=False)
        self.tree.column("nombre", width=150, minwidth=120, anchor=tk.W, stretch=True)
        self.tree.column("apellido", width=150, minwidth=120, anchor=tk.W, stretch=True)
        self.tree.column(
            "telefono", width=150, minwidth=120, anchor=tk.W, stretch=False
        )
        self.tree.column("email", width=220, minwidth=180, anchor=tk.W, stretch=True)

        # Scrollbars modernos con estilos personalizados
        vsb = ttk.Scrollbar(
            self.frame_tree,
            orient="vertical",
            command=self.tree.yview,
            style="Modern.Vertical.TScrollbar",
        )
        hsb = ttk.Scrollbar(
            self.frame_tree,
            orient="horizontal",
            command=self.tree.xview,
            style="Modern.Horizontal.TScrollbar",
        )
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # Layout mejorado
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        self.frame_tree.rowconfigure(0, weight=1)
        self.frame_tree.columnconfigure(0, weight=1)

        # Eventos
        self.tree.bind("<Double-1>", self._on_doble_click_row)
        self.tree.bind("<<TreeviewSelect>>", self._on_tree_selection_change)
        self.tree.bind(
            "<Button-3>", self._on_right_click
        )  # Click derecho para menú contextual

        # Configurar colores alternados para las filas (estilo cebra)
        self.tree.tag_configure("evenrow", background="#f8f9fa", foreground="#212529")
        self.tree.tag_configure("oddrow", background="white", foreground="#212529")

    # ---------------------------------------------------------------------
    # Barra de estado
    # ---------------------------------------------------------------------
    def _construir_barra_estado(self):
        """Construye la barra de estado inferior con diseño mejorado."""
        # Frame principal con estilo de card
        status_frame = ttk.Frame(self, style="Card.TFrame", padding=(25, 12))
        status_frame.pack(fill=tk.X, padx=20, pady=(10, 20))

        # Panel izquierdo para estado del sistema
        left_panel = ttk.Frame(status_frame, style="Card.TFrame")
        left_panel.pack(side=tk.LEFT, fill=tk.Y)

        # Estado de la aplicación con diseño mejorado
        self.status_label = ttk.Label(
            left_panel,
            text="🚀 Sistema Operativo",
            font=("Segoe UI", 10, "bold"),
            foreground=self.colors["success"],
            background=self.colors["card"],
        )
        self.status_label.pack(side=tk.LEFT)

        # Separador visual
        sep_label = ttk.Label(
            left_panel,
            text=" | ",
            font=("Segoe UI", 10),
            foreground=self.colors["border"],
            background=self.colors["card"],
        )
        sep_label.pack(side=tk.LEFT)

        # Versión del sistema
        version_label = ttk.Label(
            left_panel,
            text="v2025.1 🌟",
            font=("Segoe UI", 9),
            foreground=self.colors["text_muted"],
            background=self.colors["card"],
        )
        version_label.pack(side=tk.LEFT)

        # Panel derecho para información temporal
        right_panel = ttk.Frame(status_frame, style="Card.TFrame")
        right_panel.pack(side=tk.RIGHT, fill=tk.Y)

        # Información adicional mejorada
        self.info_label = ttk.Label(
            right_panel,
            text="⏰ Iniciado",
            font=("Segoe UI", 9),
            foreground=self.colors["text_muted"],
            background=self.colors["card"],
        )
        self.info_label.pack(side=tk.RIGHT)

    # ---------------------------------------------------------------------
    # Efectos de ventana
    # ---------------------------------------------------------------------
    def _aplicar_efectos_ventana(self):
        """Aplica efectos visuales y configuraciones avanzadas."""
        # Centrar ventana en pantalla
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"+{x}+{y}")

        # Configurar comportamiento de cierre
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _on_closing(self):
        """Maneja el cierre de la aplicación."""
        if messagebox.askokcancel("Salir", "¿Desea cerrar la aplicación?"):
            self.destroy()

    def _on_right_click(self, event):
        """Maneja el menú contextual (para futuras mejoras)."""
        # Aquí podrías agregar un menú contextual
        pass

    # ---------------------------------------------------------------------
    # Actualización de estado
    # ---------------------------------------------------------------------
    def _actualizar_contador_contactos(self, count):
        """Actualiza el contador de contactos en el header."""
        if count == 0:
            texto = "📋 Sin contactos registrados"
            color = self.colors["text_muted"]
        elif count == 1:
            texto = "👤 1 contacto activo"
            color = self.colors["info"]
        elif count <= 10:
            texto = f"👥 {count} contactos activos"
            color = self.colors["success"]
        elif count <= 50:
            texto = f"📊 {count} contactos registrados"
            color = self.colors["primary"]
        else:
            texto = f"📈 {count} contactos en sistema"
            color = self.colors["accent"]

        self.contador_label.config(text=texto, foreground=color)

    def _actualizar_estado(self, mensaje, tipo="info"):
        """Actualiza la barra de estado con un mensaje."""
        iconos = {"info": "ℹ️", "success": "✅", "warning": "⚠️", "error": "❌"}
        icon = iconos.get(tipo, "ℹ️")
        self.status_label.config(text=f"{icon} {mensaje}")

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
            self._actualizar_estado(f"Contactos cargados correctamente", "success")
        except Exception as e:
            messagebox.showerror(
                "❌ Error", f"No se pudieron leer los contactos.\n\n{e}", parent=self
            )
            self._actualizar_estado("Error al cargar contactos", "error")
            return

        # Insertar filas
        for i, c in enumerate(contactos):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.tree.insert(
                "",
                tk.END,
                values=(c.id, c.nombre, c.apellido, c.telefono, c.email),
                tags=(tag,),
            )

        # Actualizar contador
        self._actualizar_contador_contactos(len(contactos))

        # Tras refrescar, no hay selección activa
        self._set_btn_states(False)

        # Actualizar información
        self.info_label.config(text=f"Última actualización: {self._get_current_time()}")

    def _get_current_time(self):
        """Retorna la hora actual formateada."""
        from datetime import datetime

        return datetime.now().strftime("%H:%M:%S")

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
        Abre el diálogo de alta
        """
        dlg = AddContactDialog(self)
        self.wait_window(dlg)
        if dlg.result is None:
            return

        try:
            new_id = self.repo.agregar(dlg.result)
            self._refrescar_grilla()
            msg = (
                f"Contacto creado exitosamente (ID={new_id})."
                if new_id is not None
                else "Contacto creado exitosamente."
            )
            messagebox.showinfo("✅ Éxito", msg, parent=self)
            self._actualizar_estado("Nuevo contacto agregado", "success")
        except Exception as e:
            messagebox.showerror(
                "❌ Error", f"No se pudo crear el contacto.\n\n{e}", parent=self
            )
            self._actualizar_estado("Error al crear contacto", "error")

    # ---------------------------------------------------------------------
    # Edición
    # ---------------------------------------------------------------------
    def _abrir_dialogo_editar(self):
        """
        Abre el diálogo de edición sobre la fila seleccionada.
        """
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning(
                "⚠️ Atención", "Seleccioná un contacto para editar.", parent=self
            )
            return

        item_id = sel[0]
        values = self.tree.item(item_id, "values")

        try:
            contacto_id = int(values[0])
        except Exception:
            messagebox.showerror("❌ Error", "ID seleccionado inválido.", parent=self)
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
            return

        try:
            ok = self.repo.actualizar(dlg.result)
            if ok:
                self._refrescar_grilla()
                messagebox.showinfo(
                    "✅ Éxito", "Contacto actualizado correctamente.", parent=self
                )
                self._actualizar_estado("Contacto actualizado", "success")
            else:
                messagebox.showwarning(
                    "⚠️ Atención",
                    "No se actualizó ninguna fila (¿ID inexistente?).",
                    parent=self,
                )
                self._actualizar_estado("No se pudo actualizar", "warning")
        except Exception as e:
            messagebox.showerror(
                "❌ Error", f"No se pudo actualizar el contacto.\n\n{e}", parent=self
            )
            self._actualizar_estado("Error al actualizar contacto", "error")

    # ---------------------------------------------------------------------
    # Borrado
    # ---------------------------------------------------------------------
    def _borrar_seleccionado(self):
        """
        Elimina la fila seleccionada
        """
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning(
                "⚠️ Atención", "Seleccioná un contacto para dar de baja.", parent=self
            )
            return

        item_id = sel[0]
        values = self.tree.item(item_id, "values")

        try:
            contacto_id = int(values[0])
        except Exception:
            messagebox.showerror("❌ Error", "ID seleccionado inválido.", parent=self)
            return

        nombre, apellido = values[1], values[2]
        if not messagebox.askyesno(
            "� Confirmar Baja de Contacto",
            f"¿Estás seguro de que deseas dar de baja a:\n\n{nombre} {apellido} (ID: {contacto_id})\n\nEsta acción no se puede deshacer.",
            parent=self,
        ):
            return

        try:
            ok = None

            # Intentar diferentes métodos de eliminación según la API del repo
            if hasattr(self.repo, "eliminar_por_id"):
                ok = self.repo.eliminar_por_id(contacto_id)
            else:
                try:
                    ok = self.repo.eliminar(contacto_id)
                except Exception as e:
                    if "has no attribute 'id'" in str(e):
                        from models.contacto import Contacto

                        dummy = Contacto(
                            id=contacto_id,
                            nombre="",
                            apellido="",
                            telefono="",
                            email="",
                        )
                        ok = self.repo.eliminar(dummy)
                    else:
                        raise

            if ok:
                self._refrescar_grilla()
                messagebox.showinfo(
                    "✅ Éxito",
                    f"Contacto {nombre} {apellido} dado de baja correctamente.",
                    parent=self,
                )
                self._actualizar_estado("Contacto dado de baja", "success")
            else:
                messagebox.showwarning(
                    "⚠️ Atención",
                    "No se pudo dar de baja ninguna fila (¿ID inexistente?).",
                    parent=self,
                )
                self._actualizar_estado("No se pudo dar de baja", "warning")

        except Exception as e:
            messagebox.showerror(
                "❌ Error", f"No se pudo dar de baja el contacto.\n\n{e}", parent=self
            )
            self._actualizar_estado("Error al dar de baja contacto", "error")


# =====================================================================
# Diálogo de ALTA
# =====================================================================
class AddContactDialog(tk.Toplevel):
    """
    Diálogo MODAL para crear un contacto.
    Retorna en self.result un models.Contacto o None si cancelan.
    """

    def __init__(self, parent: tk.Tk):
        super().__init__(parent)

        # Colores modernos
        self.colors = parent.colors
        self.configure(bg=self.colors["bg"])

        # Modal sobre la ventana principal
        self.transient(parent)
        self.grab_set()

        # Variables de formulario
        self.var_nombre = tk.StringVar()
        self.var_apellido = tk.StringVar()
        self.var_telefono = tk.StringVar()
        self.var_email = tk.StringVar()
        self.result = None

        # Configurar estilos
        self._configurar_estilos(parent)

        # Construir UI
        self._construir_ui()

        # Centrar y mostrar
        self._centrar_dialogo(parent)

        # Focus en primer campo
        self.entry_nombre.focus()

    def _configurar_estilos(self, parent):
        """Configura estilos para el diálogo."""
        self.style = ttk.Style(self)

        # Estilos para entradas
        self.style.configure(
            "Dialog.TEntry",
            font=("Segoe UI", 11),
            padding=(10, 8),
            fieldbackground=self.colors["white"],
            borderwidth=1,
            relief="solid",
        )

        self.style.map(
            "Dialog.TEntry",
            focuscolor=[
                ("!focus", self.colors["border"]),
                ("focus", self.colors["primary"]),
            ],
        )

        # Estilos para labels
        self.style.configure(
            "Dialog.TLabel",
            font=("Segoe UI", 10, "bold"),
            background=self.colors["bg"],
            foreground=self.colors["text"],
        )

    def _construir_ui(self):
        """Construye la interfaz del diálogo."""
        # Frame principal con padding
        main_frame = ttk.Frame(self, padding=30)
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.configure(style="Card.TFrame")

        # Título del diálogo
        title_label = ttk.Label(
            main_frame,
            text="Agregar Nuevo Contacto",
            font=("Segoe UI", 16, "bold"),
            style="Dialog.TLabel",
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="w")

        # Campos del formulario
        self._crear_campo(main_frame, "👤 Nombre:", self.var_nombre, 1)
        self.entry_nombre = self._crear_campo(
            main_frame, "👨 Apellido:", self.var_apellido, 2
        )
        self._crear_campo(main_frame, "📞 Teléfono:", self.var_telefono, 3)
        self._crear_campo(main_frame, "📧 Email:", self.var_email, 4)

        # Frame para botones
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=(30, 0), sticky="ew")
        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)

        # Botones
        cancel_btn = ttk.Button(
            btn_frame,
            text="❌ Cancelar",
            command=self._on_cancel,
            style="Danger.TButton",
        )
        cancel_btn.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        save_btn = ttk.Button(
            btn_frame, text="💾 Guardar", command=self._on_ok, style="Success.TButton"
        )
        save_btn.grid(row=0, column=1, sticky="ew")

        # Configurar comportamiento Enter/Escape
        self.bind("<Return>", lambda e: self._on_ok())
        self.bind("<Escape>", lambda e: self._on_cancel())

    def _crear_campo(self, parent, label_text, var, row):
        """Crea un campo de formulario."""
        # Label
        label = ttk.Label(parent, text=label_text, style="Dialog.TLabel")
        label.grid(row=row, column=0, sticky="w", pady=(0, 15), padx=(0, 15))

        # Entry
        entry = ttk.Entry(parent, textvariable=var, width=25, style="Dialog.TEntry")
        entry.grid(row=row, column=1, sticky="ew", pady=(0, 15))

        # Configurar expansión de columna
        parent.columnconfigure(1, weight=1)

        return entry

    def _centrar_dialogo(self, parent):
        """Centra el diálogo sobre la ventana padre."""
        self.update_idletasks()

        # Obtener dimensiones
        width = self.winfo_width()
        height = self.winfo_height()
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()

        # Calcular posición centrada
        x = parent_x + (parent_width - width) // 2
        y = parent_y + (parent_height - height) // 2

        self.geometry(f"+{max(x, 0)}+{max(y, 0)}")

    def _on_cancel(self):
        """Cierra el diálogo sin guardar."""
        self.result = None
        self.destroy()

    def _on_ok(self):
        """Valida y guarda el contacto."""
        if self._validar_datos():
            from models.contacto import Contacto

            nombre = self.var_nombre.get().strip()
            apellido = self.var_apellido.get().strip()
            telefono = self.var_telefono.get().strip()
            email = self.var_email.get().strip()

            self.result = Contacto(
                nombre=nombre, apellido=apellido, telefono=telefono, email=email
            )
            self.destroy()

    def _validar_datos(self):
        """Valida los datos del formulario."""
        import re

        nombre = self.var_nombre.get().strip()
        apellido = self.var_apellido.get().strip()
        telefono = self.var_telefono.get().strip()
        email = self.var_email.get().strip()

        # Validaciones con mensajes más amigables
        if not (2 <= len(nombre) <= 60):
            self._mostrar_error("El nombre debe tener entre 2 y 60 caracteres.")
            self.entry_nombre.focus()
            return False

        if not (2 <= len(apellido) <= 60):
            self._mostrar_error("El apellido debe tener entre 2 y 60 caracteres.")
            return False

        if not re.match(r"^[\d+\-\(\)\s]{6,20}$", telefono):
            self._mostrar_error(
                "El teléfono debe tener entre 6 y 20 caracteres\ny solo contener dígitos, +, -, ( ), y espacios."
            )
            return False

        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            self._mostrar_error("Por favor, ingresa un email válido.")
            return False

        return True

    def _mostrar_error(self, mensaje):
        """Muestra un mensaje de error amigable."""
        messagebox.showerror("⚠️ Error de validación", mensaje, parent=self)


# =====================================================================
# Diálogo de EDICIÓN
# =====================================================================
class EditContactDialog(tk.Toplevel):
    """
    Diálogo modal para EDITAR un contacto existente.
    """

    def __init__(self, parent: tk.Tk, contacto):
        super().__init__(parent)
        self.title("✏️ Editar Contacto")
        self.resizable(False, False)

        # Colores modernos
        self.colors = parent.colors
        self.configure(bg=self.colors["bg"])

        # Modal sobre la ventana principal
        self.transient(parent)
        self.grab_set()

        # ID del contacto a editar
        self.contacto_id = contacto.id

        # Variables pre-cargadas
        self.var_nombre = tk.StringVar(value=contacto.nombre)
        self.var_apellido = tk.StringVar(value=contacto.apellido)
        self.var_telefono = tk.StringVar(value=contacto.telefono)
        self.var_email = tk.StringVar(value=contacto.email)
        self.result = None

        # Configurar estilos
        self._configurar_estilos(parent)

        # Construir UI
        self._construir_ui()

        # Centrar y mostrar
        self._centrar_dialogo(parent)

        # Focus en primer campo
        self.entry_nombre.focus()
        self.entry_nombre.select_range(0, tk.END)

    def _configurar_estilos(self, parent):
        """Configura estilos para el diálogo."""
        self.style = ttk.Style(self)

        # Heredar estilos de la ventana principal si existen
        if hasattr(parent, "style"):
            self.style = parent.style

    def _construir_ui(self):
        """Construye la interfaz del diálogo de edición."""
        # Frame principal con padding
        main_frame = ttk.Frame(self, padding=30)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título del diálogo con ID
        title_label = ttk.Label(
            main_frame,
            text=f"Editar Contacto (ID: {self.contacto_id})",
            font=("Segoe UI", 16, "bold"),
            background=self.colors["bg"],
            foreground=self.colors["text"],
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="w")

        # Campos del formulario
        self.entry_nombre = self._crear_campo(
            main_frame, "👤 Nombre:", self.var_nombre, 1
        )
        self._crear_campo(main_frame, "👨 Apellido:", self.var_apellido, 2)
        self._crear_campo(main_frame, "📞 Teléfono:", self.var_telefono, 3)
        self._crear_campo(main_frame, "📧 Email:", self.var_email, 4)

        # Frame para botones
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=(30, 0), sticky="ew")
        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)

        # Botones
        cancel_btn = ttk.Button(
            btn_frame,
            text="❌ Cancelar",
            command=self._on_cancel,
            style="Danger.TButton",
        )
        cancel_btn.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        save_btn = ttk.Button(
            btn_frame,
            text="💾 Actualizar",
            command=self._on_ok,
            style="Success.TButton",
        )
        save_btn.grid(row=0, column=1, sticky="ew")

        # Configurar comportamiento Enter/Escape
        self.bind("<Return>", lambda e: self._on_ok())
        self.bind("<Escape>", lambda e: self._on_cancel())

    def _crear_campo(self, parent, label_text, var, row):
        """Crea un campo de formulario para edición."""
        # Label
        label = ttk.Label(
            parent,
            text=label_text,
            font=("Segoe UI", 10, "bold"),
            background=self.colors["bg"],
            foreground=self.colors["text"],
        )
        label.grid(row=row, column=0, sticky="w", pady=(0, 15), padx=(0, 15))

        # Entry
        entry = ttk.Entry(parent, textvariable=var, width=25, font=("Segoe UI", 11))
        entry.grid(row=row, column=1, sticky="ew", pady=(0, 15))

        # Configurar expansión de columna
        parent.columnconfigure(1, weight=1)

        return entry

    def _centrar_dialogo(self, parent):
        """Centra el diálogo sobre la ventana padre."""
        self.update_idletasks()

        width = self.winfo_width()
        height = self.winfo_height()
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()

        x = parent_x + (parent_width - width) // 2
        y = parent_y + (parent_height - height) // 2

        self.geometry(f"+{max(x, 0)}+{max(y, 0)}")

    def _on_cancel(self):
        """Cierra el diálogo sin guardar cambios."""
        self.result = None
        self.destroy()

    def _on_ok(self):
        """Valida y actualiza el contacto."""
        if self._validar_datos():
            from models.contacto import Contacto

            nombre = self.var_nombre.get().strip()
            apellido = self.var_apellido.get().strip()
            telefono = self.var_telefono.get().strip()
            email = self.var_email.get().strip()

            self.result = Contacto(
                id=self.contacto_id,
                nombre=nombre,
                apellido=apellido,
                telefono=telefono,
                email=email,
            )
            self.destroy()

    def _validar_datos(self):
        """Valida los datos del formulario de edición."""
        import re

        nombre = self.var_nombre.get().strip()
        apellido = self.var_apellido.get().strip()
        telefono = self.var_telefono.get().strip()
        email = self.var_email.get().strip()

        if not (2 <= len(nombre) <= 60):
            self._mostrar_error("El nombre debe tener entre 2 y 60 caracteres.")
            self.entry_nombre.focus()
            return False

        if not (2 <= len(apellido) <= 60):
            self._mostrar_error("El apellido debe tener entre 2 y 60 caracteres.")
            return False

        if not re.match(r"^[\d+\-\(\)\s]{6,20}$", telefono):
            self._mostrar_error(
                "El teléfono debe tener entre 6 y 20 caracteres\ny solo contener dígitos, +, -, ( ), y espacios."
            )
            return False

        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            self._mostrar_error("Por favor, ingresa un email válido.")
            return False

        return True

    def _mostrar_error(self, mensaje):
        """Muestra un mensaje de error."""
        messagebox.showerror("⚠️ Error de validación", mensaje, parent=self)


# -------------------------------------------------------------------------
# Entry point
# -------------------------------------------------------------------------
if __name__ == "__main__":
    app = ContactosApp()
    app.mainloop()
