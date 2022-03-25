from similarity import find_most_similar
from corpus import CORPUS

class Bot:

    def __init__(self):
        self.event_stack = []
        self.settings = {
            "min_score": 0.2
        }
        print("Ask a question:")
        while(True):
            self.allow_question()

    def allow_question(self):
        potential_event = None
        if(len(self.event_stack)):
            potential_event = self.event_stack.pop()
        if potential_event:
            text = input("Response: ")
            potential_event.handle_response(text, self)
        else:
            text = input("Question: ")
            answer = self.pre_built_responses_or_none(text)
            if not answer:
                answer = find_most_similar(text)
                self.answer_question(answer, text)

    def answer_question(self, answer, text):
        if answer['score'] > self.settings['min_score']:
            print ("\nBest-fit question: %s (Score: %s)\nAnswer: %s\n" % (answer['question'],answer['score'],answer['answer']))
        else:
            print("Woops! I'm having trouble finding the answer to your question. \nWould you like to see the list of questions that I am able to answer?\n")
            self.event_stack.append(Event("corpus_dump", text))

    def pre_built_responses_or_none(self, text):
        pre_built = [
            {
                "Question": "What is your purpose?",
                "Answer": "I assist user experience by providing an interactive FAQ chat.\n"
            },
            {
                "Question": "Ok",
                "Answer": "Yeah.\n"
            },
            {
                "Question": "Thanks",
                "Answer": "Glad I could help!\n"
            },
            {
                "Question": "Thank you",
                "Answer": "Glad I could help!\n"
            },
            {
                "Question":"Bye",
                "Answer":"Good Bye!\n"
            },
            {
                "Question":"exit",
                "Answer":"Bye\n"
            }
        ]
        for each_question in pre_built:
            if each_question['Question'].lower() in text.lower():
                print(each_question['Answer'])
                if each_question['Question'].lower() in ["thanks", "thank you", "bye", "exit"]:
                    exit()
                return each_question


    def dump_corpus(self):
        question_stack = []
        for each_item in CORPUS:
            question_stack.append(each_item['Question'])
        return question_stack
class Event:

    def __init__(self, kind, text):
        self.kind = kind
        self.CONFIRMATIONS = ["yes", "sure", "okay", "that would be nice", "yep"]
        self.NEGATIONS = ["no", "don't", "dont", "nope"]
        self.original_text = text

    def handle_response(self, text, bot):
        if self.kind == "corpus_dump":
            self.corpus_dump(text, bot)

    def corpus_dump(self, text, bot):
        for each_confirmation in self.CONFIRMATIONS:
            for each_word in text.split(" "):
                if each_confirmation.lower() == each_word.lower():
                    corpus = bot.dump_corpus()
                    corpus = ["-" + s for s in corpus]
                    print("%s%s%s" % ("\n", "\n".join(corpus), "\n"))
                    return 0
        for each_negation in self.NEGATIONS:
            for each_word in text.split(" "):
                if each_negation.lower() == each_word.lower():
                    print ("Feel free to ask another question.")
                    bot.allow_question()
                    return 0
        print("I'm having trouble understanding what you are saying. At the time, my ability is quite limited.")
        return 0
Bot()