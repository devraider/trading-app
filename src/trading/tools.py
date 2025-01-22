import time
from typing import Optional

from django import forms
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import UploadedFile
from django.utils.text import get_valid_filename

from .settings import MEDIA_ROOT


def save_to_disk(uploaded_file: UploadedFile) -> None:
    """Persist file on the disk at location mentioned in setting for MEDIA.
    To reduce collision of the files we keep original file name, after we secure the name
    and replace risky characters, and then adding current timestamp.
    Args:
        uploaded_file: Files uploaded by the user

    Returns:
        None
    """
    fs = FileSystemStorage(location=MEDIA_ROOT)
    file_name = f"{int(time.time())}-{get_valid_filename(uploaded_file.name)}"
    fs.save(file_name, uploaded_file)


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
