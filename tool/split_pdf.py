import fitz
import os

def split_and_rename_pdf(input_file, ranges, output_directory):
    pdf_document = fitz.open(input_file)

    for range_start, range_end in ranges:
        output_filename = f"{output_directory}_{range_start}_{range_end}.pdf"
        pdf_writer = fitz.open()
        for page_number in range(range_start-1, range_end):
            pdf_writer.insert_pdf(pdf_document, from_page=page_number, to_page=page_number)
        pdf_writer.save(output_filename)
        pdf_writer.close()

    pdf_document.close()

file_name = "善恶之源 (（美）保罗·布卢姆"
input_file = f"C:/Users/Zz/Downloads/{file_name}.pdf"
output_directory = f"C:/Users/Zz/Downloads/{file_name}"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

page_ranges = [(16, 46), (47, 76), (77, 123), (124, 156), (157, 184), (185, 214), (215, 252)]
split_and_rename_pdf(input_file, page_ranges, output_directory)