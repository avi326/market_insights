from trafilatura import fetch_url, bare_extraction


class WebTextExtractor:
    def __init__(self, url):
        self.url = url

    def extract_text(self):
        downloaded = fetch_url(self.url)
        extracted_text = bare_extraction(downloaded, output_format='csv', favor_precision=True, date_extraction_params={
            "original_date": True})
        return extracted_text if extracted_text else None
