#!/usr/bin/env python3
"""
Text File Splitter - Efficiently split large text files into smaller chunks
Designed to handle files with 100+ million lines
"""

import os
import argparse
from pathlib import Path


def split_file_by_lines(input_file, lines_per_file=1000000, output_dir=None):
    """
    Split a text file into multiple smaller files by number of lines.
    
    Args:
        input_file: Path to the input file
        lines_per_file: Number of lines per output file (default: 1 million)
        output_dir: Directory for output files (default: same as input file)
    """
    input_path = Path(input_file)
    
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    # Set output directory
    if output_dir is None:
        output_dir = input_path.parent / f"{input_path.stem}_split"
    else:
        output_dir = Path(output_dir)
    
    output_dir.mkdir(exist_ok=True)
    
    # Get file extension
    file_ext = input_path.suffix
    base_name = input_path.stem
    
    print(f"Splitting {input_file}...")
    print(f"Output directory: {output_dir}")
    print(f"Lines per file: {lines_per_file:,}")
    
    file_number = 1
    line_count = 0
    total_lines = 0
    output_file = None
    
    try:
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as infile:
            for line in infile:
                # Open new output file if needed
                if line_count == 0:
                    if output_file:
                        output_file.close()
                    
                    output_filename = output_dir / f"{base_name}_part_{file_number:04d}{file_ext}"
                    output_file = open(output_filename, 'w', encoding='utf-8')
                    print(f"Creating: {output_filename.name}")
                
                # Write line to current output file
                output_file.write(line)
                line_count += 1
                total_lines += 1
                
                # Progress indicator (every 1 million lines)
                if total_lines % 1000000 == 0:
                    print(f"  Processed {total_lines:,} lines...")
                
                # Check if we need to start a new file
                if line_count >= lines_per_file:
                    line_count = 0
                    file_number += 1
        
        # Close the last output file
        if output_file:
            output_file.close()
    
    except Exception as e:
        if output_file:
            output_file.close()
        raise e
    
    print(f"\nSplitting complete!")
    print(f"Total lines processed: {total_lines:,}")
    print(f"Total files created: {file_number}")
    print(f"Output location: {output_dir}")


def split_file_by_size(input_file, size_mb=100, output_dir=None):
    """
    Split a text file into multiple smaller files by size (in MB).
    
    Args:
        input_file: Path to the input file
        size_mb: Maximum size per output file in MB (default: 100 MB)
        output_dir: Directory for output files (default: same as input file)
    """
    input_path = Path(input_file)
    
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    # Set output directory
    if output_dir is None:
        output_dir = input_path.parent / f"{input_path.stem}_split"
    else:
        output_dir = Path(output_dir)
    
    output_dir.mkdir(exist_ok=True)
    
    # Get file extension
    file_ext = input_path.suffix
    base_name = input_path.stem
    max_size_bytes = size_mb * 1024 * 1024
    
    print(f"Splitting {input_file}...")
    print(f"Output directory: {output_dir}")
    print(f"Max size per file: {size_mb} MB")
    
    file_number = 1
    current_size = 0
    total_lines = 0
    output_file = None
    
    try:
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as infile:
            for line in infile:
                line_bytes = len(line.encode('utf-8'))
                
                # Open new output file if needed
                if current_size == 0 or current_size + line_bytes > max_size_bytes:
                    if output_file:
                        output_file.close()
                    
                    output_filename = output_dir / f"{base_name}_part_{file_number:04d}{file_ext}"
                    output_file = open(output_filename, 'w', encoding='utf-8')
                    print(f"Creating: {output_filename.name}")
                    current_size = 0
                    file_number += 1
                
                # Write line to current output file
                output_file.write(line)
                current_size += line_bytes
                total_lines += 1
                
                # Progress indicator (every 1 million lines)
                if total_lines % 1000000 == 0:
                    print(f"  Processed {total_lines:,} lines...")
        
        # Close the last output file
        if output_file:
            output_file.close()
    
    except Exception as e:
        if output_file:
            output_file.close()
        raise e
    
    print(f"\nSplitting complete!")
    print(f"Total lines processed: {total_lines:,}")
    print(f"Total files created: {file_number - 1}")
    print(f"Output location: {output_dir}")


def interactive_mode():
    """Interactive mode - asks user for input"""
    print("=" * 60)
    print("     TEXT FILE SPLITTER - Interactive Mode")
    print("=" * 60)
    print()
    
    # Get input file
    while True:
        input_file = input("Enter the path to your text file: ").strip().strip('"')
        if not input_file:
            print("❌ Please enter a file path!")
            continue
        
        input_path = Path(input_file)
        if not input_path.exists():
            print(f"❌ File not found: {input_file}")
            print("Please try again.")
            continue
        
        # Show file info
        file_size_mb = input_path.stat().st_size / (1024 * 1024)
        print(f"\n✓ File found: {input_path.name}")
        print(f"  Size: {file_size_mb:.2f} MB")
        break
    
    print()
    
    # Choose split method
    print("How do you want to split the file?")
    print("1. By number of lines (recommended for large files)")
    print("2. By file size (MB)")
    print()
    
    while True:
        choice = input("Enter your choice (1 or 2): ").strip()
        if choice in ['1', '2']:
            break
        print("❌ Please enter 1 or 2")
    
    print()
    
    # Get split parameters
    if choice == '1':
        print("How many lines per file?")
        print("  - For 100M lines total: suggest 1,000,000 to 10,000,000 lines per file")
        print("  - Examples: 1000000 (1 million), 5000000 (5 million), 10000000 (10 million)")
        print()
        
        while True:
            lines_input = input("Lines per file [default: 1000000]: ").strip()
            if not lines_input:
                lines_per_file = 1000000
                break
            try:
                lines_per_file = int(lines_input.replace(',', '').replace('_', ''))
                if lines_per_file > 0:
                    break
                print("❌ Please enter a positive number")
            except ValueError:
                print("❌ Please enter a valid number")
        
        print(f"\n✓ Will split into files with {lines_per_file:,} lines each")
    
    else:  # choice == '2'
        print("What size should each file be (in MB)?")
        print("  - Examples: 50, 100, 500")
        print()
        
        while True:
            size_input = input("Size in MB [default: 100]: ").strip()
            if not size_input:
                size_mb = 100
                break
            try:
                size_mb = int(size_input)
                if size_mb > 0:
                    break
                print("❌ Please enter a positive number")
            except ValueError:
                print("❌ Please enter a valid number")
        
        print(f"\n✓ Will split into files of approximately {size_mb} MB each")
    
    print()
    
    # Ask about output directory
    default_output = input_path.parent / f"{input_path.stem}_split"
    print(f"Output directory:")
    print(f"  Default: {default_output}")
    custom_output = input("Press Enter for default, or enter custom path: ").strip().strip('"')
    
    output_dir = custom_output if custom_output else str(default_output)
    
    print()
    print("=" * 60)
    print("Starting split operation...")
    print("=" * 60)
    print()
    
    # Perform the split
    try:
        if choice == '1':
            split_file_by_lines(input_file, lines_per_file, output_dir)
        else:
            split_file_by_size(input_file, size_mb, output_dir)
        
        print()
        print("=" * 60)
        print("✓ SUCCESS! Your file has been split.")
        print("=" * 60)
        return 0
    
    except Exception as e:
        print()
        print("=" * 60)
        print(f"❌ ERROR: {e}")
        print("=" * 60)
        return 1


def main():
    parser = argparse.ArgumentParser(
        description='Split large text files into smaller chunks',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode (asks questions)
  python file_splitter.py
  
  # Command-line mode: Split by lines (default: 1 million lines per file)
  python file_splitter.py input.txt
  
  # Split into files with 5 million lines each
  python file_splitter.py input.txt -l 5000000
  
  # Split by size (100 MB per file)
  python file_splitter.py input.txt -s 100
  
  # Specify custom output directory
  python file_splitter.py input.txt -o ./output_folder
        """
    )
    
    parser.add_argument('input_file', nargs='?', help='Path to the input text file')
    parser.add_argument('-l', '--lines', type=int, metavar='N',
                        help='Split by number of lines (e.g., 1000000 for 1 million)')
    parser.add_argument('-s', '--size', type=int, metavar='MB',
                        help='Split by size in megabytes (e.g., 100 for 100 MB)')
    parser.add_argument('-o', '--output', metavar='DIR',
                        help='Output directory for split files')
    
    args = parser.parse_args()
    
    # If no input file provided, run interactive mode
    if not args.input_file:
        return interactive_mode()
    
    # Validate arguments
    if args.lines and args.size:
        parser.error("Cannot specify both --lines and --size. Choose one splitting method.")
    
    try:
        if args.size:
            split_file_by_size(args.input_file, args.size, args.output)
        else:
            # Default: split by lines (1 million if not specified)
            lines = args.lines if args.lines else 1000000
            split_file_by_lines(args.input_file, lines, args.output)
    
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
