from core.extract_content import extract_content
from core.trans_service import TranslationService
import os
import argparse

def process_and_merge_subtitles(input_file: str, output_file: str, translator: TranslationService):
    # Extract subtitles
    subtitles = extract_content(input_file)
    
    # Process each subtitle and create output content
    output_content = []
    for subtitle in subtitles:
        # Original content
        block = [
            subtitle['index'],
            subtitle['timestamp'],
            subtitle['text']
        ]
        
        # Translate the text
        translated_text = translator.translate_text(subtitle['text'])
        if translated_text:
            block.append(translated_text)
        else:
            block.append("[Translation Error]")
            
        # Add empty line between blocks
        block.append('')
        
        # Add to output content
        output_content.extend(block)
    
    # Write to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_content))

def main():
    parser = argparse.ArgumentParser(description='Translate SRT subtitles using Azure Translator')
    parser.add_argument('input_file', help='Input SRT file path')
    parser.add_argument('output_file', help='Output SRT file path')
    parser.add_argument('--key', help='Azure Translator API key (or use AZURE_TRANSLATOR_KEY env var)')
    parser.add_argument('--location', help='Azure resource location (or use AZURE_TRANSLATOR_LOCATION env var)')
    
    args = parser.parse_args()
    
    translator = TranslationService(args.key, args.location)
    process_and_merge_subtitles(args.input_file, args.output_file, translator)
    print(f"Translation completed. Output saved to {args.output_file}")

if __name__ == '__main__':
    main() 