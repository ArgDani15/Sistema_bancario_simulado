import pytest
from bank.models import Client, Account


def test_crear_cliente():
    c = Client("Juan", "Perez", "12345678", "juanp", "1234")
    assert c.validar_pin("1234")
    assert not c.validar_pin("0000")


def test_cuenta_deposito_y_retiro():
    c = Client("Ana", "Lopez", "98765432", "anita", "4321")
    cuenta = Account(1, "mi_alias", c)
    cuenta.depositar(100)
    assert cuenta.saldo == 100
    cuenta.retirar(50)
    assert cuenta.saldo == 50


def test_transferencia():
    c1 = Client("A", "B", "1", "u1", "1111")
    c2 = Client("C", "D", "2", "u2", "2222")
    a1 = Account(1, "alias1", c1)
    a2 = Account(2, "alias2", c2)
    a1.depositar(200)
    a1.transferir(100, a2)
    assert a1.saldo == 100
    assert a2.saldo == 100
