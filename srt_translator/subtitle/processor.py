"""Subtitle processing functionality."""
import os
from typing import List

from tqdm import tqdm

from ..translator.base import BaseTranslator
from .parser import SubtitleEntry


class SubtitleProcessor:
    """Handles subtitle processing and translation."""

    def __init__(self, translator: BaseTranslator):
        self.translator = translator

    def _load_progress(self, output_file: str) -> int:
        """Load progress from existing output file."""
        try:
            if os.path.exists(output_file):
                with open(output_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip().split('\n\n')
                    return len(content)
        except Exception:
            pass
        return 0

    def process_subtitles(
        self,
        subtitles: List[SubtitleEntry],
        output_file: str,
        target_lang: str = 'zh-Hans',
        interrupt_handler=None
    ) -> None:
        """Process and translate subtitles.
        
        Args:
            subtitles: List of subtitle entries to process
            output_file: Path to output file
            target_lang: Target language code
            interrupt_handler: Optional interrupt handler for graceful shutdown
        """
        start_index = self._load_progress(output_file)
        output_content = []

        if start_index > 0:
            print(f"Resuming from subtitle {start_index}")
            with open(output_file, 'r', encoding='utf-8') as f:
                output_content = f.read().strip().split('\n')
                if output_content[-1] != '':
                    output_content.append('')

        pbar = tqdm(
            subtitles[start_index:],
            desc="Translating",
            unit="subtitle",
            initial=start_index,
            total=len(subtitles)
        )

        try:
            for subtitle in pbar:
                if interrupt_handler and interrupt_handler.interrupted:
                    print("\nSaving progress and exiting...")
                    break

                block = [
                    subtitle.index,
                    subtitle.timestamp,
                    subtitle.text
                ]

                pbar.set_description(f"Translating: {subtitle.text[:30]}...")

                translated_text = self.translator.translate_text(subtitle.text, target_lang)
                block.append(translated_text if translated_text else "[Translation Error]")
                block.append('')

                output_content.extend(block)

                if len(output_content) % 10 == 0:  # Save every 10 subtitles
                    self._save_progress(output_file, output_content)

        finally:
            self._save_progress(output_file, output_content)

    def _save_progress(self, output_file: str, content: List[str]) -> None:
        """Save current progress to file."""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content)) 