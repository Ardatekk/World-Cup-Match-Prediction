from src.assistant.tools import (
    get_team_elo,
    get_team_group,
    get_team_fixtures,
    compare_teams,
    get_match_prediction,
)

from src.assistant.formatters import (
    format_elo,
    format_group,
    format_fixtures,
    format_comparison,
    format_prediction,
)

def ask_assistant(question: str):

    question = question.lower()

    if "elo" in question:
        team = (
            question
            .replace("what is", "")
            .replace("what's", "")
            .replace("the", "")
            .replace("elo", "")
            .replace("rating", "")
            .strip()
        )
        return format_elo(get_team_elo(team))

    elif "group" in question:
        team = (
            question
            .replace("what group is", "")
            .replace("which group is", "")
            .replace("in", "")
            .strip()
        )
        return format_group(get_team_group(team))

    elif "fixture" in question:
        team = (
            question
            .replace("show", "")
            .replace("fixtures", "")
            .replace("fixture", "")
            .strip()
        )
        return format_fixtures(get_team_fixtures(team))

    elif "compare" in question:
        teams = question.replace("compare", "").split("and")

        if len(teams) == 2:
            return format_comparison(
                compare_teams(teams[0].strip(), teams[1].strip())
            )
    
    elif "predict" in question:
        teams = question.replace("predict", "").split("vs")

        if len(teams) == 2:
            return format_prediction(
                get_match_prediction(
                    teams[0].strip().title(),
                    teams[1].strip().title()
                )
            )

    return "Sorry, I don't understand that question yet."

if __name__ == "__main__":

    print("⚽ World Cup Assistant")
    print("Type 'quit' to exit.\n")

    while True:

        question = input("You: ")

        if question.lower() in ["quit", "exit"]:
            print("Assistant: Goodbye!")
            break

        response = ask_assistant(question)

        print(f"\nAssistant: {response}\n")