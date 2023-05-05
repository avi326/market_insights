from googlesearch import search


class GoogleSearchAPI:
    def __init__(self):
        return

    def get_links(self, query):
        search_results = []
        for url in search(query, num_results=10):
            search_results.append(url)
        return search_results


if __name__ == "__main__":
    google_search_api = GoogleSearchAPI()
    google_search_data = google_search_api.get_links("size of the online shoe market")
    print("Google Search API Data:")
    for result in google_search_data:
        print(result['link'])
