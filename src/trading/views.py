import logging
import time
from typing import Optional

import pandas as pd
from django import forms
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import UploadedFile
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.text import get_valid_filename
from django.views import View

from .repository.tranzactions import PsqlTransactionRepo
from .services.trading_processor import TradingProcessor
from .settings import MEDIA_ROOT

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

    def clean_file(self) -> Optional[UploadedFile]:
        """Check whether the file is present and if type of the file is `xlsx`.
        Returns:
            File after checking.
        """
        uploaded_file = self.cleaned_data["file"]
        if (
            uploaded_file.content_type
            != "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ):
            # raise forms.ValidationError("Only text files are allowed.")
            return None
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
        form = TextFileUploadForm(request.POST, request.FILES)
        context = {"form": form, "table_data": pd.DataFrame(), "error": None}

        # file validation
        if not form.is_valid() or form.cleaned_data["file"] is None:
            context["error"] = "Invalid file type. Please use an `xlsx` file."
            log.info(context["error"])
            return render(request, "trade_processor.html", context=context)

        uploaded_file = form.cleaned_data["file"]

        # persist file on disk
        fs = FileSystemStorage(location=MEDIA_ROOT)
        file_name = f"{int(time.time())}-{get_valid_filename(uploaded_file.name)}"
        fs.save(file_name, uploaded_file)

        # persist transaction in database
        tp = TradingProcessor.from_excel(uploaded_file)

        tp.save(PsqlTransactionRepo)

        # TODO: Implement Pydantic or other validation method to check data consistency
        context["table_data"] = tp.df

        return render(request, "trade_processor.html", context=context)
