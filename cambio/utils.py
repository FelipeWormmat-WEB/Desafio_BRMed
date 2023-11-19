from datetime import datetime, timedelta

from .models import Currency, Cambio


def validate_input(start_date, end_date, selected_currencie):
    if not start_date or not end_date or not selected_currencie:
        return "Por favor, selecione data inicial, final e a moeda."

    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

    if end_date > datetime.today().date():
        return "A data final não pode ser maior do que o dia de hoje"

    if start_date > end_date:
        return "A data de inicial não pode ser maior que a data final."

    total_days = (end_date - start_date).days
    business_days = sum(
        1
        for day in range(total_days + 1)
        if (start_date + timedelta(days=day)).weekday() < 5
    )

    if business_days > 5:
        return "O período informado deve ser de no máximo 5 dias úteis."

    return None


def fetch_currency_cambio(start_date, end_date, selected_currencie):
    currency = Currency.objects.filter(symbol=selected_currencie).first()
    print(f"Currency: {currency}")
    currency_cambio = (
        Cambio.objects.filter(
            target_currency=currency, date__range=[start_date, end_date]
        )
        .order_by("date")
        .values("date", "price")
    )
    print(f"Cambio: {currency_cambio}")

    # Convertendo os valores para o formato adequado para o gráfico
    cambio = [
        {
            "date": cambio["date"].strftime("%Y-%m-%d"),
            "price": float(cambio["price"]),
        }
        for cambio in list(currency_cambio)
    ]

    return currency, cambio
