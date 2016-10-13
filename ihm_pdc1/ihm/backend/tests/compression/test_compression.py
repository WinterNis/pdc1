from compression import vb_encode, vb_decode

def test_vb_compression():
    for val in range(10000):
        compressed_val = vb_encode(val)
        uncompressed_val = vb_decode(compressed_val)
        assert(uncompressed_val == val)
    return
    