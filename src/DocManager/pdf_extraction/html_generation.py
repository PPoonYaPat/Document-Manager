import asyncio
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple

import fitz
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import MultiModalMessage
from autogen_core import CancellationToken, Image

from DocManager.pdf_extraction.extraction_data import RectData, TextStyle
from DocManager.pdf_extraction.html_template import html_template
from DocManager.pdf_extraction.prompt import non_image_generation_prompt


class HTMLGenerator:
    def __init__(
        self,
        input_pdf_path: str,
        output_dir: str,
        rect_data: List[List[RectData]],
        leftmost_coordinates: float,
        rightmost_coordinates: float,
        page_width: float,
        page_height: float,
        model_client=None,
        margin_top_decrease: int = 3,
        padding_left_ratio: float = 0.8,
        max_agents: int = 10,
        text_limit: int = -1, # If we want to extract the style, we don't need to get the full text which might waste the token used when sending request to the llm model.
    ):

        self.rect_data = [
            [
                rect
                for rect in page_rects
                if rect.x0 <= rightmost_coordinates and rect.x1 >= leftmost_coordinates
            ]
            for page_rects in rect_data
        ]
        self.output_path = output_dir + "/final.html"
        self.input_pdf_path = input_pdf_path
        self.images_dir = os.path.join(output_dir, "components")
        os.makedirs(self.images_dir, exist_ok=True)
        self.doc = fitz.open(self.input_pdf_path)
        self.rightmost_coordinates = rightmost_coordinates
        self.leftmost_coordinates = leftmost_coordinates
        self.padding = leftmost_coordinates
        self.cnt = 0
        self.page_width = page_width
        self.page_height = page_height
        self.margin_top_decrease = margin_top_decrease
        self.padding_left_ratio = padding_left_ratio
        self.model_client = model_client
        self.max_agents = max_agents
        self.available_agents = asyncio.Queue()
        self.total_tokens = 0
        self.model_request = []
        self.text_limit = text_limit
        
        # Create multiple agents for generating html simultaneously
        if model_client is not None:
            for i in range(self.max_agents):
                html_agent = AssistantAgent(
                    name=f"HTMLGenerator_{i}",
                    model_client=model_client,
                    system_message=non_image_generation_prompt,
                )
                self.available_agents.put_nowait(html_agent)

    def truncate_html(self, html_content: str, max_length: int) -> str:
        if len(html_content) <= max_length or max_length == -1:
            return html_content
            
        text_count = 0
        in_tag = False
        i = 0
        tag_stack = []
        
        while i < len(html_content) and text_count < max_length:
            char = html_content[i]
            
            if char == '<':
                in_tag = True
                # Check if it's a closing tag
                if i + 1 < len(html_content) and html_content[i + 1] == '/':
                    tag_stack.pop()
                else:
                    tag_end = html_content.find('>', i)
                    if tag_end != -1:
                        tag_content = html_content[i + 1:tag_end]
                        space_pos = tag_content.find(' ')
                        if space_pos != -1:
                            tag_name = tag_content[:space_pos]
                        else:
                            tag_name = tag_content
                        
                        tag_stack.append(tag_name)

            elif char == '>':
                in_tag = False
            
            if not in_tag:
                text_count += 1
                
            i += 1
        
        if text_count >= max_length:
            truncated_html = html_content[:i]
            
            for tag in reversed(tag_stack):
                truncated_html += f"</{tag}>"
            
            return truncated_html + "..."
        else:
            return html_content
        

    # Generate HTML code for text without using the model
    def generate_text_html(
        self,
        rect_data: RectData,
        prev_y_coordinate: float,
        bound_left: float,
        class_name: str = "",
        spans: List[Dict[str, Any]] = None,
    ) -> str:

        sentence_design = []
        prev_origin = -1
        prev_size = -1

        # Merge the spans that have the same style (ex. different lines mean different span which we can merge them together into the same span) and also consider the sub/sup script
        for span in spans:
            if rect_data.contain_rect(fitz.Rect(span["bbox"])):
                new_text_style = TextStyle(
                    font=span["font"],
                    color=span["color"],
                    alpha=span["alpha"],
                    size=span["size"],
                )
                origin = span["origin"][1]

                if (
                    prev_origin != -1
                    and prev_origin + 0.3 < origin
                    and prev_origin + 2 > origin
                    and prev_size > span["size"]
                ):
                    sentence_design[-1][1] += f"<sub style='font-size: {span['size']}pt; color: {span['color']}; font-family: {span['font']};'>{span['text']}</sub>"

                elif (
                    prev_origin != -1
                    and origin + 0.5 < prev_origin
                    and origin + span["size"] > prev_origin
                    and prev_size > span["size"]
                ):
                    sentence_design[-1][1] += f"<sup style='font-size: {span['size']}pt; color: {span['color']}; font-family: {span['font']};'>{span['text']}</sup>"

                elif len(sentence_design) == 0 or not sentence_design[-1][0].same_style(
                    new_text_style
                ):
                    sentence_design.append([new_text_style, span["text"]])
                else:
                    sentence_design[-1][1] += span["text"]

                prev_origin = span["origin"][1]
                prev_size = span["size"]

        # Generate the HTML code for the text
        html_parts = []
        first_style = None
        for style, text in sentence_design:
            font_size = round(style.size, 1)
            font_color = f"#{style.color:06x}"
            opacity = style.alpha / 255
            font_family = style.font
            font_weight = None

            if "-" in font_family:
                parts = font_family.split("-")
                font_family = parts[0]
                weight_part = parts[-1].lower()
                if "bold" in weight_part:
                    font_weight = "bold"
                elif (
                    "light" in weight_part or "lg" in weight_part or "lt" in weight_part
                ):
                    font_weight = "300"
                elif "regular" in weight_part or "regul" in weight_part:
                    font_weight = "normal"

            style_str = f"font-family: {font_family}"
            if font_weight:
                style_str += f"; font-weight: {font_weight}"
            style_str += f"; color: {font_color}; font-size: {font_size}pt"
            style_str += f"; opacity: {opacity}"

            if first_style is None:
                first_style = style_str

            if style_str == first_style:
                html_parts.append(text)
            else:
                html_parts.append(f"<span style='{style_str}'>{text}</span>")

        result_html = self.truncate_html("\n".join(html_parts), self.text_limit)

        # Generate the margin and padding style
        # Have to decrease the margin and padding because, in real html, the margin and padding are tend to be larger than the actual content
        margin_style = "margin-top: 0pt;"
        if (
            prev_y_coordinate != -1
            and rect_data.y0 > prev_y_coordinate + self.margin_top_decrease
        ):
            margin_style = f"margin-top: {(rect_data.y0 - prev_y_coordinate - self.margin_top_decrease)}pt;"

        padding_style = "padding-left: 0pt;"
        if rect_data.x0 - bound_left > 20:
            padding_style = f"padding-left: {(rect_data.x0 - bound_left) * self.padding_left_ratio}pt;"

        if len(html_parts) != 0:
            return (
                f"<div class='{class_name}' style='{margin_style} {padding_style} overflow-wrap: break-word; line-height: 1.2; {first_style}'>\n"
                + result_html
                + f"\n</div>"
            )
        else:
            return ""

    # Crop the image and save it to the images directory for the model to use
    def crop_image(
        self, rect_data: RectData, page_number: int, file_path: str, dpi: int = 300
    ):
        page = self.doc[page_number]
        page.set_cropbox(rect_data.get_org_rect())
        mat = fitz.Matrix(dpi / 72, dpi / 72)
        pix = page.get_pixmap(matrix=mat)
        pix.save(file_path)

    # Generate HTML code for non-text (Picture and Table)
    async def generate_non_text_html(
        self,
        rect_data: RectData,
        prev_y_coordinate: float,
        bound_left: float,
        page_number: int,
        class_name: str = "",
        spans: List[Dict[str, Any]] = None,
    ) -> str:

        style_dict: Dict[str, List[str]] = {}

        # Get the style information of the text. This will also be included in the model request
        for span in spans:
            if rect_data.contain_rect(fitz.Rect(span["bbox"])):
                if span["text"] == " ":
                    continue

                font_size = round(span["size"], 1)
                font_color = f"#{span['color']:06x}"
                opacity = span["alpha"] / 255
                font_family = span["font"]
                font_weight = None

                if "-" in font_family:
                    parts = font_family.split("-")
                    font_family = parts[0]
                    weight_part = parts[-1].lower()
                    if "bold" in weight_part:
                        font_weight = "bold"
                    elif (
                        "light" in weight_part
                        or "lg" in weight_part
                        or "lt" in weight_part
                    ):
                        font_weight = "300"
                    elif "regular" in weight_part or "regul" in weight_part:
                        font_weight = "normal"

                style_info = f"font: {font_family}, color: {font_color}, opacity: {opacity}, size: {font_size}"
                if font_weight:
                    style_info += f", weight: {font_weight}"

                if style_info not in style_dict:
                    style_dict[style_info] = []
                style_dict[style_info].append(span["text"])

        # Format the style information for the model request
        formatted_styles = []
        for i, (style_info, texts) in enumerate(style_dict.items(), 1):
            text_list = ", ".join([f'"{text}"' for text in texts])

            formatted_styles.append(
                f"{i}. Text style: {style_info}\n   Texts: {text_list}"
            )

        text_styles_format = "\n".join(formatted_styles)

        # Generate the margin and padding style
        # Have to decrease the margin and padding because, in real html, the margin and padding are tend to be larger than the actual content
        margin_style = "margin-top: 0pt;"
        if (
            prev_y_coordinate != -1
            and rect_data.y0 > prev_y_coordinate + self.margin_top_decrease
        ):
            margin_style = f"margin-top: {(rect_data.y0 - prev_y_coordinate - self.margin_top_decrease)}pt;"

        padding_style = "padding-left: 0pt;"
        if rect_data.x0 - bound_left > 20:
            padding_style = f"padding-left: {(rect_data.x0 - bound_left) * self.padding_left_ratio}pt;"

        # Crop the image and save it to the images directory for the model to use
        image_path = os.path.join(self.images_dir, f"{class_name}.png")
        self.crop_image(rect_data, page_number, image_path)

        # Generate the model request
        img = Image.from_file(Path(image_path))
        message = MultiModalMessage(
            content=[
                img,
                f"Here is the text style information:\n{text_styles_format}",
                f"The class name is {class_name}",
                f"You have to fit the image into the container with the width of {rect_data.x1 - rect_data.x0}pt and a height of {rect_data.y1 - rect_data.y0}pt"
            ],
            source="user",
        )

        if rect_data.type == "Table":
            message_table = MultiModalMessage(
                content=[
                    "This is the table component, you MUST refer to this given HTML for the table information. You only have to decorate this table. You don't have to change the table data and structure.",
                    rect_data.text
                ],
                source="user",
            )

        # If the model client is not None, then we can use the model to generate the HTML code
        if self.model_client is not None:
            # Store the model request to do it simultaneously in case we want to do concurrent requests to save the time
            self.model_request.append(
                [
                    class_name,
                    [message] if rect_data.type != "Table" else [message_table, message],
                    image_path,
                    rect_data.x1 - rect_data.x0,
                    rect_data.y1 - rect_data.y0,
                ]
            )
            return (
                f"<div class='{class_name}' style='{margin_style} {padding_style} max-height: {rect_data.y1 - rect_data.y0}pt; width: {rect_data.x1 - rect_data.x0}pt;'>\n"
                + f"ffff-{class_name}-content"
                + "\n</div>"
            )
        else:
            return (
                f"<div class='{class_name}' style='{margin_style} {padding_style}'>\n"
                + f"<div style='height: {rect_data.y1 - rect_data.y0}pt; width: {rect_data.x1 - rect_data.x0}pt; border: 1px solid black;'>\n"
                + f"ffff-{class_name}-content"
                + "\n</div>"
                + "\n</div>"
            )

    # Clean the grid coordinates to remove some small gaps/errors (ex. 2 columns of x-coordinates (1,12.6) and (12.7, 20), there is a small gap/error here which we can fix it to (1,12.65) and (12.65,20))
    def clean_grid_coordinates(
        self, coords: List[float], tolerance: float = 15
    ) -> List[float]:
        coords = sorted(coords)
        cleaned_data = [coords[0]]

        sum = 0
        cnt = 0

        for i in range(1, len(coords)):
            current = coords[i]
            previous = cleaned_data[-1]

            if current - previous > tolerance:
                sum = current
                cnt = 1
                cleaned_data.append(current)
            else:
                sum += current
                cnt += 1
                cleaned_data[-1] = round(sum / cnt, 1)

        return cleaned_data

    # Redistribute the grid coordinates to make the columns more balanced. Like divide the row into 3 part EQUALLY
    def redistribute_grid_coordinates(
        self, rect_data: List[RectData], av_tolerance: int = 20
    ):

        coords = []
        start_x = -1
        max_x = -1
        for rect in rect_data:
            if start_x == -1:
                start_x = rect.x0
                max_x = rect.x1
            else:
                if rect.x0 >= max_x:
                    coords.append(start_x)
                    coords.append(max_x)
                    start_x = rect.x0
                    max_x = rect.x1
                else:
                    max_x = max(max_x, rect.x1)

        coords.append(start_x)
        coords.append(max_x)
        coords = list(sorted(set(coords)))
        total_width = coords[-1] - coords[0]

        def generate_permutations(n: int) -> List[List[int]]:
            if n == 0:
                return [[]]
            else:
                res = []
                for i in range(1, 4):
                    for perm in generate_permutations(n - 1):
                        res.append([i] + perm)
                return res

        best_perm = None
        best_diff = 1000000

        # Try all the permutations and find the best one
        for perm in generate_permutations(len(coords) - 1):
            segment_sizes = [p * total_width / sum(perm) for p in perm]
            new_coords = [coords[0]]
            for segment_size in segment_sizes[:-1]:
                new_coords.append(new_coords[-1] + segment_size)
            new_coords.append(coords[-1])

            total_diff = sum(abs(coords[i] - new_coords[i]) for i in range(len(coords)))

            if total_diff < best_diff:
                best_diff = total_diff
                best_perm = perm

        # If the best diff is too large, then we don't need to redistribute the grid coordinates
        if best_diff > av_tolerance * (len(coords) - 2):
            return

        result = {}

        segment_sizes = [p * total_width / sum(best_perm) for p in best_perm]
        new_coords = [coords[0]]
        for segment_size in segment_sizes[:-1]:
            new_coords.append(new_coords[-1] + segment_size)
        new_coords.append(coords[-1])

        for i in range(len(coords)):
            result[coords[i]] = round(new_coords[i], 2)

        for rect in rect_data:
            rect.x0 = result[rect.x0] if rect.x0 in result else rect.x0
            rect.x1 = result[rect.x1] if rect.x1 in result else rect.x1

    # Check if the text box has multiple text lines
    def has_multiple_lines(self, coord: RectData, spans: List[Dict[str, Any]]) -> bool:
        max_y = -1
        for span in spans:
            if coord.contain_rect(fitz.Rect(span["bbox"])):
                if max_y != -1 and max_y <= span["bbox"][1] + 1.5:
                    return True
                max_y = max(max_y, span["bbox"][3])
        return False

    # Check if the component is a new group of components (ex. a new paragraph or a new group of columns)
    def is_new_group(
        self,
        coord: RectData,
        previous_y: float,
        new_y: float,
        rect_data: List[RectData],
        bound_left: float,
        bound_right: float,
        spans: List[Dict[str, Any]],
        error: int = 3,
    ) -> bool:

        threshold = 1 if coord.type == "Text" else 10

        if self.is_column(
            coord, rect_data, bound_left, bound_right, spans, error=error
        ):

            if new_y - previous_y <= 2:
                return False

            if self.has_multiple_lines(coord, spans) and (
                coord.x0 > bound_left + error or coord.x1 < bound_right - error
            ):
                return False

            ranges = []
            for rect in rect_data:
                if new_y <= rect.y0 and rect.y0 <= new_y + threshold:
                    ranges.append((rect.x0, rect.x1))

            for rect in rect_data:
                if new_y + threshold < rect.y0 <= new_y + threshold + 20:
                    overlap = False
                    for rx0, rx1 in ranges:
                        if min(rx1, rect.x1) - max(rx0, rect.x0) > 5:
                            overlap = True
                            break
                    if not overlap:
                        return False

            return True
        else:
            return True

    # Check if the component is a column component, i.e. not the row component that cover the whole lines
    def is_column(
        self,
        coord: RectData,
        rect_data: List[RectData],
        bound_left: float,
        bound_right: float,
        spans: List[Dict[str, Any]],
        error: int = 3,
    ) -> bool:

        for rect in rect_data:
            if (
                rect != coord
                and rect.y1 - coord.y0 >= error
                and coord.y1 - rect.y0 >= error
                and (rect.x0 + error > coord.x1 or rect.x1 - error < coord.x0)
            ):
                return True
        if self.has_multiple_lines(coord, spans) and (
            coord.x0 > bound_left + error or coord.x1 < bound_right - error
        ):
            return True
        return False

    # Generate the HTML code for the column component
    async def generate_column_html(
        self,
        rect_data: List[RectData],
        page_number: int,
        spans: List[Dict[str, Any]],
        prev_y_coordinate: float,
        bound_left: float,
        bound_right: float,
    ) -> str:

        # Preprocess the x-coordinates of the rect_data to divide the rect_data into multiple smaller columns (ex. col1, col2, ...)
        rect_data.sort(key=lambda r: (r.x0, r.y0))
        x_coordinates = [bound_left, bound_right]
        for rect in rect_data:
            x_coordinates.append(rect.x0)
            x_coordinates.append(rect.x1)
        x_coordinates = self.clean_grid_coordinates(x_coordinates)
        x_coordinates[0] = bound_left
        x_coordinates[-1] = bound_right

        for rect in rect_data:
            rect.x0 = min(x_coordinates, key=lambda x: abs(x - rect.x0))
            rect.x1 = min(x_coordinates, key=lambda x: abs(x - rect.x1))
        rect_data.sort(key=lambda r: (r.x0, r.y0))

        max_prev_x = -1
        for rect in rect_data:
            if max_prev_x != -1 and rect.x0 > max_prev_x:
                middle_x = (max_prev_x + rect.x0) / 2
                change_start = rect.x0
                change_end = max_prev_x

                for temp_rect in rect_data:
                    if temp_rect.x0 == change_start:
                        temp_rect.x0 = middle_x
                    if temp_rect.x1 == change_end:
                        temp_rect.x1 = middle_x

            max_prev_x = max(max_prev_x, rect.x1)

        self.redistribute_grid_coordinates(rect_data)

        # recursively generate the HTML code for each smaller column
        columns_components = []
        temp: List[RectData] = []
        start_x = -1
        max_x = -1
        for rect in rect_data:
            if start_x == -1:

                if rect.x0 != bound_left:
                    columns_components.append(
                        f"<div style='width: {rect.x0 - bound_left}pt;'></div>"
                    )

                start_x = rect.x0
                max_x = rect.x1
            else:
                if rect.x0 >= max_x:
                    html_parts = await self.generate_row_html(
                        temp, page_number, spans, start_x, max_x
                    )
                    columns_components.append(
                        (
                            f"<div style='width: {max_x - start_x}pt;'>\n"
                            + html_parts
                            + "\n</div>"
                        )
                    )
                    temp = []
                    start_x = rect.x0
                    max_x = rect.x1
                else:
                    max_x = max(max_x, rect.x1)
            temp.append(rect)

        if len(temp) != 0:
            html_parts = await self.generate_row_html(
                temp, page_number, spans, start_x, max_x
            )
            columns_components.append(
                (
                    f"<div style='width: {max_x - start_x}pt;'>\n"
                    + html_parts
                    + "\n</div>"
                )
            )

        margin_style = "margin-top: 0pt;"
        if (
            prev_y_coordinate != -1
            and rect_data[0].y0 > prev_y_coordinate + self.margin_top_decrease
        ):
            margin_style = f"margin-top: {(rect_data[0].y0 - prev_y_coordinate - self.margin_top_decrease)}pt;"

        return (
            f"<div class='column_container' style='{margin_style}'>\n"
            + "\n".join(columns_components)
            + f"\n</div>"
        )

    # Generate the HTML code for the row component
    async def generate_row_html(
        self,
        rect_data: List[RectData],
        page_number: int,
        spans: List[Dict[str, Any]],
        bound_left: float = None,
        bound_right: float = None,
    ) -> str:

        if bound_left is None:
            bound_left = self.leftmost_coordinates
        if bound_right is None:
            bound_right = self.rightmost_coordinates

        rect_data.sort(key=lambda r: (r.y0, r.x0))
        html_parts = []
        prev_y_coordinate = -1

        temp: List[RectData] = []
        for i, rect in enumerate(rect_data):

            # Check if the component is a new group of components (ex. a new paragraph or a new group of columns)
            # If it is a new group of components, then we will call 'generate_column_html' to generate the HTML code for the previous group of column component
            temp_max_y = (
                max(prev_y_coordinate, max(rect.y1 for rect in temp))
                if len(temp) != 0
                else prev_y_coordinate
            )
            if (
                len(temp) != 0
                and rect.y0 > temp_max_y
                and self.is_new_group(
                    rect, temp_max_y, rect.y0, rect_data, bound_left, bound_right, spans
                )
            ):
                html_parts.append(
                    await self.generate_column_html(
                        temp,
                        page_number,
                        spans,
                        prev_y_coordinate,
                        bound_left,
                        bound_right,
                    )
                )
                for rect_temp in temp:
                    prev_y_coordinate = max(prev_y_coordinate, rect_temp.y1)
                temp = []

            # If it is a row component, then we can directly generate the HTML code and add it to the html_parts list.
            if not self.is_column(rect, rect_data, bound_left, bound_right, spans):
                if (
                    rect.type == "Text"
                    or rect.type == "Page-header"
                    or rect.type == "Page-footer"
                ):
                    self.cnt += 1
                    html_parts.append(
                        self.generate_text_html(
                            rect,
                            prev_y_coordinate,
                            bound_left,
                            f"component_{self.cnt}_{page_number}",
                            spans,
                        )
                    )

                elif rect.type == "Picture" or rect.type == "Table":
                    self.cnt += 1
                    html_parts.append(
                        await self.generate_non_text_html(
                            rect,
                            prev_y_coordinate,
                            bound_left,
                            page_number,
                            f"component_{self.cnt}_{page_number}",
                            spans,
                        )
                    )

                prev_y_coordinate = rect.y1

            else:
                temp.append(rect)

        if len(temp) != 0:
            html_parts.append(
                await self.generate_column_html(
                    temp, page_number, spans, prev_y_coordinate, bound_left, bound_right
                )
            )

        return "\n".join(html_parts)

    # Generate the HTML code for each page
    async def generate_page_html(self, page_number: int) -> str:
        self.cnt = 0
        page = self.doc[page_number]
        spans = []
        for block in page.get_text("dict")["blocks"]:
            if "lines" in block and len(block["lines"]) > 0:
                for line in block["lines"]:
                    for span in line["spans"]:
                        spans.append(span)

        result_html = f"<div class='background-page' id='page_{page_number}'>\n"

        # Consider the header part
        header_rect_data = [
            rect for rect in self.rect_data[page_number] if rect.type == "Page-header"
        ]
        if len(header_rect_data) > 0:
            header_y_coordinate = min(rect.y0 for rect in header_rect_data)
            html_header = await self.generate_row_html(
                header_rect_data, page_number, spans
            )
            result_html += f"""
                <div class='header_{page_number}' style='position: absolute; top: {header_y_coordinate}pt; left: {self.padding}pt; right: {self.padding}pt;'>
                    {html_header}
                </div>
            """

        # Consider the body part
        body_rect_data = [
            rect
            for rect in self.rect_data[page_number]
            if rect.type != "Page-header" and rect.type != "Page-footer"
        ]
        if len(body_rect_data) > 0:
            body_y_coordinate = min(rect.y0 for rect in body_rect_data)
            html_body = await self.generate_row_html(body_rect_data, page_number, spans)
            result_html += f"""
                <div class='body_{page_number}' style='position: absolute; top: {body_y_coordinate}pt; left: {self.padding}pt; right: {self.padding}pt;'>
                    {html_body}
                </div>
            """

        # Consider the footer part
        footer_rect_data = [
            rect for rect in self.rect_data[page_number] if rect.type == "Page-footer"
        ]
        if len(footer_rect_data) > 0:
            footer_y_coordinate = min(rect.y0 for rect in footer_rect_data)
            html_footer = await self.generate_row_html(
                footer_rect_data, page_number, spans
            )
            result_html += f"""
                <div class='footer_{page_number}' style='position: absolute; top: {footer_y_coordinate}pt; left: {self.padding}pt; right: {self.padding}pt;'>
                    {html_footer}
                </div>
            """

        result_html += "\n</div>"
        return result_html

    def reset(self):
        self.cnt = 0
        self.total_tokens = 0
        self.model_request = []

    # Format the length of the html code to make it more accurate
    # Ex. the space between paragraph should be equal for every page (We generate each page seperately, so it might not be equal for each page)
    def format_length(
        self, template_html: str, styles: List[Tuple[str, int]]
    ):  # List of tuples (style_field, tolerance)

        # Use regex for single pass (Don't have to read the whole long string multiple times)
        field_pattern = "|".join(re.escape(field) for field, _ in styles)
        pattern = rf"({field_pattern}):\s*([0-9]*\.?[0-9]+)pt"
        style_dict = {style: [] for style, _ in styles}
        tolerances = {style: tolerance for style, tolerance in styles}

        matches = re.findall(pattern, template_html)
        for field_name, value_str in matches:
            value = float(value_str)
            style_dict[field_name].append(value)

        processed_dict = {}
        for style_field, data in style_dict.items():
            if len(data) == 0:
                continue
            cleaned_data = self.clean_grid_coordinates(
                data, tolerance=tolerances[style_field]
            )
            cleaned_data = [round(length, 2) for length in cleaned_data]
            cleaned_data.append(0)
            processed_dict[style_field] = cleaned_data

        def replacer(match):
            field_name = match.group(1)
            value = float(match.group(2))
            new_value = min(processed_dict[field_name], key=lambda x: abs(x - value))
            return f"{field_name}: {new_value}pt"

        return re.sub(pattern, replacer, template_html)

    # Process the model request to generate the HTML code for the non-text component
    # We can choose to do it simultaneously or not
    async def process_model_request(
        self, template_html: str, simultaneous_requests: bool = True
    ):

        if self.model_client is None or len(self.model_request) == 0:
            return template_html

        async def process_request(request: List[Any]):
            class_name, messages, image_path, width, height = request

            try:
                agent = await self.available_agents.get()
                response = await agent.run(task=messages)
                self.total_tokens += (
                    response.messages[-1].models_usage.completion_tokens
                    + response.messages[-1].models_usage.prompt_tokens
                )
                print(
                    f"Completion tokens: {response.messages[-1].models_usage.completion_tokens}, Prompt tokens: {response.messages[-1].models_usage.prompt_tokens}"
                )

            finally:
                await agent.on_reset(CancellationToken())
                self.available_agents.put_nowait(agent)
                print(f"Completed request for {class_name}")

            if "CANNOT_BE_GENERATED" in response.messages[-1].content:
                relative_image_path = os.path.relpath(
                    image_path,
                    os.path.dirname(self.output_path) if self.output_path else ".",
                )
                return [
                    f"ffff-{class_name}-content",
                    f"<img src='{relative_image_path}' style='width: {width}pt; height: {height}pt;'>",
                ]
            else:
                return [f"ffff-{class_name}-content", response.messages[-1].content]

        results = None
        if simultaneous_requests:
            tasks = [process_request(request) for request in self.model_request]
            results = await asyncio.gather(*tasks)
        else:
            results = [await process_request(request) for request in self.model_request]

        # Use regex for single pass (Don't have to read the whole long string multiple times)
        replacements = {result[0]: result[1] for result in results}
        pattern = "|".join([re.escape(key) for key in replacements.keys()])
        template_html = re.sub(
            pattern, lambda m: replacements[m.group(0)], template_html
        )
        return template_html

    async def generate_all_pages(self, simultaneous_requests: bool = False):
        self.reset()
        template = (
            html_template.replace("ffff-width", str(self.page_width))
            .replace("ffff-height", str(self.page_height))
            .replace("ffff-padding", str(self.padding))
        )

        html_parts = []
        for page_number in range(len(self.rect_data)):
            page_html = await self.generate_page_html(page_number)
            html_parts.append(page_html)

        template = template.replace("ffff-content", "\n".join(html_parts))
        template = self.format_length(
            template,
            [("margin-top", 0.3), ("top", 5), ("width", 4), ("padding-left", 4)],
        )

        if self.model_client is not None:
            template = await self.process_model_request(template, simultaneous_requests)

        if self.output_path is not None:
            with open(self.output_path, "w") as file:
                file.write(template)

        print(f"Total tokens: {self.total_tokens}")

        return template
