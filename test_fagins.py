from fagin import fagin_loop
from sortedcontainers import SortedDict
from operator import itemgetter

def test_fag():
	pls0 = test_get_pls(0)
	pls1 = test_get_pls(1)
	pls2 = test_get_pls(2)

	sorted_id_pl_list = list()#will contain pl sorted by docId
	sorted_score_pl_list = list()#will contain pl sorted by score
	results_list = list()

	sorted_id_pl_list.append(pls0[0])
	sorted_score_pl_list.append(pls0[1])
	sorted_id_pl_list.append(pls1[0])
	sorted_score_pl_list.append(pls1[1])
	sorted_id_pl_list.append(pls2[0])
	sorted_score_pl_list.append(pls2[1])

	k = 3

	n = 3
	last_index_seen = 0


	results_list = fagin_loop(n,k,last_index_seen,sorted_score_pl_list,sorted_id_pl_list,results_list,True)
	results_list = sorted(results_list,key=itemgetter(1),reverse=1)#sort by score

	print(results_list)


def test_get_pls(number):

	pl0 = SortedDict()
	pl1 = SortedDict()

	if number==0:
		#pl0 is the pl sorted by docID
		pl0[5]=12
		pl0[8]=8
		pl0[12]=15
		pl0[15]=13

		#pl1 is the pl sorted by score
		pl1[15]=12
		pl1[13]=15
		pl1[12]=5
		pl1[8]=8

	elif number == 1:
		#pl0 is the pl sorted by docID
		pl0[3]=12
		pl0[5]=8
		pl0[12]=9
		pl0[16]=5

		#pl1 is the pl sorted by score
		pl1[12]=3
		pl1[9]=12
		pl1[8]=5
		pl1[5]=16

	elif number == 2:
		#pl0 is the pl sorted by docID
		pl0[1]=3
		pl0[5]=5
		pl0[7]=6
		pl0[12]=15

		#pl1 is the pl sorted by score
		pl1[15]=12
		pl1[6]=7
		pl1[5]=5
		pl1[3]=1

	return [pl0,pl1]

test_fag()
