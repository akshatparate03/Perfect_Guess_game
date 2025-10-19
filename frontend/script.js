let gamesPlayed = 0;
let bestScore = null;
const BACKEND_URL = "http://127.0.0.1:5000"; // Backend URL

const guessInput = document.getElementById("guessInput");
const guessBtn = document.getElementById("guessBtn");
const newGameBtn = document.getElementById("newGameBtn");
const message = document.getElementById("message");
const attempts = document.getElementById("attempts");
const celebration = document.getElementById("celebration");
const container = document.querySelector(".container");

// Load stats from localStorage
if (localStorage.getItem("gamesPlayed")) {
  gamesPlayed = parseInt(localStorage.getItem("gamesPlayed"));
  document.getElementById("gamesPlayed").textContent = gamesPlayed;
}
if (localStorage.getItem("bestScore")) {
  bestScore = parseInt(localStorage.getItem("bestScore"));
  document.getElementById("bestScore").textContent = bestScore;
}

newGameBtn.addEventListener("click", startNewGame);
guessBtn.addEventListener("click", submitGuess);
guessInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") submitGuess();
});

async function startNewGame() {
  try {
    const response = await fetch(`${BACKEND_URL}/start`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include", // Important for session cookies
    });
    const data = await response.json();

    message.textContent = data.message;
    attempts.textContent = "0";
    guessInput.value = "";
    guessInput.disabled = false;
    guessBtn.disabled = false;
    guessInput.focus();

    container.classList.add("pulse");
    setTimeout(() => container.classList.remove("pulse"), 500);
  } catch (error) {
    message.textContent = "Error starting game. Please try again!";
  }
}

async function submitGuess() {
  const guess = guessInput.value;

  if (!guess) {
    message.textContent = "Please enter a number!";
    container.classList.add("shake");
    setTimeout(() => container.classList.remove("shake"), 500);
    return;
  }

  try {
    const response = await fetch(`${BACKEND_URL}/guess`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include", // Important for session cookies
      body: JSON.stringify({ guess: parseInt(guess) }),
    });
    const data = await response.json();

    message.textContent = data.message;

    if (data.guesses) {
      attempts.textContent = data.guesses;
    }

    if (data.status === "correct") {
      guessInput.disabled = true;
      guessBtn.disabled = true;
      celebration.classList.add("active");
      setTimeout(() => celebration.classList.remove("active"), 1000);

      // Update stats
      gamesPlayed++;
      if (bestScore === null || data.guesses < bestScore) {
        bestScore = data.guesses;
        document.getElementById("bestScore").textContent = bestScore;
        localStorage.setItem("bestScore", bestScore);
      }
      document.getElementById("gamesPlayed").textContent = gamesPlayed;
      localStorage.setItem("gamesPlayed", gamesPlayed);
    } else if (
      data.status === "higher" ||
      data.status === "lower" ||
      data.status === "invalid"
    ) {
      container.classList.add("shake");
      setTimeout(() => container.classList.remove("shake"), 500);
    }

    guessInput.value = "";
    guessInput.focus();
  } catch (error) {
    message.textContent = "Error submitting guess. Please try again!";
  }
}
