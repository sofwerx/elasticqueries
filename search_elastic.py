import json

# Elastic Search

def search_elastic(ix, query = None):
    from elasticsearch import Elasticsearch
    all_results = []

    es = Elasticsearch(['https://elastic:taiko7Ei@elasticsearch.blueteam.devwerx.org'])

    if query is not None:

        body = query
    else:
        body = None

    query_count = es.search(index=ix ,body=body,size=0)

    n = query_count['hits']['total']

    if (n <= 10000):
        result = es.search(index=ix, size=n , body=body)
        return(result)

    scan_es = es.search(index=ix, size=10000, scroll="60m" , body=body)

    # print("search: ", json.dumps(scan_es, indent=4))

    sid = scan_es['_scroll_id']
    all_results.append(scan_es)

    # print("all_results: ", json.dumps(all_results))

    count = 1
    print(count)

    while (n > 0):
        n = n - 10000
        result = es.scroll(scroll_id=sid, scroll="60m")

        # print("result: ", json.dumps(result))
        count = count + 1
        print(count)

        all_results.append(result)

    return(all_results)


# data = search_elastic('auditbeat-6.2.2-2018.02.27')
#
# print("data: ", json.dumps(data, indent=4))