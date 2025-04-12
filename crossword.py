import streamlit as st
import random
import time

class ImpossibleCrossword:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.grid_size = self.set_grid_size()
        self.words, self.hints = self.generate_words_and_hints()
        self.grid = self.create_grid()
        self.correct_answers = self.get_correct_answers()

    def set_grid_size(self):
        return {"easy": 5, "medium": 7, "hard": 10}.get(self.difficulty, 5)

    def generate_words_and_hints(self):
        word_bank = {
            "easy": [("CODE", "What programmers write"), ("BUG", "An error in a program"),
                     ("DATA", "Information stored in computers"), ("AI", "Artificial ___"), ("LOOP", "Repeating structure")],
            "medium": [("PYTHON", "A popular programming language"), ("SCRIPT", "Automated command sequence"),
                       ("LOGIC", "Foundation of computing"), ("OBJECT", "Instance in OOP"), ("STACK", "LIFO data structure")],
            "hard": [("RECURSION", "Function calling itself"), ("NEURAL", "Type of AI network"),
                     ("MACHINE", "Learning in AI"), ("ENCRYPTION", "Data protection method"), ("OPTIMIZATION", "Improving efficiency")]
        }
        words = random.sample(word_bank[self.difficulty], 5)
        return [w[0] for w in words], [w[1] for w in words]

    def create_grid(self):
        return [[" " for _ in range(self.grid_size)] for _ in range(self.grid_size)]

    def get_correct_answers(self):
        answers = {}
        x, y = 0, 0
        for idx, word in enumerate(self.words):
            for letter in word:
                if y >= self.grid_size:
                    x += 1
                    y = 0
                if x >= self.grid_size:
                    break
                answers[(x, y)] = letter
                y += 1
            x += 1
        return answers

    def scramble_grid(self):
        # Scramble the grid by shuffling the letters
        letters = list(self.correct_answers.values())
        random.shuffle(letters)
        scrambled = {key: letters[i] for i, key in enumerate(self.correct_answers.keys())}
        return scrambled

# Streamlit App
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

st.title("🧩 Impossible AI Crossword Generator 🤖")

difficulty = st.selectbox("Select Difficulty", ["easy", "medium", "hard"], index=0)
crossword = ImpossibleCrossword(difficulty)

st.write("### 📝 Clues:")
for i, hint in enumerate(crossword.hints):
    st.write(f"**Word {i+1}:** {hint}")

# Scramble the grid
scrambled_answers = crossword.scramble_grid()

# Display crossword grid
st.write("### 🔤 Fill the Crossword:")

user_answers = {}
for i in range(crossword.grid_size):
    cols = st.columns(crossword.grid_size)
    for j in range(crossword.grid_size):
        key = f"{i}-{j}"
        user_answers[(i, j)] = cols[j].text_input("", value="", max_chars=1, key=key)

# Button to check answers
if st.button("Submit"):
    st.session_state.attempts += 1
    end_time = time.time()
    time_taken = round(end_time - st.session_state.start_time, 2)

    # AI Trickery: Always low accuracy
    accuracy = round(random.uniform(0, 15), 2)  # Random low accuracy
    st.write(f"🎯 Accuracy: **{accuracy}%**")
    st.write(f"🕒 Time taken: **{time_taken} seconds**")

    # AI Feedback: Always encourage trying again
    if accuracy < 10:
        st.error("❌ Try again! The AI is too smart for you!")
    elif accuracy < 50:
        st.warning("⚠️ Almost there! (Just kidding, try again 😆)")
    else:
        st.success("✅ You solved it! (Nope, the AI shuffled it again 😈)")

    # Restart game with a new scrambled puzzle
    st.session_state.start_time = time.time()
    st.rerun()