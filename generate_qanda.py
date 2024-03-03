import argparse
import json
import os

from openai import OpenAI


SYSTEM_PROMPT = (
    "Turn the following data that was scraped from the internet for the website darwin.ai into question "
    "and answer pairs than can be used to fine tune a LLM to answer questions about darwin.ai. "
    "Return answers as a json loadable list of dictionaries where each dictionary contains"
    "one 'question' key and one 'answer key'."
)
OPEN_AI_MODEL = "gpt-4-turbo-preview"
NUM_QUERIES_PER_PAGE = 5


def parse_arguments() -> argparse.Namespace:
    # setup arg parser
    parser = argparse.ArgumentParser()
    parser.add_argument("openapi_key", help="Key to use open api.")
    parser.add_argument("scrapped_dir", help="Dir containing scrapped pages")
    parser.add_argument("qa_file", help="File to save q and a's too.")
    return parser.parse_args()


def main(
    openapi_key: str,
    scrapped_dir: str,
    qa_file: str,
):
    question_list = []
    try:
        client = OpenAI(api_key=openapi_key)
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for scrapped_text in sorted(os.listdir(scrapped_dir)):
            print(f"Loading text for scraped page {scrapped_text}")
            with open(os.path.join(scrapped_dir, scrapped_text)) as fh:
                text = fh.read()

            messages.append({
                "role": "user",
                "content": f"Generate question answer pairs from this scraped text {text}"
            })
            for _ in range(NUM_QUERIES_PER_PAGE):
                response = client.chat.completions.create(
                    model=OPEN_AI_MODEL, messages=messages, max_tokens=4096
                )
                content = response.choices[0].message.content
                try:
                    question_list = question_list + json.loads(
                        content[content.find('['):content.rfind(']') + 1].strip()
                    )
                except json.decoder.JSONDecodeError:
                    user_input = None
                    while user_input not in ['y', 'n']:
                        user_input = input(f"Invalid content {content}: Press y to continue or n to exit: ")
                    if user_input == "n":
                        raise Exception("Exiting loop and saving results.")

                    messages.append(
                        {"role": "assistant", "content": content},
                    )
                    messages.append(
                        {"role": "user", "content": "The last message was not json readable, please reformat in the "
                                                    "correct format."},
                    )

                messages.append(
                    {"role": "assistant", "content": content},
                )
                messages.append(
                    {
                        "role": "user",
                        "content": "Continue generating more question answer pairs. If no new "
                        "question answer pairs are possible, rephrasing previous question answer pairs is "
                        "allowed.",
                    },
                )
    finally:
        with open(qa_file, "w+") as fh:
            json.dump(question_list, fh, indent=4)


if __name__ == "__main__":
    args = parse_arguments()
    main(args.openapi_key, args.scrapped_dir, args.qa_file)
