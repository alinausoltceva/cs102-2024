def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    import string

    lowercase_alphabet = string.ascii_lowercase
    uppercase_alphabet = string.ascii_uppercase
    for char in plaintext:
        if char in lowercase_alphabet:
            ciphertext += lowercase_alphabet[(lowercase_alphabet.index(char) + shift) % 26]
        elif char in uppercase_alphabet:
            ciphertext += uppercase_alphabet[(uppercase_alphabet.index(char) + shift) % 26]
        else:
            ciphertext += char
    # PUT YOUR CODE HERE
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    # PUT YOUR CODE HERE
    import string

    lowercase_alphabet = string.ascii_lowercase
    uppercase_alphabet = string.ascii_uppercase
    for char in ciphertext:
        if char in lowercase_alphabet:
            plaintext += lowercase_alphabet[(lowercase_alphabet.index(char) - shift) % 26]
        elif char in uppercase_alphabet:
            plaintext += uppercase_alphabet[(uppercase_alphabet.index(char) - shift) % 26]
        else:
            plaintext += char
    return plaintext
