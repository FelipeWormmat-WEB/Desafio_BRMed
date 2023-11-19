from datetime import datetime, timedelta
from django.views.generic import TemplateView
from .models import Currency, Cambio


class ConsultaMoeda(TemplateView):
    template_name = "cambio/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        start_date = self.request.GET.get("start_date")
        end_date = self.request.GET.get("end_date")
        selected_currency = self.request.GET.get("currency")

        # Validar os dados do input
        validation_result = self.validate_input(start_date, end_date, selected_currency)
        if validation_result:
            context["error_message"] = validation_result
            return context

        # Buscar a moeda selecionada
        currency = Currency.objects.filter(symbol=selected_currency).first()
        currency_cambio = (
            Cambio.objects.filter(
                target_currency=currency, date__range=[start_date, end_date]
            )
            .order_by("date")
            .values("date", "price")
        )

        # Converter o valor para o gráfico
        cambio = [
            {
                "date": cambio["date"].strftime("%Y-%m-%d"),
                "price": float(cambio["price"]),
            }
            for cambio in list(currency_cambio)
        ]

        context.update({
            "symbol": currency.symbol if currency else None,
            "cambio": cambio,
            "start_date": start_date,
            "end_date": end_date,
            "selected_currency": selected_currency,
        })

        return context

    def validate_input(self, start_date, end_date, selected_currency):
        if not start_date or not end_date or not selected_currency:
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
