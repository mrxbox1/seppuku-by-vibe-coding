import secrets
import string
from typing import Generator


def generate_random_strings(count: int = None, charset: str = None) -> Generator[str, None, None]:
    """
    Generate random 16-character strings.
    
    Args:
        count: Number of strings to generate. If None, generates indefinitely.
        charset: Character set to use. Defaults to letters, digits, and punctuation.
                If None, uses: ascii_letters + digits + punctuation
    
    Yields:
        Random 16-character strings
    
    Example:
        # Generate 5 random strings
        for s in generate_random_strings(count=5):
            print(s)
        
        # Generate strings indefinitely using only alphanumeric characters
        gen = generate_random_strings(charset=string.ascii_letters + string.digits)
        for _ in range(3):
            print(next(gen))
    """
    if charset is None:
        charset = string.ascii_letters + string.digits + string.punctuation
    
    i = 0
    while count is None or i < count:
        yield ''.join(secrets.choice(charset) for _ in range(16))
        i += 1


if __name__ == "__main__":
    # Example: Generate 5 random 16-character strings
    print("5 random 16-character strings:")
    for s in generate_random_strings(count=5):
        print(s)
    
    print("\n3 alphanumeric-only strings:")
    for s in generate_random_strings(count=3, charset=string.ascii_letters + string.digits):
        print(s)
