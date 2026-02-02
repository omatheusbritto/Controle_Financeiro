from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

def format_valor(valor):
    """Formata valor para string com vírgula e duas casas decimais."""
    val = Decimal(str(valor)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return str(val).replace(".", ",")

def inserir_registro(cursor, conn, usuario, tipo, categoria, valor, comentario):
    data = datetime.now().strftime("%d/%m/%Y")
    hora = datetime.now().strftime("%H:%M")
    cursor.execute("""
        INSERT INTO registros (usuario, tipo, categoria, valor, comentario, data, hora)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (usuario, tipo, categoria, float(valor), comentario, data, hora))
    conn.commit()

def excluir_registro(cursor, conn, usuario, categoria, valor, data, hora):
    cursor.execute("""
        DELETE FROM registros WHERE usuario=? AND categoria=? AND valor=? AND data=? AND hora=?
    """, (usuario, categoria, valor, data, hora))
    conn.commit()

def listar_registros(cursor, usuario):
    cursor.execute("SELECT * FROM registros WHERE usuario=?", (usuario,))
    return cursor.fetchall()
