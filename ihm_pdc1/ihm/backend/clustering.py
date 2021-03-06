import math
import random
from sklearn.cluster import KMeans

def calculate_cosine_matrix(terms_dict_doc_list):
    #for a given list of document vectors represented by dic where key is term and value is nb occ
    #calculate and return the cosine matrix
    print("begin")

    #first we create the square matrix
    width = len(terms_dict_doc_list)

    #creation of the matrix and initialization
    matrix = [[0 for x in range(width)] for y in range(width)]

    for i in range(width):
        for j in range(width):
            #in diagonale, matrix[i][j]=1
            if i==j:
                matrix[i][j] = 1
            else:
                matrix[i][j] = calculate_cosine_between_docs(terms_dict_doc_list[i],terms_dict_doc_list[j])
                matrix[j][i] = matrix[i][j] # symetric matrix

    return matrix



def calculate_norm_of_document_vector(document_vector):
    #calculate and return the norm of a document vector represented by a list.

    norm = 0

    for value in document_vector:
        norm += value*value

    return math.sqrt(norm)



def calculate_cosine_between_docs(terms_dict_doc_1,terms_dict_doc_2):
    #calculate and return cosine similarity between two docs with their document vector represented by dict
    #where key is term and value is nb occ

    norm_vect_1 = calculate_norm_of_document_vector(terms_dict_doc_1.values())
    norm_vect_2 = calculate_norm_of_document_vector(terms_dict_doc_2.values())

    dot_product = 0

    #we check that vectors have norms different from 0 in order to calculate dot product
    if norm_vect_1!=0 and norm_vect_2!=0:
        # we get the one who has the min vector to calculate cosine
        
        if len(terms_dict_doc_1)<len(terms_dict_doc_2):
            for key in terms_dict_doc_1.keys():
                if key in terms_dict_doc_2:
                    dot_product += terms_dict_doc_1[key]*terms_dict_doc_2[key]
        else:
            for key in terms_dict_doc_2.keys():
                if key in terms_dict_doc_1:
                    dot_product += terms_dict_doc_1[key]*terms_dict_doc_2[key]

        dot_product = dot_product/ (norm_vect_1*norm_vect_2)
    
    return dot_product
    
#return k lists representing k clusters with list containing the index of docs in the similarity_matrix
#k must be lower than length of matrix, or we return a list where all doc belongs to the same cluster
def get_k_clusters_from_matrix(k,similarity_matrix):
    #k must be lower than length of matrix
    if k>len(similarity_matrix):
        j=0
        res = list()
        for j in range(len(similarity_matrix)):
            res.append(j)
            j += 1
        return [res]

    num_clusters = k

    km = KMeans(n_clusters=num_clusters)
    #km = KMeans()
    km.fit(similarity_matrix)

    clusters = km.labels_.tolist()
    print(clusters)

    result = list()

    for i in range(num_clusters):
        result.append(list())

    i = 0
    while i<len(clusters):
        result[clusters[i]].append(i)
        i += 1

    return result

# return a list of descriptions for a cluster
def get_description_of_cluster(dict_list,number_of_keys_to_considered=3):
    result = dict()
    for dico in dict_list:
        i=0
        keys = sorted(dico, key=dico.get, reverse=1) # get keys sorted  by values

        while i in range(number_of_keys_to_considered) and i<len(keys):
            key = keys[i]
            i += 1
            if key in result:
                result[key] += dico[key]
            else:
                result[key] = dico[key]

    return sorted(result, key=result.get, reverse = 1)



def clustering_process_for_best_results_query(voc, query_results_list, number_of_keys_to_considered=3, number_of_clusters_wanted=3, number_of_describing_words=3):
# this method take in parameters an object vocabulary 'voc', and a list of results of a query which is a list of [docId, score]
# two optional parameters, 'number_of_keys_to_considered' for the number of words we look in a doc's terms_dict
#                          'number_of_clusters_wanted' for the number of clusters to create
#                          'number_of_describing_words' for the number of words for describing a cluster
# this method will create clusters and for each cluster see the best words that describe the cluster
# it returns a dict where value is the number of cluster and key is doc_id, and an other dict where key is the number of cluster and value is a list taht contains describing words
    
    #first we get the dict for all docs where key is docId and value is an other dict where key is term and value is score
    terms_dicts_for_docs_dic = voc.get_terms_dicts_for_docs()

    # we will get the term_dict for the doc_ids in query_results_list
    fagin_result_doc_list = list()

    #so we get the term_dict with the doc_id
    for item in query_results_list:
        fagin_result_doc_list.append(terms_dicts_for_docs_dic[item[0]])#item[0] is docId


    #Then we will calculate cosine similarity with the docs's terms dicts where key is term and value is score 
    #we calculate the cosine matrix
    matrix = calculate_cosine_matrix(fagin_result_doc_list)

    #with the cosine matrix, we can find clusters
    doc_id_clusters = get_k_clusters_from_matrix(number_of_clusters_wanted,matrix)
    print(doc_id_clusters)

    #we create a dictionary where key is the number of cluster and value is a list of words that describes this cluster
    describing_words_clusters_lists_dict = dict()

    # we create a dict where value is the number of the cluster and key is the doc_id
    doc_id_clusters_dict = dict()

    #then we go through each cluster in order to see which words best describe them
    i=0
    for id_cluster in doc_id_clusters:
        print("cluster ",i," : ")
        i +=1

        

        dict_cluster_list = list()

        for index_doc_id in id_cluster:
            print(index_doc_id)
            doc_id_clusters_dict[query_results_list[index_doc_id][0]] = i
            dict_cluster_list.append(fagin_result_doc_list[index_doc_id])

        description = get_description_of_cluster(dict_cluster_list,number_of_keys_to_considered)

        describing_words_clusters_lists_dict[i] = description[0:number_of_describing_words]

        for j in range(len(describing_words_clusters_lists_dict[i])):
            print(description[j])

        print("____________________________")

    return (doc_id_clusters_dict,describing_words_clusters_lists_dict)





def test():

    
    dico0 = {"insa":10,"informatique":3,"ordinateur":5,"cours":7,"sport":2}
    #norm1 = calculate_norm_of_document_vector(dico1.values())
    #print("norm1 = ",norm1)

    dico1 = {"insa":18,"informatique":6,"ordinateur":7,"cours":5,"chaise":2,"table":4}

    dico2 = {"insa":18,"ordinateur":3,"cours":6,"pantalon":2}

    dico3 = {"insa":14,"informatique":3,"ordinateur":2,"cours":5,"chaise":6,"pantalon":4}

    dico4 = {"insa":10,"informatique":3,"ordinateur":5,"cours":7,"sport":3}
    dico5 = {"insa":11,"informatique":3,"ordinateur":5,"cours":7,"sport":3}

    fagin_result_doc_list = [dico0,dico1,dico2,dico3,dico4,dico5]

    #liste = [dico0,dico1,dico2,dico3]
    liste = [dico0,dico1,dico2,dico3,dico4,dico5]
    matrix = calculate_cosine_matrix(liste)

    id_clusters = get_k_clusters_from_matrix(3,matrix)
    print(id_clusters)

    i=0
    for id_cluster in id_clusters:
        print("cluster ",i," : ")
        i +=1

        dict_cluster_list = list()

        for doc_id in id_cluster:
            print(doc_id)
            dict_cluster_list.append(fagin_result_doc_list[doc_id])

        description = get_description_of_cluster(dict_cluster_list)

        number_of_words_wanted = 3
        for j in range(number_of_words_wanted):
            print(description[j])

        print("____________________________")


    
    #print(calculate_cosine_between_docs(dico1,dico2))

#test()






