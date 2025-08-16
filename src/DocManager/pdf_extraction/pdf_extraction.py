import os
import re

from DocManager.pdf_extraction.html_generation import HTMLGenerator
from DocManager.pdf_extraction.html_template import editable_html_template
from DocManager.pdf_extraction.segmentation import Segmentation


class PDF_Extraction:

    @classmethod
    async def extract_pdf_with_model(
        cls,
        input_path: str,
        output_dir: str,
        model_client,
        simultaneous_requests: bool = True,
        save_output_on_s3: bool = False,
        text_limit: int = -1, # If we want to extract the style, we don't need to get the full text which might waste the token used when sending request to the llm model. "-1" means no limit.
    ) -> str:

        os.makedirs(output_dir, exist_ok=True)
        page_info_path = output_dir + "/page_info" if output_dir.endswith("/") else output_dir + "/page_info"
        
        Segmentation.call_segmentation(
            input_path, page_info_path, save_output_on_s3=save_output_on_s3
        )
        rect_data, leftmost, rightmost, page_width, page_height = (
            Segmentation.load_json(page_info_path)
        )
        html_generator = HTMLGenerator(
            input_pdf_path=input_path,
            output_dir=output_dir,
            rect_data=rect_data,
            leftmost_coordinates=leftmost,
            rightmost_coordinates=rightmost,
            page_width=page_width,
            page_height=page_height,
            model_client=model_client,
            text_limit=text_limit,
        )
        return await html_generator.generate_all_pages(
            simultaneous_requests=simultaneous_requests
        )

    # In this function, the chart/image generation will be skipped
    @classmethod
    async def extract_pdf_without_model(
        cls,
        input_path: str,
        output_dir: str,
        save_output_on_s3: bool = False,
        text_limit: int = -1, # If we want to extract the style, we don't need to get the full text which might waste the token used when sending request to the llm model. "-1" means no limit.
    ) -> str:

        os.makedirs(output_dir, exist_ok=True)
        page_info_path = output_dir + "/page_info" if output_dir.endswith("/") else output_dir + "/page_info"

        Segmentation.call_segmentation(
            input_path, page_info_path, save_output_on_s3=save_output_on_s3
        )
        rect_data, leftmost, rightmost, page_width, page_height = (
            Segmentation.load_json(page_info_path)
        )
        html_generator = HTMLGenerator(
            input_pdf_path=input_path,
            output_dir=output_dir,
            rect_data=rect_data,
            leftmost_coordinates=leftmost,
            rightmost_coordinates=rightmost,
            page_width=page_width,
            page_height=page_height,
            text_limit=text_limit,
        )
        return await html_generator.generate_all_pages()

    @classmethod
    def make_editable_document(cls, input_dir: str):

        input_path = input_dir + "final.html" if input_dir.endswith("/") else input_dir + "/final.html"
        output_path = input_dir + "final_editable.html" if input_dir.endswith("/") else input_dir + "/final_editable.html"
        title = os.path.basename(os.path.dirname(input_path))

        def extract_page_content(content: str, page_number: int) -> str | None:
            start_pattern = (
                rf"<div class=\'background-page\' id=\'page_{page_number}\'>"
            )
            start_match = re.search(start_pattern, content)
            if not start_match:
                return None

            start_pos = start_match.start()

            pos = start_pos
            div_count = 0
            in_page_div = False

            for i in range(start_pos, len(content)):
                if content[i : i + 5] == "<div ":
                    div_count += 1
                    if i == start_pos:
                        in_page_div = True
                elif content[i : i + 6] == "</div>":
                    div_count -= 1
                    if in_page_div and div_count == 0:
                        end_pos = i + 6
                        return content[start_pos:end_pos]
            else:
                return None

        with open(input_path, "r") as f:
            content = f.read()

        match = re.search(r"width:\s*([0-9.]+)pt", content)
        width = float(match.group(1)) if match else None
        match = re.search(r"height:\s*([0-9.]+)pt", content)
        height = float(match.group(1)) if match else None

        if width is None or height is None:
            raise ValueError("Width and height not found in input file")

        result = editable_html_template
        result = result.replace("ffff-width", f"{width}pt")
        result = result.replace("ffff-height", f"{height}pt")
        result = result.replace("ffff-title", title)
        result = result.replace("ffff-extra-width", f"{width + 0.1}pt")

        content_dict = ""

        page_number = 0
        while True:
            page_content = extract_page_content(content, page_number)
            if page_content is None:
                break

            content_dict += f'"gjs{page_number}": `{page_content}`,'
            page_number += 1

        content_dict = "{" + content_dict + "};"
        content_dict = content_dict.replace("</script>", "</`+`script>")

        result = result.replace("ffff-length", str(page_number))
        result = result.replace("ffff-content", content_dict)

        with open(output_path, "w") as f:
            f.write(result)
