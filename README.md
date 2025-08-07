 
<div align="center">

# Static Site Generator

[![License](https://img.shields.io/badge/License-Placeholder-blue.svg)](https://opensource.org/licenses/Placeholder)
[![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen.svg)](https://example.com/build)
[![Code Coverage](https://img.shields.io/badge/Coverage-80%25-green.svg)](https://example.com/coverage)

</div>

This project is a simple static site generator written in Python. It takes Markdown files as input and converts them into static HTML pages, using a provided HTML template for styling. It's designed to be a lightweight tool for creating blogs, documentation sites, and other content-focused websites.

## Features

*   **Markdown to HTML Conversion**: Converts Markdown files to HTML using custom parsing logic.
*   **Templating**: Uses an HTML template to wrap the generated HTML content for consistent styling.
*   **Static Asset Handling**: Copies static assets (CSS, images, etc.) from a source directory to the output directory.
*   **Recursive Directory Traversal**: Processes content in nested directories, generating a corresponding directory structure in the output.
*   **Customizable**: The template file and base path can be specified.

## Table of Contents

*   [Installation](#installation)
*   [Usage](#usage)
*   [Dependencies](#dependencies)
*   [Contributing](#contributing)
*   [License](#license)

## Installation

1.  Clone the repository:

    ```bash
    git clone https://github.com/mcoluomo/Static-Site-Generator.git
    cd Static-Site-Generator
    ```

2.  Create a virtual environment (optional but recommended):

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate.bat  # On Windows
    ```


## Usage

1.  Prepare your content:

    *   Place your Markdown files in the `content/` directory.
    *   Create or modify the `template.html` file to define the HTML structure and styling.
    *   Add any static assets (CSS, images, etc.) to the `static/` directory.

2.  Run the generator:

    ```bash
    ./main.sh
    ```

3.  The generated HTML files will be located in the `docs/` directory.

## Dependencies

*   Python 3.x

## Contributing

Contributions are welcome! Here's how you can contribute:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Implement your changes.
4.  Test your changes.
5.  Submit a pull request.

## License

Placeholder. This project is open source; refer to the repository for specific licensing details.
