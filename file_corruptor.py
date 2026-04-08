import os
import random
import argparse
from pathlib import Path
from typing import Callable


class FileCorruptor:
    """Generic file corruptor with multiple corruption strategies."""

    def __init__(self, seed: int | None = None):
        """Initialize the corruptor with optional random seed."""
        if seed is not None:
            random.seed(seed)

    def flip_bits(self, data: bytes, corruption_percent: float = 1.0) -> bytes:
        """Flip random bits in the data.
        
        Args:
            data: Input bytes
            corruption_percent: Percentage of bits to flip (0-100)
        
        Returns:
            Corrupted bytes
        """
        if not 0 <= corruption_percent <= 100:
            raise ValueError("corruption_percent must be between 0 and 100")
        
        data_list = bytearray(data)
        total_bits = len(data) * 8
        bits_to_flip = int(total_bits * corruption_percent / 100)
        
        for _ in range(bits_to_flip):
            byte_idx = random.randint(0, len(data_list) - 1)
            bit_idx = random.randint(0, 7)
            data_list[byte_idx] ^= (1 << bit_idx)
        
        return bytes(data_list)

    def delete_bytes(self, data: bytes, corruption_percent: float = 1.0) -> bytes:
        """Delete random bytes from the data.
        
        Args:
            data: Input bytes
            corruption_percent: Percentage of bytes to delete (0-100)
        
        Returns:
            Corrupted bytes
        """
        if not 0 <= corruption_percent <= 100:
            raise ValueError("corruption_percent must be between 0 and 100")
        
        bytes_to_delete = int(len(data) * corruption_percent / 100)
        indices_to_delete = set(random.sample(range(len(data)), min(bytes_to_delete, len(data))))
        
        return bytes(b for i, b in enumerate(data) if i not in indices_to_delete)

    def insert_bytes(self, data: bytes, corruption_percent: float = 1.0) -> bytes:
        """Insert random bytes into the data.
        
        Args:
            data: Input bytes
            corruption_percent: Percentage of new bytes to insert (relative to original size)
        
        Returns:
            Corrupted bytes
        """
        if not 0 <= corruption_percent <= 100:
            raise ValueError("corruption_percent must be between 0 and 100")
        
        bytes_to_insert = int(len(data) * corruption_percent / 100)
        data_list = bytearray(data)
        
        for _ in range(bytes_to_insert):
            position = random.randint(0, len(data_list))
            random_byte = random.randint(0, 255)
            data_list.insert(position, random_byte)
        
        return bytes(data_list)

    def swap_bytes(self, data: bytes, corruption_percent: float = 1.0) -> bytes:
        """Swap random pairs of bytes in the data.
        
        Args:
            data: Input bytes
            corruption_percent: Percentage of byte pairs to swap (0-100)
        
        Returns:
            Corrupted bytes
        """
        if not 0 <= corruption_percent <= 100:
            raise ValueError("corruption_percent must be between 0 and 100")
        
        data_list = bytearray(data)
        swaps_to_perform = int(len(data) * corruption_percent / 100 / 2)
        
        for _ in range(swaps_to_perform):
            if len(data_list) < 2:
                break
            idx1, idx2 = random.sample(range(len(data_list)), 2)
            data_list[idx1], data_list[idx2] = data_list[idx2], data_list[idx1]
        
        return bytes(data_list)

    def replace_bytes(self, data: bytes, corruption_percent: float = 1.0) -> bytes:
        """Replace random bytes with random values.
        
        Args:
            data: Input bytes
            corruption_percent: Percentage of bytes to replace (0-100)
        
        Returns:
            Corrupted bytes
        """
        if not 0 <= corruption_percent <= 100:
            raise ValueError("corruption_percent must be between 0 and 100")
        
        data_list = bytearray(data)
        bytes_to_replace = int(len(data) * corruption_percent / 100)
        indices_to_replace = random.sample(range(len(data_list)), min(bytes_to_replace, len(data_list)))
        
        for idx in indices_to_replace:
            data_list[idx] = random.randint(0, 255)
        
        return bytes(data_list)

    def corrupt_file(
        self,
        input_path: str,
        output_path: str,
        method: Callable = None,
        corruption_percent: float = 1.0,
    ) -> None:
        """Corrupt a file and save the result.
        
        Args:
            input_path: Path to the file to corrupt
            output_path: Path to save the corrupted file
            method: Corruption method (default: flip_bits)
            corruption_percent: Percentage of data to corrupt
        
        Raises:
            FileNotFoundError: If input file doesn't exist
        """
        if method is None:
            method = self.flip_bits
        
        input_path = Path(input_path)
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
        
        with open(input_path, "rb") as f:
            data = f.read()
        
        corrupted_data = method(data, corruption_percent)
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, "wb") as f:
            f.write(corrupted_data)


def main():
    parser = argparse.ArgumentParser(description="Generic file corruptor")
    parser.add_argument("input_file", help="Path to the file to corrupt")
    parser.add_argument(
        "-o", "--output",
        required=True,
        help="Path to save the corrupted file"
    )
    parser.add_argument(
        "-m", "--method",
        choices=["flip_bits", "delete_bytes", "insert_bytes", "swap_bytes", "replace_bytes"],
        default="flip_bits",
        help="Corruption method (default: flip_bits)"
    )
    parser.add_argument(
        "-p", "--percent",
        type=float,
        default=1.0,
        help="Percentage of data to corrupt (0-100, default: 1.0)"
    )
    parser.add_argument(
        "-s", "--seed",
        type=int,
        help="Random seed for reproducibility"
    )
    
    args = parser.parse_args()
    
    corruptor = FileCorruptor(seed=args.seed)
    method = getattr(corruptor, args.method)
    
    try:
        corruptor.corrupt_file(
            args.input_file,
            args.output,
            method=method,
            corruption_percent=args.percent,
        )
        print(f"✓ File corrupted successfully")
        print(f"  Input:  {args.input_file}")
        print(f"  Output: {args.output}")
        print(f"  Method: {args.method}")
        print(f"  Corruption: {args.percent}%")
    except FileNotFoundError as e:
        print(f"✗ Error: {e}")
        exit(1)


if __name__ == "__main__":
    main()
