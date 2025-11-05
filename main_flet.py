# main_flet.py
from typing import Optional, List
import flet
from flet import (
    Page, Column, Row, Text, TextField, ElevatedButton, ListTile, IconButton,
    Icons, SnackBar
)
import traceback
from bank.manager import BankManager
from generator_pdf import generar_pdf

# ---------------- Manager global ----------------
manager = BankManager()

# ---------- Utilidades ----------
def show_snack(page: Page, text: str):
    try:
        page.snack_bar = SnackBar(Text(text))
        page.snack_bar.open = True
        page.update()
    except Exception:
        # fallback sencillo
        print("SNACK:", text)

def safe_float(val: str) -> Optional[float]:
    try:
        return float(val)
    except Exception:
        return None

# ---------- Wrappers para compatibilidad con distintas APIs de BankManager ----------
def wrap_create_client(first, last, dni, username, pin):
    try:
        if hasattr(manager, "create_client"):
            return manager.create_client(first, last, dni, username, pin)
        if hasattr(manager, "crear_cliente"):
            return manager.crear_cliente(first, last, dni, username, pin)
        raise AttributeError("El gestor no expone método de creación de cliente esperado.")
    except Exception:
        raise

def wrap_get_clients() -> List:
    """Devuelve la lista de clientes"""
    if hasattr(manager, "clients") and callable(getattr(manager, "clients")):
        return manager.clients()
    if hasattr(manager, "clientes"):
        attr = getattr(manager, "clientes")
        if callable(attr):
            return attr()
        return attr
    # fallback: inspeccionar atributos
    for name in ("_clients", "_clientes", "clients_list"):
        if hasattr(manager, name):
            return getattr(manager, name)
    return []

def wrap_find_client_by_username(username: str):
    """Busca cliente por username con distintos nombres de método."""
    if hasattr(manager, "find_client_by_username"):
        return manager.find_client_by_username(username)
    if hasattr(manager, "find_client"):
        return manager.find_client(username)
    if hasattr(manager, "buscar_cliente"):
        return manager.buscar_cliente(username)
    # si no hay método, hacer búsqueda manual sobre wrap_get_clients
    for c in wrap_get_clients():
        uname = getattr(c, "username", None) or getattr(c, "usuario", None)
        if uname == username:
            return c
    return None

def wrap_create_account_for_client(client, alias: str):
    if hasattr(manager, "create_account_for_client"):
        return manager.create_account_for_client(client, alias)
    if hasattr(manager, "crear_cuenta"):
        return manager.crear_cuenta(client, alias)
    raise AttributeError("El gestor no expone método para crear cuenta.")

def wrap_find_accounts_by_alias(alias: str):
    if hasattr(manager, "find_accounts_by_alias"):
        return manager.find_accounts_by_alias(alias)
    if hasattr(manager, "find_account_by_alias"):
        return manager.find_account_by_alias(alias)
    if hasattr(manager, "buscar_cuenta_por_alias"):
        return manager.buscar_cuenta_por_alias(alias)
    # fallback: buscar manualmente
    res = []
    for c in wrap_get_clients():
        accs = getattr(c, "accounts", None)
        if callable(accs):
            accs = accs()
        if not accs:
            accs = getattr(c, "_accounts", []) or getattr(c, "cuentas", []) or getattr(c, "accounts", [])
        for a in accs:
            if getattr(a, "alias", None) == alias:
                res.append(a)
    return res

# ---------- Vistas (menús) ----------
def view_main_menu(page: Page):
    page.controls.clear()
    page.add(Text("Bienvenido al sistema bancario", size=20))
    page.add(ElevatedButton("Ingresar", on_click=lambda e: view_login_menu(page)))
    page.add(ElevatedButton("Crear cliente", on_click=lambda e: view_create_client(page)))
    page.add(ElevatedButton("Ver clientes", on_click=lambda e: view_list_clients(page)))
    page.add(ElevatedButton("Salir", on_click=lambda e: page.window_close()))
    page.update()

# --- Login ---
def view_login_menu(page: Page):
    page.controls.clear()
    page.add(Text("Ingreso de usuario", size=18))
    username = TextField(label="Usuario", width=300)
    pin = TextField(label="PIN (4 dígitos)", password=True, width=200)

    def on_login(e):
        try:
            u = username.value.strip()
            p = pin.value.strip()
            if not u or not p:
                show_snack(page, "Completar todos los campos")
                return
            client = wrap_find_client_by_username(u)
            if not client:
                show_snack(page, "Usuario no encontrado")
                return
            # método verify_pin o validar_pin
            verify = getattr(client, "verify_pin", None) or getattr(client, "validar_pin", None)
            if not verify:
                show_snack(page, "El objeto cliente no expone verificación de PIN.")
                return
            if not verify(p):
                show_snack(page, "PIN incorrecto")
                return
            view_client_menu(page, client)
        except Exception:
            traceback.print_exc()
            show_snack(page, "Error interno al intentar ingresar (ver consola).")

    # Volver arriba para mayor visibilidad
    page.add(Row([ElevatedButton("Volver", on_click=lambda e: view_main_menu(page))]))
    page.add(username, pin)
    page.add(Row([ElevatedButton("Ingresar", on_click=on_login)]))
    page.update()

# --- Crear cliente ---
def view_create_client(page: Page):
    global manager
    page.controls.clear()
    page.add(Text("Crear cliente", size=18))
    first = TextField(label="Nombre", width=300)
    last = TextField(label="Apellido", width=300)
    dni = TextField(label="DNI", width=200)
    username = TextField(label="Nombre de usuario", width=200)
    pin = TextField(label="PIN (4 dígitos)", width=100, password=True)

    def on_register(e):
        try:
            f = first.value.strip()
            l = last.value.strip()
            d = dni.value.strip()
            u = username.value.strip()
            p = pin.value.strip()
            if not all([f, l, d, u, p]):
                show_snack(page, "Todos los campos son obligatorios")
                return
            if not (p.isdigit() and len(p) == 4):
                show_snack(page, "PIN debe ser numérico y 4 dígitos")
                return
            # usa wrapper que intenta distintos nombres
            wrap_create_client(f, l, d, u, p)
            show_snack(page, f"Cliente {f} {l} creado")
            page.update()
            view_main_menu(page)
        except Exception as ex:
            traceback.print_exc()
            show_snack(page, f"Error al crear cliente: {ex}")

    # Volver arriba y abajo para asegurar visibilidad
    page.add(Row([ElevatedButton("Volver", on_click=lambda e: view_main_menu(page))]))
    page.add(first, last, dni, username, pin)
    page.add(Row([ElevatedButton("Registrar cliente", on_click=on_register)]))
    page.add(Row([ElevatedButton("Volver", on_click=lambda e: view_main_menu(page))]))
    page.update()

# --- Listar clientes ---
def view_list_clients(page: Page):
    page.controls.clear()
    page.add(Row([ElevatedButton("Volver", on_click=lambda e: view_main_menu(page))]))  # botón arriba
    page.add(Text("Lista de clientes", size=18))
    try:
        clients = wrap_get_clients()
    except Exception:
        traceback.print_exc()
        clients = []

    if not clients:
        page.add(Text("No hay clientes."))
        page.add(ElevatedButton("Volver", on_click=lambda e: view_main_menu(page)))  # botón abajo
        page.update()
        return

    col = Column()
    for c in clients:
        try:
            uname = getattr(c, "username", None) or getattr(c, "usuario", None) or "<sin usuario>"
            fullname = getattr(c, "full_name", None)
            if callable(fullname):
                fullname = fullname()
            else:
                fullname = fullname or (getattr(c, "first_name", "") + " " + getattr(c, "last_name", ""))
            subtitle = f"{len(getattr(c, 'accounts', [])() if callable(getattr(c, 'accounts', None)) else (getattr(c, 'accounts', []) or getattr(c, '_accounts', []) or getattr(c, 'cuentas', [])) )} cuentas - DNI: {getattr(c, 'dni', getattr(c, 'dni', ''))}"
        except Exception:
            fullname = str(c)
            uname = getattr(c, "username", None) or getattr(c, "usuario", None)
            subtitle = ""

        # capturar variable en lambda con cli=c
        enter_btn = ElevatedButton("Entrar", on_click=lambda e, cli=c: view_client_menu(page, cli))
        tile_row = Row([Text(f"{uname} - {fullname}", expand=True), enter_btn])
        col.controls.append(tile_row)

    page.add(col)
    page.add(ElevatedButton("Volver", on_click=lambda e: view_main_menu(page)))  # botón final
    page.update()

# --- Menú cliente ---
def view_client_menu(page: Page, client):
    page.controls.clear()
    # safe obtener nombre
    try:
        fullname = client.full_name() if callable(getattr(client, "full_name", None)) else (getattr(client, "full_name", None) or f"{getattr(client,'first_name','')} {getattr(client,'last_name','')}")
    except Exception:
        fullname = str(client)
    page.add(Row([ElevatedButton("Volver", on_click=lambda e: view_main_menu(page))]))  # botón arriba
    page.add(Text(f"Sesión: {fullname}", size=18))
    page.add(ElevatedButton("Ingresar a cuentas", on_click=lambda e: view_accounts_list(page, client)))
    page.add(ElevatedButton("Crear cuenta", on_click=lambda e: view_create_account(page, client)))
    page.add(ElevatedButton("Imprimir datos (PDF)", on_click=lambda e: generar_pdf(client)))
    page.add(ElevatedButton("Cerrar sesión", on_click=lambda e: view_main_menu(page)))
    page.update()

# --- Crear cuenta ---
def view_create_account(page: Page, client):
    page.controls.clear()
    page.add(Row([ElevatedButton("Volver", on_click=lambda e: view_client_menu(page, client))]))
    page.add(Text(f"Crear cuenta para {client.full_name() if callable(getattr(client,'full_name',None)) else client}"))
    alias_field = TextField(label="Alias de la cuenta", width=300)

    def on_create(e):
        try:
            alias = alias_field.value.strip()
            if not alias:
                show_snack(page, "Alias obligatorio")
                return
            wrap_create_account_for_client(client, alias)
            show_snack(page, f"Cuenta creada para {client}")
            view_client_menu(page, client)
        except Exception:
            traceback.print_exc()
            show_snack(page, "Error creando cuenta (ver consola).")

    page.add(alias_field)
    page.add(Row([ElevatedButton("Crear", on_click=on_create)]))
    page.add(Row([ElevatedButton("Volver", on_click=lambda e: view_client_menu(page, client))]))
    page.update()

# --- Listado de cuentas ---
def get_client_accounts(client):
    accs = getattr(client, "accounts", None)
    if callable(accs):
        return accs()
    # intentar atributos en español/privados
    return getattr(client, "_accounts", None) or getattr(client, "cuentas", None) or []

def view_accounts_list(page: Page, client):
    page.controls.clear()
    page.add(Row([ElevatedButton("Volver", on_click=lambda e: view_client_menu(page, client))]))
    page.add(Text(f"Cuentas de {getattr(client,'full_name', lambda: str(client))()}", size=16) if callable(getattr(client,'full_name', None)) else Text(f"Cuentas de {client}"))
    accs = get_client_accounts(client)
    if not accs:
        page.add(Text("El cliente no tiene cuentas."))
        page.add(ElevatedButton("Volver", on_click=lambda e: view_client_menu(page, client)))
        page.update()
        return
    col = Column()
    for i, a in enumerate(accs, start=1):
        btn = ElevatedButton("Abrir", on_click=lambda e, acc=a: view_account_menu(page, client, acc))
        col.controls.append(Row([Text(f"{i}. N° {getattr(a,'account_number', getattr(a,'numero', ''))} - Alias: {getattr(a,'alias','') } - Saldo: ${getattr(a,'balance', getattr(a,'saldo',0)):.2f}", expand=True), btn]))
    page.add(col)
    page.add(ElevatedButton("Volver", on_click=lambda e: view_client_menu(page, client)))
    page.update()

# --- Menú transacciones ---
def view_account_menu(page: Page, client, account):
    page.controls.clear()
    page.add(Row([ElevatedButton("Volver", on_click=lambda e: view_accounts_list(page, client))]))
    page.add(Text(f"Cuenta {getattr(account,'account_number', getattr(account,'numero',''))} - {getattr(account,'alias','')}", size=16))
    balance = getattr(account, "balance", getattr(account, "saldo", 0.0))
    page.add(Text(f"Saldo: ${balance:.2f}"))
    amt_field = TextField(label="Monto", width=200)

    def on_deposit(e):
        try:
            amt = safe_float(amt_field.value or "")
            if amt is None or amt <= 0:
                show_snack(page, "Monto inválido")
                return
            # deposit puede llamarse deposit o depositar
            if hasattr(account, "deposit"):
                account.deposit(amt)
            elif hasattr(account, "depositar"):
                account.depositar(amt)
            else:
                raise AttributeError("Método de depósito no disponible.")
            show_snack(page, "Depósito realizado")
            view_account_menu(page, client, account)
        except Exception:
            traceback.print_exc()
            show_snack(page, "Error en depósito (ver consola).")

    def on_withdraw(e):
        try:
            amt = safe_float(amt_field.value or "")
            if amt is None or amt <= 0:
                show_snack(page, "Monto inválido")
                return
            if hasattr(account, "withdraw"):
                account.withdraw(amt)
            elif hasattr(account, "retirar"):
                account.retirar(amt)
            else:
                raise AttributeError("Método de retiro no disponible.")
            show_snack(page, "Retiro realizado")
            view_account_menu(page, client, account)
        except Exception:
            traceback.print_exc()
            show_snack(page, "Error en retiro (ver consola).")

    page.add(Row([amt_field, ElevatedButton("Ingresar monto", on_click=on_deposit), ElevatedButton("Retirar monto", on_click=on_withdraw)]))
    page.add(ElevatedButton("Transferir", on_click=lambda e: view_transfer_menu(page, client, account)))
    page.add(ElevatedButton("Volver", on_click=lambda e: view_accounts_list(page, client)))
    page.update()

# --- Transferencias ---
def view_transfer_menu(page: Page, client, account):
    page.controls.clear()
    page.add(Row([ElevatedButton("Volver", on_click=lambda e: view_account_menu(page, client, account))]))
    page.add(Text(f"Transferir desde cuenta {getattr(account,'account_number', getattr(account,'numero',''))}", size=16))
    alias_field = TextField(label="Alias de destino", width=200)
    amount_field = TextField(label="Monto a transferir", width=200)

    def on_transfer(e):
        try:
            alias = alias_field.value.strip()
            amt = safe_float(amount_field.value or "")
            if not alias or amt is None or amt <= 0:
                show_snack(page, "Datos inválidos")
                return
            matches = wrap_find_accounts_by_alias(alias)
            if not matches:
                show_snack(page, "Alias no encontrado")
                return
            # si hay varias, tomo la primera (podemos mejorar con elección)
            dest_acc = matches[0] if isinstance(matches, (list,tuple)) else matches
            # transfer puede llamarse transfer_to o transferir
            if hasattr(account, "transfer_to"):
                account.transfer_to(dest_acc, amt)
            elif hasattr(account, "transferir"):
                account.transferir(amt, dest_acc)
            else:
                raise AttributeError("Método de transferencia no disponible.")
            show_snack(page, "Transferencia realizada")
            view_account_menu(page, client, account)
        except Exception:
            traceback.print_exc()
            show_snack(page, "Error en transferencia (ver consola).")

    page.add(alias_field)
    page.add(amount_field)
    page.add(Row([ElevatedButton("Transferir", on_click=on_transfer), ElevatedButton("Volver", on_click=lambda e: view_account_menu(page, client, account))]))
    page.update()

# ---------- Entrada de la app ----------
def main(page: Page):
    page.title = "Sistema Bancario - Flet"
    view_main_menu(page)

if __name__ == "__main__":
    flet.app(target=main)
