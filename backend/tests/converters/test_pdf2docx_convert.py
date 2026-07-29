from converters.pdf2docx_convert import PDF2DOCXConverter


def test_convert_uses_pdf2docx_converter(monkeypatch, safe_path_test_settings):
    input_name = "c" * 32
    input_file = safe_path_test_settings.upload_dir / f"{input_name}.pdf"
    input_file.write_text("pdf fixture")

    output_file = safe_path_test_settings.output_dir / f"{input_name}.docx"
    calls: list[tuple[str, str]] = []
    closed: list[bool] = []

    class FakeConverter:
        def __init__(self, source_path):
            assert source_path == str(input_file)

        def convert(self, target_path):
            calls.append((str(input_file), target_path))
            output_file.write_text("docx output")

        def close(self):
            closed.append(True)

    monkeypatch.setattr(
        PDF2DOCXConverter,
        "_load_pdf_converter_class",
        staticmethod(lambda: FakeConverter),
    )

    converter = PDF2DOCXConverter(
        input_file=str(input_file),
        output_dir=str(safe_path_test_settings.output_dir),
        input_type="pdf",
        output_type="docx",
    )

    assert converter.convert() == [str(output_file)]
    assert calls == [(str(input_file), str(output_file))]
    assert closed == [True]


def test_can_register_false_when_dependency_missing(monkeypatch):
    def raise_runtime_error():
        raise RuntimeError("missing dependency")

    monkeypatch.setattr(
        PDF2DOCXConverter,
        "_load_pdf_converter_class",
        staticmethod(raise_runtime_error),
    )

    assert PDF2DOCXConverter.can_register() is False