import json
import os
import logging
from typing import Any
from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse
from starlette.background import BackgroundTasks
from .routes import RENDER_FILE
from config import config
from tempfile import NamedTemporaryFile
from services.documents_processor import WordDocumentProcessor
from utils.doc_utils import generate_file_name, delete_file
from constants import (
    OUTPUT_EXTENSION,
    OUTPUT_NAME_PREFIX,
    DOWNLOAD_NAME,
    PDF_MIME_TYPE,
    INTERMEDIATE_NAME,
    INTERMEDIATE_FILE_EXTENSION,
)

route = APIRouter(tags=["document"])


#  i didn't test it yet
@route.post(RENDER_FILE)
def file_render(*, ph: str, background_task: BackgroundTasks) -> Any:
    parsed_ph = json.loads(ph)
    output_file_name = generate_file_name(OUTPUT_NAME_PREFIX, OUTPUT_EXTENSION)

    pdf_path = os.path.join(config.STORAGE_PATH, output_file_name)

    with NamedTemporaryFile(delete=False) as temp_file:
        replaced_path = os.path.join(
            config.STORAGE_PATH,
            generate_file_name(INTERMEDIATE_NAME, INTERMEDIATE_FILE_EXTENSION),
        )

        if parsed_ph is not None and bool(parsed_ph):
            (
                missing_placeholders,
                unused_placeholders,
            ) = WordDocumentProcessor.replace_placeholders(
                src_path=temp_file.name,
                dst_path=replaced_path,
                placeholder_values=parsed_ph,
            )

            if unused_placeholders or missing_placeholders:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "error": "Placeholders mismatch",
                        "unused_placeholders": unused_placeholders,
                        "missing_placeholders": missing_placeholders,
                    },
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="no placeholders found"
            )
        WordDocumentProcessor.export_pdf(replaced_path, pdf_path)

    if os.path.isfile(pdf_path):
        logging.info(f"Found file in storage: {pdf_path}")
        background_task.add_task(delete_file, temp_file.name, replaced_path)
        return FileResponse(
            pdf_path,
            filename=DOWNLOAD_NAME,
            media_type=PDF_MIME_TYPE,
        )
