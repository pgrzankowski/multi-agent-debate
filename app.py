from agents import proposition, opposition, judge, summarizer
from agents.proposition import PropositionDependencies
from agents.oppisition import OppositionDependencies
from agents.judge import JudgeDependencies
from agents.summarizer import SummarizerDependencies
from colorama import Fore, Style
from dotenv import load_dotenv


load_dotenv()

def main():

    thesis = "People will not manage to leave solar system in the future"

    scores = {'proposition': 0, 'opposition': 0}
    debate_history = []

    for i in range(1, 2):
        arguments = []
        print(Style.BRIGHT + Fore.CYAN + f"Round: {i}" + Style.NORMAL)

        # Proposition turn
        proposition_deps = PropositionDependencies(thesis=thesis)
        result = proposition.run_sync(
            user_prompt="It's your turn! Write an argument supporting the thesis.",
            deps=proposition_deps,
            message_history=debate_history
        )
        arguments += result.new_messages()
        debate_history += result.new_messages()
        print(Style.BRIGHT + Fore.GREEN + "Proposition:" + Style.NORMAL)
        print(f"{result.data.argument}" + Fore.RESET)

        # Opposition turn
        opposition_deps = OppositionDependencies(thesis=thesis)
        result = opposition.run_sync(
            user_prompt="It's your turn! Write an argument denying the thesis.",
            deps=opposition_deps,
            message_history=debate_history
        )
        arguments += result.new_messages()
        debate_history += result.new_messages()
        print(Style.BRIGHT + Fore.RED + "Opposition:" + Style.NORMAL)
        print(f"{result.data.argument}" + Fore.RESET)

        # Judging the turn
        judge_deps = JudgeDependencies(thesis=thesis)
        result = judge.run_sync(
            user_prompt="Judge the last 2 arguments",
            deps=judge_deps,
            message_history=arguments
        )
        round_scores = result.data.score
        scores['proposition'] += round_scores.proposition
        scores['opposition'] += round_scores.opposition
        print(Style.BRIGHT + Fore.YELLOW + "Scores:" + Style.NORMAL)
        print(f"\tProposition: {scores['proposition']} (+{round_scores.proposition})")
        print(f"\tOpposition: {scores['opposition']} (+{round_scores.opposition})")
        print(Style.BRIGHT + f"Explanation:\n" + Style.NORMAL + f"\t{result.data.explanation}" + Fore.RESET)
        print()

    summarizer_deps = SummarizerDependencies(
        thesis=thesis,
        proposition_score=scores['proposition'],
        opposition_score=scores['opposition']
    )
    result = summarizer.run_sync(
        user_prompt="Summarize the debate",
        deps=summarizer_deps,
        message_history=debate_history
    )
    winner = result.data.winner
    repeated = result.data.repeated
    mismatch = result.data.mismatch
    summary = result.data.summary
    print(Style.BRIGHT + Fore.CYAN + "Debate report:" + Style.NORMAL)
    print(Style.BRIGHT + "\tWinner: " + Style.NORMAL + f"{winner}")
    print(Style.BRIGHT + "\tRepeated arguments: " + Style.NORMAL + f"{repeated}")
    print(Style.BRIGHT + "\tThesis mismatch: " + Style.NORMAL + f"{mismatch}") # Arguments which didn't stick to the thesis
    print(Style.BRIGHT + "\t\nSummary:\n" + Style.NORMAL + f"{summary}" + Fore.RESET)

if __name__ == '__main__':
    main()
