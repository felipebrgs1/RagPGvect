from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage


import os
from dotenv import load_dotenv
load_dotenv()


token = os.getenv('GOOGLE_API_KEY')
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=token)


message = HumanMessage(
    content=[
        {
            "type": "text",
            "text": "What's in this image?",
        },
        {"type": "image_url", "image_url": "https://picsum.photos/seed/picsum/200/300"},
    ]
)

for chunk in llm.stream([message]):
    print(chunk.content)