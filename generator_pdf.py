import os
from fpdf import FPDF
from datetime import datetime


def generar_pdf(cliente):
    os.makedirs("pdfs", exist_ok=True)
    nombre_archivo = f"pdfs/{cliente.dni} - {cliente.nombre} {cliente.apellido} - {datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Datos del Cliente", ln=True, align="C")

    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 10, f"Nombre: {cliente.nombre} {cliente.apellido}", ln=True)
    pdf.cell(0, 10, f"DNI: {cliente.dni}", ln=True)
    pdf.cell(0, 10, f"Usuario: {cliente.usuario}", ln=True)
    pdf.ln(10)

    for cuenta in cliente.cuentas:
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, f"Cuenta N° {cuenta.numero} - Alias: {cuenta.alias}", ln=True)
        pdf.set_font("Helvetica", "", 12)
        pdf.cell(0, 10, f"Saldo actual: ${cuenta.saldo:.2f}", ln=True)
        pdf.cell(0, 10, "Historial de transacciones:", ln=True)
        if not cuenta.transacciones:
            pdf.cell(0, 10, "  Sin movimientos.", ln=True)
        else:
            for t in cuenta.transacciones:
                pdf.cell(0, 8, f"  - {t}", ln=True)
        pdf.ln(5)

    pdf.output(nombre_archivo)
    return nombre_archivo
