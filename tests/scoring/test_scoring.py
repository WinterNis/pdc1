import math
import scoring


def test_calculatePostingListScore():
    # TODO: write correct unit test with idf scoring
    postingList = [["a.doc", 180], ["b.doc", 200], ["c.doc", 37]]
    docsTokenCounts = {"a.doc": 200, "b.doc": 400, "c.doc": 200, "d.doc": 40}
    postingList = scoring.calculatePostingListScore(postingList, docsTokenCounts)
    assert(postingList[0][1] == int((180/200)*math.log(4/3)*1000000000))
    assert(postingList[1][1] == int((200/400)*math.log(4/3)*1000000000))
    assert(postingList[2][1] == int((37/200)*math.log(4/3)*1000000000))
