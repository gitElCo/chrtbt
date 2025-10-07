import unittest
import os
from kompas_lib.watermark import add_watermark
from PyPDF2 import PdfFileWriter

class TestWatermark(unittest.TestCase):
    def test_add_watermark(self):
        input_pdf = "test_input.pdf"
        output_pdf = "test_output.pdf"
        watermark_image = "assets/watermark.png"

        pdf_writer = PdfFileWriter()
        pdf_writer.addBlankPage(width=595, height=842)
        with open(input_pdf, "wb") as f:
            pdf_writer.write(f)

        add_watermark(input_pdf, output_pdf, watermark_image, position="center")

        self.assertTrue(os.path.exists(output_pdf))
        os.remove(input_pdf)
        os.remove(output_pdf)

if __name__ == "__main__":
    unittest.main()
