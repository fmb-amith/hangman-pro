import pygame
import random
import sys
from pygame import mixer

# Initialize Pygame and mixer (for sound)
pygame.init()
mixer.init()

# ===== CONSTANTS =====
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_LARGE = pygame.font.SysFont("Arial", 48)
FONT_SMALL = pygame.font.SysFont("Arial", 32)

# ===== LOAD ASSETS =====
def load_assets():
    assets = {
        # Hangman images (0-6 stages)
        "hangman_stages": [pygame.image.load(f"assets/images/stage_{i}.png") for i in range(7)],
        # Sound effects
        "click_sound": mixer.Sound("assets/sounds/click.wav"),
        "win_sound": mixer.Sound("assets/sounds/win.wav"),
        "lose_sound": mixer.Sound("assets/sounds/lose.wav"),
    }
    return assets

# ===== LOAD WORDS =====
def load_words(filename="words.txt"):
    with open(filename, "r") as file:
        return [word.strip().upper() for word in file.readlines()]

# ===== GAME CLASS =====
class HangmanGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Hangman Pro")
        self.assets = load_assets()
        self.words = load_words()
        self.reset_game()

    def reset_game(self):
        self.secret_word = random.choice(self.words)
        self.guessed_letters = set()
        self.attempts_left = 6
        self.game_state = "playing"  # "playing", "won", "lost"

    def draw(self):
        self.screen.fill(WHITE)

        # Draw hangman stage (0-6)
        stage = 6 - self.attempts_left
        self.screen.blit(self.assets["hangman_stages"][stage], (50, 100))

        # Draw word progress (e.g., _ _ A _ B)
        word_display = " ".join([letter if letter in self.guessed_letters else "_" for letter in self.secret_word])
        word_text = FONT_LARGE.render(word_display, True, BLACK)
        self.screen.blit(word_text, (300, 200))

        # Draw guessed letters
        guessed_text = FONT_SMALL.render(f"Guessed: {' '.join(sorted(self.guessed_letters))}", True, BLACK)
        self.screen.blit(guessed_text, (300, 300))

        # Draw attempts left
        attempts_text = FONT_SMALL.render(f"Attempts left: {self.attempts_left}", True, BLACK)
        self.screen.blit(attempts_text, (300, 350))

        # Draw game result
        if self.game_state == "won":
            result_text = FONT_LARGE.render("YOU WON!", True, (0, 200, 0))
            self.screen.blit(result_text, (300, 400))
            mixer.Sound.play(self.assets["win_sound"])
        elif self.game_state == "lost":
            result_text = FONT_LARGE.render(f"WORD: {self.secret_word}", True, (200, 0, 0))
            self.screen.blit(result_text, (300, 400))
            mixer.Sound.play(self.assets["lose_sound"])

        # Draw restart prompt
        if self.game_state != "playing":
            restart_text = FONT_SMALL.render("Press R to restart", True, BLACK)
            self.screen.blit(restart_text, (300, 450))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if self.game_state == "playing" and event.unicode.isalpha():
                    letter = event.unicode.upper()
                    if letter not in self.guessed_letters:
                        self.guessed_letters.add(letter)
                        if letter not in self.secret_word:
                            self.attempts_left -= 1
                            mixer.Sound.play(self.assets["click_sound"])

                # Restart game
                if event.key == pygame.K_r and self.game_state != "playing":
                    self.reset_game()

    def update(self):
        if set(self.secret_word).issubset(self.guessed_letters):
            self.game_state = "won"
        elif self.attempts_left <= 0:
            self.game_state = "lost"

    def run(self):
        clock = pygame.time.Clock()
        while True:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            clock.tick(60)

# ===== RUN GAME =====
if __name__ == "__main__":
    game = HangmanGame()
    game.run()
