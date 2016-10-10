from struct import pack, unpack


def vb_compress(number):
    bytes = []
    while True:
        bytes.insert(0, number % 128)
        if number < 128:
            break
        number = int(number/128)
    bytes[-1] += 128

    return pack('%dB' % len(bytes), *bytes)


def vb_decompress(byte_stream):
    n = 0
    numbers = 0
    byte_stream = unpack('%dB' % len(byte_stream), byte_stream)
    for byte in byte_stream:
        if byte < 128:
            n = 128 * n + byte
        else:
            n = 128 * n + (byte - 128)
            numbers += n
            n = 0
    return numbers
