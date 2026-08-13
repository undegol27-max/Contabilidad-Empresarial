import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from datetime import datetime
import hashlib
import secrets
import subprocess
import sys


# ============================================================
# CONFIGURACION
# ============================================================

NOMBRE_PROGRAMA = "CONTABILIDAD"

CARPETA_PROGRAMA = Path(__file__).resolve().parent
CARPETA_BASE = CARPETA_PROGRAMA / "CONTABILIDAD"
ARCHIVO_SEGURIDAD = CARPETA_PROGRAMA / "seguridad_admin.dat"
ARCHIVO_CONFIGURACION = CARPETA_PROGRAMA / "configuracion.dat"

CARPETA_INGRESOS = CARPETA_BASE / "INGRESOS"
CARPETA_EGRESOS = CARPETA_BASE / "EGRESOS"

FILAS = 500

MESES = [
    "ENERO",
    "FEBRERO",
    "MARZO",
    "ABRIL",
    "MAYO",
    "JUNIO",
    "JULIO",
    "AGOSTO",
    "SEPTIEMBRE",
    "OCTUBRE",
    "NOVIEMBRE",
    "DICIEMBRE"
]


# ============================================================
# COLORES
# ============================================================

FONDO = "#E7EAED"
BLANCO = "#FFFFFF"
NEGRO = "#111111"
GRIS = "#D2D6DA"
ENCABEZADO = "#C9CED3"

VERDE = "#D9E9DD"
ROJO_SUAVE = "#F2D6D6"
AZUL = "#DCE5EE"
DORADO = "#E8DFCA"


# ============================================================
# VARIABLES
# ============================================================

tabla = None

tipo_libro_actual = None
archivo_actual = None

anio_actual = None
mes_actual = None
dia_actual = None


# ============================================================
# VENTANA
# ============================================================

ventana = tk.Tk()

ventana.title("CONTABILIDAD EMPRESARIAL")

ventana.geometry("1250x780")

ventana.minsize(
    1000,
    650
)

ventana.configure(
    bg=FONDO
)


# ============================================================
# CONFIGURACIÓN INICIAL
# ============================================================

MONEDAS_DISPONIBLES = [
    "ARS — Peso argentino",
    "BOB — Boliviano",
    "BRL — Real brasileño",
    "CAD — Dólar canadiense",
    "CLP — Peso chileno",
    "CNY — Yuan chino",
    "COP — Peso colombiano",
    "CRC — Colón costarricense",
    "DOP — Peso dominicano",
    "EUR — Euro",
    "GBP — Libra esterlina",
    "GTQ — Quetzal guatemalteco",
    "HNL — Lempira hondureño",
    "INR — Rupia india",
    "JPY — Yen japonés",
    "MXN — Peso mexicano",
    "NIO — Córdoba nicaragüense",
    "PEN — Sol peruano",
    "PYG — Guaraní paraguayo",
    "CHF — Franco suizo",
    "USD — Dólar estadounidense",
    "UYU — Peso uruguayo",
    "VES — Bolívar venezolano",
]


configuracion = {
    "negocio": "",
    "propietario": "",
    "moneda": "COP"
}


def cargar_configuracion():
    global configuracion

    if not ARCHIVO_CONFIGURACION.exists():
        return False

    try:
        lineas = ARCHIVO_CONFIGURACION.read_text(
            encoding="utf-8"
        ).splitlines()

        datos = {}

        for linea in lineas:
            if "=" in linea:
                clave, valor = linea.split("=", 1)
                datos[clave.strip()] = valor.strip()

        configuracion["negocio"] = datos.get(
            "negocio",
            ""
        )

        configuracion["propietario"] = datos.get(
            "propietario",
            ""
        )

        configuracion["moneda"] = datos.get(
            "moneda",
            "COP"
        ) or "COP"

        return bool(
            configuracion["negocio"]
            and configuracion["propietario"]
        )

    except Exception:
        return False


def guardar_configuracion():

    ARCHIVO_CONFIGURACION.write_text(
        f"negocio={configuracion['negocio']}\n"
        f"propietario={configuracion['propietario']}\n"
        f"moneda={configuracion['moneda']}\n",
        encoding="utf-8"
    )


def pedir_texto(
    titulo,
    etiqueta,
    valor_inicial=""
):

    dialogo = tk.Toplevel(ventana)

    dialogo.title(titulo)

    dialogo.configure(
        bg=FONDO
    )

    dialogo.resizable(
        False,
        False
    )

    dialogo.transient(
        ventana
    )

    dialogo.grab_set()

    resultado = {
        "valor": None
    }

    tk.Label(
        dialogo,
        text=etiqueta,
        font=("Segoe UI", 13, "bold"),
        bg=FONDO,
        fg=NEGRO
    ).pack(
        padx=30,
        pady=(25, 10)
    )

    entrada = tk.Entry(
        dialogo,
        font=("Segoe UI", 13),
        width=32
    )

    entrada.pack(
        padx=30,
        pady=8
    )

    entrada.insert(
        0,
        valor_inicial
    )

    entrada.focus_set()

    marco = tk.Frame(
        dialogo,
        bg=FONDO
    )

    marco.pack(
        pady=(10, 25)
    )

    def aceptar():

        valor = entrada.get().strip()

        if not valor:

            messagebox.showwarning(
                "Dato requerido",
                "Debes completar este campo."
            )

            return

        resultado["valor"] = valor

        dialogo.destroy()

    def cancelar():

        dialogo.destroy()

    tk.Button(
        marco,
        text="ACEPTAR",
        font=("Segoe UI", 10, "bold"),
        bg=BLANCO,
        fg=NEGRO,
        relief="solid",
        command=aceptar,
        padx=18,
        pady=8
    ).pack(
        side="left",
        padx=5
    )

    tk.Button(
        marco,
        text="CANCELAR",
        font=("Segoe UI", 10, "bold"),
        bg=NEGRO,
        fg=BLANCO,
        relief="solid",
        command=cancelar,
        padx=18,
        pady=8
    ).pack(
        side="left",
        padx=5
    )

    dialogo.bind(
        "<Return>",
        lambda event: aceptar()
    )

    dialogo.wait_window()

    return resultado["valor"]


def configuracion_inicial():

    limpiar_pantalla()

    ventana.title(
        "CONTABILIDAD EMPRESARIAL"
    )

    tk.Label(
        ventana,
        text="CONTABILIDAD EMPRESARIAL",
        font=("Segoe UI", 27, "bold"),
        bg=FONDO,
        fg=NEGRO
    ).pack(
        pady=(40, 8)
    )

    tk.Label(
        ventana,
        text="CONFIGURACIÓN INICIAL",
        font=("Segoe UI", 14, "bold"),
        bg=FONDO,
        fg="#56616B"
    ).pack(
        pady=(0, 28)
    )

    marco = tk.Frame(
        ventana,
        bg=FONDO
    )

    marco.pack()

    tk.Label(
        marco,
        text="NOMBRE DEL NEGOCIO O DE LA EMPRESA",
        font=("Segoe UI", 10, "bold"),
        bg=FONDO,
        fg=NEGRO
    ).grid(
        row=0,
        column=0,
        sticky="w",
        padx=10,
        pady=9
    )

    entrada_negocio = tk.Entry(
        marco,
        font=("Segoe UI", 12),
        width=32
    )

    entrada_negocio.grid(
        row=0,
        column=1,
        padx=10,
        pady=9
    )

    tk.Label(
        marco,
        text="DUEÑO O PROPIETARIO",
        font=("Segoe UI", 10, "bold"),
        bg=FONDO,
        fg=NEGRO
    ).grid(
        row=1,
        column=0,
        sticky="w",
        padx=10,
        pady=9
    )

    entrada_propietario = tk.Entry(
        marco,
        font=("Segoe UI", 12),
        width=32
    )

    entrada_propietario.grid(
        row=1,
        column=1,
        padx=10,
        pady=9
    )

    tk.Label(
        marco,
        text="MONEDA",
        font=("Segoe UI", 10, "bold"),
        bg=FONDO,
        fg=NEGRO
    ).grid(
        row=2,
        column=0,
        sticky="w",
        padx=10,
        pady=9
    )

    entrada_moneda = ttk.Combobox(
        marco,
        font=("Segoe UI", 12),
        width=30,
        state="readonly",
        values=MONEDAS_DISPONIBLES
    )

    entrada_moneda.grid(
        row=2,
        column=1,
        padx=10,
        pady=9
    )

    entrada_moneda.set(
        "COP — Peso colombiano"
    )

    if configuracion.get("negocio"):

        entrada_negocio.insert(
            0,
            configuracion["negocio"]
        )

    if configuracion.get("propietario"):

        entrada_propietario.insert(
            0,
            configuracion["propietario"]
        )

    if configuracion.get("moneda"):

        for moneda in MONEDAS_DISPONIBLES:

            if moneda.startswith(
                configuracion["moneda"] + " —"
            ):

                entrada_moneda.set(
                    moneda
                )

                break

    def continuar():

        negocio = entrada_negocio.get().strip()

        propietario = entrada_propietario.get().strip()

        moneda = entrada_moneda.get().strip()

        if not negocio or not propietario or not moneda:

            messagebox.showwarning(
                "Configuración incompleta",
                "Debes completar los tres datos para continuar."
            )

            return

        configuracion["negocio"] = negocio

        configuracion["propietario"] = propietario

        configuracion["moneda"] = moneda.split(
            " — ",
            1
        )[0]

        guardar_configuracion()

        menu_principal()

    marco_botones = tk.Frame(
        ventana,
        bg=FONDO
    )

    marco_botones.pack(
        pady=35
    )

    tk.Button(
        marco_botones,
        text="CONTINUAR",
        font=("Segoe UI", 11, "bold"),
        bg=VERDE,
        fg=NEGRO,
        relief="flat",
        cursor="hand2",
        padx=30,
        pady=12,
        command=continuar
    ).pack(
        side="left",
        padx=5
    )

    tk.Button(
        marco_botones,
        text="SALIR",
        font=("Segoe UI", 11, "bold"),
        bg=GRIS,
        fg=NEGRO,
        relief="flat",
        cursor="hand2",
        padx=30,
        pady=12,
        command=cerrar_programa
    ).pack(
        side="left",
        padx=5
    )


def abrir_configuracion():

    configuracion_inicial()


def fecha_del_pc():

    ahora = datetime.now()

    return (
        ahora.year,
        ahora.month,
        ahora.day
    )


# ============================================================
# DIAS DEL MES
# ============================================================

def dias_del_mes(
    anio,
    mes
):

    if mes == 2:

        if (
            anio % 400 == 0
            or (
                anio % 4 == 0
                and anio % 100 != 0
            )
        ):

            return 29

        return 28

    if mes in [4, 6, 9, 11]:

        return 30

    return 31


# ============================================================
# LIMPIAR PANTALLA
# ============================================================

def limpiar_pantalla():

    global tabla

    tabla = None

    for widget in ventana.winfo_children():

        widget.destroy()


# ============================================================
# BOTON DEVOLVERSE
# ============================================================

def boton_devolverse(
    contenedor,
    funcion
):

    tk.Button(
        contenedor,
        text="DEVOLVERSE",
        font=("Segoe UI", 11, "bold"),
        bg=GRIS,
        fg=NEGRO,
        relief="flat",
        cursor="hand2",
        padx=25,
        pady=10,
        command=funcion
    ).pack(
        side="left",
        padx=5
    )


# ============================================================
# SEGURIDAD DE ADMINISTRADOR
# ============================================================

def hash_codigo(codigo, sal):

    return hashlib.pbkdf2_hmac(
        "sha256",
        codigo.encode("utf-8"),
        sal,
        200000
    ).hex()


def guardar_codigos(codigos):

    lineas = []

    for codigo in codigos:

        sal = secrets.token_bytes(16)

        digest = hash_codigo(
            codigo,
            sal
        )

        lineas.append(
            sal.hex() + ":" + digest
        )

    ARCHIVO_SEGURIDAD.write_text(
        "\n".join(lineas),
        encoding="utf-8"
    )


def cargar_codigos():

    if not ARCHIVO_SEGURIDAD.exists():

        return None

    try:

        lineas = ARCHIVO_SEGURIDAD.read_text(
            encoding="utf-8"
        ).splitlines()

        if len(lineas) != 3:

            return None

        resultado = []

        for linea in lineas:

            sal_hex, digest = linea.split(
                ":",
                1
            )

            resultado.append(
                (
                    bytes.fromhex(sal_hex),
                    digest
                )
            )

        return resultado

    except Exception:

        return None


def verificar_codigo(codigo, datos):

    sal, digest = datos

    nuevo = hash_codigo(
        codigo,
        sal
    )

    return secrets.compare_digest(
        nuevo,
        digest
    )


def configurar_codigos_iniciales():

    if cargar_codigos() is not None:

        return True

    messagebox.showinfo(
        "Configuración de seguridad",
        "Es la primera vez que se activa la seguridad.\n\n"
        "Ahora debes crear tus 3 códigos de seguridad."
    )

    codigos = []

    for numero in range(1, 4):

        while True:

            codigo = pedir_codigo(
                f"CREAR CÓDIGO {numero} DE 3"
            )

            if codigo is None:

                return False

            if len(codigo) < 4:

                messagebox.showwarning(
                    "Código no válido",
                    "El código debe tener al menos 4 caracteres."
                )

                continue

            confirmar = pedir_codigo(
                f"CONFIRMAR CÓDIGO {numero} DE 3"
            )

            if confirmar is None:

                return False

            if codigo != confirmar:

                messagebox.showerror(
                    "No coincide",
                    "Los códigos no coinciden. Inténtalo de nuevo."
                )

                continue

            codigos.append(
                codigo
            )

            break

    guardar_codigos(
        codigos
    )

    messagebox.showinfo(
        "Seguridad configurada",
        "Los 3 códigos fueron guardados correctamente."
    )

    return True


def pedir_codigo(titulo):

    dialogo = tk.Toplevel(
        ventana
    )

    dialogo.title(
        titulo
    )

    dialogo.configure(
        bg=FONDO
    )

    dialogo.resizable(
        False,
        False
    )

    dialogo.transient(
        ventana
    )

    dialogo.grab_set()

    resultado = {
        "valor": None
    }

    tk.Label(
        dialogo,
        text=titulo,
        font=("Segoe UI", 15, "bold"),
        bg=FONDO,
        fg=NEGRO
    ).pack(
        padx=30,
        pady=(25, 12)
    )

    entrada = tk.Entry(
        dialogo,
        show="*",
        font=("Segoe UI", 13),
        width=28
    )

    entrada.pack(
        padx=30,
        pady=8
    )

    entrada.focus_set()

    marco = tk.Frame(
        dialogo,
        bg=FONDO
    )

    marco.pack(
        pady=(10, 25)
    )

    def aceptar():

        resultado["valor"] = entrada.get()

        dialogo.destroy()

    def cancelar():

        dialogo.destroy()

    tk.Button(
        marco,
        text="ACEPTAR",
        font=("Segoe UI", 10, "bold"),
        bg=BLANCO,
        fg=NEGRO,
        relief="solid",
        command=aceptar,
        padx=18,
        pady=8
    ).pack(
        side="left",
        padx=5
    )

    tk.Button(
        marco,
        text="CANCELAR",
        font=("Segoe UI", 10, "bold"),
        bg=NEGRO,
        fg=BLANCO,
        relief="solid",
        command=cancelar,
        padx=18,
        pady=8
    ).pack(
        side="left",
        padx=5
    )

    dialogo.bind(
        "<Return>",
        lambda event: aceptar()
    )

    dialogo.wait_window()

    return resultado["valor"]


def guardar_y_cerrar_por_fallo():

    try:

        if tabla is not None:

            guardar_txt(False)

    except Exception:

        pass

    messagebox.showerror(
        "Acceso denegado",
        "Código incorrecto.\n\n"
        "Los libros se guardarán y el programa se cerrará."
    )

    ventana.destroy()


def autenticar_tres_codigos():

    if not configurar_codigos_iniciales():

        return False

    datos = cargar_codigos()

    if datos is None:

        messagebox.showerror(
            "Seguridad",
            "No se pudo cargar la configuración de seguridad."
        )

        return False

    for numero in range(1, 4):

        codigo = pedir_codigo(
            f"CÓDIGO {numero} DE 3"
        )

        if codigo is None:

            return False

        if not verificar_codigo(
            codigo,
            datos[numero - 1]
        ):

            guardar_y_cerrar_por_fallo()

            return False

    messagebox.showinfo(
        "Acceso autorizado",
        "Los 3 códigos son correctos."
    )

    return True


def mostrar_codigo_fuente():

    if not autenticar_tres_codigos():

        return

    limpiar_pantalla()

    tk.Label(
        ventana,
        text="ACCESO A CÓDIGOS",
        font=("Segoe UI", 24, "bold"),
        bg=FONDO,
        fg=NEGRO
    ).pack(
        pady=(25, 10)
    )

    tk.Label(
        ventana,
        text="Modo solo lectura",
        font=("Segoe UI", 11),
        bg=FONDO,
        fg="#56616B"
    ).pack(
        pady=(0, 10)
    )

    marco = tk.Frame(
        ventana,
        bg=FONDO
    )

    marco.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=10
    )

    texto = tk.Text(
        marco,
        wrap="none",
        font=("Consolas", 9),
        bg=BLANCO,
        fg=NEGRO
    )

    texto.pack(
        side="left",
        fill="both",
        expand=True
    )

    barra = tk.Scrollbar(
        marco,
        command=texto.yview
    )

    barra.pack(
        side="right",
        fill="y"
    )

    texto.configure(
        yscrollcommand=barra.set
    )

    try:

        contenido = Path(
            __file__
        ).read_text(
            encoding="utf-8"
        )

        texto.insert(
            "1.0",
            contenido
        )

        texto.configure(
            state="disabled"
        )

    except Exception as error:

        texto.configure(
            state="normal"
        )

        texto.insert(
            "1.0",
            "No se pudo leer el archivo:\n\n"
            + str(error)
        )

        texto.configure(
            state="disabled"
        )

    boton_devolverse(
        ventana,
        menu_administrador
    )


def modificar_codigos():

    if not autenticar_tres_codigos():

        return

    messagebox.showinfo(
        "Modificar códigos",
        "Se abrirá el archivo del programa para modificarlo.\n\n"
        "Antes de hacer cambios, conserva siempre una copia de seguridad."
    )

    try:

        if sys.platform.startswith("win"):

            subprocess.Popen(
                [
                    "notepad.exe",
                    str(
                        Path(__file__).resolve()
                    )
                ]
            )

        else:

            subprocess.Popen(
                [
                    "xdg-open",
                    str(
                        Path(__file__).resolve()
                    )
                ]
            )

    except Exception as error:

        messagebox.showerror(
            "Error",
            "No se pudo abrir el archivo.\n\n"
            + str(error)
        )


def cambiar_codigos():

    if not autenticar_tres_codigos():

        return

    nuevos = []

    for numero in range(1, 4):

        while True:

            codigo = pedir_codigo(
                f"NUEVO CÓDIGO {numero} DE 3"
            )

            if codigo is None:

                return

            if len(codigo) < 4:

                messagebox.showwarning(
                    "Código no válido",
                    "El código debe tener al menos 4 caracteres."
                )

                continue

            confirmar = pedir_codigo(
                f"CONFIRMAR NUEVO CÓDIGO {numero} DE 3"
            )

            if confirmar is None:

                return

            if codigo != confirmar:

                messagebox.showerror(
                    "No coincide",
                    "Los códigos no coinciden."
                )

                continue

            nuevos.append(
                codigo
            )

            break

    guardar_codigos(
        nuevos
    )

    messagebox.showinfo(
        "Códigos actualizados",
        "Los 3 códigos fueron modificados correctamente."
    )


def menu_administrador():

    limpiar_pantalla()

    tk.Label(
        ventana,
        text="ACCESO DE ADMINISTRADOR",
        font=("Segoe UI", 25, "bold"),
        bg=FONDO,
        fg=NEGRO
    ).pack(
        pady=(45, 30)
    )

    estilo = {
        "font": ("Segoe UI", 12, "bold"),
        "width": 32,
        "height": 2,
        "bg": BLANCO,
        "fg": NEGRO,
        "activebackground": NEGRO,
        "activeforeground": BLANCO,
        "relief": "solid",
        "bd": 1,
        "cursor": "hand2"
    }

    tk.Button(
        ventana,
        text="ACCESO A CÓDIGOS",
        command=mostrar_codigo_fuente,
        **estilo
    ).pack(
        pady=8
    )

    tk.Button(
        ventana,
        text="MODIFICAR CÓDIGOS",
        command=modificar_codigos,
        **estilo
    ).pack(
        pady=8
    )

    tk.Button(
        ventana,
        text="SALIR / MENÚ PRINCIPAL",
        command=menu_principal,
        **estilo
    ).pack(
        pady=8
    )


def abrir_seguridad():

    if autenticar_tres_codigos():

        menu_administrador()


# ============================================================
# MENU PRINCIPAL
# ============================================================

def menu_principal():

    limpiar_pantalla()

    ventana.title(
        "CONTABILIDAD EMPRESARIAL"
    )

    tk.Label(
        ventana,
        text="CONTABILIDAD EMPRESARIAL",
        font=("Segoe UI", 29, "bold"),
        bg=FONDO,
        fg=NEGRO
    ).pack(
        pady=(30, 3)
    )

    if configuracion.get("negocio"):

        tk.Label(
            ventana,
            text=configuracion["negocio"],
            font=("Segoe UI", 12, "bold"),
            bg=FONDO,
            fg="#56616B"
        ).pack(
            pady=(0, 3)
        )

    tk.Label(
        ventana,
        text="MENÚ PRINCIPAL",
        font=("Segoe UI", 12),
        bg=FONDO,
        fg="#56616B"
    ).pack(
        pady=(0, 18)
    )

    tk.Button(
        ventana,
        text="1. CREAR LIBRO DE INGRESOS",
        font=("Segoe UI", 12, "bold"),
        width=36,
        height=2,
        bg=VERDE,
        fg=NEGRO,
        relief="flat",
        cursor="hand2",
        command=lambda: seleccionar_fecha(
            "ingresos"
        )
    ).pack(
        pady=5
    )

    tk.Button(
        ventana,
        text="2. CREAR LIBRO DE EGRESOS",
        font=("Segoe UI", 12, "bold"),
        width=36,
        height=2,
        bg=ROJO_SUAVE,
        fg=NEGRO,
        relief="flat",
        cursor="hand2",
        command=lambda: seleccionar_fecha(
            "egresos"
        )
    ).pack(
        pady=5
    )

    tk.Button(
        ventana,
        text="3. LIBROS ANTERIORES",
        font=("Segoe UI", 12, "bold"),
        width=36,
        height=2,
        bg=AZUL,
        fg=NEGRO,
        relief="flat",
        cursor="hand2",
        command=libros_anteriores
    ).pack(
        pady=5
    )

    tk.Button(
        ventana,
        text="4. CUENTAS AUTOMÁTICAS",
        font=("Segoe UI", 12, "bold"),
        width=36,
        height=2,
        bg=DORADO,
        fg=NEGRO,
        relief="flat",
        cursor="hand2",
        command=contabilidad_automatica
    ).pack(
        pady=5
    )

    tk.Button(
        ventana,
        text="5. CONFIGURACIÓN",
        font=("Segoe UI", 12, "bold"),
        width=36,
        height=2,
        bg=BLANCO,
        fg=NEGRO,
        relief="flat",
        cursor="hand2",
        command=abrir_configuracion
    ).pack(
        pady=5
    )

    tk.Button(
        ventana,
        text="6. SALIR",
        font=("Segoe UI", 12, "bold"),
        width=36,
        height=2,
        bg=GRIS,
        fg=NEGRO,
        relief="flat",
        cursor="hand2",
        command=cerrar_programa
    ).pack(
        pady=5
    )


def seleccionar_fecha(
    tipo
):

    limpiar_pantalla()

    anio_hoy, mes_hoy, dia_hoy = (
        fecha_del_pc()
    )

    if tipo == "ingresos":

        titulo = "CREAR LIBRO DE INGRESOS"

    else:

        titulo = "CREAR LIBRO DE EGRESOS"

    tk.Label(
        ventana,
        text=titulo,
        font=("Segoe UI", 25, "bold"),
        bg=FONDO,
        fg=NEGRO
    ).pack(
        pady=(35, 10)
    )

    tk.Label(
        ventana,
        text="Seleccione año, mes y día",
        font=("Segoe UI", 12),
        bg=FONDO,
        fg="#56616B"
    ).pack(
        pady=(0, 25)
    )

    marco = tk.Frame(
        ventana,
        bg=FONDO
    )

    marco.pack()

    tk.Label(
        marco,
        text="AÑO",
        font=("Segoe UI", 11, "bold"),
        bg=FONDO
    ).grid(
        row=0,
        column=0,
        padx=10,
        pady=8
    )

    combo_anio = ttk.Combobox(
        marco,
        values=list(
            range(
                anio_hoy - 4,
                anio_hoy + 51
            )
        ),
        state="readonly",
        width=15
    )

    combo_anio.set(
        anio_hoy
    )

    combo_anio.grid(
        row=1,
        column=0,
        padx=10
    )

    tk.Label(
        marco,
        text="MES",
        font=("Segoe UI", 11, "bold"),
        bg=FONDO
    ).grid(
        row=0,
        column=1,
        padx=10,
        pady=8
    )

    combo_mes = ttk.Combobox(
        marco,
        values=MESES,
        state="readonly",
        width=18
    )

    combo_mes.current(
        mes_hoy - 1
    )

    combo_mes.grid(
        row=1,
        column=1,
        padx=10
    )

    tk.Label(
        marco,
        text="DÍA",
        font=("Segoe UI", 11, "bold"),
        bg=FONDO
    ).grid(
        row=0,
        column=2,
        padx=10,
        pady=8
    )

    combo_dia = ttk.Combobox(
        marco,
        state="readonly",
        width=10
    )

    combo_dia.grid(
        row=1,
        column=2,
        padx=10
    )

    def actualizar_dias(
        event=None
    ):

        try:

            anio = int(
                combo_anio.get()
            )

            mes = (
                combo_mes.current()
                + 1
            )

            cantidad = dias_del_mes(
                anio,
                mes
            )

            combo_dia["values"] = list(
                range(
                    1,
                    cantidad + 1
                )
            )

            if (
                anio == anio_hoy
                and mes == mes_hoy
            ):

                combo_dia.set(
                    dia_hoy
                )

            else:

                combo_dia.set(
                    1
                )

        except Exception:

            pass

    combo_anio.bind(
        "<<ComboboxSelected>>",
        actualizar_dias
    )

    combo_mes.bind(
        "<<ComboboxSelected>>",
        actualizar_dias
    )

    actualizar_dias()

    marco_botones = tk.Frame(
        ventana,
        bg=FONDO
    )

    marco_botones.pack(
        pady=45
    )

    tk.Button(
        marco_botones,
        text="ABRIR LIBRO",
        font=("Segoe UI", 12, "bold"),
        bg=(
            VERDE
            if tipo == "ingresos"
            else ROJO_SUAVE
        ),
        fg=NEGRO,
        relief="flat",
        cursor="hand2",
        padx=25,
        pady=12,
        command=lambda:
        abrir_fecha_seleccionada(
            tipo,
            combo_anio,
            combo_mes,
            combo_dia
        )
    ).pack(
        side="left",
        padx=5
    )

    boton_devolverse(
        marco_botones,
        menu_principal
    )


# ============================================================
# CREAR RUTA DEL LIBRO
# ============================================================

def crear_ruta_libro(
    tipo,
    anio,
    mes,
    dia
):

    if tipo == "ingresos":

        base = CARPETA_INGRESOS

    else:

        base = CARPETA_EGRESOS

    numero_mes = (
        MESES.index(mes) + 1
    )

    carpeta = (
        base
        / str(anio)
        / mes
        / (
            f"{dia:02d}-"
            f"{numero_mes:02d}-"
            f"{anio}"
        )
    )

    carpeta.mkdir(
        parents=True,
        exist_ok=True
    )

    return carpeta


# ============================================================
# ABRIR FECHA SELECCIONADA
# ============================================================

def abrir_fecha_seleccionada(
    tipo,
    combo_anio,
    combo_mes,
    combo_dia
):

    global tipo_libro_actual
    global archivo_actual
    global anio_actual
    global mes_actual
    global dia_actual

    try:

        anio_actual = int(
            combo_anio.get()
        )

        mes_actual = (
            combo_mes.get()
        )

        dia_actual = int(
            combo_dia.get()
        )

        tipo_libro_actual = tipo

        carpeta = crear_ruta_libro(
            tipo,
            anio_actual,
            mes_actual,
            dia_actual
        )

        archivo_actual = (
            carpeta /
            "contabilidad.txt"
        )

        abrir_hoja_calculo()

    except Exception as error:

        messagebox.showerror(
            "Error",
            "Ocurrió un error al abrir "
            "el libro.\n\n"
            + str(error)
        )


# ============================================================
# LEER ARCHIVO TXT
# ============================================================

def leer_archivo_txt():

    registros = []

    if (
        archivo_actual is None
        or not archivo_actual.exists()
    ):

        return registros

    try:

        with open(
            archivo_actual,
            "r",
            encoding="utf-8"
        ) as archivo:

            lineas = archivo.readlines()

        inicio = False

        for linea in lineas:

            linea = linea.rstrip("\n")

            if linea == "DATOS":

                inicio = True
                continue

            if not inicio:

                continue

            if not linea.strip():

                continue

            partes = linea.split("\t")

            if tipo_libro_actual == "ingresos":

                if len(partes) >= 5:

                    registros.append({
                        "quien": partes[0],
                        "cliente": partes[1],
                        "procedimiento": partes[2],
                        "precio": partes[3],
                        "pago": partes[4]
                    })

            else:

                if len(partes) >= 3:

                    registros.append({
                        "concepto": partes[0],
                        "valor": partes[1],
                        "pago": partes[2]
                    })

    except Exception as error:

        messagebox.showerror(
            "Error",
            "No se pudo leer el archivo.\n\n"
            + str(error)
        )

    return registros


# ============================================================
# GUARDAR ARCHIVO TXT
# ============================================================

def guardar_txt(
    mostrar_mensaje=False
):

    if (
        tabla is None
        or archivo_actual is None
    ):

        return False

    try:

        filas = []

        for item in tabla.get_children():

            valores = tabla.item(
                item,
                "values"
            )

            if tipo_libro_actual == "ingresos":

                if len(valores) < 6:

                    continue

                datos = [
                    str(valores[1]).strip(),
                    str(valores[2]).strip(),
                    str(valores[3]).strip(),
                    str(valores[4]).strip(),
                    str(valores[5]).strip()
                ]

                if any(datos):

                    filas.append(
                        datos
                    )

            else:

                if len(valores) < 4:

                    continue

                datos = [
                    str(valores[1]).strip(),
                    str(valores[2]).strip(),
                    str(valores[3]).strip()
                ]

                if any(datos):

                    filas.append(
                        datos
                    )

        total = 0

        if tipo_libro_actual == "ingresos":

            indice_valor = 3

        else:

            indice_valor = 1

        for datos in filas:

            valor = datos[
                indice_valor
            ]

            valor = (
                valor
                .replace("$", "")
                .replace(".", "")
                .replace(",", "")
                .strip()
            )

            if valor:

                try:

                    total += float(
                        valor
                    )

                except ValueError:

                    pass

        with open(
            archivo_actual,
            "w",
            encoding="utf-8"
        ) as archivo:

            archivo.write(
                "CONTABILIDAD\n"
            )

            archivo.write(
                "========================================\n"
            )

            if tipo_libro_actual == "ingresos":

                archivo.write(
                    "TIPO: INGRESOS\n"
                )

            else:

                archivo.write(
                    "TIPO: EGRESOS\n"
                )

            archivo.write(
                f"FECHA: "
                f"{dia_actual:02d}/"
                f"{MESES.index(mes_actual)+1:02d}/"
                f"{anio_actual}\n"
            )

            archivo.write(
                f"MES: {mes_actual}\n"
            )

            archivo.write(
                "========================================\n"
            )

            archivo.write(
                "DATOS\n"
            )

            for datos in filas:

                archivo.write(
                    "\t".join(datos)
                    + "\n"
                )

            archivo.write(
                "\n"
            )

            archivo.write(
                "========================================\n"
            )

            archivo.write(
                f"TOTAL DEL DIA: ${total:,.0f}\n"
            )

            archivo.write(
                "========================================\n"
            )

        if mostrar_mensaje:

            messagebox.showinfo(
                "Guardado correcto",
                "Se guardó correctamente."
            )

        return True

    except Exception as error:

        messagebox.showerror(
            "Error al guardar",
            str(error)
        )

        return False


# ============================================================
# ABRIR HOJA TIPO EXCEL
# ============================================================

def abrir_hoja_calculo():

    global tabla

    limpiar_pantalla()

    if tipo_libro_actual == "ingresos":

        columnas = [
            "numero",
            "quien",
            "cliente",
            "procedimiento",
            "precio",
            "pago"
        ]

        nombres = {
            "numero": "N°",
            "quien": "QUIÉN REALIZÓ LA VENTA O EL PROCEDIMIENTO",
            "cliente": "NOMBRE DEL CLIENTE",
            "procedimiento": "PROCEDIMIENTO O VENTA",
            "precio": "VALOR O PRECIO",
            "pago": "MEDIO DE PAGO"
        }

        titulo = (
            f"INGRESOS - "
            f"{mes_actual} "
            f"{anio_actual}"
        )

    else:

        columnas = [
            "numero",
            "concepto",
            "valor",
            "pago"
        ]

        nombres = {
            "numero": "N°",
            "concepto": "DEFINICIÓN",
            "valor": "VALOR",
            "pago": "MEDIO DE PAGO"
        }

        titulo = (
            f"EGRESOS - "
            f"{mes_actual} "
            f"{anio_actual}"
        )

    tk.Label(
        ventana,
        text=titulo,
        font=("Segoe UI", 22, "bold"),
        bg=FONDO,
        fg=NEGRO
    ).pack(
        pady=(15, 2)
    )

    if configuracion.get("negocio"):

        tk.Label(
            ventana,
            text=configuracion["negocio"],
            font=("Segoe UI", 11, "bold"),
            bg=FONDO,
            fg="#56616B"
        ).pack(
            pady=(0, 2)
        )

    tk.Label(
        ventana,
        text=f"DÍA {dia_actual:02d}",
        font=("Segoe UI", 11, "bold"),
        bg=FONDO,
        fg="#56616B"
    ).pack()

    tk.Label(
        ventana,
        text=(
            "Haga doble clic en la celda "
            "que desea editar."
        ),
        font=("Segoe UI", 11, "italic"),
        bg=FONDO,
        fg="#56616B"
    ).pack(
        pady=8
    )

    marco_tabla = tk.Frame(
        ventana,
        bg=ENCABEZADO,
        bd=1,
        relief="solid"
    )

    marco_tabla.pack(
        fill="both",
        expand=True,
        padx=18,
        pady=5
    )

    estilo = ttk.Style()

    try:

        estilo.theme_use(
            "clam"
        )

    except Exception:

        pass

    estilo.configure(
        "Excel.Treeview",
        background=BLANCO,
        foreground="#000000",
        fieldbackground=BLANCO,
        rowheight=30,
        borderwidth=1,
        relief="solid",
        font=("Segoe UI", 10)
    )

    estilo.configure(
        "Excel.Treeview.Heading",
        background=ENCABEZADO,
        foreground="#000000",
        borderwidth=1,
        relief="solid",
        font=("Segoe UI", 10, "bold")
    )

    tabla = ttk.Treeview(
        marco_tabla,
        columns=columnas,
        show="headings",
        style="Excel.Treeview"
    )

    for columna in columnas:

        tabla.heading(
            columna,
            text=nombres[columna]
        )

    if tipo_libro_actual == "ingresos":

        anchos = {
            "numero": 60,
            "quien": 350,
            "cliente": 210,
            "procedimiento": 250,
            "precio": 130,
            "pago": 160
        }

    else:

        anchos = {
            "numero": 60,
            "concepto": 600,
            "valor": 180,
            "pago": 200
        }

    for columna in columnas:

        if columna == "numero":

            alineacion = "center"

        elif columna == "pago":

            alineacion = "center"

        else:

            alineacion = "w"

        tabla.column(
            columna,
            width=anchos[columna],
            anchor=alineacion
        )

    barra_vertical = ttk.Scrollbar(
        marco_tabla,
        orient="vertical",
        command=tabla.yview
    )

    barra_horizontal = ttk.Scrollbar(
        marco_tabla,
        orient="horizontal",
        command=tabla.xview
    )

    tabla.configure(
        yscrollcommand=barra_vertical.set,
        xscrollcommand=barra_horizontal.set
    )

    tabla.grid(
        row=0,
        column=0,
        sticky="nsew"
    )

    barra_vertical.grid(
        row=0,
        column=1,
        sticky="ns"
    )

    barra_horizontal.grid(
        row=1,
        column=0,
        sticky="ew"
    )

    marco_tabla.grid_rowconfigure(
        0,
        weight=1
    )

    marco_tabla.grid_columnconfigure(
        0,
        weight=1
    )

    registros = leer_archivo_txt()

    for numero in range(
        1,
        FILAS + 1
    ):

        if numero <= len(registros):

            registro = (
                registros[
                    numero - 1
                ]
            )

            if tipo_libro_actual == "ingresos":

                valores = (
                    numero,
                    registro.get(
                        "quien",
                        ""
                    ),
                    registro.get(
                        "cliente",
                        ""
                    ),
                    registro.get(
                        "procedimiento",
                        ""
                    ),
                    registro.get(
                        "precio",
                        ""
                    ),
                    registro.get(
                        "pago",
                        ""
                    )
                )

            else:

                valores = (
                    numero,
                    registro.get(
                        "concepto",
                        ""
                    ),
                    registro.get(
                        "valor",
                        ""
                    ),
                    registro.get(
                        "pago",
                        ""
                    )
                )

        else:

            valores = (
                numero,
                *[
                    ""
                    for _ in range(
                        len(columnas) - 1
                    )
                ]
            )

        tabla.insert(
            "",
            "end",
            values=valores
        )

    tabla.bind(
        "<Double-1>",
        editar_celda
    )

    inferior = tk.Frame(
        ventana,
        bg=FONDO
    )

    inferior.pack(
        fill="x",
        padx=18,
        pady=10
    )

    tk.Label(
        inferior,
        text=(
            "500 renglones disponibles "
            "- Guardado automático"
        ),
        font=("Segoe UI", 10),
        bg=FONDO,
        fg="#56616B"
    ).pack(
        side="left"
    )

    marco_acciones = tk.Frame(
        inferior,
        bg=FONDO
    )

    marco_acciones.pack(
        side="right"
    )

    tk.Button(
        marco_acciones,
        text="GUARDAR",
        font=("Segoe UI", 10, "bold"),
        bg=VERDE,
        fg=NEGRO,
        relief="flat",
        cursor="hand2",
        padx=22,
        pady=10,
        command=guardar_desde_tabla
    ).pack(
        side="left",
        padx=5
    )

    boton_devolverse(
        marco_acciones,
        volver_desde_hoja
    )


# ============================================================
# EDITAR CELDA
# ============================================================

def editar_celda(
    event
):

    if tabla is None:

        return

    region = tabla.identify_region(
        event.x,
        event.y
    )

    if region != "cell":

        return

    fila = tabla.identify_row(
        event.y
    )

    columna = tabla.identify_column(
        event.x
    )

    if not fila:

        return

    if columna == "#1":

        return

    datos = tabla.bbox(
        fila,
        columna
    )

    if not datos:

        return

    x, y, ancho, alto = datos

    valor = tabla.set(
        fila,
        columna
    )

    entrada = tk.Entry(
        tabla,
        font=("Segoe UI", 10),
        bg=BLANCO,
        fg=NEGRO
    )

    entrada.place(
        x=x,
        y=y,
        width=ancho,
        height=alto
    )

    entrada.insert(
        0,
        valor
    )

    entrada.focus_set()

    entrada.select_range(
        0,
        tk.END
    )

    terminado = [
        False
    ]

    def terminar(
        event=None
    ):

        if terminado[0]:

            return

        terminado[0] = True

        tabla.set(
            fila,
            columna,
            entrada.get()
        )

        entrada.destroy()

        guardar_txt(
            False
        )

    entrada.bind(
        "<Return>",
        terminar
    )

    entrada.bind(
        "<FocusOut>",
        terminar
    )

    entrada.bind(
        "<Escape>",
        lambda e:
        entrada.destroy()
    )


# ============================================================
# GUARDAR DESDE BOTON
# ============================================================

def guardar_desde_tabla():

    guardar_txt(
        True
    )


# ============================================================
# DEVOLVERSE DESDE HOJA
# ============================================================

def volver_desde_hoja():

    guardar_txt(
        False
    )

    menu_principal()


# ============================================================
# LIBROS ANTERIORES
# ============================================================

def libros_anteriores():

    limpiar_pantalla()

    tk.Label(
        ventana,
        text="LIBROS ANTERIORES",
        font=("Segoe UI", 25, "bold"),
        bg=FONDO,
        fg=NEGRO
    ).pack(
        pady=(30, 5)
    )

    tk.Label(
        ventana,
        text=(
            "Las hojas de cálculo se almacenan automáticamente "
            "en la carpeta de datos de este equipo y se organizan "
            "por año, mes y día."
        ),
        font=("Segoe UI", 11),
        bg=FONDO,
        fg="#56616B",
        wraplength=1050,
        justify="center"
    ).pack(
        pady=(0, 8)
    )

    tk.Label(
        ventana,
        text=(
            "Seleccione el año, mes y día para consultar "
            "los registros guardados."
        ),
        font=("Segoe UI", 11),
        bg=FONDO,
        fg="#56616B"
    ).pack(
        pady=(0, 15)
    )

    marco = tk.Frame(
        ventana,
        bg=FONDO
    )

    marco.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=5
    )

    arbol = ttk.Treeview(
        marco,
        columns=(
            "ruta",
            "tipo"
        ),
        show="tree"
    )

    arbol.heading(
        "#0",
        text="LIBROS GUARDADOS"
    )

    barra = ttk.Scrollbar(
        marco,
        orient="vertical",
        command=arbol.yview
    )

    arbol.configure(
        yscrollcommand=barra.set
    )

    arbol.pack(
        side="left",
        fill="both",
        expand=True
    )

    barra.pack(
        side="right",
        fill="y"
    )

    cargar_carpetas_arbol(
        arbol,
        CARPETA_INGRESOS,
        "INGRESOS"
    )

    cargar_carpetas_arbol(
        arbol,
        CARPETA_EGRESOS,
        "EGRESOS"
    )

    def abrir_libro(
        event
    ):

        item = arbol.focus()

        valores = arbol.item(
            item,
            "values"
        )

        if valores:

            cargar_libro_anterior(
                Path(
                    valores[0]
                ),
                valores[1]
            )

    arbol.bind(
        "<Double-1>",
        abrir_libro
    )

    marco_botones = tk.Frame(
        ventana,
        bg=FONDO
    )

    marco_botones.pack(
        pady=15
    )

    boton_devolverse(
        marco_botones,
        menu_principal
    )


# ============================================================
# CARGAR CARPETAS EN LIBROS ANTERIORES
# ============================================================

def cargar_carpetas_arbol(
    arbol,
    carpeta_base,
    nombre_tipo
):

    if not carpeta_base.exists():

        return

    id_tipo = arbol.insert(
        "",
        "end",
        text=nombre_tipo
    )

    anios = [
        carpeta
        for carpeta in carpeta_base.iterdir()
        if carpeta.is_dir()
    ]

    anios.sort(
        key=lambda x: x.name,
        reverse=True
    )

    for carpeta_anio in anios:

        id_anio = arbol.insert(
            id_tipo,
            "end",
            text=carpeta_anio.name
        )

        for mes in MESES:

            carpeta_mes = (
                carpeta_anio /
                mes
            )

            if not carpeta_mes.exists():

                continue

            id_mes = arbol.insert(
                id_anio,
                "end",
                text=mes
            )

            dias = [
                carpeta
                for carpeta in carpeta_mes.iterdir()
                if carpeta.is_dir()
            ]

            dias.sort(
                key=lambda x: x.name
            )

            for carpeta_dia in dias:

                id_dia = arbol.insert(
                    id_mes,
                    "end",
                    text=carpeta_dia.name
                )

                archivo = (
                    carpeta_dia /
                    "contabilidad.txt"
                )

                if archivo.exists():

                    arbol.insert(
                        id_dia,
                        "end",
                        text=(
                            f"CONTABILIDAD "
                            f"DE {nombre_tipo}"
                        ),
                        values=(
                            str(archivo),
                            (
                                "ingresos"
                                if nombre_tipo
                                == "INGRESOS"
                                else "egresos"
                            )
                        )
                    )


# ============================================================
# CARGAR LIBRO ANTERIOR
# ============================================================

def cargar_libro_anterior(
    archivo,
    tipo
):

    global archivo_actual
    global tipo_libro_actual
    global anio_actual
    global mes_actual
    global dia_actual

    try:

        archivo_actual = archivo

        tipo_libro_actual = tipo

        anio_actual = int(
            archivo.parent.parent.parent.name
        )

        mes_actual = (
            archivo.parent.parent.name
        )

        nombre_dia = (
            archivo.parent.name
        )

        dia_actual = int(
            nombre_dia.split("-")[0]
        )

        abrir_hoja_calculo()

    except Exception as error:

        messagebox.showerror(
            "Error",
            "No se pudo abrir el libro.\n\n"
            + str(error)
        )


# ============================================================
# OBTENER TOTAL DE UN ARCHIVO
# ============================================================

def obtener_total_archivo(
    archivo,
    tipo
):

    if not archivo.exists():

        return 0

    try:

        with open(
            archivo,
            "r",
            encoding="utf-8"
        ) as f:

            lineas = f.readlines()

        for linea in lineas:

            if (
                linea.startswith(
                    "TOTAL DEL DIA:"
                )
            ):

                valor = (
                    linea
                    .replace(
                        "TOTAL DEL DIA:",
                        ""
                    )
                    .replace(
                        "$",
                        ""
                    )
                    .replace(
                        ",",
                        ""
                    )
                    .strip()
                )

                try:

                    return float(
                        valor
                    )

                except ValueError:

                    return 0

    except Exception:

        return 0

    return 0


# ============================================================
# CONTABILIDAD AUTOMATICA
# ============================================================

def contabilidad_automatica():

    limpiar_pantalla()

    anio, mes_numero, dia = (
        fecha_del_pc()
    )

    mes = MESES[
        mes_numero - 1
    ]

    carpeta_dia_ingresos = (
        crear_ruta_libro(
            "ingresos",
            anio,
            mes,
            dia
        )
    )

    carpeta_dia_egresos = (
        crear_ruta_libro(
            "egresos",
            anio,
            mes,
            dia
        )
    )

    archivo_ingresos = (
        carpeta_dia_ingresos
        / "contabilidad.txt"
    )

    archivo_egresos = (
        carpeta_dia_egresos
        / "contabilidad.txt"
    )

    total_ingresos = (
        obtener_total_archivo(
            archivo_ingresos,
            "ingresos"
        )
    )

    total_egresos = (
        obtener_total_archivo(
            archivo_egresos,
            "egresos"
        )
    )

    resultado = (
        total_ingresos
        - total_egresos
    )

    tk.Label(
        ventana,
        text="CONTABILIDAD AUTOMÁTICA",
        font=("Segoe UI", 25, "bold"),
        bg=FONDO,
        fg=NEGRO
    ).pack(
        pady=(40, 20)
    )

    tk.Label(
        ventana,
        text=(
            f"Fecha actual: "
            f"{dia:02d}/"
            f"{mes_numero:02d}/"
            f"{anio}"
        ),
        font=("Segoe UI", 12),
        bg=FONDO,
        fg="#56616B"
    ).pack()

    tk.Label(
        ventana,
        text=(
            f"TOTAL INGRESOS: "
            f"${total_ingresos:,.0f}"
        ),
        font=("Segoe UI", 16, "bold"),
        bg=FONDO,
        fg=NEGRO
    ).pack(
        pady=(25, 5)
    )

    tk.Label(
        ventana,
        text=(
            f"TOTAL EGRESOS: "
            f"${total_egresos:,.0f}"
        ),
        font=("Segoe UI", 16, "bold"),
        bg=FONDO,
        fg=NEGRO
    ).pack(
        pady=5
    )

    tk.Label(
        ventana,
        text=(
            f"RESULTADO DEL DÍA: "
            f"${resultado:,.0f}"
        ),
        font=("Segoe UI", 18, "bold"),
        bg=FONDO,
        fg=NEGRO
    ).pack(
        pady=20
    )

    marco_botones = tk.Frame(
        ventana,
        bg=FONDO
    )

    marco_botones.pack(
        pady=10
    )

    boton_devolverse(
        marco_botones,
        menu_principal
    )


# ============================================================
# CERRAR PROGRAMA
# ============================================================

def cerrar_programa():

    guardado = True

    try:

        if tabla is not None:

            guardado = guardar_txt(
                False
            )

    except Exception:

        guardado = False

    if not guardado:

        continuar = messagebox.askyesno(
            "Guardar antes de salir",
            "No se pudo confirmar el último guardado.\n\n"
            "¿Cerrar de todas formas?"
        )

        if not continuar:

            return

    ventana.destroy()


ventana.protocol(
    "WM_DELETE_WINDOW",
    cerrar_programa
)


# ============================================================
# INICIAR
# ============================================================

if cargar_configuracion():

    menu_principal()

else:

    configuracion_inicial()


ventana.mainloop()