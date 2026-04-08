#!/usr/bin/env python3
"""
File Corruptor - A tool to intentionally corrupt files for testing purposes.
Supports various corruption strategies including JPEG-specific methods.
"""

import os
import random
import sys
from pathlib import Path
from typing import Literal


class FileCorruptor:
    """Corrupts files using various strategies."""

    def __init__(self, input_file: str, output_file: str | None = None):
        """
        Initialize the corruptor.
        
        Args:
            input_file: Path to the file to corrupt
            output_file: Path to save corrupted file. If None, appends '_corrupted' to input filename
        """
        self.input_file = Path(input_file)
        
        if not self.input_file.exists():
            raise FileNotFoundError(f"File not found: {input_file}")
        
        if output_file is None:
            stem = self.input_file.stem
            suffix = self.input_file.suffix
            self.output_file = self.input_file.parent / f"{stem}_corrupted{suffix}"
        else:
            self.output_file = Path(output_file)
    
    def _read_file(self) -> bytearray:
        """Read file into bytearray for manipulation."""
        with open(self.input_file, 'rb') as f:
            return bytearray(f.read())
    
    def _write_file(self, data: bytearray) -> None:
        """Write bytearray to output file."""
        with open(self.output_file, 'wb') as f:
            f.write(data)
    
    def corrupt_random_bytes(self, num_bytes: int = 10, seed: int | None = None) -> None:
        """
        Corrupt random bytes throughout the file.
        
        Args:
            num_bytes: Number of random bytes to modify
            seed: Random seed for reproducibility
        """
        if seed is not None:
            random.seed(seed)
        
        data = self._read_file()
        file_size = len(data)
        
        if num_bytes > file_size:
            raise ValueError(f"Cannot corrupt {num_bytes} bytes in file of size {file_size}")
        
        positions = random.sample(range(file_size), num_bytes)
        for pos in positions:
            data[pos] = random.randint(0, 255)
        
        self._write_file(data)
        print(f"✓ Corrupted {num_bytes} random bytes at positions: {sorted(positions)}")
    
    def corrupt_header(self, num_bytes: int = 10) -> None:
        """
        Corrupt the file header (first N bytes).
        Useful for testing header validation.
        
        Args:
            num_bytes: Number of header bytes to corrupt (default 10)
        """
        data = self._read_file()
        
        if num_bytes > len(data):
            num_bytes = len(data)
        
        for i in range(num_bytes):
            data[i] = random.randint(0, 255)
        
        self._write_file(data)
        print(f"✓ Corrupted first {num_bytes} header bytes")
    
    def corrupt_chunk(self, offset: int, size: int) -> None:
        """
        Corrupt a specific chunk of the file.
        
        Args:
            offset: Starting byte position
            size: Number of bytes to corrupt
        """
        data = self._read_file()
        file_size = len(data)
        
        if offset >= file_size:
            raise ValueError(f"Offset {offset} exceeds file size {file_size}")
        
        end = min(offset + size, file_size)
        actual_size = end - offset
        
        for i in range(offset, end):
            data[i] = random.randint(0, 255)
        
        self._write_file(data)
        print(f"✓ Corrupted {actual_size} bytes at offset {offset}")
    
    def corrupt_percentage(self, percentage: float) -> None:
        """
        Corrupt a percentage of the file.
        
        Args:
            percentage: Percentage of file to corrupt (0-100)
        """
        if not 0 <= percentage <= 100:
            raise ValueError("Percentage must be between 0 and 100")
        
        data = self._read_file()
        num_bytes = max(1, int(len(data) * percentage / 100))
        
        positions = random.sample(range(len(data)), num_bytes)
        for pos in positions:
            data[pos] = random.randint(0, 255)
        
        self._write_file(data)
        print(f"✓ Corrupted {percentage}% of file ({num_bytes} bytes)")
    
    def corrupt_jpeg_specific(self, strategy: Literal["sof", "scan", "quantization"] = "scan") -> None:
        """
        JPEG-specific corruption targeting specific markers.
        
        Args:
            strategy: Corruption strategy
                - 'sof': Corrupt Start of Frame marker data
                - 'scan': Corrupt compressed scan data
                - 'quantization': Corrupt quantization tables
        """
        data = self._read_file()
        
        if data[:2] != b'\xff\xd8':
            raise ValueError("File does not appear to be a valid JPEG (missing SOI marker)")
        
        markers = self._find_jpeg_markers(data)
        
        if strategy == "sof":
            self._corrupt_sof_markers(data, markers)
        elif strategy == "scan":
            self._corrupt_scan_data(data, markers)
        elif strategy == "quantization":
            self._corrupt_quantization_tables(data, markers)
        
        self._write_file(data)
        print(f"✓ Applied JPEG-specific corruption: {strategy}")
    
    def _find_jpeg_markers(self, data: bytearray) -> dict:
        """Find JPEG marker positions."""
        markers = {}
        i = 0
        while i < len(data) - 1:
            if data[i] == 0xFF:
                marker_type = data[i + 1]
                markers.setdefault(marker_type, []).append(i)
                i += 2
            else:
                i += 1
        return markers
    
    def _corrupt_sof_markers(self, data: bytearray, markers: dict) -> None:
        """Corrupt Start of Frame markers (0xC0, 0xC1, etc)."""
        sof_types = [0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF]
        
        for marker_type in sof_types:
            if marker_type in markers:
                for pos in markers[marker_type]:
                    if pos + 9 < len(data):
                        for i in range(pos + 4, min(pos + 9, len(data))):
                            data[i] = random.randint(0, 255)
    
    def _corrupt_scan_data(self, data: bytearray, markers: dict) -> None:
        """Corrupt the compressed scan data."""
        if 0xDA in markers:
            for pos in markers[0xDA]:
                if pos + 20 < len(data):
                    for i in range(pos + 10, min(pos + 20, len(data))):
                        data[i] = random.randint(0, 255)
    
    def _corrupt_quantization_tables(self, data: bytearray, markers: dict) -> None:
        """Corrupt quantization table markers."""
        if 0xDB in markers:
            for pos in markers[0xDB]:
                if pos + 10 < len(data):
                    for i in range(pos + 4, min(pos + 10, len(data))):
                        data[i] = random.randint(0, 255)


def main():
    """CLI interface for the file corruptor."""
    if len(sys.argv) < 2:
        print("File Corruptor - Intentionally corrupt files for testing")
        print("\nUsage: python file_corruptor.py <input_file> [options]")
        print("\nOptions:")
        print("  --random N              Corrupt N random bytes")
        print("  --header [N]            Corrupt header (default 10 bytes)")
        print("  --chunk OFFSET SIZE     Corrupt SIZE bytes at OFFSET")
        print("  --percentage PCT        Corrupt PCT percent of file")
        print("  --jpeg-sof              JPEG-specific: corrupt Start of Frame")
        print("  --jpeg-scan             JPEG-specific: corrupt scan data")
        print("  --jpeg-quant            JPEG-specific: corrupt quantization tables")
        print("  --output FILE           Output file path")
        print("  --seed N                Random seed for reproducibility")
        print("\nExamples:")
        print("  python file_corruptor.py image.jpg --random 50")
        print("  python file_corruptor.py image.jpg --jpeg-scan --output corrupted.jpg")
        print("  python file_corruptor.py image.jpg --percentage 5")
        sys.exit(0)
    
    input_file = sys.argv[1]
    output_file = None
    seed = None
    
    try:
        corruptor = FileCorruptor(input_file, output_file)
        
        args = sys.argv[2:]
        i = 0
        while i < len(args):
            arg = args[i]
            
            if arg == "--random" and i + 1 < len(args):
                num_bytes = int(args[i + 1])
                corruptor.corrupt_random_bytes(num_bytes, seed)
                i += 2
            
            elif arg == "--header":
                num_bytes = 10
                if i + 1 < len(args) and not args[i + 1].startswith("--"):
                    num_bytes = int(args[i + 1])
                    i += 2
                else:
                    i += 1
                corruptor.corrupt_header(num_bytes)
            
            elif arg == "--chunk" and i + 2 < len(args):
                offset = int(args[i + 1])
                size = int(args[i + 2])
                corruptor.corrupt_chunk(offset, size)
                i += 3
            
            elif arg == "--percentage" and i + 1 < len(args):
                percentage = float(args[i + 1])
                corruptor.corrupt_percentage(percentage)
                i += 2
            
            elif arg in ["--jpeg-sof", "--jpeg-scan", "--jpeg-quant"]:
                strategy = arg[7:].replace("-", "")
                strategy_map = {"sof": "sof", "scan": "scan", "quant": "quantization"}
                corruptor.corrupt_jpeg_specific(strategy_map.get(strategy, "scan"))
                i += 1
            
            elif arg == "--output" and i + 1 < len(args):
                corruptor.output_file = Path(args[i + 1])
                i += 2
            
            elif arg == "--seed" and i + 1 < len(args):
                seed = int(args[i + 1])
                i += 2
            
            else:
                i += 1
        
        print(f"\n✓ Corrupted file saved to: {corruptor.output_file}")
    
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
