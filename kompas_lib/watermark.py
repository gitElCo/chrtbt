from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
import os

def add_watermark(
    input_pdf_path: str,
    output_pdf_path: str,
    watermark_image_path: str,
    position: str = "center",
    over_tech_requirements: bool = False,
    scale: float = 1.0
) -> None:
    """
    Добавляет вотермарку на PDF с учётом нестандартных размеров.
    """
    with open(input_pdf_path, "rb") as input_pdf:
        reader = PdfFileReader(input_pdf)
        page = reader.getPage(0)
        page_width = float(page.mediaBox.getWidth())
        page_height = float(page.mediaBox.getHeight())

    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=(page_width, page_height))

    watermark = ImageReader(watermark_image_path)
    img_width, img_height = watermark.getSize()
    img_width *= scale
    img_height *= scale

    x, y = 0, 0
    if position == "center":
        x = (page_width - img_width) / 2
        y = (page_height - img_height) / 2
    elif position == "top-left":
        x, y = 50, page_height - img_height - 50
    elif position == "top-right":
        x, y = page_width - img_width - 50, page_height - img_height - 50
    elif position == "bottom-left":
        x, y = 50, 50
    elif position == "bottom-right":
        x, y = page_width - img_width - 50, 50

    if over_tech_requirements:
        y = page_height - img_height - 100

    can.drawImage(watermark_image_path, x, y, width=img_width, height=img_height, preserveAspectRatio=True)
    can.save()

    packet.seek(0)
    watermark_pdf = PdfFileReader(packet)
    output = PdfFileWriter()

    for page_num in range(reader.numPages):
        page = reader.getPage(page_num)
        page.mergePage(watermark_pdf.getPage(0))
        output.addPage(page)

    with open(output_pdf_path, "wb") as output_pdf:
        output.write(output_pdf)
