from config import quest_config


class Question:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

    def check_answer(self, answer):
        return self.answer == answer

    def __str__(self):
        return f'Question: {self.question}, Answer: {self.answer}'


class Quest:
    def __init__(self, questions: list[Question], start_message: str, base_final: str, good_final: str, bad_final: str):
        self.questions = questions
        self.start_message = start_message
        self._base_final = base_final
        self._good_final = good_final
        self._bad_final = bad_final
        self.current_question = 0

    def get_question(self, number: int) -> str:
        return self.questions[number - 1].question

    def check_answer(self, question_number: int, answer: str) -> bool:
        return self.questions[question_number - 1].check_answer(answer)

    def _get_base_final(self, position: int):
        return self._base_final.replace('{}', str(position))

    def get_good_final(self, position: int, reward: str) -> str:
        return f"{self._get_base_final(position)}\n\n{self._good_final.replace('{}', reward)}"

    def get_bad_final(self, position: int) -> str:
        return f"{self._get_base_final(position)}\n\n{self._bad_final}"


main_quest = Quest(
    [
        Question(
            "Here's the riddle! Answer should be uppercase\n\n1110011 1100001 1111001 1111001 1100101 1110011",
            'SAYYES',
        ),
        Question(
            f"Explore {quest_config.YESCOIN_CHANNEL} to find the answer. It should be uppercase and without whitespaces. Look for a Morse code!",
            'YES2024COIN',
        ),
        Question(
            f'Explore this chat {quest_config.CHAT_WITH_AGENT}. Our manager will write an answer there',
            'We express respect for all projects on TON. With love, Yescoin.',
        ),
        Question(
            "Decipher it (it's two parts of the same phrase)\n\n12. Kqe Oauz iuxx nqoayq ftq yaef babgxmd fawqz\n18. gf Lzw Ghwf Fwlogjc tdgucuzsaf",
            'Yes Coin will become the most popular token on The Open Network blockchain',
        ),
    ],
    start_message="Hey! Here's the quest from YesCoin. If you complete it, you could get valuable prizes. Good luck!",
    base_final="Congratulations, you've completed the quest! Your position is {}.",
    good_final="Your reward is {}!\n\nPlease provide your TON wallet address to receive your reward.",
    bad_final="Unfortunately, there's no available rewards. But you can try again next time!",
)
