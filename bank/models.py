from datetime import datetime


class Client:
    def __init__(self, nombre: str, apellido: str, dni: str, usuario: str, pin: str):
        self.__nombre = nombre
        self.__apellido = apellido
        self.__dni = dni
        self.__usuario = usuario
        self.__pin = pin
        self.cuentas = []

    # Encapsulamiento: getters y setters seguros
    @property
    def nombre(self):
        return self.__nombre

    @property
    def apellido(self):
        return self.__apellido

    @property
    def dni(self):
        return self.__dni

    @property
    def usuario(self):
        return self.__usuario

    def validar_pin(self, pin: str) -> bool:
        return self.__pin == pin

    def mostrar_datos(self):
        return f"{self.__nombre} {self.__apellido} - DNI: {self.__dni} - Usuario: {self.__usuario}"


class Account:
    def __init__(self, numero: int, alias: str, cliente: Client):
        self.numero = numero
        self.alias = alias
        self.saldo = 0.0
        self.cliente = cliente
        self.transacciones = []

    def depositar(self, monto: float):
        if monto <= 0:
            raise ValueError("El monto debe ser mayor a cero.")
        self.saldo += monto
        self.transacciones.append(Deposit(monto))

    def retirar(self, monto: float):
        if monto <= 0:
            raise ValueError("El monto debe ser mayor a cero.")
        if monto > self.saldo:
            raise ValueError("Saldo insuficiente.")
        self.saldo -= monto
        self.transacciones.append(Withdrawal(monto))

    def transferir(self, monto: float, destino):
        if monto <= 0:
            raise ValueError("El monto debe ser mayor a cero.")
        if monto > self.saldo:
            raise ValueError("Saldo insuficiente.")
        if destino == self:
            raise ValueError("No se puede transferir a la misma cuenta.")
        self.saldo -= monto
        destino.saldo += monto
        self.transacciones.append(Transfer(monto, destino.alias))

    def __str__(self):
        return f"N°: {self.numero} | Alias: {self.alias} | Saldo: ${self.saldo:.2f}"


class Transaction:
    def __init__(self, tipo: str, monto: float):
        self.tipo = tipo
        self.monto = monto
        self.fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def __str__(self):
        return f"{self.fecha} - {self.tipo}: ${self.monto:.2f}"


class Deposit(Transaction):
    def __init__(self, monto):
        super().__init__("Depósito", monto)


class Withdrawal(Transaction):
    def __init__(self, monto):
        super().__init__("Retiro", monto)


class Transfer(Transaction):
    def __init__(self, monto, destino_alias):
        super().__init__(f"Transferencia a {destino_alias}", monto)
