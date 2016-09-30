import scoring

def test_calculatePostingListScore():
    postingList = [["a.doc", 3], ["b.doc", 2], ["c.doc", 1], ["d.doc", 7]]
    docsTokenCounts = {"a.doc": 20, "b.doc": 20, "c.doc": 20, "d.doc": 20}
    postingList = scoring.calculatePostingListScore(postingList, docsTokenCounts)
    assert(postingList[0][1]==(3/20))
    assert(postingList[1][1]==(2/20))
    assert(postingList[2][1]==(1/20))
    assert(postingList[3][1]==(7/20))
