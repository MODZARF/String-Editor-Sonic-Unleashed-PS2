import os
import re
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import xml.etree.ElementTree as ET


# ==============================================================================
# SCRIPT 2: EDITOR DE TABLA DE CARACTERES (VENTANA SECUNDARIA NO BLOQUEANTE)
# ==============================================================================
class TablaCaracteresEditor:

  def __init__(self, parent):
    self.top = tk.Toplevel(parent)
    self.top.title("Editor de Tablas de Caracteres - ZARF")
    self.top.geometry("700x250")
    self.top.minsize(500, 200)

    # NOTA: Se eliminó grab_set() para que la ventana principal NO se congele
    # y ambas funcionen en paralelo sin afectarse.

    self.file_path = None
    self.create_widgets()

  def create_widgets(self):
    # --- FRAME SUPERIOR (Botones de Control) ---
    top_frame = ttk.Frame(self.top, padding=10)
    top_frame.pack(fill=tk.X)

    # Botones alineados a la izquierda
    self.btn_open = ttk.Button(
        top_frame, text="Abrir Tabla", command=self.abrir_tabla
    )
    self.btn_open.pack(side=tk.LEFT, padx=5)

    self.lbl_status = ttk.Label(
        top_frame, text="Ningún archivo abierto", foreground="gray"
    )
    self.lbl_status.pack(side=tk.LEFT, padx=20)

    # Botones alineados a la derecha
    self.btn_save = ttk.Button(
        top_frame,
        text="Guardar Tabla",
        command=self.guardar_tabla,
        state=tk.DISABLED,
    )
    self.btn_save.pack(side=tk.RIGHT, padx=5)

    self.btn_create = ttk.Button(
        top_frame,
        text="Crear Tabla",
        command=self.crear_tabla,
        state=tk.DISABLED,
    )
    self.btn_create.pack(side=tk.RIGHT, padx=5)

    # --- FRAME CENTRAL (Editor de Texto con Scroll Horizontal) ---
    mid_frame = ttk.Frame(self.top, padding=15)
    mid_frame.pack(fill=tk.BOTH, expand=True)

    ttk.Label(
        mid_frame,
        text="Caracteres de la tabla (Edición continua en una línea):",
        font=("Segoe UI", 9, "bold"),
    ).pack(anchor=tk.W, pady=(0, 5))

    scrollbar_x = ttk.Scrollbar(mid_frame, orient=tk.HORIZONTAL)

    self.txt_editor = tk.Text(
        mid_frame,
        height=3,
        font=("Consolas", 12),
        wrap=tk.NONE,
        xscrollcommand=scrollbar_x.set,
    )
    scrollbar_x.config(command=self.txt_editor.xview)

    self.txt_editor.pack(fill=tk.X, expand=True)
    scrollbar_x.pack(fill=tk.X)

    # Bloquear la tecla Enter/Intro para mantener todo en 1 sola línea
    self.txt_editor.bind("<Return>", lambda e: "break")
    self.txt_editor.bind("<KP_Enter>", lambda e: "break")

    # Evento para activar/desactivar botones según si hay texto escrito
    self.txt_editor.bind("<KeyRelease>", self.evaluar_estado_botones)

  def evaluar_estado_botones(self, event=None):
    texto = self.txt_editor.get("1.0", "end-1c").strip()
    if texto:
      self.btn_create.config(state=tk.NORMAL)
      if self.file_path:
        self.btn_save.config(state=tk.NORMAL)
    else:
      self.btn_create.config(state=tk.DISABLED)
      self.btn_save.config(state=tk.DISABLED)

  def abrir_tabla(self):
    file_path = filedialog.askopenfilename(
        filetypes=[("Archivos de Texto", "*.txt"), ("Todos los archivos", "*.*")]
    )
    if not file_path:
      return

    try:
      with open(file_path, "r", encoding="utf-8") as f:
        lineas = f.readlines()

      caracteres_extraidos = []

      for linea in lineas:
        linea_limpia = linea.strip()
        if not linea_limpia:
          continue

        if "////" in linea_limpia:
          caracteres_extraidos.append("$")
        else:
          start_idx = linea_limpia.find('"')
          end_idx = linea_limpia.rfind('"')

          if start_idx != -1 and end_idx != -1 and start_idx < end_idx:
            contenido_char = linea_limpia[start_idx + 1 : end_idx]
            caracteres_extraidos.append(contenido_char)

      texto_final = "".join(caracteres_extraidos)
      self.txt_editor.delete("1.0", tk.END)
      self.txt_editor.insert("1.0", texto_final)

      self.file_path = file_path
      self.lbl_status.config(
          text=os.path.basename(file_path), foreground="green"
      )
      self.evaluar_estado_botones()

    except Exception as e:
      messagebox.showerror(
          "Error", f"No se pudo leer el archivo:\n{str(e)}", parent=self.top
      )

  def formatear_y_escribir_tabla(self, ruta_destino):
    texto_usuario = self.txt_editor.get("1.0", "end-1c")

    lineas_salida = []
    contador_hex = 0x0A

    for char in texto_usuario:
      if char == "$":
        lineas_salida.append("////\n")
      else:
        lineas_salida.append(f'0x{contador_hex:02X} "{char}"\n')
        contador_hex += 1

    with open(ruta_destino, "w", encoding="utf-8") as f:
      f.writelines(lineas_salida)

  def guardar_tabla(self):
    if not self.file_path:
      return

    try:
      self.formatear_y_escribir_tabla(self.file_path)
      messagebox.showinfo(
          "Éxito",
          "Tabla guardada y formateada correctamente.",
          parent=self.top,
      )
    except Exception as e:
      messagebox.showerror(
          "Error al guardar",
          f"Hubo un fallo al escribir el archivo:\n{str(e)}",
          parent=self.top,
      )

  def crear_tabla(self):
    texto_usuario = self.txt_editor.get("1.0", "end-1c").strip()
    if not texto_usuario:
      return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[
            ("Archivos de Texto (*.txt)", "*.txt"),
            ("Todos los archivos", "*.*"),
        ],
        title="Crear Nueva Tabla de Caracteres",
    )

    if not file_path:
      return

    try:
      self.formatear_y_escribir_tabla(file_path)

      # Asignar la nueva ruta como activa
      self.file_path = file_path
      self.lbl_status.config(
          text=os.path.basename(file_path), foreground="green"
      )
      self.evaluar_estado_botones()

      messagebox.showinfo(
          "Éxito",
          f"Nueva tabla creada y guardada con éxito en:\n{file_path}",
          parent=self.top,
      )
    except Exception as e:
      messagebox.showerror(
          "Error al crear tabla",
          f"Hubo un fallo al crear el archivo:\n{str(e)}",
          parent=self.top,
      )


# ==============================================================================
# SCRIPT 1: EDITOR STRINGS V3 (PRINCIPAL)
# ==============================================================================
class ROMTranslationEditor:

  def __init__(self, root):
    self.root = root
    self.root.title("String Editor Sonic Unleashed V3_By ZARF")
    self.root.geometry("850x620")

    # Asegura que al cerrar la ventana principal se cierren todas las sub-ventanas
    self.root.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion_completa)

    # Variables de control
    self.xml_path = None
    self.txt_path = None
    self.xml_tree = None

    # Mapeos multi-tabla
    self.fuentes_hex_to_char = []
    self.fuentes_char_to_hex = []

    self.tree_item_fuentes = {}
    self.fuente_seleccionada_actual = 0

    self.create_widgets()

  def cerrar_aplicacion_completa(self):
    # Cierra la ventana root y fuerza la finalización del proceso
    self.root.destroy()
    sys.exit()

  def create_widgets(self):
    # --- PANEL SUPERIOR (Controles de archivos y botones) ---
    top_frame = ttk.Frame(self.root, padding=10)
    top_frame.pack(fill=tk.X)

    # BOTONES ALINEADOS A LA IZQUIERDA
    self.btn_xml = ttk.Button(top_frame, text="Abrir XML", command=self.load_xml)
    self.btn_xml.pack(side=tk.LEFT, padx=3)

    self.btn_reload_table = ttk.Button(
        top_frame,
        text="Actualizar Tabla",
        command=self.reload_table,
        state=tk.DISABLED,
    )
    self.btn_reload_table.pack(side=tk.LEFT, padx=3)

    self.btn_close_table = ttk.Button(
        top_frame,
        text="Cerrar Tabla",
        command=self.close_table,
        state=tk.DISABLED,
    )
    self.btn_close_table.pack(side=tk.LEFT, padx=3)

    self.btn_table = ttk.Button(
        top_frame, text="Abrir Tabla", command=self.load_table
    )
    self.btn_table.pack(side=tk.LEFT, padx=3)

    # BOTÓN PARA LANZAR EL EDITOR DE TABLA (PARALELO/NO BLOQUEANTE)
    self.btn_editor_tabla = ttk.Button(
        top_frame, text="Editor Tabla", command=self.abrir_editor_de_tabla
    )
    self.btn_editor_tabla.pack(side=tk.LEFT, padx=3)

    # BOTÓN ALINEADO A LA DERECHA: ACERCA DE
    self.btn_about = ttk.Button(
        top_frame, text="Acerca de", command=self.mostrar_acerca_de
    )
    self.btn_about.pack(side=tk.RIGHT, padx=3)

    # --- PANEL CENTRAL (Lista de Strings con Scroll) ---
    list_frame = ttk.Frame(self.root, padding=10)
    list_frame.pack(fill=tk.BOTH, expand=True)

    columns = ("id", "text")
    self.tree = ttk.Treeview(
        list_frame, columns=columns, show="headings", selectmode="browse"
    )
    self.tree.heading("id", text="ID Celda")
    self.tree.heading("text", text="Texto / Data Codificada")
    self.tree.column("id", width=150, stretch=tk.NO)
    self.tree.column("text", width=650, stretch=tk.YES)

    scrollbar = ttk.Scrollbar(
        list_frame, orient=tk.VERTICAL, command=self.tree.yview
    )
    self.tree.configure(yscrollcommand=scrollbar.set)

    self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    self.tree.bind("<<TreeviewSelect>>", self.on_select_item)

    # --- PANEL INFERIOR (Editor y Opciones) ---
    bottom_frame = ttk.Frame(self.root, padding=10)
    bottom_frame.pack(fill=tk.X)

    info_frame = ttk.Frame(bottom_frame)
    info_frame.pack(fill=tk.X, pady=2)

    self.triple_space_var = tk.BooleanVar(value=True)
    self.chk_space = ttk.Checkbutton(
        info_frame,
        text="Triple Espacio (Auto)",
        variable=self.triple_space_var,
    )
    self.chk_space.pack(side=tk.LEFT)

    self.lbl_info_fuente = ttk.Label(
        info_frame, text="", font=("Segoe UI", 9, "bold")
    )
    self.lbl_info_fuente.pack(side=tk.RIGHT, padx=5)

    vcmd = (self.root.register(self.validate_input), "%P", "%d", "%S")

    self.editor_label = ttk.Label(bottom_frame, text="Editor de String:")
    self.editor_label.pack(anchor=tk.W, pady=(5, 0))

    self.txt_editor = ttk.Entry(
        bottom_frame,
        font=("Consolas", 11),
        validate="key",
        validatecommand=vcmd,
    )
    self.txt_editor.pack(fill=tk.X, pady=5)
    self.txt_editor.bind("<KeyRelease>", self.on_key_release)

    self.btn_apply = ttk.Button(
        bottom_frame,
        text="Aplicar Cambios",
        command=self.apply_changes,
        state=tk.DISABLED,
    )
    self.btn_apply.pack(fill=tk.X, pady=5)

    self.txt_editor.bind("<Return>", self.apply_changes)

  def abrir_editor_de_tabla(self):
    # Instancia y ejecuta la ventana secundaria del Editor de Tabla de forma independiente
    TablaCaracteresEditor(self.root)

  def mostrar_acerca_de(self):
    messagebox.showinfo(
        "Acerca de", "Diseñado por ZARF\nProgramado con Gemini AI"
    )

  # --- LÓGICA DE ARCHIVOS Y MAPEOS ---

  def load_xml(self):
    file_path = filedialog.askopenfilename(
        filetypes=[("Archivos XML", "*.xml")]
    )
    if not file_path:
      return

    try:
      self.xml_path = file_path
      self.xml_tree = ET.parse(self.xml_path)
      self.refresh_list()
    except Exception as e:
      messagebox.showerror("Error", f"No se pudo cargar el XML:\n{str(e)}")

  def load_table(self):
    file_path = filedialog.askopenfilename(
        filetypes=[("Archivos de Texto", "*.txt")]
    )
    if not file_path:
      return

    self.txt_path = file_path
    self.btn_reload_table.configure(state=tk.NORMAL)
    self.btn_close_table.configure(state=tk.NORMAL)
    self.reload_table()

  def close_table(self):
    self.txt_path = None
    self.fuentes_hex_to_char = []
    self.fuentes_char_to_hex = []
    self.tree_item_fuentes = {}
    self.lbl_info_fuente.configure(text="")
    self.btn_reload_table.configure(state=tk.DISABLED)
    self.btn_close_table.configure(state=tk.DISABLED)
    self.refresh_list()
    messagebox.showinfo(
        "Tabla Cerrada", "Los strings vuelven a mostrarse en Hexadecimal."
    )

  def reload_table(self):
    if not self.txt_path:
      return

    try:
      nuevas_fuentes_hex_to_char = [{}]
      nuevas_fuentes_char_to_hex = [{}]
      idx_tabla_actual = 0

      with open(self.txt_path, "r", encoding="utf-8") as f:
        for line in f:
          line = line.strip()

          if line == "////":
            nuevas_fuentes_hex_to_char.append({})
            nuevas_fuentes_char_to_hex.append({})
            idx_tabla_actual += 1
            continue

          if not line:
            continue

          match = re.match(r'^(0x[0-9a-fA-F]+)\s+"(.*)"$', line)
          if match:
            hex_val = match.group(1)
            char_val = match.group(2)

            if char_val == "\\n":
              char_val = "\n"

            clean_hex = hex_val.replace("0x", "").upper().zfill(2)
            formatted_hex = f"00 00 00 {clean_hex}"

            nuevas_fuentes_hex_to_char[idx_tabla_actual][
                formatted_hex
            ] = char_val
            nuevas_fuentes_char_to_hex[idx_tabla_actual][
                char_val
            ] = formatted_hex

      if idx_tabla_actual >= len(nuevas_fuentes_hex_to_char):
        idx_tabla_actual = len(nuevas_fuentes_hex_to_char) - 1

      self.fuentes_hex_to_char = nuevas_fuentes_hex_to_char
      self.fuentes_char_to_hex = nuevas_fuentes_char_to_hex

      messagebox.showinfo(
          "Éxito",
          f"Tablas cargadas correctamente.\nSe detectaron {len(self.fuentes_hex_to_char)} tablas independientes dentro del archivo.",
      )
      self.refresh_list()

    except Exception as e:
      messagebox.showerror(
          "Error", f"No se pudo procesar el archivo de tablas:\n{str(e)}"
      )

  # --- TRADUCCIÓN Y RENDERIZADO ---

  def analizar_y_decodificar_mejor_fuente(self, hex_data):
    if not self.fuentes_hex_to_char:
      return hex_data, 0

    clean_hex = hex_data.replace(" ", "")
    chunks = [clean_hex[i : i + 8] for i in range(0, len(clean_hex), 8)]

    mejor_fuente_id = 0
    max_aciertos = -1
    mejor_resultado_texto = ""

    for fuente_id, mapa_hex in enumerate(self.fuentes_hex_to_char):
      aciertos_actuales = 0
      decoded_chars = []

      for chunk in chunks:
        if len(chunk) < 8:
          continue
        formatted_chunk = (
            f"{chunk[0:2]} {chunk[2:4]} {chunk[4:6]} {chunk[6:8]}".upper()
        )

        if formatted_chunk == "00 00 00 00":
          decoded_chars.append("/")
          aciertos_actuales += 1
        elif formatted_chunk in mapa_hex:
          decoded_chars.append(mapa_hex[formatted_chunk])
          aciertos_actuales += 1
        else:
          last_byte = chunk[6:8]
          decoded_chars.append(f"[?{last_byte}]")

      if aciertos_actuales > max_aciertos:
        max_aciertos = aciertos_actuales
        mejor_fuente_id = fuente_id
        mejor_resultado_texto = "".join(decoded_chars)

    return mejor_resultado_texto, mejor_fuente_id

  def encode_string(self, text, fuente_id):
    hex_chunks = []
    i = 0
    mapa_char = self.fuentes_char_to_hex[fuente_id]

    while i < len(text):
      if text[i] == "/":
        hex_chunks.append("00 00 00 00")
        i += 1
        continue

      if text[i : i + 3] == "[?" and i + 4 < len(text) and text[i + 4] == "]":
        last_byte = text[i + 2 : i + 4]
        hex_chunks.append(f"00 00 00 {last_byte.upper()}")
        i += 5
        continue

      char = text[i]
      if char in mapa_char:
        hex_chunks.append(mapa_char[char])
      else:
        raise ValueError(
            f"El carácter '{char}' no está mapeado en la sección de la Fuente {fuente_id + 1}."
        )
      i += 1

    return " ".join(hex_chunks)

  def refresh_list(self):
    if not self.xml_tree:
      return

    selected_index = None
    selected_id = self.tree.selection()
    if selected_id:
      selected_index = self.tree.index(selected_id[0])

    scroll_pos = self.tree.yview()

    for item in self.tree.get_children():
      self.tree.delete(item)
    self.tree_item_fuentes.clear()

    root_xml = self.xml_tree.getroot()
    all_items = []

    for cell in root_xml.findall(".//Cell"):
      cell_name = cell.get("Name", "Sin Nombre")
      msg_node = cell.find("Message")

      if msg_node is not None:
        hex_data = msg_node.get("MessageData", "")

        display_text, fuente_id = self.analizar_y_decodificar_mejor_fuente(
            hex_data
        )

        item_id = self.tree.insert(
            "", tk.END, values=(cell_name, display_text)
        )
        self.tree_item_fuentes[item_id] = fuente_id
        all_items.append(item_id)

    if selected_index is not None and selected_index < len(all_items):
      target_item = all_items[selected_index]
      self.tree.selection_set(target_item)
      self.tree.focus(target_item)

    self.tree.yview_moveto(scroll_pos[0])

  # --- INTERACCIÓN Y VALIDACIÓN ---

  def on_select_item(self, event):
    selected = self.tree.selection()
    if not selected:
      self.btn_apply.configure(state=tk.DISABLED)
      self.lbl_info_fuente.configure(text="")
      return

    item_id = selected[0]
    values = self.tree.item(item_id, "values")
    current_text = values[1]

    if self.fuentes_hex_to_char and item_id in self.tree_item_fuentes:
      self.fuente_seleccionada_actual = self.tree_item_fuentes[item_id]
      self.lbl_info_fuente.configure(
          text=f"Pertenece a la Fuente ({self.fuente_seleccionada_actual + 1})"
      )
    else:
      self.fuente_seleccionada_actual = 0
      self.lbl_info_fuente.configure(text="")

    self.txt_editor.delete(0, tk.END)
    self.txt_editor.insert(0, current_text)

    if self.xml_tree:
      self.btn_apply.configure(state=tk.NORMAL)

  def validate_input(self, proposed_value, action_type, input_char):
    if not self.fuentes_char_to_hex:
      return True

    if action_type == "1":
      mapa_char_activo = self.fuentes_char_to_hex[
          self.fuente_seleccionada_actual
      ]
      for char in input_char:
        if char == "/":
          continue
        if char not in mapa_char_activo:
          messagebox.showwarning(
              "Carácter no permitido",
              f"El carácter '{char}' no pertenece al bloque asignado para la Fuente {self.fuente_seleccionada_actual + 1}.",
          )
          return False
    return True

  def on_key_release(self, event):
    if event.keysym == "space" and self.triple_space_var.get():
      current_pos = self.txt_editor.index(tk.INSERT)
      self.txt_editor.insert(current_pos, "  ")

  def apply_changes(self, event=None):
    selected = self.tree.selection()
    if not selected or not self.xml_tree:
      return

    item_id = selected[0]
    selected_index = self.tree.index(item_id)
    new_text = self.txt_editor.get()

    try:
      new_hex_data = self.encode_string(
          new_text, self.fuente_seleccionada_actual
      )

      root_xml = self.xml_tree.getroot()
      all_cells = root_xml.findall(".//Cell")

      if selected_index < len(all_cells):
        cell_node = all_cells[selected_index]
        msg_node = cell_node.find("Message")
        if msg_node is not None:
          msg_node.set("MessageData", new_hex_data)

          self.xml_tree.write(
              self.xml_path, encoding="utf-8", xml_declaration=True
          )
          self.refresh_list()

    except Exception as e:
      messagebox.showerror(
          "Error al guardar",
          f"Sucedió un error inyectando los bytes al XML:\n{str(e)}",
      )


# ==============================================================================
# PUNTO DE ENTRADA PRINCIPAL
# ==============================================================================
if __name__ == "__main__":
  root = tk.Tk()
  app = ROMTranslationEditor(root)
  root.mainloop()
