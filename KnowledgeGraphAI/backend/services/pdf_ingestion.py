import os
import re
import unicodedata
import logging
import hashlib
import time

logger = logging.getLogger(__name__)

# Try loading pymupdf/fitz, fallback to pypdf
try:
    import pymupdf as fitz
    fitz_available = True
    logger.info("Using pymupdf for PDF extraction.")
except ImportError:
    try:
        import fitz
        fitz_available = True
        logger.info("Using fitz for PDF extraction.")
    except ImportError:
        fitz_available = False
        import pypdf
        logger.warning("PyMuPDF not available, falling back to pypdf.")


# Backward compatibility re-export for normalize_whitespace
# Phase 1 tests expect simple whitespace normalization: all whitespace runs -> single space
def normalize_whitespace(text: str) -> str:
    if not text:
        return ""
    return re.sub(r'\s+', ' ', text).strip()


class PDFIngestionService:
    SCANNED_TEXT_THRESHOLD = 50

    @staticmethod
    def compute_sha256(file_path: str) -> str:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    @staticmethod
    def compute_content_hash(file_path: str) -> str:
        """Compute content-level SHA-256 hash using normalized extracted text."""
        extracted = PDFIngestionService.extract_pdf_data(file_path)
        combined = "\n".join(page["text"] for page in extracted.get("pages", []))
        normalized = normalize_whitespace(combined)
        return hashlib.sha256(normalized.encode("utf-8")).hexdigest()

    @staticmethod
    def extract_pdf_data(
        file_path: str,
        paper_id: int = 0,
        fallback_title: str | None = None,
    ) -> dict:
        start_time = time.time()
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"PDF file not found: {file_path}")

        default_title = (fallback_title or "").strip() or os.path.basename(file_path)

        try:
            if not fitz_available:
                # Fallback to pypdf when PyMuPDF is unavailable
                try:
                    reader = pypdf.PdfReader(file_path)
                except Exception as exc:
                    raise ValueError(f"Corrupted or invalid PDF file: {exc}") from exc

                total_pages = len(reader.pages)
                if total_pages == 0:
                    raise ValueError("The provided PDF is empty (0 pages).")

                metadata = reader.metadata or {}
                raw_title = metadata.get("/Title")
                title = str(raw_title).strip() if raw_title and str(raw_title).strip() else default_title
                author = metadata.get("/Author") or "Unknown"

                pages = []
                total_text_length = 0
                for i, page in enumerate(reader.pages):
                    text = page.extract_text() or ""
                    stripped = text.strip()
                    total_text_length += len(stripped)
                    pages.append({
                        "page_number": i + 1,
                        "text": text,
                        "char_count": len(stripped),
                        "image_count": 0,
                        "has_text": len(stripped) > 0
                    })

                if total_text_length == 0:
                    # Check if empty vs scanned
                    raise ValueError("The provided PDF contains no extractable text.")

                is_scanned = (total_text_length / total_pages) < PDFIngestionService.SCANNED_TEXT_THRESHOLD

                return {
                    "paper_id": paper_id,
                    "title": str(title).strip() if title else os.path.basename(file_path),
                    "author": str(author).strip() if author else "Unknown",
                    "page_count": total_pages,
                    "total_text_length": total_text_length,
                    "is_scanned": is_scanned,
                    "has_extractable_text": True,
                    "extraction_duration": round(time.time() - start_time, 3),
                    "pages": pages,
                    "warnings": ["Extracted using pypdf fallback."]
                }

            # Using PyMuPDF (fitz)
            try:
                doc = fitz.open(file_path)
            except Exception as exc:
                # Catch fitz.FileDataError or any opening error and raise ValueError
                raise ValueError(f"Corrupted or invalid PDF file: {exc}") from exc

            total_pages = len(doc)
            if total_pages == 0:
                doc.close()
                raise ValueError("The provided PDF is empty (0 pages).")

            metadata = doc.metadata or {}
            raw_title = metadata.get("title")
            title = str(raw_title).strip() if raw_title and str(raw_title).strip() else default_title
            author = metadata.get("author") or "Unknown"

            pages = []
            total_text_length = 0
            total_images = 0

            for page_num in range(total_pages):
                page = doc[page_num]
                text = page.get_text() or ""
                stripped = text.strip()
                total_text_length += len(stripped)
                try:
                    images = page.get_images()
                    img_count = len(images)
                except Exception:
                    img_count = 0
                total_images += img_count

                pages.append({
                    "page_number": page_num + 1,
                    "text": text,
                    "char_count": len(stripped),
                    "image_count": img_count,
                    "has_text": len(stripped) > 0
                })

            doc.close()

            if total_text_length == 0:
                if total_images == 0:
                    raise ValueError("The provided PDF contains no extractable text or visual content (blank PDF).")
                else:
                    is_scanned = True
            else:
                is_scanned = (total_text_length / total_pages) < PDFIngestionService.SCANNED_TEXT_THRESHOLD

            return {
                "paper_id": paper_id,
                "title": title.strip() if title else default_title,
                "author": author.strip() if author else "Unknown",
                "page_count": total_pages,
                "total_text_length": total_text_length,
                "total_images": total_images,
                "is_scanned": is_scanned,
                "has_extractable_text": total_text_length > 0,
                "extraction_duration": round(time.time() - start_time, 3),
                "pages": pages,
                "warnings": []
            }

        except ValueError:
            raise
        except Exception as exc:
            # Wrap any unexpected PDF parsing exception into ValueError with chaining
            raise ValueError(f"Corrupted or invalid PDF file: {exc}") from exc
