[1.0.0] Version inicial del proyecto

Estructura del proyecto:
Sistema_bancario_simulado/
│
├── bank/
│   ├── __init__.py
│   ├── models.py         # Clases Cliente, Cuenta, Transacción
│   └── manager.py        # Lógica del sistema (manejo de clientes, cuentas, transacciones)
│
├── tests/
│   ├── __init__.py
│   ├── test_manager.py   # Pruebas con pytest
│   └── test_models.py
│
├── pdfs/                 # Carpeta donde se guardan los PDFs generados
│
├── generator_pdf.py      # Genera reportes PDF con fpdf2
├── main.py               # Versión del menú por consola
├── requirements.txt      # Dependencias del proyecto
├── README.md             
├── CHANGELOG             # Este archivo
└── .gitignore            # Archivos que no se suben al repositorio

[1.1.0] Version del proyecto con flet
Se agrego main_flet.py
Se actualizo requirements.txt