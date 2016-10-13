from struct import pack, unpack


def vb_encode(number):
    bytes = []
    while True:
        bytes.insert(0, number % 128)
        if number < 128:
            break
        number = int(number/128)
    bytes[-1] += 128

    return pack('%dB' % len(bytes), *bytes)


def vb_decode(byte_stream):
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

def pl_compress(uncompressed_pl):
    temp = int(uncompressed_pl[0][0])
    compressed_pl = [[vb_encode(temp), uncompressed_pl[0][1]]]
    if len(uncompressed_pl) > 1:
        for l in uncompressed_pl[1:]:
            docId = int(l[0])
            score = l[1]
            compressed_pl.append([vb_encode(docId-temp), score])
            temp = docId

    return compressed_pl


def pl_uncompress(compressed_pl):
    temp = vb_decode(compressed_pl[0][0])
    uncompressed_pl = [[temp, compressed_pl[0][1].decode()]]
    if len(compressed_pl) > 1:
        for l in compressed_pl[1::]:
            reducedDocId = vb_decode(l[0])
            score = l[1].decode()
            uncompressed_pl.append([reducedDocId+temp, score])
            temp += reducedDocId

    return uncompressed_pl
    