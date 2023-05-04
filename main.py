from dotenv import dotenv_values
import json

from data_importer.api_data_downloader import GoogleSearchAPI
from data_importer.web_text_extractor import WebTextExtractor
from data_analysis.chatgpt import MarketInsighter
import utils


def extract_text_data(links):
    text_data = []
    for link in links:
        text_extractor = WebTextExtractor(link)
        data = text_extractor.extract_text()
        if data:
            data['link'] = link
            text_data.append(data)
    return text_data


def generate_market_insights(text_data, openai_key):
    market_analyzer = MarketInsighter(openai_key)
    insights = []
    for data in text_data:
        res = market_analyzer.create_insights(json.dumps(data))
        if res["insights"]:
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

    text_data = extract_text_data(links)

    keys_to_keep = ['title', 'description', 'date', 'raw_text', 'pagetype', 'link']
    filtered_text_data = utils.filter_text_data(text_data, keys_to_keep)

    x_years = 1
    last_x_years_text_data = utils.filter_last_x_years_text_data(filtered_text_data, x_years)

    truncated_text_data = utils.truncate_text_data(last_x_years_text_data)

    insights = generate_market_insights(truncated_text_data, config["OPENAI_KEY"])

    print_insights(insights)


if __name__ == "__main__":
    query = "online shoe market size"
    analyze_market(query)
