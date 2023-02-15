import logging
import os
import subprocess
from typing import Dict, List, Tuple

from docxtpl import DocxTemplate

from config import config
from exceptions import DocumentProcessorServiceException
from my_typing import CompletedProcessAny


class WordDocumentProcessor:
    @staticmethod
    def replace_placeholders(
        src_path: str, dst_path: str, placeholder_values: Dict[str, str] = None
    ) -> Tuple[List[str], List[str]]:
        if placeholder_values is None:
            placeholder_values = {}

        word_doc = DocxTemplate(src_path)

        document_placeholders = word_doc.get_undeclared_template_variables()
        given_placeholders = set(placeholder_values.keys())

        word_doc.render(placeholder_values)

        missing_placeholders = document_placeholders - given_placeholders
        unused_placeholders = given_placeholders - document_placeholders

        word_doc.save(dst_path)

        logging.info("Word document processing completed.")

        logging.info(f"Used placeholders: {unused_placeholders}")
        logging.info(f"Missing placeholders: {missing_placeholders}")

        return list(missing_placeholders), list(unused_placeholders)

    @staticmethod
    def export_pdf(src_path: str, dst_path: str) -> None:
        def unocov() -> None:
            try:
                cmd_params = [
                    "unoconv",
                    "-c",
                    "socket,host=localhost,port=8997;urp;StarOffice.ComponentContext",
                    "-f",
                    "pdf",
                    "-n",
                    "-o",
                    dst_path,
                    src_path,
                ]
                result: CompletedProcessAny = subprocess.run(
                    cmd_params,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=True,
                )

                if result.returncode == 0:
                    if not os.path.isfile(dst_path):
                        raise DocumentProcessorServiceException(
                            f"Output file doesn't exist: {dst_path}"
                        )

                else:
                    raise DocumentProcessorServiceException(
                        f"script {result.args} failed with code {result.returncode},"
                        + f"stdout: {result.stdout}, stderr: {result.stderr}"
                    )

            except subprocess.CalledProcessError as exc:
                logging.error(f"Failed to export pdf: {exc}")
                raise DocumentProcessorServiceException(str(exception)) from exc

        print(f"Exporting {src_path} to {dst_path}")

        # with retries https://github.com/unoconv/unoconv#conversion-problems
        for _ in range(config.UNOCOV_RETRIES):
            try:
                unocov()
            except Exception as exception:
                logging.error(f"Failed to export pdf: {exception}. Retrying ...")
                raise Exception(exception) from exception
