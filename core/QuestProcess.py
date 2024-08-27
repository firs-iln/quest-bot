from config import quest_config


class Question:
    def __init__(self, question: str, answers: list[str]):
        self.question = question
        self.answers = answers

    def check_answer(self, answer):
        for lol in self.answers:
            if lol == answer:
                return True
        return False

    def __str__(self):
        return f'Question: {self.question}, Answer: {", ".join(self.answers)}'


class Quest:
    def __init__(self, questions: list[Question], start_message: str, good_final: str, bad_final: str):
        self.questions = questions
        self.start_message = start_message
        self._good_final = good_final
        self._bad_final = bad_final
        self.current_question = 0

    def get_question(self, number: int) -> str:
        return self.questions[number - 1].question

    def check_answer(self, question_number: int, answer: str) -> bool:
        return self.questions[question_number - 1].check_answer(answer)

    def get_good_final(self, position: int, reward: str) -> str:
        return self._good_final.format(str(position), reward)

    def get_bad_final(self, position: int) -> str:
        return self._bad_final


main_quest = Quest(
    [
        Question(
            "Hi! Did you guess the key of the first day? Send it to me!"
            "(write it using CapsLock)",
            ["SEASON TWO", "SEASONTWO"],
        ),
        Question(
            "Hi! Have you returned from your chat walk yet? Send me the passphrase!",
            ["Funny guys"],
        ),
        Question(
            "Shall we go for a walk? Find our spy agent (@scamjettontonchat) in the chat and ask him for the key. Enter it.",
            ["The Yumify team says hello to this chat!"],
        ),
        Question(
            "Congratulations! but let's not stop and go to the next chat! The rules are the same."
            "lets gooo @cheitochat",
            ["Yumify go ahead!!!"]
        ),
        Question(
            "Let's start with a simple task. Decipher it:"
            "Pldzwp nvctfdvj pfl!",
            ["Yumify welcomes you!"],
        ),
        Question(
            "Find the updated @yumify travel guide. Count the number of words in it (don't count the links)."
            "Did you count it? Insert this number instead of X into this equation:"
            "3+(X/3+7*7)/4+14=????",
            ["31"],
        ),
        Question(
            "Try to decipher it. I'll tell you right away that you'll need a key."
            "Guess for yourself which word is the key😁"
            "rqa utvrbe. djzw fubytc nuuj",
            [
                "Two months. Very little time",
                "two months.very little time"
            ],
        ),
        Question(
            "Let's go back to the dark times of human history, in 1939-1945."
            "(Hint: M3, then 2>2>8)"
            "Qjctsp evqekdjux bn gjv vspz esucdzzir mq zfp gqdxg",
            [
                "Yumify community is the best community in the world",
                "YUMIFYCOMMUNITYISTHEBESTCOMMUNITYINTHEWORLD",
                "YUMIFY COMMUNITY IS THE BEST COMMUNITY IN THE WORLD"
            ],
        ),
        Question(
            "The answer is in this picture. It's not that simple. Work with this image…",
            ["Yumify on BingX soon"],
        ),
        Question(
            "Up to what price can we pump our token?😎"
            "“hint”: 4.67736, -74.09938",
            ["3.5 Ton", "3,5 Ton", "3.5 TON", "3,5 TON"],
        ),
        Question(
            "10. It won't be that easy, don't get too excited. Moreover, one letter is missing."
            "I will say that this is letter number 5. But where it is lost and why I will not say. Good luck!"
            "(Use Caps Lock when writing your answer. And if you get an answer without spaces... do them yourself)"
            ".-- --  -... -- --.  .--. ... --.- .  .... - ... ..  -.- --. . .. .... ..--..",

            ["DO YOU LIKE THIS QUEST?"],
        ),
    ],
    start_message="",
    good_final="Congratulations! You took the {} place and won {}$! We will check your TG stories, and if there is one, we will send you a prize! If it is not published, we will send you 50% of the reward.",
    bad_final="Unfortunately, 25 participants have already solved this quest☹️\nDon’t worry, there are still many cool activities ahead!",
)
