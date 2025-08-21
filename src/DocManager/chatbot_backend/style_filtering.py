from typing import Dict

def filter_default_styles(style_values: Dict[str, str]) -> Dict[str, str]:
        default_values = {
            'auto', 'none', 'normal', 'initial', 'inherit', 'unset',
            '0', '0px', '0s', '0%', '0deg', '1', '100%',
            'transparent', 'rgba(0, 0, 0, 0)', 'rgb(0, 0, 0)',
            'visible', 'static', 'start', 'baseline', 'stretch',
            'repeat', 'scroll', 'border-box', 'ease', 'running',
            'replace', 'fill', 'butt', 'miter', 'round',
            'horizontal-tb', 'ltr', 'wrap', 'collapse', 'isolate',
            'slice', 'show', 'disc', 'outside', 'clip', 'economy',
            'over', 'space-around', 'luminance', 'add', 'match-source',
            'numeric-only', 'manual', 'from-image', 'srgb', 'linearrgb',
            'nonzero', 'separate', 'row', 'nowrap', 'fixed', 'no-limit',
            'logical', 'inline', 'top', 'break-word', 'solid', 'flat',
            'all', 'sub', 'block', 'always', 'element', 'read-only',
            'vertical-right', 'padding-box', 'auto 0deg', '0% 0%',
            '50% 50%', '0px 0px', '4', '1px', '8', '2', '8.32px',
            'none solid rgb(255, 0, 0)', 'text-decoration', 'rgb(255, 255, 255)'
        }

        default_properties = {
            'corner-bottom-left-shape', 'corner-bottom-right-shape',
            'corner-end-end-shape', 'corner-end-start-shape',
            'corner-start-end-shape', 'corner-start-start-shape',
            'corner-top-left-shape', 'corner-top-right-shape',
            
            'perspective-origin', 'transform-origin', 'outline-color',
            'outline-offset', 'outline-style', 'outline-width',
            'lighting-color', 'object-position', 'offset-rotate',
            'orphans', 'widows', 'tab-size', 'stroke-miterlimit',
            'stroke-width', 'scroll-timeline-axis', 'view-timeline-axis',
            'position-visibility', 'transform-style', 'transition-property',
            
            'animation-delay', 'animation-duration', 'animation-fill-mode',
            'animation-iteration-count', 'animation-name', 'animation-play-state',
            'animation-timing-function', 'animation-composition', 'animation-timeline',
            'transition-delay', 'transition-duration', 'transition-timing-function',
            
            'border-image-outset', 'border-image-repeat', 'border-image-slice',
            'border-image-source', 'border-image-width',
            
            'background-attachment', 'background-clip', 'background-origin',
            'background-position', 'background-repeat', 'background-size',
            
            'grid-auto-columns', 'grid-auto-flow', 'grid-auto-rows',
            'grid-column-end', 'grid-column-start', 'grid-row-end', 'grid-row-start',
            'grid-template-areas', 'grid-template-columns', 'grid-template-rows',
            
            'flex-basis', 'flex-direction', 'flex-grow', 'flex-shrink', 'flex-wrap',
            
            'mask-clip', 'mask-composite', 'mask-image', 'mask-mode',
            'mask-origin', 'mask-position', 'mask-repeat', 'mask-size', 'mask-type',
            
            'text-align', 'text-decoration-line', 'text-decoration-style',
            'text-emphasis-style', 'text-emphasis-position', 'text-underline-position',
            'text-wrap-mode', 'text-wrap-style', 'white-space-collapse',
            
            'baseline-shift', 'border-collapse', 'box-decoration-break',
            'caption-side', 'clip-rule', 'color-interpolation', 'color-interpolation-filters',
            'dominant-baseline', 'empty-cells', 'field-sizing', 'fill-opacity',
            'fill-rule', 'flood-opacity', 'font-kerning', 'font-optical-sizing',
            'font-synthesis-small-caps', 'font-synthesis-style', 'font-synthesis-weight',
            'hyphenate-character', 'hyphenate-limit-chars', 'hyphens',
            'image-orientation', 'image-rendering', 'interpolate-size',
            'line-break', 'list-style-position', 'list-style-type',
            'object-fit', 'overflow-wrap', 'pointer-events', 'print-color-adjust',
            'ruby-align', 'ruby-position', 'scroll-behavior', 'shape-rendering',
            'stop-opacity', 'stroke-linecap', 'stroke-linejoin', 'stroke-opacity',
            'table-layout', 'text-align-last', 'text-anchor', 'text-decoration-skip-ink',
            'text-rendering', 'text-size-adjust', 'user-select', 'vector-effect',
            'vertical-align'
        }
        
        color_properties_with_text_color = {
            'border-bottom-color', 'border-top-color', 'border-left-color', 'border-right-color',
            'border-block-end-color', 'border-block-start-color', 
            'border-inline-end-color', 'border-inline-start-color',
            'caret-color', 'column-rule-color', 'outline-color',
            'text-decoration-color', 'text-emphasis-color', 
            '-webkit-text-fill-color', '-webkit-text-stroke-color'
        }
        
        filtered_styles = {}
        
        for prop, value in style_values.items():
            if prop.startswith("-webkit-"):
                continue
                
            if prop in default_properties:
                continue
                
            if value in default_values:
                continue
                
            if prop in color_properties_with_text_color and value == style_values.get('color', ''):
                continue
                
            if (prop.startswith(('margin-', 'padding-')) or 
                prop.startswith(('inset-', 'scroll-margin-', 'scroll-padding-')) or
                prop in ['margin-block-end', 'margin-block-start', 'margin-inline-end', 'margin-inline-start',
                        'padding-block-end', 'padding-block-start', 'padding-inline-end', 'padding-inline-start']) and \
                value == '0px':
                continue
                
            if prop.endswith('radius') and value == '0px':
                continue
                
            if prop.endswith(('-width', '-style')) and prop.startswith('border-') and value in ['0px', 'none']:
                continue
                
            if prop in ['x', 'y', 'cx', 'cy', 'r'] and value == '0px':
                continue
            if prop in ['rx', 'ry'] and value == 'auto':
                continue
                
            filtered_styles[prop] = value
        
        return filtered_styles