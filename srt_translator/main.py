"""Main entry point for SRT translator."""
import argparse
import signal

from .subtitle import SubtitleParser, SubtitleProcessor
from .translator import AzureTranslator


class GracefulInterruptHandler:
    """Handles graceful interruption of the translation process."""
    
    def __init__(self):
        self.interrupted = False
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        print("\nInterrupt received, completing current translation...")
        self.interrupted = True


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Translate SRT subtitles using Azure Translator')
    parser.add_argument('input_file', help='Input SRT file path')
    parser.add_argument('output_file', help='Output SRT file path')
    parser.add_argument('--key', help='Azure Translator API key (or use AZURE_TRANSLATOR_KEY env var)')
    parser.add_argument('--location', help='Azure resource location (or use AZURE_TRANSLATOR_LOCATION env var)')
    parser.add_argument('--target-lang', default='zh-Hans', help='Target language code')
    parser.add_argument('--max-retries', type=int, default=3, help='Maximum number of retry attempts for failed translations')
    parser.add_argument('--retry-delay', type=int, default=1, help='Delay in seconds between retry attempts')
    
    args = parser.parse_args()
    
    # Initialize components
    translator = AzureTranslator(
        key=args.key,
        location=args.location,
        max_retries=args.max_retries,
        retry_delay=args.retry_delay
    )
    
    parser = SubtitleParser()
    processor = SubtitleProcessor(translator)
    interrupt_handler = GracefulInterruptHandler()

    # Process subtitles
    print(f"Reading subtitles from {args.input_file}...")
    subtitles = parser.parse(args.input_file)
    print(f"Found {len(subtitles)} subtitle entries")

    processor.process_subtitles(
        subtitles,
        args.output_file,
        args.target_lang,
        interrupt_handler
    )
    
    print(f"\nTranslation completed! Output saved to {args.output_file}")


if __name__ == '__main__':
    main() 