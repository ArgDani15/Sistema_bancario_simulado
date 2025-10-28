import pytest
from bank.manager import BankManager


def test_crear_y_buscar_cliente():
    banco = BankManager()
    banco.crear_cliente("Juan", "Perez", "123", "jp", "1111")
    cliente = banco.buscar_cliente("jp")
    assert cliente is not None
    assert cliente.usuario == "jp"


def test_crear_cuenta():
    banco = BankManager()
    c = banco.crear_cliente("Ana", "Lopez", "456", "anita", "2222")
    cuenta = banco.crear_cuenta(c, "alias_ana")
    assert cuenta in c.cuentas
