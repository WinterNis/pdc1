import os
import sys

from vocabulary import Vocabulary

def simple_score(count, *args):
    return count

def test_merge_based():
    pl_dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pl')

    voc = Vocabulary(
        None,
        simple_score,
        pl_dir=pl_dir_path,
        temp_dir=os.path.dirname(os.path.realpath(__file__)))

    voc.merge_pl()
    file_result = (
        '010189 5 \n5 010189 \n010150 37 010189 2 010190 4 \n2 010189 37 010150 4 010190 \n'
        '010189 4 \n4 010189 \n010150 10 010189 6 \n10 010150 6 010189 \n010150 7 \n7 010150 \n')

    with open(os.path.join(pl_dir_path, 'PL_MERGED')) as f:
        assert (f.read() == file_result)

    if sys.platform.startswith('linux'):
        assert(
            voc.voc_dict['apple'] == [1, 0] and
            voc.voc_dict['boat'] == [3, 20] and
            voc.voc_dict['brave'] == [1, 78] and
            voc.voc_dict['craft'] == [2, 98] and
            voc.voc_dict['pen'] == [1, 138])
