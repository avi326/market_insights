from dotenv import dotenv_values
import json

from data_importer.api_data_downloader import GoogleSearchAPI
from data_importer.web_text_extractor import WebTextExtractor
from data_analysis.chatgpt import MarketInsighter
import utils


def extract_text_data(link):
    text_extractor = WebTextExtractor(link)
    data = text_extractor.extract_text()
    if data:
        data['link'] = link
    return data


def generate_market_insights(text_data, openai_key):
    market_analyzer = MarketInsighter(openai_key)
    insights = []
    for data in text_data:
        keys_to_keep = ['title', 'description', 'raw_text']
        temp_data = utils.filter_text_data(text_data, keys_to_keep)
        res = market_analyzer.create_insights(json.dumps(temp_data))
        insights.append((data['link'], res))
    return insights


def print_insights(insights):
    for link, insight in insights:
        print("#########################################")
        print(f"link {link}")
        print(insight)


def analyze_market(google_query):
    config = dotenv_values(".env")

    google_search = GoogleSearchAPI()
    links = google_search.get_links(google_query)

    text_data = []
    for link in links:
        try:
            data = extract_text_data(link)
            text_data.append(data)
        except Exception:
            print(f"fail to get data from {link}")

    keys_to_keep = ['title', 'description', 'date', 'raw_text', 'pagetype', 'link']
    filtered_text_data = utils.filter_text_data(text_data, keys_to_keep)

    x_years = 1
    last_x_years_text_data = utils.filter_last_x_years_text_data(filtered_text_data, x_years)

    truncated_text_data = utils.truncate_text_data(last_x_years_text_data)

    insights = generate_market_insights(truncated_text_data, config["OPENAI_KEY"])

    print_insights(insights)


if __name__ == "__main__":
    query = "old age home care market"
    analyze_market(query)
