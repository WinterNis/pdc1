import os

from vocabulary import Vocabulary


def test_merge_based():
    pl_dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pl')

    voc = Vocabulary(None, 0, pl_dir=pl_dir_path, temp_dir=pl_dir_path)

    voc.merge_pl()
    file_result = '010189 5 \n010150 37 010189 2 010190 4 \n010189 4 \n010150 10 010189 6 \n010150 7 \n'
    with open(os.path.join(pl_dir_path, 'PL_MERGED')) as f:
        assert (f.read() == file_result)

    assert(
        voc.voc_dict['apple'] == [1, 0] and
        voc.voc_dict['boat'] == [3, 11] and
        voc.voc_dict['brave'] == [1, 41] and
        voc.voc_dict['craft'] == [2, 52] and
        voc.voc_dict['pen'] == [1, 73])
