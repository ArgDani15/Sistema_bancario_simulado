from bank.models import Client, Account
import random


class BankManager:
    def __init__(self):
        self.clientes = []
        self.cuentas = []

    def crear_cliente(self, nombre, apellido, dni, usuario, pin):
        if any(c.usuario == usuario for c in self.clientes):
            raise ValueError("El usuario ya existe.")
        cliente = Client(nombre, apellido, dni, usuario, pin)
        self.clientes.append(cliente)
        return cliente

    def buscar_cliente(self, usuario):
        for cliente in self.clientes:
            if cliente.usuario == usuario:
                return cliente
        return None

    def generar_numero_unico(self):
        import random
        while True:
            numero = random.randint(100000, 999999)
            if all(c.numero != numero for c in self.cuentas):
                return numero

    def crear_cuenta(self, cliente, alias):
        numero = self.generar_numero_unico()
        cuenta = Account(numero, alias, cliente)
        cliente.cuentas.append(cuenta)
        self.cuentas.append(cuenta)
        return cuenta


    def buscar_cuenta_por_alias(self, alias):
        return [c for c in self.cuentas if c.alias == alias]

    def listar_clientes(self):
        if not self.clientes:
            return "No hay clientes registrados."
        texto = ""
        for idx, c in enumerate(self.clientes, 1):
            texto += f"{idx}. {c.usuario} - {c.nombre} {c.apellido} - DNI: {c.dni}\n"
        return texto.strip()
