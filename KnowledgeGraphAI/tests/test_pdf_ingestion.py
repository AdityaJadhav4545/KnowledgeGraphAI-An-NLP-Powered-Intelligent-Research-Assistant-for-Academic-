import os
import shutil
import tempfile
import pytest
from PIL import Image
from reportlab.pdfgen import canvas
from KnowledgeGraphAI.backend.services.pdf_ingestion import PDFIngestionService, normalize_whitespace


def make_pdf(path: str, text: str = "Hello world", title: str = "Test Paper", author: str = "Jane Doe"):
    c = canvas.Canvas(path)
    c.setTitle(title)
    c.setAuthor(author)
    c.drawString(72, 720, text)
    c.showPage()
    c.save()


def make_blank_pdf(path: str):
    c = canvas.Canvas(path)
    c.showPage()
    c.save()


def make_scanned_pdf(path: str):
    img_path = path + ".png"
    img = Image.new("RGB", (200, 200), color="white")
    img.save(img_path)
    c = canvas.Canvas(path)
    c.drawImage(img_path, 100, 100, width=200, height=200)
    c.showPage()
    c.save()
    if os.path.exists(img_path):
        os.remove(img_path)


def test_normalize_whitespace():
    assert normalize_whitespace("  Hello \n  world \t ") == "Hello world"
    assert normalize_whitespace("") == ""


def test_compute_sha256_is_deterministic(tmp_path):
    p = tmp_path / "sample.pdf"
    make_pdf(str(p))
    h1 = PDFIngestionService.compute_sha256(str(p))
    h2 = PDFIngestionService.compute_sha256(str(p))
    assert h1 == h2
    assert len(h1) == 64


def test_exact_file_duplicate_detection(tmp_path):
    p1 = tmp_path / "a.pdf"
    make_pdf(str(p1))
    p2 = tmp_path / "a_copy.pdf"
    shutil.copyfile(str(p1), str(p2))

    # Exact byte duplicate should produce matching sha256
    assert PDFIngestionService.compute_sha256(str(p1)) == PDFIngestionService.compute_sha256(str(p2))
    assert PDFIngestionService.compute_content_hash(str(p1)) == PDFIngestionService.compute_content_hash(str(p2))


def test_content_duplicate_detection(tmp_path):
    p1 = tmp_path / "paper1.pdf"
    make_pdf(str(p1), text="Quantum computing principles and applications.")
    p2 = tmp_path / "paper2.pdf"
    make_pdf(str(p2), text="Quantum computing principles and applications.")

    # Content hash should match even if ReportLab metadata timestamps differ
    content_hash1 = PDFIngestionService.compute_content_hash(str(p1))
    content_hash2 = PDFIngestionService.compute_content_hash(str(p2))
    assert content_hash1 == content_hash2


def test_metadata_extraction(tmp_path):
    p = tmp_path / "paper.pdf"
    make_pdf(str(p), text="Abstract content here", title="Deep Learning", author="Alice")
    data = PDFIngestionService.extract_pdf_data(str(p))
    assert data["title"] == "Deep Learning"
    assert data["author"] == "Alice"
    assert data["page_count"] == 1
    assert data["pages"][0]["page_number"] == 1
    assert "Abstract content here" in data["pages"][0]["text"]


def test_empty_pdf_raises(tmp_path):
    p = tmp_path / "empty.pdf"
    make_blank_pdf(str(p))
    with pytest.raises(ValueError) as exc_info:
        PDFIngestionService.extract_pdf_data(str(p))
    assert "no extractable text or visual content" in str(exc_info.value)


def test_corrupted_file_raises(tmp_path):
    p = tmp_path / "bad.pdf"
    p.write_bytes(b"not a real pdf content")
    with pytest.raises(ValueError) as exc_info:
        PDFIngestionService.extract_pdf_data(str(p))
    assert "Corrupted or invalid PDF" in str(exc_info.value)


def test_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        PDFIngestionService.extract_pdf_data("/nonexistent/path/file.pdf")


def test_scanned_pdf_detection(tmp_path):
    p = tmp_path / "scanned.pdf"
    make_scanned_pdf(str(p))
    data = PDFIngestionService.extract_pdf_data(str(p))
    assert data["is_scanned"] is True
    assert data["total_images"] > 0