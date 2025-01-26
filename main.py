import openai
from openai import OpenAI
from flask import Flask

app = Flask(__name__)


def main():
    prompt = ""
    open_ai_client = OpenAI()
    try:
        response = open_ai_client.images.generate(
            model="dall-e-2",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        print(response.data)

        print(response.data[0].url)

    except openai.OpenAIError as e:
        print(e.http_status)
        print(e.error)

if __name__ == "__main__":
    main()