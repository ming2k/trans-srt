# SRT Translator

A Python tool to translate SRT subtitle files using Azure Translator API.

## Installation

Clone the repository and install in development mode:

```bash
git clone https://github.com/yourusername/translate-srt.git
cd translate-srt
pip install -e .
```

## Usage

This project uses the Azure Translator API. You'll need an Azure account and Translator resource. For more information, see [Azure Translator documentation](https://learn.microsoft.com/en-us/azure/ai-services/translator/quickstart-text-rest-api?tabs=python).

### Setting up Azure credentials

Set your Azure credentials using environment variables:

```bash
export AZURE_TRANSLATOR_KEY="your-key"
export AZURE_TRANSLATOR_LOCATION="your-location"
```

for example:

```bash
export AZURE_TRANSLATOR_KEY="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export AZURE_TRANSLATOR_LOCATION="japanwest"
```

### Translating subtitles

Basic usage:
```bash
srt-translator input.srt output.srt
```

With optional parameters:
```bash
srt-translator input.srt output.srt --target-lang ja --max-retries 5
```

For all available options:
```bash
srt-translator --help
```

### Target Language Codes

Common language codes:
- `zh-Hans`: Simplified Chinese (default)
- `zh-Hant`: Traditional Chinese
- `ja`: Japanese
- `ko`: Korean
- `es`: Spanish
- `fr`: French
- `de`: German
- `ru`: Russian
- `ar`: Arabic
- `hi`: Hindi
- `pt`: Portuguese
- `it`: Italian
- `vi`: Vietnamese
- `th`: Thai

For a complete list of supported languages and their codes, see [Azure's supported languages](https://learn.microsoft.com/en-us/azure/ai-services/translator/language-support).

## Development

To set up the development environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .
```
