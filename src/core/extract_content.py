import os
import re

def extract_content(srt_file):
    subtitles = []
    with open(srt_file, 'r', encoding='utf-8') as file:
        content = file.read().strip().split('\n\n')
        
    for block in content:
        lines = block.split('\n')
        if len(lines) >= 3:  # Valid subtitle block
            index = lines[0]
            timestamp = lines[1]
            text = ' '.join(lines[2:])  # Combine all text lines
            subtitles.append({
                'index': index,
                'timestamp': timestamp,
                'text': text
            })
    return subtitles 