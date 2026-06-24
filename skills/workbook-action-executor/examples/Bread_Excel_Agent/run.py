#!/usr/bin/env python3
"""
Quick run script for the Excel Action Space system
"""

import argparse
from excel_action_space.integration.llm_client import main

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Excel Action Space - LLM-powered Excel automation')
    parser.add_argument('--recording-file', type=str, help='Path to Excel recording JSON file to execute')
    parser.add_argument('--log', action='store_true', help='Enable tool call logging to model_logs/ directory')
    args = parser.parse_args()
    
    main(recording_file=args.recording_file, enable_logging=args.log)