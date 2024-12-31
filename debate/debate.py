from agents import (thesis_analyzer,
                    proposition,
                    opposition,
                    judge,
                    summarizer)
from agents.proposition import PropositionDependencies
from agents.oppisition import OppositionDependencies
from agents.judge import JudgeDependencies
from agents.summarizer import SummarizerDependencies
from colorama import Fore, Style
from dotenv import load_dotenv


class Debate:
    def __init__(self):
        load_dotenv()
        self._scores = {'proposition': 0, 'opposition': 0}
        self._debate_history = []
        self._round_arguments = []

    def _verify_thesis(self, thesis):
        result = thesis_analyzer.run_sync(user_prompt=thesis)

        if result.data.debatable:
            print(Style.BRIGHT + Fore.GREEN + "Thesis is debatable" + Style.NORMAL)
            return True
        else:
            print(Style.BRIGHT + Fore.RED + "Thesis is not debatable" + Style.NORMAL)
            print(Style.BRIGHT + f"Explanation:\n" + Style.NORMAL + f"\t{result.data.explanation}" + Fore.RESET)
            return False
        
    def _proposition_turn(self, thesis):
        proposition_deps = PropositionDependencies(thesis=thesis)
        result = proposition.run_sync(
            user_prompt="It's your turn! Write an argument supporting the thesis.",
            deps=proposition_deps,
            message_history=self._debate_history
        )
        self._round_arguments += result.new_messages()
        self._debate_history += result.new_messages()
        print(Style.BRIGHT + Fore.GREEN + "Proposition:" + Style.NORMAL)
        print(f"{result.data.argument}" + Fore.RESET)

    def _opposition_turn(self, thesis):
        opposition_deps = OppositionDependencies(thesis=thesis)
        result = opposition.run_sync(
            user_prompt="It's your turn! Write an argument denying the thesis.",
            deps=opposition_deps,
            message_history=self._debate_history
        )
        self._round_arguments += result.new_messages()
        self._debate_history += result.new_messages()
        print(Style.BRIGHT + Fore.RED + "Opposition:" + Style.NORMAL)
        print(f"{result.data.argument}" + Fore.RESET)

    def _judge_round(self, thesis):
        judge_deps = JudgeDependencies(thesis=thesis)
        result = judge.run_sync(
            user_prompt="Judge the last 2 arguments. Remeber to give more points to the winning side.",
            deps=judge_deps,
            message_history=self._round_arguments
        )
        round_scores = result.data.score
        self._scores['proposition'] += round_scores.proposition
        self._scores['opposition'] += round_scores.opposition
        print(Style.BRIGHT + Fore.YELLOW + "Scores:" + Style.NORMAL)
        print(f"\tProposition: {self._scores['proposition']} (+{round_scores.proposition})")
        print(f"\tOpposition: {self._scores['opposition']} (+{round_scores.opposition})")
        print(Style.BRIGHT + f"Explanation:\n" + Style.NORMAL + f"\t{result.data.explanation}" + Fore.RESET)
        print()

    def _perform_rounds(self, thesis, rounds):
        for i in range(1, rounds + 1):
            print(Style.BRIGHT + Fore.CYAN + f"Round: {i}" + Style.NORMAL)
            self._proposition_turn(thesis)
            self._opposition_turn(thesis)
            self._judge_round(thesis)

    def _summarize(self, thesis):
        summarizer_deps = SummarizerDependencies(
            thesis=thesis,
            proposition_score=self._scores['proposition'],
            opposition_score=self._scores['opposition']
        )
        result = summarizer.run_sync(
            user_prompt="Get the winner and summarize the debate",
            deps=summarizer_deps,
            message_history=self._debate_history
        )
        print(Style.BRIGHT + Fore.CYAN + "Debate report:" + Style.NORMAL)
        print(Style.BRIGHT + "\tWinner: " + Style.NORMAL + f"{result.data.winner}")
        print(Style.BRIGHT + "\tRepeated arguments: " + Style.NORMAL + f"{result.data.repeated}")
        print(Style.BRIGHT + "\tThesis mismatch: " + Style.NORMAL + f"{result.data.mismatch}") # Arguments which didn't stick to the thesis
        print(Style.BRIGHT + "\t\nSummary:\n" + Style.NORMAL + f"{result.data.summary}" + Fore.RESET)


    def perform(self, thesis, rounds):
        print(Style.BRIGHT + Fore.CYAN + "Thesis: " + Style.NORMAL)
        print(f"{thesis}" + Fore.RESET)

        if not self._verify_thesis(thesis):
            return

        self._perform_rounds(thesis, rounds)

        self._summarize(thesis)




