# 🎮 Word Detective 🎮

**Word Detective** is an interactive and engaging word-guessing game. Built with Python, HTML, and CSS, it offers an immersive experience for word enthusiasts. Whether you want to test your vocabulary, add new words to the database, or explore existing ones, Word Detective has it all with a sleek and responsive interface. 

---

## 🚀 Features

- 🎮 **Word Guessing Game**: Solve word puzzles based on unique hints.
- 📝 **Add New Words**: Expand the database with custom words and descriptions.
- 📋 **Preview Data**: View and manage the word database effortlessly.
- 🌙 **Dark Mode Support**: Switch between light and dark themes for a comfortable experience.
- 💡 **Interactive UI**: Fully responsive design for seamless usage across devices.

---

## 🛠️ Technologies Used

This project leverages modern technologies to deliver a smooth and efficient experience:

- **HTML**: For building the structure of the user interface.
- **CSS**: To style and ensure responsiveness.
- **Python**: Handles backend logic and data management.

---

## 🖥️ Installation

Get started with Word Detective in just a few steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/hrosicka/WordDetective.git
   ```
   
2. Navigate to the project directory:
   ```bash
   cd WordDetective
   ```
   
3. Run the application:
   ```bash
   python app.py
   ```
   
4. Open your browser and navigate to:
   ```Code
   http://localhost:5000
   ```
---

## 🎮 How to Play
### 🔍 Start the Game
- Launch the game and start guessing words based on the provided hints.
  
### ✍️ Add New Words
- Head over to the "Add New Word" section to contribute to the word database.

### 📖 Preview Data
- Explore and manage the database from the "Preview Data" section.

### 🌗 Toggle Dark Mode
- Use the toggle button to switch between light and dark themes.

---

## 🧪 Testing
Word Detective includes automated tests to ensure robustness and reliability. The tests are implemented using **unittest** and **Selenium**.
  


---

## Project structure
```Code
GameWebWordHunt/
│
├── routes/
│   ├── game_logic.py
│   ├── game.py
│   ├── player.py
│   ├── score.py
│   └── word.py
│ 
├── static/
│   └── style.css  # Main stylesheet
│
├── templates/
│   ├── index.html     # Main game interface
│   ├── add_word.html  # Add new words page
│   ├── change_name.html
│   ├── error.html
│   ├── leaderboard.html
│   └── preview.html   # Data preview page
│ 
├── app.py             # Main application logic
└── README.md          # Project documentation
```
