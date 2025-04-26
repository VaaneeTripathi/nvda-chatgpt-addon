# NVDA ChatGPT Add-on

An NVDA add-on that enables users to interact with OpenAI's ChatGPT directly from NVDA.

## Overview

This add-on provides a simple interface for NVDA users to send queries to ChatGPT and receive responses through a dialog box. It was developed as part of an assignment to explore screen reader accessibility and add-on development.

## Features

- Send text queries to ChatGPT using a simple dialog interface
- Receive and read responses within NVDA
- Access via keyboard shortcut (NVDA+Shift+C) or through NVDA's Tools menu
- Configure API settings through a dedicated settings dialog

## Usage

1. Press `NVDA+Shift+C` to open the ChatGPT dialog
2. Type your query in the input field
3. Press Enter or click the Submit button
4. The response from ChatGPT will be displayed in the response field and announced by NVDA

## Configuration

The add-on requires an OpenAI API key to function. To set up:

1. Obtain an API key from [OpenAI's platform](https://platform.openai.com/)
2. Edit the `interface.py` file to include your API key
3. Rebuild and reinstall the add-on

## Technical Implementation

### Project Structure

This add-on was built using the **NVDA add-on template** and follows the standard NVDA add-on structure:

```
nvda-chatgpt-addon/
├── addon/
│   └── globalPlugins/
│       └── NVDAChatGPTAddOn/
│           ├── __init__.py      # Main plugin code
│           └── interface.py     # ChatGPT API handling
├── buildVars.py                 # Build configuration
├── manifest.ini.tpl             # Template for manifest
├── sconstruct                   # SCons build script
└── README.md                    # This file
```

### Components

- **GlobalPlugin**: Handles integration with NVDA, provides menu items and keyboard shortcuts
- **ChatGPTDialog**: Provides the user interface for query input and response display
- **ChatGPTInterface**: Manages communication with the OpenAI API

### Pipeline

1. User initiates the add-on via keyboard shortcut or menu
2. The add-on displays a dialog box with input and output fields
3. User enters a query and submits
4. Query is sent to OpenAI's API via the interface module
5. Response is received and displayed in the dialog
6. NVDA announces the arrival of the response


## Development

This add-on was developed using the SCons template for NVDA add-ons. To build from source:

1. Clone the repository
2. Install requirements: `pip install scons`
3. Build the add-on: `scons`

## Known Issues

- The API key is currently hardcoded in the source code
- Error handling for network issues could be improved
- No conversation history is maintained between sessions
- The add-on was attempted to be set up for internationalization using NVDA's translation system. All user-facing strings are marked for translation with the `_()` function. However, it hasn't been executed.
