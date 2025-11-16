# Text File Splitter

A Python utility to efficiently split large text files into smaller, manageable chunks. Designed to handle massive files with 100+ million lines.

## Features

- ✂️ **Two splitting modes**: By line count or by file size
- 🚀 **High performance**: Efficiently processes files with millions of lines
- 📊 **Progress tracking**: Real-time progress updates during splitting
- 🎯 **Interactive mode**: User-friendly prompts for easy operation
- 💻 **Command-line mode**: Scriptable for automation
- 📁 **Automatic organization**: Creates organized output directories
- 🔒 **Error handling**: Robust error handling with UTF-8 encoding support

## Requirements

- Python 3.6 or higher
- No external dependencies required (uses only standard library)

## Installation

Simply download the `file_splitter.py` script - no installation needed!

```bash
# Make the script executable (Linux/Mac)
chmod +x file_splitter.py
```

## Usage

### Interactive Mode (Recommended for Beginners)

Simply run the script without arguments to enter interactive mode:

```bash
python file_splitter.py
```

The script will guide you through:
1. Selecting your input file
2. Choosing split method (by lines or size)
3. Setting split parameters
4. Specifying output directory

### Command-Line Mode

#### Basic Usage (Default: 1 million lines per file)

```bash
python file_splitter.py input.txt
```

#### Split by Number of Lines

```bash
# Split into files with 5 million lines each
python file_splitter.py input.txt -l 5000000

# Split into files with 1 million lines each
python file_splitter.py input.txt --lines 1000000
```

#### Split by File Size

```bash
# Split into 100 MB files
python file_splitter.py input.txt -s 100

# Split into 500 MB files
python file_splitter.py input.txt --size 500
```

#### Specify Custom Output Directory

```bash
# Use custom output folder
python file_splitter.py input.txt -o ./my_output_folder

# Combine with other options
python file_splitter.py input.txt -l 2000000 -o ./split_files
```

## Examples

### Example 1: Split Large Log File

```bash
# Split a 10 GB log file into 1 million line chunks
python file_splitter.py server.log -l 1000000
```

### Example 2: Split Database Dump

```bash
# Split database dump into 200 MB files
python file_splitter.py database_dump.sql -s 200 -o ./db_splits
```

### Example 3: Split CSV File

```bash
# Split large CSV into 5 million row chunks
python file_splitter.py large_dataset.csv -l 5000000
```

## Output

The script creates:
- A new directory named `{filename}_split` (or your custom directory)
- Multiple output files named `{filename}_part_0001.{ext}`, `{filename}_part_0002.{ext}`, etc.
- Progress updates showing lines processed
- Summary statistics upon completion

### Example Output Structure

```
original_file.txt (100 MB)
original_file_split/
    ├── original_file_part_0001.txt
    ├── original_file_part_0002.txt
    ├── original_file_part_0003.txt
    └── ...
```

## Command-Line Options

```
usage: file_splitter.py [-h] [-l N] [-s MB] [-o DIR] [input_file]

positional arguments:
  input_file            Path to the input text file

optional arguments:
  -h, --help            Show this help message and exit
  -l N, --lines N       Split by number of lines (e.g., 1000000 for 1 million)
  -s MB, --size MB      Split by size in megabytes (e.g., 100 for 100 MB)
  -o DIR, --output DIR  Output directory for split files
```

## Performance Tips

### For Very Large Files (100M+ lines):

- **Use line-based splitting**: More predictable and efficient
- **Recommended chunk size**: 1-10 million lines per file
- **Monitor disk space**: Ensure you have enough space for output files
- **Use SSD if available**: Faster read/write speeds

### Choosing Split Size:

| Total File Size | Recommended Lines/File | Recommended Size/File |
|----------------|------------------------|----------------------|
| < 1 GB         | 500,000 - 1,000,000   | 50 - 100 MB         |
| 1 - 10 GB      | 1,000,000 - 5,000,000 | 100 - 200 MB        |
| 10 - 100 GB    | 5,000,000 - 10,000,000| 200 - 500 MB        |
| > 100 GB       | 10,000,000+           | 500 - 1000 MB       |

## Error Handling

The script includes robust error handling:
- ✓ File not found errors
- ✓ Permission errors
- ✓ Encoding issues (uses UTF-8 with error ignoring)
- ✓ Disk space issues
- ✓ Interruption handling

## Use Cases

- 📝 **Log File Analysis**: Split large server logs for easier processing
- 💾 **Database Management**: Break down large SQL dumps
- 📊 **Data Processing**: Divide massive CSV/TSV files for parallel processing
- 📚 **Text Archives**: Manage large text document collections
- 🔬 **Scientific Data**: Split large datasets for distributed analysis

## Limitations

- Designed for text files only (uses UTF-8 encoding)
- Splits are line-based (won't split in the middle of a line)
- Size-based splitting is approximate (completes the current line before splitting)

## Troubleshooting

### "File not found" error
- Check the file path is correct
- Use absolute paths or ensure you're in the correct directory
- On Windows, use forward slashes `/` or escape backslashes `\\`

### "Permission denied" error
- Ensure you have read access to the input file
- Ensure you have write access to the output directory

### Out of memory errors
- This script is memory-efficient and reads line-by-line
- Ensure you have disk space for output files

## License

This script is provided as-is for free use and modification.

## Contributing

Feel free to modify and enhance this script for your needs!

## Author

Created for efficient text file processing and management.

---

**Happy Splitting! ✂️**
