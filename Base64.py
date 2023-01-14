class Base64:
    B64_TABLE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'  # RFC 4648
    B64_PADDING_BYTE = bytes([0])
    B64_PADDING_CHAR = '='

    @staticmethod
    def b64encode(utf_encoded: bytes):
        """
        Encodes a given utf-8 encoded string.
        1. As long as the length of the utf_encoded bytes is not divisible by 3 add padding null bytes
        2. Convert each three byte block to four sextets and add the results to the b64_encoded string
        3. Add padding chars

        :param utf_encoded: String encoded in utf-8
        :return: String encoded in Base64
        """
        padding_counter = 0
        while len(utf_encoded) % 3 != 0:
            utf_encoded += Base64.B64_PADDING_BYTE
            padding_counter += 1

        b64_encoded = ''
        for i in range(len(utf_encoded) // 3):
            current_bytes = utf_encoded[i * 3:i * 3 + 3]
            for bin_sextet in Base64._convert_bytes_encode(current_bytes):
                b64_encoded += Base64.B64_TABLE[bin_sextet]
        b64_encoded = b64_encoded[:len(b64_encoded) - padding_counter]
        b64_encoded += Base64.B64_PADDING_CHAR * padding_counter
        return b64_encoded

    @staticmethod
    def b64decode(b64_encoded: str):
        """
        Decodes a given Base64 encoded string.
        1. Take four bytes (as they are four sextets = three bytes)
        2. Convert each block of four sextets to three bytes and add the results to the b64_decoded string
        3. Eliminate padding bytes

        :param b64_encoded: String encoded in Base64
        :return: String encoded in utf-8
        """
        padding_bytes = b64_encoded.count(Base64.B64_PADDING_CHAR)
        encoded_bytes = bytes([Base64.B64_TABLE.find(c) if c != Base64.B64_PADDING_CHAR else 0 for c in b64_encoded])
        b64_decoded = ''
        for i in range(len(b64_encoded) // 4):
            current_bytes = encoded_bytes[i * 4:i * 4 + 4]
            for bin_octet in Base64._convert_bytes_decode(current_bytes):
                b64_decoded += chr(bin_octet)
        return b64_decoded[:len(b64_decoded) - padding_bytes]

    @staticmethod
    def _convert_bytes_encode(utf_blocks: bytes):
        """
        Masks are:
        - First sextet:     111111000000000000000000
        - Second sextet:    000000111111000000000000
        - Third sextet:     000000000000111111000000
        - Fourth sextet:    000000000000000000111111

        :param utf_blocks: Three blocks b64_encoded in utf-8
        :return: Four Base64 b64_encoded blocks
        """
        utf_blocks = utf_blocks[0] << 16 | utf_blocks[1] << 8 | utf_blocks[2]  # pack three bytes into one block
        return (utf_blocks & (0xfc << 16)) >> 18, \
               (utf_blocks & (0xfc << 10)) >> 12, \
               (utf_blocks & (0xfc << 4)) >> 6, \
               (utf_blocks & (0xfc >> 2))

    @staticmethod
    def _convert_bytes_decode(b64_blocks: bytes):
        """
        Masks are:
        - First octet:      111111110000000000000000
        - Second octet:     000000001111111100000000
        - Third octet:      000000000000000011111111

        :param b64_blocks: Four blocks b64_encoded in Base64
        :return: Three utf-8 b64_encoded blocks
        """
        b64_blocks = b64_blocks[0] << 18 | b64_blocks[1] << 12 | b64_blocks[2] << 6 | b64_blocks[3]
        return (b64_blocks & (0xff << 16) >> 16), \
               (b64_blocks & (0xff << 8) >> 8), \
               (b64_blocks & 0xff)
