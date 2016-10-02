import os

from merged_based import merge_pl


def test_merge_based():
    pl_dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pl')

    voc_dict = {}
    merge_pl(voc_dict, temp_path=pl_dir_path, output_path=pl_dir_path)
    file_result = '010189 5 \n010150 37 010189 2 010190 4 \n010189 4 \n010150 10 010189 6 \n010150 7 \n'
    with open(os.path.join(pl_dir_path, 'PL_MERGED')) as f:
        assert (f.read() == file_result)

    assert(
        voc_dict['apple'] == [1, 0] and
        voc_dict['boat'] == [3, 11] and
        voc_dict['brave'] == [1, 41] and
        voc_dict['craft'] == [2, 52] and
        voc_dict['pen'] == [1, 73])
