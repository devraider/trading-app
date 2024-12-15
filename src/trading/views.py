import logging

import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from .repository.positions import DailyNetPositionRepo
from .repository.tranzactions import TransactionRepo
from .services.trading_processor import TradingProcessor
from .tools import TextFileUploadForm, save_to_disk

log = logging.getLogger("root")


def welcome(request) -> HttpResponse:
    """Renders Welcome page
    Args:
        request: Request context

    Returns:
        Http response containing formatted html
    """
    return render(request, "welcome.html")


class TradingProcessorView(View):
    """
    View for processing trading files.
    The context of this view contains `form`, `table_data` and `error`.
    None:
        - `form`: is a custom class form class with file type validation
        - `table_data`: are table rows to be shown after file is uploaded to let user confirm that
        uploaded file contains required data
        - `error`: Any errors to be shown in HTML
    """

    @staticmethod
    def get(request) -> HttpResponse:
        """Get method of trading file processor
        A method to render the HTML template for Trading processor.
        Args:
            request: Request context

        Returns:
            HTTP response containing HTML file.
        """
        form = TextFileUploadForm()
        return render(
            request,
            "trade_processor.html",
            context={
                "form": form,
                "transactions": pd.DataFrame(),
                "daily_net": pd.DataFrame(),
                "error": None,
            },
        )

    @staticmethod
    def post(request):
        """Validate and process file.
        Validate file by using our custom method implemented in the TextFileUploadForm
        and decide whether to move forward or no based on file details.
        Once file validation we proceed further, to validate file content and processing the file
        to be shown to the user for final confirmation.
        Args:
            request: Request context

        Returns:
            HTTP response containing HTML file.
        """
        form = TextFileUploadForm(request.POST, request.FILES)
        context = {
            "form": form,
            "transactions": pd.DataFrame(),
            "daily_net": pd.DataFrame(),
            "error": None,
        }

        # file validation
        if not form.is_valid() or form.cleaned_data["file"] is None:
            context["error"] = "Invalid file type. Please use an `xlsx` file."
            log.info(context["error"])
            return render(request, "trade_processor.html", context=context)
        uploaded_file = form.cleaned_data["file"]

        # persist file on disk
        save_to_disk(uploaded_file)

        # persist transaction in database
        transactions_repo = TransactionRepo()
        positions_repo = DailyNetPositionRepo()
        tp = TradingProcessor.from_excel(uploaded_file)

        tp.save(transactions_repo)
        tp.save_daily_net(positions_repo)

        # TODO: Implement Pydantic or other validation method to check data consistency
        context["transactions"] = tp.df
        context["daily_net"] = tp.calc_daily_net()

        return render(request, "trade_processor.html", context=context)
