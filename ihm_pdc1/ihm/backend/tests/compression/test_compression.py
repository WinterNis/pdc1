def test_vb_compression():
    for val in range(10000):
        compressed_val = vb_compress(val)
        uncompressed_val = vb_decompress(compressed_val)
        assert(uncompressed_val == val)
    return
    