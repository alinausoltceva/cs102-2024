def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    import string
    new_keyword = keyword
    lowercase_alphabet = string.ascii_lowercase
    uppercase_alphabet = string.ascii_uppercase
    while len(new_keyword) <= len(plaintext):
        new_keyword += keyword

    for i in range(len(plaintext)):
        char = plaintext[i]
        shift_char = new_keyword[i]
        shift = lowercase_alphabet.index(shift_char.lower())
        if char in lowercase_alphabet:
            ciphertext += lowercase_alphabet[(lowercase_alphabet.index(char) + shift) % 26]
        elif char in uppercase_alphabet:
            ciphertext += uppercase_alphabet[(uppercase_alphabet.index(char) + shift) % 26]
        else:
            ciphertext += char
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    import string
    new_keyword = keyword
    lowercase_alphabet = string.ascii_lowercase
    uppercase_alphabet = string.ascii_uppercase
    while len(new_keyword) <= len(ciphertext):
        new_keyword += keyword
    # PUT YOUR CODE HERE
    for i in range(len(ciphertext)):
        char = ciphertext[i]
        shift_char = new_keyword[i]
        shift = lowercase_alphabet.index(shift_char.lower())
        if char in lowercase_alphabet:
            plaintext += lowercase_alphabet[(lowercase_alphabet.index(char) - shift) % 26]
        elif char in uppercase_alphabet:
            plaintext += uppercase_alphabet[(uppercase_alphabet.index(char) - shift) % 26]
        else:
            plaintext += char
    return plaintext
