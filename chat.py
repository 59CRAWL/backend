from dotenv import load_dotenv
import os

import replicate

load_dotenv()

def llama(json="", prompt=""):    
    if not os.getenv("REPLICATE_API_TOKEN"):
        return "REPLICATE_API_TOKEN not found, please configure in .env."
    else:
        context = "Given a json object of " + json

        output = replicate.run(
            "meta/llama-2-7b-chat:8e6975e5ed6174911a6ff3d60540dfd4844201974602551e10e9e87ab143d81e",
            input={"prompt": context + prompt}
        )

        response = ""
    
        # The meta/llama-2-70b-chat model can stream output as it's running.
        # The predict method returns an iterator, and you can iterate over that output.
        for item in output:
            # https://replicate.com/meta/llama-2-70b-chat/versions/02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3/api#output-schema
            response += item

        return response