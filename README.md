# SRT Translator

A Python tool to translate SRT subtitle files using Azure Translator API.

## Installation 


## Usage

This project uses the Azure Translator API. For more information, see [here](https://learn.microsoft.com/en-us/azure/ai-services/translator/quickstart-text-rest-api?tabs=python).

For make it work, you need to set the following environment variables:

```
export AZURE_TRANSLATOR_KEY="your-key"
export AZURE_TRANSLATOR_LOCATION="your-location"
```

Then run the script:

```
python src/main.py input.srt output.srt
```