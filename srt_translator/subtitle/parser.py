"""SRT subtitle parser."""
from dataclasses import dataclass
from typing import List


@dataclass
class SubtitleEntry:
    """Represents a single subtitle entry."""
    index: str
    timestamp: str
    text: str


class SubtitleParser:
    """Parser for SRT subtitle files."""
    
    @staticmethod
    def parse(srt_file: str) -> List[SubtitleEntry]:
        """Parse an SRT file into subtitle entries.
        
        Args:
            srt_file: Path to SRT file
            
        Returns:
            List of SubtitleEntry objects
        """
        subtitles = []
        with open(srt_file, 'r', encoding='utf-8') as file:
            content = file.read().strip().split('\n\n')
            
        for block in content:
            lines = block.split('\n')
            if len(lines) >= 3:  # Valid subtitle block
                index = lines[0]
                timestamp = lines[1]
                text = ' '.join(lines[2:])  # Combine all text lines
                subtitles.append(SubtitleEntry(index, timestamp, text))
                
        return subtitles 