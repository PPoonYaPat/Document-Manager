import argparse
import sys
import os
import asyncio

from DocManager.pdf_extraction.pdf_extraction import PDF_Extraction

from dotenv import load_dotenv

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Parse file with specified output directory",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python parse.py -f input.pdf -o output
        """
    )
    
    parser.add_argument(
        "-f", "--filename",
        required=True,
        help="Input filename to process"
    )
    
    parser.add_argument(
        "-o", "--output",
        required=True,
        help="Output directory for results"
    )

    parser.add_argument(
        "-l", "--local-ocr-result-path",
        required=False,
        help="Local OCR result path"
    )
    
    return parser.parse_args()

def validate_file(filename: str, file_type: str):
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.")
        return False
    if not filename.endswith(f".{file_type}"):
        print(f"Error: File '{filename}' is not a {file_type} file.")
        return False
    return True

async def main():
    load_dotenv()
    try:
        args = parse_arguments()
        
        if not validate_file(args.filename, "pdf"):
            sys.exit(1)

        if args.local_ocr_result_path is not None and not validate_file(args.local_ocr_result_path, "json"):
            sys.exit(1)

        os.makedirs(args.output, exist_ok=True)
            
        print(f"Processing file: {args.filename}")
        print(f"Output directory: {args.output}")

        await PDF_Extraction.extract_pdf_without_model(
            input_path=args.filename,
            output_dir=args.output,
            local_ocr_result_path=args.local_ocr_result_path,
        )

        PDF_Extraction.make_editable_document(
            input_dir=args.output,
        )
        
        print("File processed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
