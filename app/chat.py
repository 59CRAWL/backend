from dotenv import load_dotenv
import os

import replicate
from transformers import PreTrainedTokenizerFast

from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
from langchain.agents import create_csv_agent
import pandas as pd

load_dotenv()

def csv_agent(json="", prompt=""):``
    # Create a Pandas DataFrame from the list of dictionaries
    df = pd.DataFrame(json)

    # Specify the CSV file name
    csv_file_name = "output.csv"

    # Save the DataFrame to a CSV file
    df.to_csv(csv_file_name, index=False)

    agent = create_csv_agent(
        ChatOpenAI(model="gpt-3.5-turbo-0613", temperature=0),
        "output.csv",
        verbose=True,
        agent_type=AgentType.OPENAI_FUNCTIONS,
    )

    return agent.run(prompt)
    

def llama(json="", prompt=""):
    MAX_TOKEN = 4096 - 300 # 300 is lee way for the prompt, more than enough
    fast_tokenizer = PreTrainedTokenizerFast(tokenizer_file="tokenizer.json")

    # Create a list to store CSV lines
    csv_lines = []

    # Get CSV headers
    header = ','.join(json[0].keys())
    csv_lines.append(header)

    # Create data lines
    for row in json[0:20]:
        data_line = ','.join(map(str, row.values()))
        csv_lines.append(data_line)

    # Combine the lines into a CSV string
    csv_string = '\n'.join(csv_lines)

    # Figure out the token size and do accordingly
    print(len(fast_tokenizer.tokenize(csv_string)))

    # print(fast_tokenizer.tokenize(csv_string))

    response = "simplereactchatbot"

    print(json)

    if not os.getenv("REPLICATE_API_TOKEN"):
        return "REPLICATE_API_TOKEN not found, please configure in .env."
    else:
        context = "Given a csv of " + csv_string + "\n Return me a list of id and vessel name \n"

        output = replicate.run(
            "meta/llama-2-7b-chat:8e6975e5ed6174911a6ff3d60540dfd4844201974602551e10e9e87ab143d81e",
            input={"prompt": context + prompt},
            max_new_tokens=100000,
        )

        response = ""
    
        # The meta/llama-2-70b-chat model can stream output as it's running.
        # The predict method returns an iterator, and you can iterate over that output.
        for item in output:
            # https://replicate.com/meta/llama-2-70b-chat/versions/02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3/api#output-schema
            response += item

    return response