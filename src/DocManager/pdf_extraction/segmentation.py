import json
import os
import random
import string
from dataclasses import dataclass
from typing import Dict, List, Literal
import fitz

from DocManager._utils import (
    cnt_files_in_s3,
    delete_dir_from_s3,
    download_file_from_s3,
    ocr_parse,
    upload_file_to_s3,
)
from DocManager.pdf_extraction.extraction_data import RectData

class Segmentation:

    @classmethod
    def call_segmentation(cls, input_path: str, storage_dir: str, save_output_on_s3: bool = False):
        os.makedirs(storage_dir, exist_ok=True)
        random_string = "".join(random.choices(string.ascii_letters + string.digits, k=8))
        basename = os.path.splitext(os.path.basename(input_path))[0]

        s3_dir_path = f"pdf-extraction/{basename}_{random_string}"
        s3_input_path = os.path.join(s3_dir_path, os.path.basename(input_path))
        
        upload_file_to_s3(input_path, s3_input_path)
        ocr_parse(s3_input_path, s3_dir_path)

        s3_result_path = f"{s3_dir_path}/{basename}_{random_string}"
        storage_path = f"{storage_dir}/{basename}"

        download_file_from_s3(s3_result_path + ".json", storage_path + ".json")
        download_file_from_s3(s3_result_path + ".md", storage_path + ".md")
        download_file_from_s3(s3_result_path + "_nohf.md", storage_path + "_nohf.md")

        if not save_output_on_s3:
            delete_dir_from_s3(s3_dir_path)

    @classmethod
    def post_process_page_number(cls, rect_info: List[RectData], page: fitz.Page) -> List[RectData]:
        
        return rect_info

    @classmethod
    def load_json(cls, input_path: str, storage_path: str):
        ratio = 72 / 200
        result: List[List[RectData]] = []
        with open(storage_path, "r") as file:
            json_data = json.load(file)

        doc = fitz.open(input_path)

        for page_info in json_data:
            rect_info = []
            for component in page_info["full_layout_info"]:
                type = component["category"]
                if (type == "Caption"
                    or type == "Footnote"
                    or type == "List-item"
                    or type == "Section-header"
                    or type == "Title"
                ):
                    type = "Text"
                text = component["text"] if "text" in component else None
                bbox = component["bbox"]
                x0, y0, x1, y1 = bbox
                rect_info.append(RectData(type, x0 * ratio, y0 * ratio, x1 * ratio, y1 * ratio, text))

            result.append(cls.post_process_page_number(rect_info, doc[page_info["page_no"]]))

        page = doc[0]
        height = round(page.get_text("dict")["height"])
        width = round(page.get_text("dict")["width"])
        leftmost = min(rect.x0 for rect_data in result for rect in rect_data)
        rightmost = width - leftmost

        return result, leftmost, rightmost, width, height