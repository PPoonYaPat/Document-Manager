from typing import Dict, List, Tuple
from DocManager.chatbot_backend.backend_data import ComponentStyle
import re

class TreeComponents:
    def __init__(self, html_content: str):
        self.tree_dict = self.get_tree_components(html_content)

    def get_tree_components(self, html_content: str) -> Dict[str, List[int]]: # List of size 2 for In index and Out 
        result: Dict[str, List[int]] = {}
        stack: List[Tuple[str, int]] = []
        cnt = 0
        div_pattern = r'(<div[^>]*>|</div>)'
        
        for match in re.finditer(div_pattern, html_content):
            tag = match.group(1)
            start_pos = match.start()
            end_pos = match.end() - 1
            
            if tag.startswith('<div'):
                class_name = self._extract_classname(tag)
                stack.append((class_name, cnt))
                if "component_" in class_name:
                    cnt += 1
            else:
                assert tag == '</div>'
                assert len(stack) >= 1
                class_name, div_start = stack.pop()
                result[class_name] = [div_start, cnt]
        
        return result

    def _extract_classname(self, tag: str) -> str:
        class_pattern = r'class\s*=\s*["\']([^"\']*)["\']'
        match = re.search(class_pattern, tag)
        return match.group(1) if match else ""

    def merge_components(self, components: List[ComponentStyle]) -> List[List[ComponentStyle]]:

        for component in components:
            if component.component_name not in self.tree_dict:
                self.tree_dict[component.component_name] = [100000, 100000]

        sorted_components = sorted(components, key=lambda c: self.tree_dict[c.component_name][0])

        result: List[List[ComponentStyle]] = []
        temp_components: List[ComponentStyle] = []
        for component in sorted_components:
            if len(temp_components) == 0 or (temp_components[-1].page == component.page and self.tree_dict[temp_components[-1].component_name][1] == self.tree_dict[component.component_name][0]):
                temp_components.append(component)
            else:
                result.append(temp_components)
                temp_components = [component]
                
        result.append(temp_components)

        sorted_result = sorted(result, key=lambda x: x[0].page)

        return sorted_result