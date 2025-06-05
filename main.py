"""A research assistant that will help generate a research paper and answer the user's questions to the best of its ability.
Objective: Provide the application with a question or series of questions, and have it return an answer and a suitable explaination thereof, as well as a document containing a summary of those findings along with sources used as a report from its interactions with the user.
Purpose: To obtain a better understanding of AI agents, including their interaction with web APIs, local databases and retrieval augmented generation (RAG), tool usage, embeddings, and the limitations of all of the above
"""

# Imports
from typing import Optional, Literal
from pydantic import BaseModel, Field
from ollama import chat
import logging, copy, datetime, json

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

SYSTEM_PROMPT = [
    {
        "role": "system",
        "content": """\
You are a research assistant that will help generate a research paper.
Answer the user query, use necessary tools, and always provide sources or references for your answers. If you cannot find a source, clearly state so.""",
    },
]

# Data model definitions

# Tools

# Model Chain

# Main Functionality


def save_to_report(user_input: str, assistant_response: str, report_path: str = "research_report.md"):
    """Append the latest Q&A to a markdown report file, including a timestamp."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(report_path, "a", encoding="utf-8") as f:
        f.write(f"### Timestamp: {timestamp}\n\n")
        f.write(f"## Question\n{user_input}\n\n")
        f.write(f"## Answer\n{assistant_response}\n\n---\n\n")


def save_session(messages, session_path="saved_output/session.json"):
    """Save the current conversation history to a JSON file."""
    with open(session_path, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)


def load_session(session_path="saved_output/session.json"):
    """Load conversation history from a JSON file."""
    try:
        with open(session_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def main(user_input: str = "", messages: list[dict] = SYSTEM_PROMPT, report_path: str = "research_report.md") -> str:
    """Main function to run the research assistant."""
    logger.debug("Starting the research assistant...")

    if user_input == "":
        return "Please provide a question or topic to research."
    if user_input.strip() == "/summary":
        # Generate a summary of the session
        summary_prompt = "Summarize the research session so far, including key findings and sources."
        messages.append({"role": "user", "content": summary_prompt})
        try:
            response = chat(
                MODEL,
                messages=messages,
            )
            messages.append({"role": "assistant", "content": response.message.content})
            save_to_report(summary_prompt, response.message.content, report_path=report_path)
            return f"Session summary appended to report.\n\n{response.message.content}"
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return "An error occurred while generating the summary. Please try again."

    messages.append({"role": "user", "content": user_input})

    try:
        response = chat(
            MODEL,
            messages=messages,
        )
        messages.append({"role": "assistant", "content": response.message.content})
        # Save Q&A to report after each response
        save_to_report(user_input, response.message.content, report_path=report_path)
        return response.message.content

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return "An error occurred while processing your request. Please try again."


# Operating Loop

if __name__ == "__main__":
    messages = copy.deepcopy(SYSTEM_PROMPT)
    report_path = input("Enter a filename for your research report (default: saved_output/research_report.md): ").strip()
    if not report_path:
        report_path = "saved_output/research_report.md"
    session_path = input("Enter a session filename to load (or press Enter to start new): ").strip()
    if session_path:
        loaded = load_session(session_path)
        if loaded:
            messages = loaded
            print(f"Loaded session from {session_path}.")
        else:
            print(f"Could not load session from {session_path}, starting new session.")
    while True:
        try:
            user_input = input("Enter your question (type 'exit' to quit, '/summary' for session summary, '/save' to save session): ")
            if user_input.lower() == "exit" or user_input.lower() == "quit":
                logger.info("Exiting the research assistant.")
                break
            if user_input.strip() == "/save":
                session_path = input("Enter a filename to save the session (default: saved_output/session.json): ").strip()
                if not session_path:
                    session_path = "saved_output/session.json"
                save_session(messages, session_path)
                print(f"Session saved to {session_path}.")
                continue
            # Process the user input
            response = main(user_input=user_input, messages=messages, report_path=report_path)
            print(response)
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt received. Exiting...")
            break
        except Exception as e:
            logger.error(f"An error occurred: {e}")
