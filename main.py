"""A research assistant that will help generate a research paper and answer the user's questions to the best of its ability.
Objective: Provide the application with a question or series of questions, and have it return an answer and a suitable explaination thereof, as well as a document containing a summary of those findings along with sources used as a report from its interactions with the user.
Purpose: To obtain a better understanding of AI agents, including their interaction with web APIs, local databases and retrieval augmented generation (RAG), tool usage, embeddings, and the limitations of all of the above
"""

# Imports
from typing import Optional, Literal
from pydantic import BaseModel, Field
from ollama import chat
import logging

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Variable Definitions
MODEL = "llama3.1"
# TOOLS = [search_tool, wiki_tool, summary_tool]

# Data model definitions

# Tools

# Model Chain

# Main Functionality


def main(user_input: str = "") -> str:
    """Main function to run the research assistant."""
    logger.debug("Starting the research assistant...")

    if user_input == "":
        return "Please provide a question or topic to research."

    try:
        response = chat(
            MODEL,
            messages=[
                {
                    "role": "system",
                    "content": """\
                    You are a research assistant that will help generate a research paper. 
                    Answer the user query and use neccessary tools.""",
                },
                {"role": "user", "content": user_input},
            ],
        )
        return response.message.content

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return "An error occurred while processing your request. Please try again."


# Operating Loop

if __name__ == "__main__":
    while True:
        try:
            user_input = input("Enter your question (type 'exit' to quit): ")
            if user_input.lower() == "exit" or user_input.lower() == "quit":
                logger.info("Exiting the research assistant.")
                break

            # Process the user input
            response = main(user_input=user_input)
            print(response)

        except KeyboardInterrupt:
            logger.info("Keyboard interrupt received. Exiting...")
            break
        except Exception as e:
            logger.error(f"An error occurred: {e}")
