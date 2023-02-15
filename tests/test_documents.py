import os

from services.documents_processor import WordDocumentProcessor

from tests.conftest import placeholders

out_file_path = os.path.join(
    os.getcwd(),
    "files/test_replace_placeholders.out.docx",
)
print(os.path.abspath("files/test-doc.doc"))
in_file_path = os.path.join(os.getcwd(), "files/test-doc.docx")


def test_replace_placeholders_all() -> None:
    print(os.path.abspath("files/test-doc.doc"))
    (
        unused_placeholders,
        missing_placeholders,
    ) = WordDocumentProcessor.replace_placeholders(
        in_file_path, out_file_path, placeholders
    )
    assert unused_placeholders == []
    assert missing_placeholders == []

    os.remove(out_file_path)


def test_replace_placeholders_extra_placeholder() -> None:
    tags_with_extra_tag = {
        **placeholders,
        "extra_placeholder": "This is an extra placeholder",
    }
    (
        missing_placeholders,
        unused_placeholders,
    ) = WordDocumentProcessor.replace_placeholders(
        in_file_path, out_file_path, tags_with_extra_tag
    )
    assert unused_placeholders == ["extra_placeholder"]
    assert missing_placeholders == []

    os.remove(out_file_path)


def test_replace_placeholders_missing_placeholder() -> None:
    placeholders_with_missing_ph = placeholders.copy()
    del placeholders_with_missing_ph["CompanyMemberAddress"]
    (
        missing_placeholders,
        unused_placeholders,
    ) = WordDocumentProcessor.replace_placeholders(
        in_file_path, out_file_path, placeholders_with_missing_ph
    )
    assert unused_placeholders == []
    assert missing_placeholders == ["CompanyMemberAddress"]

    os.remove(out_file_path)
