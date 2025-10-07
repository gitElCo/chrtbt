import unittest
from unittest.mock import MagicMock
from kompas_lib.analyzer import analyze_drawing

class TestAnalyzer(unittest.TestCase):
    def test_analyze_drawing(self):
        mock_kompas = MagicMock()
        mock_doc = MagicMock()
        mock_sheet = MagicMock()
        mock_sheet.Name = "Sheet1"
        mock_sheet.Format = "A3"
        mock_kompas.Documents.Open.return_value = mock_doc
        mock_doc.Sheets = [mock_sheet]
        mock_doc.TechRequirements.Count = 5
        mock_doc.Tables = []
        mock_doc.Dimensions.Count = 10
        mock_doc.Developer.Name = "Иванов И.И."

        result = analyze_drawing(mock_kompas, "fake_path.cdw")
        self.assertIsNotNone(result)
        self.assertEqual(len(result["sheets"]), 1)

if __name__ == "__main__":
    unittest.main()
