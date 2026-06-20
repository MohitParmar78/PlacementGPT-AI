# Import PyMuPDF
import fitz


def extract_text_from_pdf(pdf_path):
    """
    Extract text from PDF.

    Parameters:
        pdf_path (str)

    Returns:
        str
    """

    # Store extracted text
    extracted_text = ""

    # Open PDF
    document = fitz.open(pdf_path)

    # Loop through pages
    for page in document:

        # Extract text from page
        page_text = page.get_text()

        # Append text
        extracted_text += page_text

    # Close document
    document.close()

    return extracted_text