from operator import itemgetter


def fagin(voc, search_terms_list, number_of_results_wanted, is_and_query):
    """Return the top-k docs for a research. We use a finished inverted file 'voc'
    from which we use interface functions. If there are not enough docs for this research,
    it returns the more that we can. Parameter "is_and_query" is a boolean that indicates
    if wa want a "and" query, if false it is an "or" query"""
    # initialization

    k = number_of_results_wanted  # number of results wanted

    results_list = list()  # the list of results
    n = len(search_terms_list)  # n is equal to the number of searched terms
    last_index_seen = 0  # the index of the last doc seen in posting lists sorting by score
    sorted_id_pl_list = list()  # will contain pl sorted by docId
    sorted_score_pl_list = list()  # will contain pl sorted by score

    # first we get the PL sorted by docID and the PL sorted by score for each search term
    for term in search_terms_list:
        # we retrieve the two PL for term, one sorted by doc_id and the other sorted by score
        pls_for_term = voc.access_pl(term)

        if pls_for_term is not None:
            sorted_id_pl_list.append(pls_for_term[0])
            sorted_score_pl_list.append(pls_for_term[1])

    # let's go in fagin's awesomeness
    print(sorted_score_pl_list)
    results_list = fagin_loop(n, k, last_index_seen, sorted_score_pl_list, sorted_id_pl_list, results_list, is_and_query)

    results_list = sorted(results_list, key=itemgetter(1), reverse=1)  # sort by score

    return results_list


def fagin_loop(n, k, last_index_seen, sorted_score_pl_list, sorted_id_pl_list, results_list, is_and_query):
    """This function is the heart of fagin's algo. It takes a list of results (that can be empty),
    the pl of searched terms, the index of last doc seen in pl, the number of results wanted 'k',
    the length of terms that we are considering in the request 'n'. Parameter "is_and_query" is a
    boolean that indicates if wa want a "and" query, if false it is an "or" query. it returns a new
    list of results"""
    is_results_list_found = False
    while not is_results_list_found:

        i = 0
        all_pl_completely_seen = True  # check if all the pl are entirely seen in order to know if we can find more docs or not
        tau = 0  # the heart variable

        while i < n:  # go through the algo for each term of the research list

            # we will go through each posting list
            doc_id = ""

            for pl in sorted_score_pl_list:
                if last_index_seen < len(pl):

                    all_pl_completely_seen = False  # we don't have finished to see all the current pl

                    item = pl.peekitem(last_index_seen)
                    doc_id = item[1]  # get docID
                    # score = item[0]#get score
                    score = 0
                    tau += int(item[0])  # tau is calculated on live

                    # we get the total score for this doc in all PL of research terms
                    is_doc_in_all_pl = True  # boolean value use for "and" type query

                    for sorted_by_id_pl in sorted_id_pl_list:

                        if doc_id in sorted_by_id_pl:
                            score += int(sorted_by_id_pl[doc_id])
                        else:
                            is_doc_in_all_pl = False

                    # we check if we can add this doc to results
                    # first we check that if we are in an "and" query, the doc_id is in all pl, else we can't add it to results
                    if is_doc_in_all_pl or not is_and_query:
                        if [doc_id, score] not in results_list:
                            if len(results_list) < k:
                                results_list.append([doc_id, score])

                            else:
                                # we check the lowest score in result list and if we have a better score we replace it with the new doc
                                min_item = min(results_list, key=itemgetter(1))

                                if score > int(min_item[1]):
                                    results_list.remove(min_item)
                                    results_list.append([doc_id, score])
                else:
                    # if we are in a conjonctive query, we must end when we reach the end of a posting list
                    if is_and_query:
                        return results_list

            i += 1  # end of this turn of loop
        # end of loop

        # if we do not have enough results in list we re iterate,
        # incrementing the last_index seen in order to see the next best score in pl
        if len(results_list) < k and not all_pl_completely_seen:
            last_index_seen = last_index_seen+1
            continue
            # return fagin_loop(n,k,last_index_seen+1,sorted_score_pl_list,sorted_id_pl_list,results_list,is_and_query)

        # we check tau, if there is a doc in results_list that has a lower score than tau, we re iterate,
        # incrementing the last_index seen in order to see the next best score in pl
        if len(results_list) > 0:
            min_item = min(results_list, key=itemgetter(1))
            if min_item[1] < tau:
                last_index_seen = last_index_seen+1
                continue
                # return fagin_loop(n,k,last_index_seen+1,sorted_score_pl_list,sorted_id_pl_list,results_list,is_and_query)

        is_results_list_found = True

    return results_list
