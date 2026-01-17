#!/usr/bin/env python3
"""
Extract text content from DOCX files.
"""
import zipfile
import xml.etree.ElementTree as ET
import sys
from pathlib import Path

def extract_docx_text(docx_path: str) -> str:
    """Extract plain text from a DOCX file."""
    # DOCX is a ZIP file containing XML
    with zipfile.ZipFile(docx_path, 'r') as docx:
        # Read the main document content
        with docx.open('word/document.xml') as document:
            tree = ET.parse(document)
            root = tree.getroot()
            
            # Define namespaces
            namespaces = {
                'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
            }
            
            # Extract all text elements
            paragraphs = []
            for para in root.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
                texts = []
                for text in para.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'):
                    if text.text:
                        texts.append(text.text)
                if texts:
                    paragraphs.append(''.join(texts))
            
            return '\n'.join(paragraphs)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python extract_docx.py <path_to_docx>")
        sys.exit(1)
    
    docx_path = sys.argv[1]
    if not Path(docx_path).exists():
        print(f"Error: File not found: {docx_path}")
        sys.exit(1)
    
    text = extract_docx_text(docx_path)
    print(text)
