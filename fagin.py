#from sortedcontainers import SortedDict
from operator import itemgetter

#return the top-k docs for a research.
#if there are not enough docs for this research, it returns the more that we can
def fagin(search_terms_list,number_of_results_wanted):
    #initialization

    k = number_of_results_wanted# number of results wanted

    results_list = list()#the list of results 
    n = len(search_terms) #n is equal to the number of searched terms
    last_index_seen = 0 #the index of the last doc seen in posting lists sorting by score
    sorted_id_pl_list = list()#will contain pl sorted by docId
    sorted_score_pl_list = list()#will contain pl sorted by score


    #first we get the PL sorted by docID and the PL sorted by score for each search term
    for term in search_terms_list:
        #we retrieve the two PL for term, one sorted by doc_id and the other sorted by score
        pls_for_term = access_pl(term)

        if pls_for_term != NONE:
            sorted_id_pl_list.append(pls_for_term[0])
            sorted_score_pl_list.append(pls_for_term[1])


    #let's go in fagin's awesomeness
    results_list = fagin_loop(n,k,last_index_seen,sorted_score_pl_list,sorted_by_id_pl,results_list)

    resultsList = sorted(resultsList,key=itemgetter(1),reverse=1)#sort by score

    return results_list


#this function is the heart of fagin's algo
#it takes a list of results (that can be empty), the pl of searched terms, the index of last doc seen in pl,
# the number of results wanted 'k', the length of terms that we are considering in the request 'n'
#it returns a new list of results
def fagin_loop(n,k,last_index_seen,sorted_score_pl_list,sorted_by_id_pl,results_list):
    i = 0
    all_pl_completely_seen = true#check if all the pl are entirely seen in order to know if we can find more docs or not
    tau = 0#the heart variable 

    while i<n:#go through the algo for each term of the research list

        #we will go through each posting list
        doc_id = ""

        for pl in sorted_score_pl_list:
            if last_index_seen<len(pl):

                all_pl_completely_seen = false#we don't have finished to see all the pl

                item = pl.peekitem(last_index_seen)
                doc_id = item[0]#get docID
                #score = item[1]#get score
                score = 0
                tau += item[1]#tau is calculated on live

                #we get the total score for this doc in all PL of research terms
                for sorted_by_id_pl in sorted_id_pl_list:
                    if doc_id in sorted_by_id_pl:
                        score += sorted_by_id_pl[doc_id]

                #we check if we can add this doc to results
                if len(results_list)<k:
                    if [doc_id,score] not in results_list:
                        results_list.append([doc_id,score])

                else:
                    #we check the lowest score in result list and if we have a better score we replace it with the new doc
                    min_item = min(results_list,key=itemgetter(1))

                    if score > min_item[1]:
                        results_list.remove(min_item)
                        results_list.append([doc_id,score])

        i += 1# end of this turn of loop
    #end of loop

    #if we do not have enough results in list we re iterate, 
    #incrementing the last_index seen in order to see the next best score in pl
    if len(results_list)<k and all_pl_completely_seen == false:
        return fagin_loop(n,k,last_index_seen+1,sorted_score_pl_list,sorted_by_id_pl,results_list)

    #we check tau, if there is a doc in results_list that has a lower score than tau, we re iterate,
    #incrementing the last_index seen in order to see the next best score in pl
    min_item = min(results_list,key=itemgetter(1))
    if min_item[1]<tau:
        return fagin_loop(n,k,last_index_seen+1,sorted_score_pl_list,sorted_by_id_pl,results_list)

    return results_list



