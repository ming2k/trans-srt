from core.extract_content import extract_content
from core.trans_service import TranslationService
import os
import argparse
from tqdm import tqdm
import signal
import json

class GracefulInterruptHandler:
    def __init__(self):
        self.interrupted = False
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        print("\nInterrupt received, completing current translation...")
        self.interrupted = True

def load_progress(output_file):
    try:
        if os.path.exists(output_file):
            with open(output_file, 'r', encoding='utf-8') as f:
                content = f.read().strip().split('\n\n')
                return len(content)
    except Exception:
        pass
    return 0

def process_and_merge_subtitles(input_file: str, output_file: str, translator: TranslationService):
    # Extract subtitles
    print(f"Reading subtitles from {input_file}...")
    subtitles = extract_content(input_file)
    print(f"Found {len(subtitles)} subtitle entries")
    
    # Check for existing progress
    start_index = 0
    if os.path.exists(output_file):
        start_index = load_progress(output_file)
        if start_index > 0:
            print(f"Resuming from subtitle {start_index}")
    
    # Process each subtitle and create output content
    output_content = []
    interrupt_handler = GracefulInterruptHandler()
    
    # Load existing translations if any
    if start_index > 0:
        with open(output_file, 'r', encoding='utf-8') as f:
            output_content = f.read().strip().split('\n')
            if output_content[-1] != '':
                output_content.append('')
    
    # Create progress bar
    pbar = tqdm(subtitles[start_index:], desc="Translating", unit="subtitle", initial=start_index, total=len(subtitles))
    
    try:
        for subtitle in pbar:
            if interrupt_handler.interrupted:
                print("\nSaving progress and exiting...")
                break
            
            # Original content
            block = [
                subtitle['index'],
                subtitle['timestamp'],
                subtitle['text']
            ]
            
            # Update progress bar description
            pbar.set_description(f"Translating: {subtitle['text'][:30]}...")
            
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
            
            # Save progress periodically
            if len(output_content) % 10 == 0:  # Save every 10 subtitles
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(output_content))
    
    finally:
        # Always save progress before exiting
        print(f"\nWriting translations to {output_file}...")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(output_content))

def main():
    parser = argparse.ArgumentParser(description='Translate SRT subtitles using Azure Translator')
    parser.add_argument('input_file', help='Input SRT file path')
    parser.add_argument('output_file', help='Output SRT file path')
    parser.add_argument('--key', help='Azure Translator API key (or use AZURE_TRANSLATOR_KEY env var)')
    parser.add_argument('--location', help='Azure resource location (or use AZURE_TRANSLATOR_LOCATION env var)')
    parser.add_argument('--max-retries', type=int, default=3, help='Maximum number of retry attempts for failed translations')
    parser.add_argument('--retry-delay', type=int, default=1, help='Delay in seconds between retry attempts')
    
    args = parser.parse_args()
    
    translator = TranslationService(args.key, args.location, args.max_retries, args.retry_delay)
    process_and_merge_subtitles(args.input_file, args.output_file, translator)
    print(f"\nTranslation completed! Output saved to {args.output_file}")

if __name__ == '__main__':
    main() 