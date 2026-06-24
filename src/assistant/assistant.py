from src.assistant.tools import (
    get_team_elo,
    get_team_group,
    get_team_fixtures, 
    compare_teams
)

def ask_assistant(question: str): 

    question = question.lower()

    if "elo" in question: 
        team = question.replace("what is", "").replace("elo", "").strip()
        return get_team_elo(team)
    elif "group" in question:
        team = question.replace("what group is", "").replace("in", "").strip()
        return get_team_group(team)
    elif "fixture" in question:
        team = question.replace("show", "").replace("fixtures", "").strip()
        return get_team_fixtures(team)
    
    elif "compare" in question: 

        teams = (question.replace("compare", "").split("and"))

        if len(teams) == 2:
            return compare_teams(
                teams[0].strip(), teams[1].strip()
            )
        
    return {
        "message": "Sorry, I don't udenrstand that question yet."
    }

if __name__ == "__main__":

    print(
        ask_assistant(
            "What is belgium elo"
        )
    )

    print(
        ask_assistant(
            "what group is belgium in"
        )
    )

    print(
        ask_assistant(
            "show belgium fixtures"
        )
    )

    print(
        ask_assistant(
            "compare belgium and egypt"
        )
    )