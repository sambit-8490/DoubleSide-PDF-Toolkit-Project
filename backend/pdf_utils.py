import os
import fitz  # PyMuPDF
from typing import Tuple, List


def _safe_save(doc: fitz.Document, path: str, files: List[str]):
    """Save PDF only if it has pages."""
    if doc.page_count > 0:
        doc.save(path)
        files.append(path)


def process_double(
    file_path: str,
    start_page: int = 1,
    end_page: int = 0,
    reverse_order: bool = False
) -> Tuple[str, ...]:
    doc = fitz.open(file_path)
    total_pages = len(doc)

    end = min(end_page, total_pages) if end_page > 0 else total_pages
    start_idx = max(start_page - 1, 0)
    end_idx = max(end - 1, 0)

    odd_doc = fitz.open()
    even_doc = fitz.open()

    for i in range(start_idx, end_idx + 1):
        if i >= total_pages:
            break
        page_num = i + 1
        if page_num % 2 != 0:
            odd_doc.insert_pdf(doc, from_page=i, to_page=i)
        else:
            even_doc.insert_pdf(doc, from_page=i, to_page=i)

    base_name = os.path.splitext(file_path)[0]
    path1 = f"{base_name}_1.pdf"
    path2 = f"{base_name}_2.pdf"

    files_created: List[str] = []

    if reverse_order:
        _safe_save(even_doc, path1, files_created)
        _safe_save(odd_doc, path2, files_created)
    else:
        _safe_save(odd_doc, path1, files_created)
        _safe_save(even_doc, path2, files_created)

    odd_doc.close()
    even_doc.close()
    doc.close()

    return tuple(files_created)


def process_four(
    file_path: str,
    start_page: int = 1,
    end_page: int = 0,
    reverse_order: bool = False
) -> Tuple[str, ...]:
    src_doc = fitz.open(file_path)
    total_pages = len(src_doc)

    end = min(end_page, total_pages) if end_page > 0 else total_pages
    start_idx = max(start_page - 1, 0)
    end_idx = max(end - 1, 0)

    temp_doc = fitz.open()
    if start_idx <= end_idx and start_idx < total_pages:
        temp_doc.insert_pdf(src_doc, from_page=start_idx, to_page=end_idx)

    width, height = 842, 595
    padding = 20

    r1 = fitz.Rect(padding, padding, width / 2 - padding, height - padding)
    r2 = fitz.Rect(width / 2 + padding, padding, width - padding, height - padding)

    out_doc = fitz.open()

    for i in range(0, len(temp_doc), 2):
        page = out_doc.new_page(width=width, height=height)
        page.show_pdf_page(r1, temp_doc, i)

        if i + 1 < len(temp_doc):
            page.show_pdf_page(r2, temp_doc, i + 1)

    front_doc = fitz.open()
    back_doc = fitz.open()

    for i in range(len(out_doc)):
        if (i + 1) % 2 != 0:
            front_doc.insert_pdf(out_doc, from_page=i, to_page=i)
        else:
            back_doc.insert_pdf(out_doc, from_page=i, to_page=i)

    base_name = os.path.splitext(file_path)[0]
    path1 = f"{base_name}_1.pdf"
    path2 = f"{base_name}_2.pdf"

    files_created: List[str] = []

    if reverse_order:
        _safe_save(back_doc, path1, files_created)
        _safe_save(front_doc, path2, files_created)
    else:
        _safe_save(front_doc, path1, files_created)
        _safe_save(back_doc, path2, files_created)

    src_doc.close()
    temp_doc.close()
    out_doc.close()
    front_doc.close()
    back_doc.close()

    return tuple(files_created)


def process_book(
    file_path: str,
    start_page: int = 1,
    end_page: int = 0,
    reverse_order: bool = False
) -> Tuple[str, ...]:
    src_doc = fitz.open(file_path)
    total_pages = len(src_doc)

    end = min(end_page, total_pages) if end_page > 0 else total_pages
    start_idx = max(start_page - 1, 0)
    end_idx = max(end - 1, 0)

    temp_doc = fitz.open()
    if start_idx <= end_idx and start_idx < total_pages:
        temp_doc.insert_pdf(src_doc, from_page=start_idx, to_page=end_idx)

    total_pages = len(temp_doc)

    # Pad to multiple of 4
    needed = (4 - total_pages % 4) if total_pages % 4 else 0
    for _ in range(needed):
        temp_doc.new_page()

    total_pages = len(temp_doc)
    num_sheets = total_pages // 4

    width, height = 842, 595
    padding = 20

    r_left = fitz.Rect(padding, padding, width / 2 - padding, height - padding)
    r_right = fitz.Rect(width / 2 + padding, padding, width - padding, height - padding)

    front_doc = fitz.open()
    back_doc = fitz.open()

    for i in range(num_sheets):
        idx_f_l = (total_pages - 1) - 2 * i
        idx_f_r = 2 * i

        p_front = front_doc.new_page(width=width, height=height)
        p_front.show_pdf_page(r_left, temp_doc, idx_f_l)
        p_front.show_pdf_page(r_right, temp_doc, idx_f_r)

        idx_b_l = 1 + 2 * i
        idx_b_r = (total_pages - 2) - 2 * i

        p_back = back_doc.new_page(width=width, height=height)
        p_back.show_pdf_page(r_left, temp_doc, idx_b_l)
        p_back.show_pdf_page(r_right, temp_doc, idx_b_r)

    base_name = os.path.splitext(file_path)[0]
    path1 = f"{base_name}_1.pdf"
    path2 = f"{base_name}_2.pdf"

    files_created: List[str] = []

    if reverse_order:
        _safe_save(back_doc, path1, files_created)
        _safe_save(front_doc, path2, files_created)
    else:
        _safe_save(front_doc, path1, files_created)
        _safe_save(back_doc, path2, files_created)

    src_doc.close()
    temp_doc.close()
    front_doc.close()
    back_doc.close()

    return tuple(files_created)


def process_split(file_path: str, start_page: int = 1, end_page: int = 0) -> str:
    doc = fitz.open(file_path)
    total_pages = len(doc)

    end = min(end_page, total_pages) if end_page > 0 else total_pages

    out_doc = fitz.open()
    out_doc.insert_pdf(doc, from_page=start_page - 1, to_page=end - 1)

    base_name = os.path.splitext(file_path)[0]
    output_name = f"{base_name}_splitted.pdf"

    if out_doc.page_count > 0:
        out_doc.save(output_name)

    doc.close()
    out_doc.close()

    return output_name


def decrypt_pdf(file_path: str, password: str = "") -> str:
    doc = fitz.open(file_path)

    if doc.is_encrypted:
        doc.authenticate(password)

    base_name = os.path.splitext(file_path)[0]
    output_name = f"{base_name}_decrypted.pdf"

    doc.save(output_name)
    doc.close()

    return output_name


def encrypt_pdf(file_path: str, password: str) -> str:
    doc = fitz.open(file_path)

    base_name = os.path.splitext(file_path)[0]
    output_name = f"{base_name}_encrypted.pdf"

    doc.save(
        output_name,
        encryption=fitz.PDF_ENCRYPT_AES_256,
        owner_pw=password,
        user_pw=password,
    )
    doc.close()

    return output_name
