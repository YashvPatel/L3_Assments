from tkinter import *
from functools import partial
import csv
import random


class QuizApp:

    def __init__(self):
        self.root = root
        self.root.title("Animal Youth Quiz")

        # Format for all buttons
        button_font = ("Arial", "14", "bold")
        button_fg = "#FFFFFF"

        # Set up GUI Frame
        self.intro_frame = Frame(root, padx=10, pady=10)
        self.intro_frame.grid()

        self.intro_heading_label = Label(self.intro_frame, text="Animal Quiz",
                                         font=("Arial", "16", "bold"))
        self.intro_heading_label.grid(row=0)

        choose_instructions_txt = "Please enter the number of questions you want to answer (1-100), then press 'Start Quiz' to begin."
        self.choose_instructions_label = Label(self.intro_frame,
                                               text=choose_instructions_txt,
                                               wraplength=300, justify="left")
        self.choose_instructions_label.grid(row=1)

        self.quiz_entry = Entry(self.intro_frame, font=("Arial", "14"))
        self.quiz_entry.grid(row=2, padx=10, pady=10)

        # Error message label, initially hidden
        self.error_label = Label(self.intro_frame, text="", fg="#9C0000")
        self.error_label.grid(row=3)

        # Submit button
        self.button_frame = Frame(self.intro_frame)
        self.button_frame.grid(row=4)

        self.submit_button = Button(self.button_frame,
                                    text="Start Quiz",
                                    bg="#990099",
                                    fg=button_fg,
                                    font=button_font, width=20,
                                    command=self.to_submit)
        self.submit_button.grid(row=0, column=0)

    def check_quiz(self):
        error = "Enter an integer between 1 and 100"

        try:
            response = self.quiz_entry.get()
            response = int(response)

            if response < 1 or response > 100:
                self.error_label.config(text=error)
            else:
                return response

        except ValueError:
            self.error_label.config(text=error)

    def to_submit(self):
        num_rounds = self.check_quiz()

        if num_rounds is None:
            return

        Quiz(num_rounds)

        # Hide root window
        root.withdraw()


class Quiz:

    def __init__(self, how_many):
        self.quiz_box = Toplevel()
        self.quiz_box.protocol('WM_DELETE_WINDOW', partial(self.close_quiz))

        # Variables for statistics
        self.rounds_wanted = IntVar()
        self.rounds_wanted.set(how_many)

        self.rounds_played = IntVar()
        self.rounds_played.set(0)

        self.rounds_won = IntVar()
        self.rounds_won.set(0)

        self.user_scores = []

        # Get all animals for use in game
        self.all_animals = self.get_all_animals()

        # Set up GUI Frame
        self.quiz_frame = Frame(self.quiz_box, padx=10, pady=10)
        self.quiz_frame.grid()

        self.intro_heading_label = Label(self.quiz_frame, text=f"Question 1 of {how_many}",
                                         font=("Arial", "16", "bold"))
        self.intro_heading_label.grid(row=0)

        # Get animals for buttons for the first round
        self.choice_frame = Frame(self.quiz_frame, padx=10, pady=10)
        self.choice_frame.grid(row=2)

        # Fetch animals for the round
        self.button_animals_list = self.get_round_animals()
        self.correct_youth = self.button_animals_list[0][1]  # Correct answer (youth form)
        adult_animal = self.button_animals_list[0][0]  # Adult animal for the question

        # Update the animal label
        self.animal_label = Label(self.quiz_frame, text=f"What's the animal youth of?",
                                  font=("Arial", "14"))
        self.animal_label.grid(row=1)

        # Creating buttons
        for item in range(0, 4):
            self.choice_button = Button(self.choice_frame,
                                        text=self.button_animals_list[item][1],  # Displaying youth name
                                        width=15,
                                        command=lambda i=item: self.to_compare(self.button_animals_list[i][1]))
            self.choice_button.grid(row=item // 2, column=item % 2, padx=5, pady=5)

        # Frame for round results and next button
        self.rounds_frame = Frame(self.quiz_frame)
        self.rounds_frame.grid(row=4, pady=5)

        self.round_results_label = Label(self.rounds_frame, text="",
                                         width=24, bg="#FFF2CC",
                                         font=("Arial", 10),
                                         pady=5)
        self.round_results_label.grid(row=0, column=0, padx=5)

        self.next_button = Button(self.rounds_frame, text="Next Round",
                                  fg="#FFFFFF", bg="#008BFC",
                                  font=("Arial", 11, "bold"),
                                  width=10, state=DISABLED,
                                  command=self.new_round)
        self.next_button.grid(row=0, column=1)

        # at start, get 'new round'
        self.new_round()

        self.control_frame = Frame(self.quiz_frame)
        self.control_frame.grid(row=6)

        control_buttons = [
            ["#CC6600", "Help", "get help"],
            ["#808080", "Start Over", "start over"]
        ]

        for item in range(0, 2):
            self.make_control_button = Button(self.control_frame,
                                              fg="#FFFFFF",
                                              bg=control_buttons[item][0],
                                              text=control_buttons[item][1],
                                              width=11, font=("Arial", "12", "bold"),
                                              command=lambda i=item: self.to_do(control_buttons[i][2]))
            self.make_control_button.grid(row=0, column=item, padx=5, pady=5)

        self.to_help_btn = self.make_control_button  # This might be used for help

    def get_all_animals(self):
        with open("animals_young_collective.csv", "r") as file:
            var_all_animals = list(csv.reader(file, delimiter=","))
        var_all_animals.pop(0)  # Remove header row
        return var_all_animals

    def get_round_animals(self):
        round_animal_list = []
        used_animals = set()  # To track used adult animals

        while len(round_animal_list) < 4:
            chosen_animal = random.choice(self.all_animals)
            adult_name = chosen_animal[0]
            youth_name = chosen_animal[1]

            # Ensure we don't repeat the same adult animal
            if adult_name not in used_animals:
                used_animals.add(adult_name)
                round_animal_list.append(chosen_animal)

        # Shuffle the list to randomize the order of answers
        random.shuffle(round_animal_list)
        return round_animal_list

    # sets up new round when 'next' button was pressed
    def new_round(self):

        # disable next button (enable it at the end
        # of the round)
        self.next_button.config(state=DISABLED)

        # empty button list so we can get new colours
        self.button_animals_list.clear()

        # get new colours for buttons
        self.button_animals_list = self.get_round_animals()

        # retrieve number of rounds wanted / played
        how_many = self.rounds_wanted.get()
        current_round = self.rounds_played.get()
        new_heading = "Choose - Round {} of " \
                      "{}".format(current_round + 1, how_many)
        self.intro_heading_label.config(text=new_heading)

        self.choice_button_ref = []
        for item in range(4):
            self.choice_button = Button(self.choice_frame,
                                        text=self.button_animals_list[item][1],  # Displaying youth name
                                        width=15,
                                        command=lambda i=item: self.to_compare(self.button_animals_list[i][1]))
            self.choice_button.grid(row=item // 2, column=item % 2, padx=5, pady=5)
            self.choice_button_ref.append(self.choice_button)

        # Select a random question for the new round.
        current_question = random.choice(self.all_animals)
        # Remove the selected question from the data.
        self.all_animals.remove(current_question)

        # Set the question details.
        self.adult_name = current_question[0]
        self.correct_answer = current_question[1]

        # Update the UI with the new question.
        self.animal_label.config(text=f"Animal youth of? {self.adult_name}")
        self.intro_heading_label.config(text=f"Round {self.rounds_played.get() + 1} of {self.rounds_wanted.get()}")

    # updates win or lost
    def to_compare(self, user_score):
        if user_score == self.correct_youth:
            self.round_results_label.config(text="Correct!", bg="#C6EFCE")
            self.rounds_won.set(self.rounds_won.get() + 1)
        else:
            self.round_results_label.config(text=f"Wrong! correct answer: {self.correct_youth}", bg="#FFC7CE")

        self.rounds_played.set(self.rounds_played.get() + 1)
        self.next_button.config(state=NORMAL)

    def to_do(self, action):
        if action == "get help":
            DisplayHelp(self)
        elif action == "start over":
            self.quiz_box.destroy()  # Close the current quiz
            root.deiconify()  # Show the main app window again

    def close_quiz(self):
        root.deiconify()
        self.quiz_box.destroy()


# Show users help / game tips
class DisplayHelp:
    def __init__(self, partner):
        # setup dialogue box and background colour
        background = "#ECB464"
        self.help_box = Toplevel()

        # disable help button
        partner.to_help_btn.config(state=DISABLED)

        # If users press cross at top, closes help and
        # 'releases' help button
        self.help_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_help, partner))

        self.help_frame = Frame(self.help_box, width=300,
                                height=200,
                                bg=background)
        self.help_frame.grid()

        self.help_heading_label = Label(self.help_frame,
                                        bg=background,
                                        text="Help Information",
                                        font=("Arial", "14", "bold"))
        self.help_heading_label.grid(row=0)

        help_text = "Your objective is to input the amount of rounds " \
                    "you wish to play and answer through 4 choices " \
                    "correctly. Try your best even if you get them " \
                    "incorrectly as it's about struggling, not succeeding.\n\n" \
                    "There's a [start over] button to restart " \
                    "for any inconvenience you may face along " \
                    "the way.  \n\n" \
                    "Good luck, have fun! and Choose carefully."
        self.help_text_label = Label(self.help_frame, bg=background,
                                     text=help_text, wraplength=350,
                                     justify="left")
        self.help_text_label.grid(row=1, padx=10)

        self.dismiss_button = Button(self.help_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#B45840",
                                     fg="#FFFFFF",
                                     command=partial(self.close_help,
                                                     partner))
        self.dismiss_button.grid(row=2, padx=10, pady=10)

    # closes help dialogue (used by button and x at top of dialogue)
    def close_help(self, partner):
        # Put help button back to normal...
        partner.to_help_btn.config(state=NORMAL)
        self.help_box.destroy()


# Main routine
if __name__ == "__main__":
    root = Tk()
    app = QuizApp()
    root.mainloop()
