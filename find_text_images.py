import fitz  # PyMuPDF

def text_images(pdf_file):
    # Load PDF
    pdf_bytes = pdf_file.read()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    #doc = fitz.open(pdf_file)

    for page_num, page in enumerate(doc, start=1):
        text = page.get_text()
        images = page.get_images(full=True)

        print(f"--- Page {page_num} ---")
        print(f"Text layer present: {'✅ Yes' if text.strip() else '❌ No'}")
        print(f"Number of images: {len(images)}")

        # List images
        for i, img in enumerate(images):
            xref = img[0]
            print(f"  Image {i+1} (XREF {xref}) - size: {img[2]}x{img[3]}")
