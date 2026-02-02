from decimal import Decimal, ROUND_HALF_UP

def calcular_saldo(registros):
    """Calcula saldo total usando Decimal para precisão."""
    saldo = Decimal("0.00")
    for r in registros:
        valor = Decimal(str(r[4])).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        if r[2] == "Entrada":
            saldo += valor
        else:
            saldo -= valor
    return saldo
