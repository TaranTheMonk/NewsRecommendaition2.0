import gensim
from gensim import similarities
from mysql import connector
import os


class SqlFunction():




def main():
    index = gensim.similarities.SparseMatrixSimilarity()
    return


def getData_en(docs_address):
    #Import User Dataset
    #Specify dataset location
    corpus = cal.load_corpus(docs_address)
    docs = cal.corpus_docs(corpus)
    docs = cal.docs_stemmer(docs)

    ##stemmering and cleanning for reducing dimensions of vector space
    ##Use docs dictionary as the dictionary
    dictionary = gensim.corpora.Dictionary(docs)
    vecs = cal.docs_vecs(docs, dictionary)
    fileids = corpus.fileids()
    docs = {'vecs': vecs, 'dictionary': dictionary, 'file_ids': fileids, 'tf_idf': 0}
    return docs

def Computing_en(docs):
    #tf to tf-idf
    docs['tf_idf'], docs['vecs'] = cal.tf_idf(docs['vecs'])
    #Build Index
    index = similarities.SparseMatrixSimilarity(docs['vecs'], len(docs['dictionary']))
    print('EN Computing Finished')
    return index