html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            background-color: #f0f0f0;
            margin: 0;
            padding: 20px;
        }
        
        .background-page {
            width: ffff-widthpt;
            height: ffff-heightpt;
            margin: 20px auto;
            padding: ffff-paddingpt;
            background-color: white;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            display: flex;
            flex-direction: column;
            position: relative;
        }

        .column_container {
            display: flex;
            gap: 15px;
        } 
    </style>
</head>
<body>
    ffff-content
</body>
</html>
"""

editable_html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <title>ffff-title</title>
    
    <!-- GrapesJS CSS -->
    <link rel="stylesheet" href="https://unpkg.com/grapesjs/dist/css/grapes.min.css">
    
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        html, body {
            background-color: #f0f0f0;
            margin: 0;
            padding: 20px;
        }

        .editor-container {
            display: flex;
            gap: 20px;
            max-width: none;
            margin: 20px auto 0 auto;
            justify-content: center;
            align-items: flex-start;
        }

        /* Chatbot */
        .chatbot-panel {
            width: 600px;
            background: white;
            border: 1px solid #ccc;
            border-radius: 5px;
            height: 800px;
            overflow-y: auto;
            display: none;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }

        .chatbot-panel.show {
            display: block;
        }

        /* Control Panel */
        .control-panel {
            width: 200px;
            background: white;
            border: 1px solid #ccc;
            border-radius: 5px;
            padding: 15px;
            height: fit-content;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }

        .control-btn {
            display: block;
            width: 100%;
            padding: 10px 15px;
            margin-bottom: 8px;
            border: none;
            border-radius: 4px;
            background: #dc3545;
            color: white;
            font-size: 14px;
            cursor: pointer;
            transition: background 0.2s;
        }

        .control-btn:hover {
            background: #c82333;
        }

        .control-btn:last-child {
            margin-bottom: 0;
        }

        /* GrapesJS Editor Container */
        .gjs-editor-container {
            width: ffff-extra-width;
            height: ffff-height;
            background: white;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            display: flex;
            flex-direction: column;
            position: relative;
        }

        /* Style Manager Panel */
        .style-manager-panel {
            width: 300px;
            background: white;
            border: 1px solid #ccc;
            border-radius: 5px;
            height: ffff-height;
            overflow-y: auto;
            display: none;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }

        .style-manager-panel.show {
            display: block;
        }

        .panel-header {
            background: #f8f9fa;
            padding: 15px;
            border-bottom: 1px solid #ddd;
            font-weight: bold;
            color: #333;
        }

        .panel-section {
            padding: 15px;
            border-bottom: 1px solid #eee;
        }

        .panel-section h4 {
            margin: 0 0 10px 0;
            color: #333;
            font-size: 14px;
        }

        .add-element-btn {
            width: 100%;
            padding: 8px 12px;
            margin-bottom: 8px;
            border: none;
            border-radius: 4px;
            background: #28a745;
            color: white;
            font-size: 13px;
            cursor: pointer;
            transition: background 0.2s;
        }

        .add-element-btn:hover {
            background: #218838;
        }

        /* Auto-save indicator */
        .auto-save-indicator {
            position: fixed;
            top: 10px;
            right: 20px;
            background: #28a745;
            color: white;
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 12px;
            opacity: 0;
            transition: opacity 0.3s;
            z-index: 2000;
        }

        .auto-save-indicator.show {
            opacity: 1;
        }

        /* GrapesJS overrides */
        .gjs-cv-canvas {
            top: 0;
            width: 100% !important;
            height: 100% !important;
        }

        /* Hide default panels */
        .gjs-pn-panels {
            display: none !important;
        }

        .gjs-toolbar {
            display: none !important;
        }

        .gjs-pn-panel#gjs-pn-layers-panel { display: none !important; }
        .gjs-pn-panel#gjs-layers-container { display: none !important; }
        .gjs-pn-btn[data-id="open-layers"] { display: none !important; }

        .chat-container {
            width: 100%;
            height: 700px;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            padding: 20px;
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
        }

        .messages {
            flex: 1;
            overflow-y: auto;
            border-bottom: 1px solid #ddd;
            margin-bottom: 20px;
        }

        .message {
            margin: 10px 0;
        }

        .message.user {
            text-align: right;
        }

        .message.assistant {
            text-align: left;
        }

        .message.error {
            color: #721c24;
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            padding: 10px;
            border-radius: 4px;
            margin: 10px 0;
        }

        .message.system {
            color: #0c5460;
            background-color: #d1ecf1;
            border: 1px solid #bee5eb;
            padding: 10px;
            border-radius: 4px;
            margin: 10px 0;
        }

        .input-container input:disabled,
        .input-container button:disabled {
            background-color: #e0e0e0;
            cursor: not-allowed;
        }

        .chat-input-container {
            padding: 16px 0;
        }

        .chat-input {
            width: 100%;
            border: 1px solid #e0e0e0;
            border-radius: 12px;
            padding: 16px;
            font-size: 14px;
            resize: vertical;
            min-height: 80px;
            margin-bottom: 16px;
            font-family: inherit;
            background: transparent;
            transition: border-color 0.2s ease;
        }

        .chat-input:focus {
            outline: none;
            border-color: #6366f1;
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        }

        .rag-controls {
            margin-bottom: 16px;
        }

        .rag-header {
            margin-bottom: 16px;
        }

        .rag-toggle-container {
            display: flex;
            align-items: center;
            cursor: pointer;
            gap: 12px;
        }

        .rag-checkbox {
            display: none;
        }

        .rag-toggle-slider {
            position: relative;
            width: 48px;
            height: 26px;
            background: #e5e7eb;
            border-radius: 26px;
            transition: all 0.3s ease;
        }

        .rag-toggle-slider::before {
            content: '';
            position: absolute;
            width: 22px;
            height: 22px;
            border-radius: 50%;
            background: white;
            top: 2px;
            left: 2px;
            transition: all 0.3s ease;
            box-shadow: 0 2px 6px rgba(0,0,0,0.15);
        }

        .rag-checkbox:checked + .rag-toggle-slider {
            background: #6366f1;
        }

        .rag-checkbox:checked + .rag-toggle-slider::before {
            transform: translateX(22px);
        }

        .rag-label {
            font-weight: 500;
            color: #374151;
            font-size: 15px;
        }

        .rag-options {
            animation: slideDown 0.3s ease;
            padding-left: 8px;
        }

        @keyframes slideDown {
            from { opacity: 0; transform: translateY(-8px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .page-mode-options {
            display: flex;
            gap: 24px;
            margin-bottom: 16px;
            flex-wrap: wrap;
        }

        .radio-option {
            display: flex;
            align-items: center;
            cursor: pointer;
            gap: 8px;
            padding: 8px 0;
            transition: all 0.2s ease;
        }

        .radio-option:hover .radio-label {
            color: #6366f1;
        }

        .radio-option input[type="radio"] {
            display: none;
        }

        .radio-custom {
            width: 18px;
            height: 18px;
            border: 2px solid #d1d5db;
            border-radius: 50%;
            position: relative;
            transition: all 0.2s ease;
        }

        .radio-option input[type="radio"]:checked + .radio-custom {
            border-color: #6366f1;
            background: #6366f1;
        }

        .radio-option input[type="radio"]:checked + .radio-custom::after {
            content: '';
            position: absolute;
            width: 6px;
            height: 6px;
            background: white;
            border-radius: 50%;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
        }

        .radio-label {
            font-size: 14px;
            color: #6b7280;
            transition: color 0.2s ease;
        }

        .page-range-section {
            padding-top: 12px;
            margin-left: 8px;
        }

        .range-inputs {
            display: flex;
            gap: 16px;
            align-items: end;
        }

        .input-group {
            display: flex;
            flex-direction: column;
            gap: 6px;
        }

        .input-group label {
            font-size: 13px;
            color: #6b7280;
            font-weight: 500;
        }

        .input-group input {
            width: 80px;
            padding: 8px 12px;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
            background: transparent;
            transition: border-color 0.2s ease;
        }

        .input-group input:focus {
            outline: none;
            border-color: #6366f1;
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        }

        .send-button {
            background: #6366f1;
            color: white;
            border: none;
            border-radius: 10px;
            padding: 12px 24px;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 8px;
            transition: all 0.2s ease;
            margin-left: auto;
            box-shadow: 0 2px 8px rgba(99, 102, 241, 0.3);
        }

        .send-button:hover {
            background: #5855eb;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
        }

        .send-button:active {
            transform: translateY(0);
        }
    </style>
</head>
<body>
    <!-- Auto-save indicator -->
    <div class="auto-save-indicator" id="autoSaveIndicator">Auto-saved ✓</div>

    <div class="control-panel" style="margin: 0 auto; display: flex; justify-content: center;">
        <button id="saveAllBtn" class="control-btn" onclick="saveallHTML()">Download All Pages</button>
    </div>

    <div class="main-container"></div>

    <!-- GrapesJS JavaScript -->
    <script src="https://unpkg.com/grapesjs"></script>
    
    <script>
        let editors = {};
        let isEditModes = {};
        let autoSaveTimeouts = {};

        // Function to initialize editor for a specific page (according to the class name)
        async function initializePageEditor(className) {
            const editorId = className;
            
            // Initialize state for this editor (editorId is the class name)
            editors[editorId] = null;
            isEditModes[editorId] = false;
            autoSaveTimeouts[editorId] = null;

            try {
                editors[editorId] = grapesjs.init({
                    container: `#${className}`,
                    width: 'ffff-width',
                    height: 'ffff-height',
                    storageManager: false,
                    avoidInlineStyle: false,
                    panels: { defaults: [] },
                    styleManager: {
                        appendTo: `#style-manager-${className}`,
                        sectors: [{
                            name: 'Text',
                            open: true,
                            properties: [
                                'font-size',
                                'font-family', 
                                'color',
                                'text-align',
                                'font-weight',
                                'line-height'
                            ]
                        }, {
                            name: 'Appearance',
                            open: true,
                            properties: [
                                'background-color',
                                'border',
                                'border-radius',
                                'padding',
                                'margin'
                            ]
                        }, {
                            name: 'Size & Position',
                            open: true,
                            properties: [
                                'width',
                                'height',
                                'position',
                                'top',
                                'left'
                            ]
                        }]
                    },
                    canvas: { styles: [], scripts: [] }
                });

                // Set initial content
                const contentWithStyle = `
                    <style>
                        .column_container {
                            display: flex;
                            gap: 15px;
                        }
                    </style>
                    ${class_dict[className]}
                `;
                editors[editorId].setComponents(contentWithStyle);

                editors[editorId].on('load', () => {
                    setTimeout(() => {
                        // Get all components
                        const allComponents = editors[editorId].getWrapper().find('*');
                        
                        allComponents.forEach(component => {
                            const element = component.getEl();
                            if (element && element.getAttribute('style')) {
                                const styleAttr = element.getAttribute('style');
                                const styles = {};
                                
                                // Parse existing inline styles
                                styleAttr.split(';').forEach(rule => {
                                    const [prop, val] = rule.split(':').map(s => s.trim());
                                    if (prop && val) {
                                        styles[prop] = val;
                                    }
                                });
                                
                                // Apply to GrapesJS component
                                component.setStyle(styles);
                            }
                        });
                    }, 3000);
                    
                    const canvas = editors[editorId].Canvas;
                    canvas.getFrameEl().style.pointerEvents = 'none';
                });

                // Make styles sync when changed
                editors[editorId].on('component:update:style', (component) => {
                    const element = component.getEl();
                    if (element) {
                        const styles = component.getStyle();
                        const styleString = Object.keys(styles)
                            .map(prop => `${prop}: ${styles[prop]}`)
                            .join('; ');
                        element.setAttribute('style', styleString);
                    }
                });

                setupAutoSave(editorId);
                setViewMode(editorId);

                const stylePanel = document.getElementById(`styleManagerPanel-${className}`);
                if (stylePanel) {
                    stylePanel.classList.remove('show');
                }

                console.log(`GrapesJS initialized successfully for ${className}`);
            } catch (error) {
                console.error(`Error initializing GrapesJS for ${className}:`, error);
            }
        }

        // Setup event listeners for a specific page (according to the class name)
        function setupEventListeners(className) {
            const saveBtn = document.getElementById(`saveBtn-${className}`);
            const toggleViewBtn = document.getElementById(`toggleViewBtn-${className}`);
            const resetBtn = document.getElementById(`resetBtn-${className}`);
            const messageInput = document.getElementById(`message-input-${className}`);

            if (saveBtn) {
                saveBtn.addEventListener('click', () => saveHTML(className));
            }
            if (toggleViewBtn) {
                toggleViewBtn.addEventListener('click', () => toggleEditMode(className));
            }
            if (resetBtn) {
                resetBtn.addEventListener('click', () => resetContent(className));
            }
            if (messageInput) {
                messageInput.addEventListener('keydown', function (event) {
                    if (event.key === 'Enter') {
                        sendMessage(className);
                    }
                });
            }
        }

        // Toggle edit mode for a specific page
        function toggleEditMode(className) {
            const editorId = className;
            isEditModes[editorId] = !isEditModes[editorId];
            const toggleBtn = document.getElementById(`toggleViewBtn-${className}`);
            const stylePanel = document.getElementById(`styleManagerPanel-${className}`);
            const chatPanel = document.getElementById(`chatbotPanel-${className}`);
            
            if (isEditModes[editorId]) {
                if (toggleBtn) toggleBtn.textContent = 'View Result';
                if (stylePanel) stylePanel.classList.add('show');
                if (chatPanel) chatPanel.classList.add('show');
                setEditMode(editorId);
            } else {
                if (toggleBtn) toggleBtn.textContent = 'Edit Page';
                if (stylePanel) stylePanel.classList.remove('show');
                if (chatPanel) chatPanel.classList.remove('show');
                setViewMode(editorId);
            }
        }

        // Force to Edit Mode
        function forceEditMode(className) {
            const editorId = className;
            isEditModes[editorId] = true;
            const toggleBtn = document.getElementById(`toggleViewBtn-${className}`);
            const stylePanel = document.getElementById(`styleManagerPanel-${className}`);
            const chatPanel = document.getElementById(`chatbotPanel-${className}`);
            if (toggleBtn) toggleBtn.textContent = 'View Result';
            if (stylePanel) stylePanel.classList.add('show');
            if (chatPanel) chatPanel.classList.add('show');
            setEditMode(editorId);
        }

        // Set edit mode for a specific page
        function setEditMode(editorId) {
            if (editors[editorId]) {
                try {
                    const canvas = editors[editorId].Canvas;
                    canvas.getFrameEl().style.pointerEvents = 'auto';
                    editors[editorId].refresh();
                } catch (error) {
                    console.error('Error setting edit mode:', error);
                }
            }
        }

        // Set view mode for a specific page
        function setViewMode(editorId) {
            if (editors[editorId]) {
                try {
                    const canvas = editors[editorId].Canvas;
                    const frameEl = canvas.getFrameEl();

                    if (frameEl && frameEl.style) {
                        frameEl.style.pointerEvents = 'none';
                    }
                    editors[editorId].select();
                } catch (error) {
                    console.error('Error setting view mode:', error);
                }
            }
        }

        // Add row function for a specific page
        function addRow(className) {
            const editorId = className;
            if (editors[editorId] && isEditModes[editorId]) {
                try {
                    // Get the currently selected component to copy its style
                    const selectedComponent = editors[editorId].getSelected();
                    let styleToCopy = '';
                    
                    if (selectedComponent) {
                
                        const component = selectedComponent.toHTML();
                        const tempDiv = document.createElement('div');
                        tempDiv.innerHTML = component;
                        const element = tempDiv.firstElementChild;
                        
                        if (element) {
                            // Extract style from the inline style attribute
                            const inlineStyle = element.getAttribute('style') || '';
                            
                            const styleObj = {};
                            inlineStyle.split(';').forEach(rule => {
                                const [property, value] = rule.split(':').map(s => s.trim());
                                if (property && value) {
                                    styleObj[property] = value;
                                }
                            });
                            
                            styleToCopy = `
                                font-family: ${styleObj['font-family'] || 'UniversLT'};
                                font-weight: ${styleObj['font-weight'] || '300'};
                                color: ${styleObj['color'] || '#000000'};
                                font-size: ${styleObj['font-size'] || '8.0pt'};
                                line-height: ${styleObj['line-height'] || '1.2'};
                                opacity: ${styleObj['opacity'] || '1.0'};
                            `;
                        }
                    }
                    
                    // If no style was copied, use default style
                    if (!styleToCopy) {
                        styleToCopy = `
                            font-family: UniversLT;
                            font-weight: 300;
                            color: #000000;
                            font-size: 8.0pt;
                            line-height: 1.2;
                            opacity: 1.0;
                        `;
                    }
                    
                    const newRow = `
                        <div style="margin-top: 10pt; padding-left: 0.0pt; overflow-wrap: break-word; ${styleToCopy} position: relative;">
                            New row content here
                        </div>
                    `;
                    editors[editorId].addComponents(newRow);
                    debouncedSave(editorId);
                } catch (error) {
                    console.error('Error adding row:', error);
                }
            }
        }

        // Add column function for a specific page
        function addColumn(className) {
            const editorId = className;
            if (editors[editorId] && isEditModes[editorId]) {
                try {
                    // Get the currently selected component
                    const selectedComponent = editors[editorId].getSelected();
                    
                    if (selectedComponent) {
                        const component = selectedComponent.toHTML();
                        const tempDiv = document.createElement('div');
                        tempDiv.innerHTML = component;
                        const element = tempDiv.firstElementChild;
                        
                        // Check if the selected element is a column_container
                        if (element && element.classList.contains('column_container')) {
                            // Add new column to the selected column_container
                            const newColumn = '<div style="width: 30pt;"><div style="margin-top: 0.0pt; padding-left: 0.0pt; overflow-wrap: break-word; line-height: 1.2; font-family: UniversLT; font-weight: 300; color: #000000; font-size: 8.0pt; opacity: 1.0;">New column content here</div></div>';
                            const newComponent = editors[editorId].addComponents(newColumn);
                            selectedComponent.append(newComponent);
                            
                        } else {
                            // Create a new column_container with 2 example columns
                            const newColumnContainer = `
                                <div class="column_container" style="margin-top: 7.0pt;">
                                    <div style="width: 60pt;">
                                        <div style="margin-top: 0.0pt; padding-left: 0.0pt; overflow-wrap: break-word; line-height: 1.2; font-family: UniversLT; font-weight: 300; color: #000000; font-size: 8.0pt; opacity: 1.0;">
                                            First column content here
                                        </div>
                                    </div>
                                    <div style="width: 60pt;">
                                        <div style="margin-top: 0.0pt; padding-left: 0.0pt; overflow-wrap: break-word; line-height: 1.2; font-family: UniversLT; font-weight: 300; color: #000000; font-size: 8.0pt; opacity: 1.0;">
                                            Second column content here
                                        </div>
                                    </div>
                                </div>
                            `;
                            editors[editorId].addComponents(newColumnContainer);
                        }
                    } else {
                        // No selection, create a new column_container with 2 example columns
                        const newColumnContainer = `
                            <div class="column_container" style="margin-top: 7.0pt;">
                                <div style="width: 60pt;">
                                    <div style="margin-top: 0.0pt; padding-left: 0.0pt; overflow-wrap: break-word; line-height: 1.2; font-family: UniversLT; font-weight: 300; color: #000000; font-size: 8.0pt; opacity: 1.0;">
                                        First column content here
                                    </div>
                                </div>
                                <div style="width: 60pt;">
                                    <div style="margin-top: 0.0pt; padding-left: 0.0pt; overflow-wrap: break-word; line-height: 1.2; font-family: UniversLT; font-weight: 300; color: #000000; font-size: 8.0pt; opacity: 1.0;">
                                        Second column content here
                                    </div>
                                </div>
                            </div>
                        `;
                        editors[editorId].addComponents(newColumnContainer);
                    }
                    
                    debouncedSave(editorId);
                } catch (error) {
                    console.error('Error adding column:', error);
                }
            }
        }

        // Move component up to the previous editor
        function moveUp(className) {
            const editorId = className;
            if (editors[editorId] && isEditModes[editorId]) {
                try {
                    const currentIndex = parseInt(editorId.replace('gjs', ''));
                    if (currentIndex === 0) {
                        alert('Cannot move up from the first page');
                        return;
                    }

                    const selectedComponents = editors[editorId].getSelectedAll();
                    if (!selectedComponents || selectedComponents.length === 0) {
                        alert('Please select a component first');
                        return;
                    }

                    const targetEditorId = `gjs${currentIndex - 1}`;
                    if (!editors[targetEditorId]) {
                        alert('Target editor not available');
                        return;
                    }

                    selectedComponents.forEach(component => {
                        const componentHtml = component.toHTML();
                        const domEl = component.getEl();
                        let textStyles = {};
                        
                        if (domEl) {
                            // Get computed styles from the DOM element
                            const styles = window.getComputedStyle(domEl);
                            const textProperties = [
                                'color', 'font-family', 'font-size', 'font-weight', 
                                'font-style', 'text-decoration', 'line-height',
                                'letter-spacing', 'text-align', 'text-transform',
                                'font-variant', 'font-stretch', 'font-size-adjust'
                            ];
                            
                            textProperties.forEach(property => {
                                const value = styles.getPropertyValue(property);
                                if (value && value !== 'initial' && value !== 'normal') {
                                    textStyles[property] = value;
                                }
                            });

                            
                        }
                        
                        const componentClasses = component.getClasses();        
                        component.remove();
                        const newComponent = editors[targetEditorId].addComponents(componentHtml);
                        
                        // Apply computed styles and classes to the new component
                        if (newComponent && newComponent.length > 0) {
                            const firstComponent = newComponent[0];
                            
                            if (Object.keys(textStyles).length > 0) {
                                firstComponent.setStyle(textStyles);
                            }
                            
                            if (componentClasses && componentClasses.length > 0) {
                                firstComponent.setClass(componentClasses);
                            }
                        }
                    });
                   
                    debouncedSave(editorId);
                    debouncedSave(targetEditorId);
                    forceEditMode(targetEditorId);

                    console.log(`Moved component from ${editorId} to ${targetEditorId}`);
                } catch (error) {
                    console.error('Error moving component up:', error);
                    alert('Error moving component up');
                }
            }
        }

        // Move component down to the next editor
        function moveDown(className) {
            const editorId = className;
            if (editors[editorId] && isEditModes[editorId]) {
                try {
                    const currentIndex = parseInt(editorId.replace('gjs', ''));
                    if (currentIndex === Object.keys(editors).length - 1) {
                        alert('Cannot move down from the last page');
                        return;
                    }

                    const selectedComponents = editors[editorId].getSelectedAll();
                    if (!selectedComponents || selectedComponents.length === 0) {
                        alert('Please select a component first');
                        return;
                    }

                    const targetEditorId = `gjs${currentIndex + 1}`;
                    if (!editors[targetEditorId]) {
                        alert('Target editor not available');
                        return;
                    }

                    selectedComponents.forEach(component => {
                        const componentHtml = component.toHTML();
                        const domEl = component.getEl();
                        let textStyles = {};
                        
                        if (domEl) {
                            // Get computed styles from the DOM element
                            const styles = window.getComputedStyle(domEl);
                            const textProperties = [
                                'color', 'font-family', 'font-size', 'font-weight', 
                                'font-style', 'text-decoration', 'line-height',
                                'letter-spacing', 'text-align', 'text-transform',
                                'font-variant', 'font-stretch', 'font-size-adjust',
                            ];
                            
                            textProperties.forEach(property => {
                                const value = styles.getPropertyValue(property);
                                if (value && value !== 'initial' && value !== 'normal') {
                                    textStyles[property] = value;
                                }
                            });

                            // Check if it is a box of text element
                            const borderWidth = styles.getPropertyValue('border-width');
                            if (borderWidth && borderWidth !== '0px' && borderWidth !== '0') {
                                const borderProperties = [
                                    'border-width', 'border-style', 'border-color',
                                    'height', 'width'
                                ];
                                
                                borderProperties.forEach(property => {
                                    const value = styles.getPropertyValue(property);
                                    if (value && value !== 'initial' && value !== 'normal') {
                                        textStyles[property] = value;
                                    }
                                });
                            }
                        }
                        
                        const componentClasses = component.getClasses();        
                        component.remove();
                        const newComponent = editors[targetEditorId].addComponents(componentHtml);
                        
                        // Apply computed styles and classes to the new component
                        if (newComponent && newComponent.length > 0) {
                            const firstComponent = newComponent[0];
                            
                            if (Object.keys(textStyles).length > 0) {
                                firstComponent.setStyle(textStyles);
                            }
                            
                            if (componentClasses && componentClasses.length > 0) {
                                firstComponent.setClass(componentClasses);
                            }
                        }
                    });

                    debouncedSave(editorId);
                    debouncedSave(targetEditorId);
                    forceEditMode(targetEditorId);

                    console.log(`Moved component from ${editorId} to ${targetEditorId}`);
                } catch (error) {
                    console.error('Error moving component down:', error);
                    alert('Error moving component down');
                }
            }
        }

        // Save HTML for a specific page
        function saveHTML(className) {
            const editorId = className;
            if (!editors[editorId]) {
                alert('Editor not initialized');
                return;
            }

            try {
                const content = editors[editorId].getHtml();
                const css = editors[editorId].getCss();
                
                const finalHTML = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></`+`script>
    <title>ffff-title</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            background-color: #f0f0f0;
            margin: 0;
            padding: 20px;
        }
        
        .background-page {
            width: ffff-width;
            height: ffff-height;
            margin: 20px auto;
            background-color: white;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            display: flex;
            flex-direction: column;
            position: relative;
        }
        ${css}
    </style>
</head>
<body>
    ${content}
</body>
</html>`;
                
                // Download file
                const blob = new Blob([finalHTML], { type: 'text/html;charset=utf-8' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `ffff-title-${className}.html`;
                a.style.display = 'none';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);

            } catch (error) {
                console.error('Save error:', error);
                alert('Error saving file. Please try again.');
            }
        }

        // Save HTML for all pages
        function saveallHTML() {
            for (const editorId in editors) {
                if (!editors[editorId]) {
                    alert('Editor not initialized');
                    return;
                }
            }

            try {
                let content = "";
                let css = "";

                for (const editorId in editors) {
                    content += editors[editorId].getHtml() + "\\n";
                    css += editors[editorId].getCss() + "\\n";
                }
                
                const finalHTML = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></`+`script>
    <title>ffff-title</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            background-color: #f0f0f0;
            margin: 0;
            padding: 20px;
        }
        
        .background-page {
            width: 597.6pt;
            height: 842.4pt;
            margin: 20px auto;
            background-color: white;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            display: flex;
            flex-direction: column;
            position: relative;
        }
        ${css}
    </style>
</head>
<body>
    ${content}
</body>
</html>`;

                // Download file
                const blob = new Blob([finalHTML], { type: 'text/html;charset=utf-8' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `ffff-title.html`;
                a.style.display = 'none';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);

            } catch (error) {
                console.error('Save error:', error);
                alert('Error saving file. Please try again.');
            }
        }

        // Reset content for a specific page
        async function resetContent(className) {
            if (confirm('Reset all content? This cannot be undone.')) {
                const editorId = className;
                const initialContent = `
                    <style>
                        .column_container {
                            display: flex;
                            gap: 15px;
                        }
                    </style>
                ` + class_dict[className];
                
                if (editors[editorId]) {
                    editors[editorId].setComponents(initialContent);
                }
            }
        }

        // Auto-save functionality for a specific page
        async function saveToLocalStorage(editorId) {
            if (!isEditModes[editorId] || !editors[editorId]) return;
            
            try {
                const content = editors[editorId].getHtml();
                const css = editors[editorId].getCss();
                const data = {
                    html: content,
                    css: css,
                    timestamp: Date.now()
                };
                
                // Save to localStorage
                localStorage.setItem(`editor-${editorId}`, JSON.stringify(data));
                
                // Show auto-save indicator
                const indicator = document.getElementById('autoSaveIndicator');
                if (indicator) {
                    indicator.classList.add('show');
                    setTimeout(() => {
                        indicator.classList.remove('show');
                    }, 1000);
                }
            } catch (error) {
                console.error('Error saving to storage:', error);
            }
        }

        function debouncedSave(editorId) {
            clearTimeout(autoSaveTimeouts[editorId]);
            autoSaveTimeouts[editorId] = setTimeout(() => {
                saveToLocalStorage(editorId);
            }, 500);
        }

        function setupAutoSave(editorId) {
            if (!editors[editorId]) return;

            try {
                // Auto-save on component changes
                editors[editorId].on('component:add component:remove component:update', () => {
                    if (isEditModes[editorId]) {
                        debouncedSave(editorId);
                    }
                });

                // Auto-save on style changes
                editors[editorId].on('style:update', () => {
                    if (isEditModes[editorId]) {
                        debouncedSave(editorId);
                    }
                });
            } catch (error) {
                console.error('Error setting up auto-save:', error);
            }
        }

        async function sendMessage(className) {
            const input = document.getElementById(`message-input-${className}`);
            const button = document.querySelector(`#input-container-${className} button`);
            const message = input.value;
            const rag_input = getRAGSettings(className);

            if (rag_input && rag_input[0] == -1) {
                alert("Start page must be less than end page and between 1 and ffff-length");
                return;
            }

            const result = extractSelectedContent(className);
            console.log(result);

            if (rag_input) {
                displayMessage(message, 'user', className, "(rag: " + (rag_input[0] + 1) + " - " + (rag_input[rag_input.length - 1] + 1) + ")");
            } else {
                displayMessage(message, 'user', className);
            }

            input.value = '';
            input.disabled = true;
            button.disabled = true;

            try {

                let response = await fetch('http://localhost:8501/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        components: result,
                        message: message,
                        tag: "llm_call",
                        rag_range: getRAGSettings(className)
                    })
                });

                let data = await response.json();
                if (!response.ok) {
                    if (data.detail && data.detail.type === 'error') {
                        displayMessage(data.detail.content, 'error', className);
                    } else {
                        displayMessage('Error: ' + (data.detail || 'Unknown error'), 'error', className);
                    }
                    return;
                }
                
                if (data.tag == "tool_call") {
                    console.log(data.components);
                    const extracted_components = extractComponent(data.components);
                    console.log(extracted_components);
                    response = await fetch('http://localhost:8501/chat', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            components: extracted_components,
                            message: message,
                            tag: "tool_response",
                            rag_range: null
                        })
                    });
                    data = await response.json();
                    if (!response.ok) {
                        if (data.detail && data.detail.type === 'error') {
                            displayMessage(data.detail.content, 'error', className);
                        } else {
                            displayMessage('Error: ' + (data.detail || 'Unknown error'), 'error', className);
                        }
                        return;
                    } 
                }
                
                displayMessage(data.message, 'assistant', className);
                updateGrapesJSStyles(data.components);

            } catch (error) {
                console.error('Error:', error);
                displayMessage('Error: Could not reach the server.', 'error', className);

            } finally {
                input.disabled = false;
                button.disabled = false;
                input.focus();
            }
        }

        function updateGrapesJSStyles(components) {
            if (!components) return;

            components.forEach(component_group => {
                const page_number = component_group.page;
                const editorId = `gjs${page_number}`;
                const editor = editors[editorId];

                const classNames = component_group.component_name;
                const wrapper = editor.DomComponents.getWrapper();
                const grapesComponents = wrapper.find(`[class*="${classNames}"]`);

                if (grapesComponents.length !== 1) {
                    console.error(`Found ${grapesComponents.length} components (should be 1) for: ${classNames}`);
                    return;
                }

                const grapesComponent = grapesComponents[0];
                
                if (component_group.html && component_group.html.trim() !== '') {
                    const tempDiv = document.createElement('div');
                    tempDiv.innerHTML = component_group.html;
                    const newElement = tempDiv.firstElementChild;
                    
                    if (newElement && newElement.innerHTML) {
                        grapesComponent.components(newElement.innerHTML);
                    }
                }

                // Function to apply styles with retry logic
                const applyStyles = (retryCount = 0) => {
                    if (component_group.styles) {
                        Object.entries(component_group.styles).forEach(([component_name, styles]) => {
                            const targets = wrapper.find(`[class*="${component_name}"]`);

                            if (targets.length > 1) {
                                console.error(`Found ${targets.length} components (should be 1) for: ${component_name}`);
                                return; // Skip this style application
                            } else if (targets.length === 0) {
                                if (retryCount < 3) { // Retry up to 3 times
                                    console.log(`Component ${component_name} not found, retrying in 50ms... (attempt ${retryCount + 1})`);
                                    setTimeout(() => applyStyles(retryCount + 1), 50);
                                    return;
                                } else {
                                    console.error(`Component ${component_name} not found after 3 retries`);
                                    return;
                                }
                            }

                            const target = targets[0];
                            const currentHtml = target.toHTML();
                            
                            // Remove and re-add the component to force style detection
                            const parent = target.parent();
                            const index = parent.components().indexOf(target);
                            target.remove();
                            
                            // Create new element with updated styles
                            const tempEl = document.createElement('div');
                            tempEl.innerHTML = currentHtml;
                            const element = tempEl.firstElementChild;
                            
                            // Add new styles as inline styles
                            const styleString = Object.entries(styles)
                                .map(([prop, val]) => `${prop}: ${val}`)
                                .join('; ');
                            
                            const existingStyle = element.getAttribute('style') || '';
                            element.setAttribute('style', existingStyle + '; ' + styleString);
                            
                            // Re-add the component
                            const newComponent = parent.components().add(element.outerHTML, { at: index });
                            
                            // Apply the class
                            if (component_name && !newComponent.getClasses().includes(component_name)) {
                                newComponent.addClass(component_name);
                            }
                        });
                    }
                    
                    editor.refresh();
                };

                // Start applying styles
                applyStyles();
            });
        }

        function displayMessage(content, source, className, rag_content = null) {
            const messagesContainer = document.getElementById(`messages-${className}`);
            const messageElement = document.createElement('div');
            messageElement.className = `message ${source}`;

            const labelElement = document.createElement('span');
            labelElement.className = 'label';
            labelElement.textContent = source;
            messageElement.appendChild(labelElement);

            if (source == 'user') {
                const ragElement = document.createElement('div');
                ragElement.className = 'content';
                if (rag_content) ragElement.textContent = rag_content;
                else ragElement.textContent = "(no rag)";
                messageElement.appendChild(ragElement);
            }

            const contentElement = document.createElement('div');
            contentElement.className = 'content';
            contentElement.textContent = content;
            messageElement.appendChild(contentElement);

            messagesContainer.appendChild(messageElement);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }

        function initializeRAGMode(className) {
            const ragToggle = document.getElementById(`rag-mode-${className}`);
            const pageSelection = document.getElementById(`page-selection-${className}`);
            const pageRangeInputs = document.getElementById(`page-range-inputs-${className}`);
            const pageOptions = document.querySelectorAll(`input[name="page-mode-${className}"]`);

            ragToggle.addEventListener('change', function() {
                pageSelection.style.display = this.checked ? 'block' : 'none';
                if (!this.checked) {
                    pageRangeInputs.style.display = 'none';
                } else {
                    document.querySelector(`input[name="page-mode-${className}"][value="current"]`).checked = true;
                }
            });

            pageOptions.forEach(option => {
                option.addEventListener('change', function() {
                    pageRangeInputs.style.display = this.value === 'range' ? 'block' : 'none';
                });
            });
        }

        function getRAGSettings(className) {
            const ragMode = document.getElementById(`rag-mode-${className}`).checked;
            if (!ragMode) return null;

            const selectedPageMode = document.querySelector(`input[name="page-mode-${className}"]:checked`).value;
            const rag_range = [];

            if (selectedPageMode === 'range') {
                const startPage = parseInt(document.getElementById(`start-page-${className}`).value);
                const endPage = parseInt(document.getElementById(`end-page-${className}`).value);

                if (isNaN(startPage) || isNaN(endPage) || startPage === '' || endPage === '' || startPage > endPage || startPage < 1 || endPage > ffff-length) {
                    return [-1];
                }
                
                for (let i = startPage - 1; i <= endPage - 1; i++) {
                    rag_range.push(i);
                }
            }

            if (selectedPageMode === 'current') {
                const currentPage = parseInt(className.replace('gjs', ''));
                rag_range.push(currentPage);
            }

            if (selectedPageMode === 'all') {
                for (let i = 0; i < ffff-length; i++) {
                    rag_range.push(i);
                }
            }

            return rag_range;
        }

        function createEditorTemplate(index) {
            return `
                <div class="editor-container">
                    <!-- Control Panel -->
                    <div class="control-panel">
                        <button id="saveBtn-gjs${index}" class="control-btn">Save</button>
                        <button id="toggleViewBtn-gjs${index}" class="control-btn">Edit Page</button>
                        <button id="resetBtn-gjs${index}" class="control-btn">Reset</button>
                    </div>

                    <!-- GrapesJS Editor Container -->
                    <div class="gjs-editor-container">
                        <div id="gjs${index}"></div>
                    </div>

                    <!-- Style Manager Panel -->
                    <div class="style-manager-panel" id="styleManagerPanel-gjs${index}">

                        <div class="panel-header">
                            Element Properties
                        </div>
                        
                        <div class="panel-section">
                            <h4>Add Elements</h4>
                            <button class="add-element-btn" onclick="addRow('gjs${index}')">➕ Add Row</button>
                            <button class="add-element-btn" onclick="addColumn('gjs${index}')">➕ Add Column</button>
                            
                            <div style="margin-top: 15px; padding: 10px; background: #f8f9fa; border-radius: 4px; font-size: 12px; color: #666;">
                                <strong>How to use:</strong><br>
                                • <strong>Add Row:</strong> Click on any text element first, then click "Add Row" to copy its style<br>
                                • <strong>Add Column:</strong> Click on a column_container div (the container with multiple columns), then click "Add Column"<br>
                                • <strong>Position:</strong> The content will be appear on the top left of the page. You may move them to any place you want.
                            </div>
                        </div>

                        <div class="panel-section">
                            <h4>Move Components</h4>
                            <button class="add-element-btn" onclick="moveUp('gjs${index}')">⬆️ Move Up</button>
                            <button class="add-element-btn" onclick="moveDown('gjs${index}')">⬇️ Move Down</button>
                        </div>

                        <div class="panel-section">
                            <h4>Style Manager</h4>
                            <div id="style-manager-gjs${index}"></div>
                        </div>
                    </div>

                    <!-- Chatbot Panel -->
                    <div class="chatbot-panel" id="chatbotPanel-gjs${index}">

                        <div class="panel-header">
                            Chatbot
                        </div>
                        
                        <div class="panel-section">
                            <div class="chat-container">
                                <div class="messages" id="messages-gjs${index}"></div>
                                <div class="chat-input-container" id="input-container-gjs${index}">
                                    <textarea class="chat-input" id="message-input-gjs${index}" placeholder="Type your message..." rows="3"></textarea>
                                    <div class="rag-controls" id="rag-controls-gjs${index}">
                                        <div class="rag-header">
                                            <label class="rag-toggle-container">
                                                <input type="checkbox" id="rag-mode-gjs${index}" class="rag-checkbox">
                                                <span class="rag-toggle-slider"></span>
                                                <span class="rag-label">RAG Mode</span>
                                            </label>
                                        </div>
                                        
                                        <div class="rag-options" id="page-selection-gjs${index}" style="display: none;">
                                            <div class="page-mode-options">
                                                <label class="radio-option">
                                                    <input type="radio" name="page-mode-gjs${index}" value="current" checked>
                                                    <span class="radio-custom"></span>
                                                    <span class="radio-label">Current Page</span>
                                                </label>
                                                
                                                <label class="radio-option">
                                                    <input type="radio" name="page-mode-gjs${index}" value="all">
                                                    <span class="radio-custom"></span>
                                                    <span class="radio-label">All Pages</span>
                                                </label>
                                                
                                                <label class="radio-option">
                                                    <input type="radio" name="page-mode-gjs${index}" value="range">
                                                    <span class="radio-custom"></span>
                                                    <span class="radio-label">Page Range</span>
                                                </label>
                                            </div>
                                            
                                            <div class="page-range-section" id="page-range-inputs-gjs${index}" style="display: none;">
                                                <div class="range-inputs">
                                                    <div class="input-group">
                                                        <label>From</label>
                                                        <input type="number" id="start-page-gjs${index}" min="1" max="3" placeholder="1">
                                                    </div>
                                                    <div class="input-group">
                                                        <label>To</label>
                                                        <input type="number" id="end-page-gjs${index}" min="1" max="3" placeholder="3">
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    
                                    <button class="send-button" onclick="sendMessage('gjs${index}')">
                                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                            <line x1="22" y1="2" x2="11" y2="13"></line>
                                            <polygon points="22,2 15,22 11,13 2,9 22,2"></polygon>
                                        </svg>
                                        Send
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }

        function extractComponent(component_dict) {
            const allExtractedDivs = [];

            component_dict.forEach(component => {
                const page_number = component.page;
                const class_name = component.component_name;
                const editorId = `gjs${page_number}`;
            
                if (!editors[editorId]) {
                    console.error(`Editor not found for page ${page_number}`);
                    return;
                }

                try {
                    const wrapper = editors[editorId].DomComponents.getWrapper();
                    const targetComponents = wrapper.find(`[class*="${class_name}"]`); // This should work
                    
                    if (!targetComponents || targetComponents.length === 0) {
                        console.warn(`No component found with class name: ${class_name} on page ${page_number}`);
                        return;
                    }

                    const targetComponent = targetComponents[0];
                    const componentHtml = targetComponent.toHTML();
                    const allStyles = {};
                    
                    function extractStylesRecursively(comp) {
                        const domEl = comp.getEl();
                        
                        if (!domEl || !(domEl instanceof Element)) {
                            const children = comp.components();
                            if (children && children.length > 0) {
                                children.forEach(child => {
                                    extractStylesRecursively(child);
                                });
                            }
                            return;
                        }
                        
                        const compClasses = comp.getClasses();
                        const className = compClasses.length > 0 ? compClasses.join(' ') : `${comp.get('tagName')}_${comp.cid}`;
                        
                        try {
                            const styles = window.getComputedStyle(domEl);
                            const styleObj = {};
                            
                            for (let i = 0; i < styles.length; i++) {
                                const property = styles[i];
                                const value = styles.getPropertyValue(property);
                                if (value && value !== 'initial' && value !== 'normal' && value !== '') {
                                    styleObj[property] = value;
                                }
                            }
                            
                            if (Object.keys(styleObj).length > 0 && allStyles[className] === undefined) {
                                allStyles[className] = styleObj;
                            }
                        } catch (styleError) {
                            console.warn('Error getting computed styles for component:', className, styleError);
                        }
                        
                        // Recursively extract styles from all children
                        const children = comp.components();
                        if (children && children.length > 0) {
                            children.forEach(child => {
                                extractStylesRecursively(child);
                            });
                        }
                    }
                    
                    extractStylesRecursively(targetComponent);
                    
                    // main component class
                    const componentClasses = targetComponent.getClasses();
                    const componentDivName = componentClasses.length > 0 ? componentClasses.join(' ') : `${targetComponent.get('tagName')}_${targetComponent.cid}`;
                    
                    const extractedDiv = {
                        html: componentHtml,
                        styles: allStyles,
                        component_name: componentDivName,
                        page: page_number,
                    };

                    allExtractedDivs.push(extractedDiv);

                } catch (error) {
                    console.error(`Error extracting component ${class_name} on page ${page_number}:`, error);
                }
            });

            return allExtractedDivs;
        }

        function extractSelectedContent(editorId) {
            page_number = parseInt(editorId.split('gjs')[1]);
            
            if (!editors[editorId]) {
                console.error('Editor not found');
                return null;
            }

            try {
                const selectedComponents = editors[editorId].getSelectedAll();
                if (!selectedComponents || selectedComponents.length === 0) {
                    console.warn('No component selected');
                    return null;
                }

                const allExtractedDivs = [];

                selectedComponents.forEach((component, index) => {
                    const componentHtml = component.toHTML();
                    const allStyles = {};
                    
                    function extractStylesRecursively(comp) {
                        const domEl = comp.getEl();
                        
                        if (!domEl || !(domEl instanceof Element)) {
                            const children = comp.components();
                            if (children && children.length > 0) {
                                children.forEach(child => {
                                    extractStylesRecursively(child);
                                });
                            }
                            return;
                        }
                        
                        const compClasses = comp.getClasses();
                        const className = compClasses.length > 0 ? compClasses.join(' ') : `${comp.get('tagName')}_${comp.cid}`;
                        
                        try {
                            const styles = window.getComputedStyle(domEl);
                            const styleObj = {};
                            
                            for (let i = 0; i < styles.length; i++) {
                                const property = styles[i];
                                const value = styles.getPropertyValue(property);
                                if (value && value !== 'initial' && value !== 'normal' && value !== '') {
                                    styleObj[property] = value;
                                }
                            }
                            
                            if (Object.keys(styleObj).length > 0 && allStyles[className] === undefined) {
                                allStyles[className] = styleObj;
                            }
                        } catch (styleError) {
                            console.warn('Error getting computed styles for component:', className, styleError);
                        }
                        
                        // Recursively extract styles from all children
                        const children = comp.components();
                        if (children && children.length > 0) {
                            children.forEach(child => {
                                extractStylesRecursively(child);
                            });
                        }
                    }
                    
                    extractStylesRecursively(component);
                    
                    // main component class
                    const componentClasses = component.getClasses();
                    const componentDivName = componentClasses.length > 0 ? componentClasses.join(' ') : `${component.get('tagName')}_${component.cid}`;
                    
                    allExtractedDivs.push({
                        html: componentHtml,
                        styles: allStyles,
                        component_name: componentDivName,
                        page: page_number,
                    });
                });

                
                return allExtractedDivs;

            } catch (error) {
                console.error('Error extracting div:', error);
                return null;
            }
        }

        // generate all editors and add them to main-container
        function generateAllEditors() {
            const container = document.querySelector('.main-container');
            
            container.innerHTML = '';

            for (let i = 0; i < ffff-length; i++) {
                container.innerHTML += createEditorTemplate(i);
            }
            
            // initialize editors
            for (let i = 0; i < ffff-length; i++) {
                initializePageEditor(`gjs${i}`);
                setupEventListeners(`gjs${i}`);
                initializeRAGMode(`gjs${i}`);
            }
        }

        document.addEventListener('DOMContentLoaded', function() {
            generateAllEditors();
        });

        let class_dict = ffff-content
    </script>
</body>
</html>
"""
