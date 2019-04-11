attempt_allow = 2

class zero_dictionary_error(Exception):
    def __init__(self, message):
        super().__init__(message)
    
class madlibs:
    def __init__(self):
        self.madlibs = []
        self.finish = False
        self.attempt = ""
        self.trial = 0
        self.score = 0
        self.choice = 0
        self.question = ""
        self.answer = ""
        

        
    def choices(self):
        while self.choice != 4:
            self.choice = int(input("""
1. Start Quiz
2. Add Question
3. Edit Question
4. Quit
    """))
            if self.choice == 1:
                if len(self.madlibs) <= 0:
                    raise zero_dictionary_error("There is no question, Please add the question.")
                self.score = 0
                self.ask()                       
            if self.choice == 2:
                self.question_make()
            if self.choice == 3:
                for i in self.madlibs:
                    print("{}. {}".format(self.madlibs.index(i) + 1, i[0]))
                    print("Answer: {}".format(i[1]))
                    print()
                self.question_edit(self.madlibs)
        print("Good Bye!")


    def ask(self):
        for i in self.madlibs:
            print("{}. {}?".format(self.madlibs.index(i) + 1, i[0]))
            self.answer = i[1]
            self.attempt = float(input("The answer: "))
            while self.attempt != self.answer and self.trial < attempt_allow:
                print("You are incorrect!\n")
                self.trial += 1
                self.attempt = float(input("The answer: "))
            if self.trial == 2:
                print("You used all 3 attempts!\n")
            self.trial = 0
            if self.attempt == self.answer:
                print("You are correct!\n")
                self.score += 1
        print("You are done with quizzes.")
        print("Your score is: {}/{}".format(self.score, len(self.madlibs)))
        self.number = 0
        
    def question_make(self):
        self.question = input("Type your Question: ")
        self.answer = float(input("Type your Answer: "))
        print()
        self.madlibs.append([self.question,self.answer])
        self.y_n = input("""Do you want to see your question or answer made?:
Question only (Q)
Answer only (A)
Both (B)
""")
        if self.y_n.upper() == "Q":
            self.display_question()
        if self.y_n.upper() == "A":
            self.display_answer()
        if self.y_n.upper() == "B":
            self.display_both()   
            
    def display_question(self):
        print("Question: {}".format(self.question))
        
    def display_answer(self):
        print("Answer: {}".format(self.answer))
        
    def display_both(self):
        print('''
Question: {}
Answer : {}
'''.format(self.question, self.answer))
        
    def question_edit(self, madlibs):
           
        self.question_number = int(input("Which question do you want to edit?:\n "))
        self.question_content = input("Type your question: ")
        self.new_answer = float(input("Type your answer: "))
        for i in range(1,len(self.madlibs) + 1):
            if self.question_number == i:
                del self.madlibs[i - 1]
                self.madlibs.insert(i - 1, [self.question_content, self.new_answer])
                
                
                
        

                
        

        

                
                
def main():
    a = madlibs()
    print("""
You are welcome to my madlibs.
Please read the question, and type a correct answer.
if you missed 3 times, it will go to next one.
    """)
    try:
        a.choices()
    except zero_dictionary_error as e:
        print(e)
        a.choices()
    
    
if __name__ == "__main__":
    main()
    