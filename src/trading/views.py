import logging
from typing import Any

import pandas as pd
from django import forms
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from .services.trading_processor import TradingProcessor

log = logging.getLogger("root")


def welcome(request) -> HttpResponse:
    """Renders Welcome page
    Args:
        request: Request context

    Returns:
        Http response containing formatted html
    """
    return render(request, "welcome.html")


class TextFileUploadForm(forms.Form):
    """
    Custom text and file upload.
    Help us to enforce file checking.
    """

    file = forms.FileField()

    def clean_file(self) -> Any:
        """Check whether the file is present and if type of the file is `xlsx`.
        Returns:
            File after checking.
        """
        uploaded_file = self.cleaned_data["file"]
        if (
            uploaded_file.content_type
            != "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ):
            raise forms.ValidationError("Only text files are allowed.")
        return uploaded_file


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
            {"form": form, "table_data": pd.DataFrame(), "error": None},
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
        action = request.POST.get("action")
        form = TextFileUploadForm(request.POST, request.FILES)
        table_data = pd.DataFrame()
        error = None

        # file validation
        if form.is_valid():
            try:
                uploaded_file = form.cleaned_data["file"]
                log.debug("Files type checked successfully.")

                table_data = TradingProcessor.from_excel(uploaded_file).df

            except Exception as e:
                error = "An error occurred while processing the file."
                log.error(f"Exception for uploaded file: {e}")
        else:
            error = "Invalid file format. Only xlsx files are allowed."
            log.info(error)
        # File content validation

        # File content prepare for persisting into database
        if action == "confirmed":
            error = table_data = None
            log.info("Proceed for file saving on disc and persist data into database.")

        return render(
            request,
            "trade_processor.html",
            {"form": form, "table_data": table_data, "error": error},
        )
