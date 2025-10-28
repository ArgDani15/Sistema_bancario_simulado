from bank.manager import BankManager
from generator_pdf import generar_pdf

def main():
    banco = BankManager()

    while True:
        print("\n=== Sistema Bancario ===")
        print("1. Ingresar")
        print("2. Crear cliente")
        print("3. Ver clientes")
        print("4. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            if not banco.clientes:
                print("No hay clientes registrados.")
                continue

            usuario = input("Usuario: ")
            pin = input("Pin: ")
            cliente = banco.buscar_cliente(usuario)

            if not cliente or not cliente.validar_pin(pin):
                print("Usuario o PIN incorrecto.")
                continue

            menu_cliente(banco, cliente)

        elif opcion == "2":
            crear_cliente(banco)

        elif opcion == "3":
            print(banco.listar_clientes())

        elif opcion == "4":
            print("Saliendo...")
            break

        else:
            print("Opción no válida.")


def crear_cliente(banco):
    try:
        nombre = input("Nombre: ").strip()
        apellido = input("Apellido: ").strip()
        dni = input("DNI: ").strip()
        usuario = input("Usuario: ").strip()
        pin = input("Pin (4 dígitos): ").strip()

        if not pin.isdigit() or len(pin) != 4:
            raise ValueError("El PIN debe tener exactamente 4 dígitos numéricos.")

        cliente = banco.crear_cliente(nombre, apellido, dni, usuario, pin)
        print(f"Cliente creado exitosamente: {cliente.mostrar_datos()}")

    except Exception as e:
        print(f"Error: {e}")


def menu_cliente(banco, cliente):
    while True:
        print(f"\n=== Cliente: {cliente.nombre} {cliente.apellido} ===")
        print("1. Ingresar a cuentas")
        print("2. Crear cuenta")
        print("3. Imprimir datos (PDF)")
        print("4. Cerrar sesión")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            if not cliente.cuentas:
                print("No hay cuentas registradas.")
                continue
            menu_cuentas(banco, cliente)

        elif opcion == "2":
            alias = input("Alias para la nueva cuenta: ")
            cuenta = banco.crear_cuenta(cliente, alias)
            print(f"Cuenta creada con N° {cuenta.numero} - Alias: {alias}")

        elif opcion == "3":
            path = generar_pdf(cliente)
            print(f"PDF generado: {path}")

        elif opcion == "4":
            print("Sesión cerrada.")
            break

        else:
            print("Opción no válida.")


def menu_cuentas(banco, cliente):
    for i, c in enumerate(cliente.cuentas, 1):
        print(f"{i}. {c}")
    try:
        idx = int(input("Seleccione una cuenta: ")) - 1
        if idx < 0 or idx >= len(cliente.cuentas):
            raise IndexError
        menu_transacciones(banco, cliente.cuentas[idx], banco)
    except Exception:
        print("Selección inválida.")


def menu_transacciones(banco, cuenta, _):
    while True:
        print(f"\n=== Cuenta {cuenta.numero} ===")
        print(f"Saldo: ${cuenta.saldo:.2f}")
        print("1. Ingresar dinero")
        print("2. Retirar dinero")
        print("3. Transferir")
        print("4. Volver")

        opcion = input("Opción: ")

        try:
            if opcion == "1":
                monto = float(input("Monto a ingresar: "))
                cuenta.depositar(monto)
                print(f"Depósito exitoso. Saldo actual: ${cuenta.saldo:.2f}")

            elif opcion == "2":
                monto = float(input("Monto a retirar: "))
                cuenta.retirar(monto)
                print(f"Retiro exitoso. Saldo actual: ${cuenta.saldo:.2f}")

            elif opcion == "3":
                alias_destino = input("Alias destino: ")
                destinos = banco.buscar_cuenta_por_alias(alias_destino)
                if not destinos:
                    print("No se encontró cuenta con ese alias.")
                    continue

                if len(destinos) > 1:
                    print("Cuentas disponibles:")
                    for i, d in enumerate(destinos, 1):
                        print(f"{i}. {d.alias} - N° {d.numero} - {d.cliente.nombre} {d.cliente.apellido}")
                    sel = int(input("Seleccione el destino: ")) - 1
                    destino = destinos[sel]
                else:
                    destino = destinos[0]

                monto = float(input("Monto a transferir: "))
                cuenta.transferir(monto, destino)
                print("Transferencia realizada con éxito.")

            elif opcion == "4":
                break

            else:
                print("Opción inválida.")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
