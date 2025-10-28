Trabajo Práctico Integrador Final – Laboratorio I  Control de versiones

Este proyecto es un simulador de sistema bancario desarrollado en Python, que implementa, manejo de errores con try/except, generación de reportes en PDF y una interfaz por consola tipo menú.

El sistema permite:
>Registrar clientes con usuario y PIN (4 dígitos).
>Crear y gestionar cuentas bancarias por cliente.
>Realizar depósitos, retiros y transferencias entre cuentas.
>Generar reportes PDF con los datos e historial de cada cliente.
>Navegar por un menú en consola (simulando un sistema de cajero o banca online).

Tecnologías utilizadas
>Python 3.13.9
>fpdf2 → generación de PDFs.
>pytest → pruebas unitarias.
>venv → entorno virtual recomendado.

Crear y activar entorno virtual:

Windows (PowerShell):
python -m venv .venv
.venv\Scripts\Activate.ps1

Linux / macOS:
python3 -m venv .venv
source .venv/bin/activate

Instalar dependencias:
pip install -r requirements.txt

Ejecutar programa:
python main.py

Ejecución de tests:
pytest
