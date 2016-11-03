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
    number = 0
    b_s = unpack('%dB' % len(byte_stream), byte_stream)
    counter = 0
    for byte in b_s:
        counter = counter + 1
        if byte < 128:
            n = 128 * n + byte
        else:
            n = 128 * n + (byte - 128)
            number = n
            break
    byte_stream = byte_stream[counter:]
    return number, byte_stream


def pl_compress(uncompressed_pl):
    temp = int(uncompressed_pl[0][0])
    compressed_pl = vb_encode(temp) + vb_encode(uncompressed_pl[0][1])
    if len(uncompressed_pl) > 1:
        for l in uncompressed_pl[1:]:
            docId = int(l[0])
            score = l[1]
            compressed_pl += vb_encode(docId-temp) + vb_encode(score)
            temp = docId
    return compressed_pl


def pl_uncompress(compressed_pl):
    temp, compressed_pl = vb_decode(compressed_pl)
    score, compressed_pl = vb_decode(compressed_pl)
    uncompressed_pl = [[str(temp), int(score)]]
    while len(compressed_pl) > 1:
        reducedDocId, compressed_pl = vb_decode(compressed_pl)
        score, compressed_pl = vb_decode(compressed_pl)
        uncompressed_pl.append([str(reducedDocId+temp), score])
        temp += reducedDocId
    return uncompressed_pl
