import openai
import json


class ChatGPT:
    def __init__(self, api_key):
        # set up OpenAI API credentials
        openai.api_key = api_key

    def generate_response(self, prompt):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=prompt,
            max_tokens=1000,
            temperature=0
        )
        return response.choices[0].message.content.strip()


class MarketInsighter(ChatGPT):
    def __init__(self, api_key):
        super().__init__(api_key)

    def create_insights(self, text):
        prompt = f"""
                Prompt: Examine the given marketing-related article and extract crucial insights, especially any noteworthy numerical data or statistics or taking about money. If no insights are discovered, provide a JSON object with an empty insights array. don't write anything, just the json. Structure the information in the following JSON format:
                
                {{
                "insights": [
                "insight1": "A 15% average increase in sales was observed for companies that adopted social media marketing strategies.",
                "insight2": "Instagram emerged as the top-performing platform for B2C marketing, with 65% of businesses reporting successful campaigns."
                ]
                }}
                }}
                
        """
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": text},
        ]
        response = self.generate_response(messages)
        response_dict = json.loads(response)
        return response_dict
