
# AI Content Generation Assistant

A prototype of an AI-based content automation application that provides an innovative solution for marketers and content creators. The application uses both public and internal data to generate verifiable marketing content enriched with embedded cross-references. This project focuses on delivering high-quality text outputs such as newsletters and blog posts. It was implemented in cooperation with Stozone for Deutsche Telekom IoT, which highlights its practical usability and market potential.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [Usage](#usage)
- [Server Logs and Messages](#server-logs-and-messages)
- [Contributions](#contributions)
- [License](#license)

## Requirements

- Python 3.x
- Flask
- Other libraries (e.g., requests, numpy, pandas, google-generative-ai)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/username/repo_name.git
   ```

2. Navigate to the project directory:
   ```bash
   cd repo_name
   ```

3. Install the required libraries:
   ```bash
   pip install flask requests numpy pandas google-generative-ai
   ```

## Running the Project

1. Set your API key in the environment:
   ```bash
   $env:API_KEY="YOUR_ENCRYPTED_API_KEY"
   ```
   Replace `YOUR_ENCRYPTED_API_KEY` with your actual API key. Ensure the API key is valid and has the appropriate permissions.

2. Run the application:
   ```bash
   python app.py
   ```

3. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

## Usage

- Enter your desired prompt in the text area.
- Select the language from the dropdown menu.
- Click "Generate Content" to create the content based on your input.
- Once generated, you can download the content as a PDF by clicking the "Download as PDF" button.

## Server Logs and Messages

While running the application, you may see logs similar to the following:

```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

These logs indicate the server status and any incoming requests.

## Contributions

Contributions are welcome! Please feel free to submit a pull request or report issues you encounter.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
