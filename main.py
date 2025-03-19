import extract
import pf
import db
import os
import glob

def get_fs_figures(nzbn):
    pf.fetch_all_returns(nzbn)

    download_dir = os.path.join("downloads", str(nzbn))

    if not os.path.exists(download_dir):
        print(f"No directory found at {download_dir}. No PDFs to process.")
        return

    pdf_files = glob.glob(os.path.join(download_dir, "*.pdf"))
    if not pdf_files:
        print(f"No PDF files found in {download_dir}.")
        return

    # extract text from all downloaded reports
    for pdf_path in pdf_files:
        print(f"Processing {pdf_path}...")
        extract.extract_pages(pdf_path, 4, 8)
        print(f"Finished processing {pdf_path}")

if __name__ == "__main__":
    get_fs_figures(nzbn=9429040077536)
