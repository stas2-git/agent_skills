#!/usr/bin/env python3
"""
Simple token counter script for analyzing file token usage across different tokenizers.

Usage:
    python token_counter.py --file path/to/file.json --tokenizer claude --mode json
    python token_counter.py --file path/to/file.txt --tokenizer qwen3 --mode raw
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Union, Dict, Any

try:
    import tiktoken
except ImportError:
    print("Error: tiktoken not installed. Run: pip install tiktoken")
    sys.exit(1)

try:
    import qwen_tokenizer
except ImportError:
    print("Error: qwen-tokenizer not installed. Run: pip install qwen-tokenizer")
    sys.exit(1)


class TokenizerManager:
    """Manages different tokenizer implementations."""
    
    def __init__(self):
        self.tokenizers = {}
        self._initialize_tokenizers()
    
    def _initialize_tokenizers(self):
        """Initialize all available tokenizers."""
        # Claude uses cl100k_base encoding (same as GPT-4)
        self.tokenizers['claude'] = tiktoken.get_encoding("cl100k_base")
        
        # GPT-4 uses cl100k_base encoding
        self.tokenizers['gpt4'] = tiktoken.get_encoding("cl100k_base")
        
        # Qwen3 tokenizer (using qwen-max model)
        self.tokenizers['qwen3'] = qwen_tokenizer.get_tokenizer('qwen-max')
    
    def count_tokens(self, text: str, tokenizer_name: str) -> int:
        """Count tokens using the specified tokenizer."""
        if tokenizer_name not in self.tokenizers:
            raise ValueError(f"Unknown tokenizer: {tokenizer_name}. Available: {list(self.tokenizers.keys())}")
        
        tokenizer = self.tokenizers[tokenizer_name]
        
        if tokenizer_name == 'qwen3':
            # Qwen tokenizer returns token IDs
            tokens = tokenizer.encode(text)
            return len(tokens)
        else:
            # tiktoken tokenizers
            tokens = tokenizer.encode(text)
            return len(tokens)


def extract_json_tools(file_path: Path) -> str:
    """Extract only the tools array from a JSON file for accurate LLM token counting."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extract tools array if it exists
        if isinstance(data, dict) and 'tools' in data:
            tools = data['tools']
            # Convert back to JSON string for tokenization
            return json.dumps(tools, separators=(',', ':'))
        else:
            # If no tools array, return the entire JSON
            return json.dumps(data, separators=(',', ':'))
            
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON file: {e}")
    except Exception as e:
        raise ValueError(f"Error reading JSON file: {e}")


def read_file_content(file_path: Path, mode: str) -> str:
    """Read file content based on the specified mode."""
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if mode == 'json':
        # Smart JSON processing - extract tools array
        return extract_json_tools(file_path)
    elif mode == 'raw':
        # Raw file content
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            # Try with different encoding if UTF-8 fails
            with open(file_path, 'r', encoding='latin-1') as f:
                return f.read()
    else:
        raise ValueError(f"Unknown mode: {mode}. Use 'json' or 'raw'")


def main():
    parser = argparse.ArgumentParser(
        description="Count tokens in files using different tokenizers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python token_counter.py --file definitions.json --tokenizer claude --mode json
  python token_counter.py --file document.txt --tokenizer qwen3 --mode raw
  python token_counter.py --file data.json --tokenizer gpt4 --mode json
        """
    )
    
    parser.add_argument(
        '--file', '-f',
        type=str,
        required=True,
        help='Path to the file to analyze'
    )
    
    parser.add_argument(
        '--tokenizer', '-t',
        choices=['claude', 'qwen3', 'gpt4'],
        default='claude',
        help='Tokenizer to use (default: claude)'
    )
    
    parser.add_argument(
        '--mode', '-m',
        choices=['json', 'raw'],
        default='raw',
        help='Processing mode: json (extract tools array) or raw (entire file) (default: raw)'
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize tokenizer manager
        tokenizer_manager = TokenizerManager()
        
        # Read file content
        file_path = Path(args.file)
        content = read_file_content(file_path, args.mode)
        
        # Count tokens
        token_count = tokenizer_manager.count_tokens(content, args.tokenizer)
        
        # Output result
        print(f"File: {args.file}")
        print(f"Mode: {args.mode}")
        print(f"Tokenizer: {args.tokenizer}")
        print(f"Tokens: {token_count:,}")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
