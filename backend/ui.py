import pygame
import time

def draw_instructions(screen, menu_selection, current_state):
    """Draw the instructions screen or main menu based on the state."""
    screen.fill("black")  # Black background

    # Fonts
    title_font = pygame.font.Font(None, 64)
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 28)

    if current_state == 0:  # Main menu
        # Title
        title = title_font.render("MQIX", True, (255, 255, 255))  # White text
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 200))

        # Menu options
        menu_options = [
            ("Start", (255, 255, 255)),    # White
            ("Instructions", (255, 255, 255)),  # White
            ("Exit", (255, 255, 255))      # White
        ]

        for i, (option, color) in enumerate(menu_options):
            # Highlight the selected option
            if i == menu_selection:
                color = (255, 255, 0)  # Yellow for selected

            text = font.render(option, True, color)
            text_rect = text.get_rect(center=(screen.get_width() // 2, 300 + i * 50))
            screen.blit(text, text_rect)

    elif current_state == 3:  # Instructions detail screen
        # Title
        title = title_font.render("How to Play", True, (255, 255, 255))
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 50))

        # Instructions content
        instructions = [
            "Objective: Cover at least 20% of the screen",
            "",
            "Controls:",
            "- Arrow Keys: Move around the border or when not pushing",
            "- Spacebar: Start/Stop pushing to draw lines",
            "- ESC: Pause Game",
            "",
            "Gameplay:",
            "- Move along the border to start pushing",
            "- Create territories by drawing closed paths",
            "- Avoid Sparx (orange circles) and Qix (purple circle)",
            "- Don't get caught while pushing!",
            "",
            "Enemies:",
            "- Sparx: Patrol the border",
            "- Qix: Moves freely inside the play area",
            "",
            "Tips:",
            "- Be strategic in your territory claims",
            "- Watch out for enemy movements",
            "",
            "Press ESC to Return to Menu"
        ]

        # Render instructions content
        start_y = 150  # Fixed starting y-coordinate
        for i, line in enumerate(instructions):
            color = (255, 255, 255)  # White text
            if line.endswith(":"):  # Highlight section headers
                color = (255, 255, 0)  # Yellow for headers

            text = small_font.render(line, True, color)
            screen.blit(text, (50, start_y + i * 30))


def draw_pause_menu(screen, pause_menu_selection):
    """Draw the pause menu screen."""
    screen.fill("black")  # Black background

    # Fonts
    title_font = pygame.font.Font(None, 64)
    font = pygame.font.Font(None, 36)

    # Pause Title
    pause_title = title_font.render("PAUSED", True, (255, 255, 255))
    screen.blit(pause_title, (screen.get_width() // 2 - pause_title.get_width() // 2, 200))

    # Pause menu options
    pause_options = [
        ("Resume", (255, 255, 255)),    # White
        ("Main Menu", (255, 255, 255)), # White
        ("Exit Game", (255, 255, 255))  # White
    ]

    for i, (option, color) in enumerate(pause_options):
        # Highlight the selected option
        if i == pause_menu_selection:
            color = (255, 255, 0)  # Yellow for selected

        text = font.render(option, True, color)
        text_rect = text.get_rect(center=(screen.get_width() // 2, 300 + i * 50))
        screen.blit(text, text_rect)


def draw_game_over(screen, percentage):
    """Draw the game over screen."""
    screen.fill("white")  # White background

    # Fonts
    title_font = pygame.font.Font(None, 64)
    font = pygame.font.Font(None, 36)

    # Game Over Title
    game_over_text = title_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(game_over_text, (screen.get_width() // 2 - game_over_text.get_width() // 2, 200))

    # Percentage covered
    covered_text = font.render(f"Territory Covered: {percentage:.2f}%", True, (0, 0, 0))
    screen.blit(covered_text, (screen.get_width() // 2 - covered_text.get_width() // 2, 250))

    # Instructions
    restart_text = font.render("Press ENTER to Restart", True, (0, 0, 0))
    quit_text = font.render("Press ESC to Quit", True, (0, 0, 0))
    screen.blit(restart_text, (screen.get_width() // 2 - restart_text.get_width() // 2, 300))
    screen.blit(quit_text, (screen.get_width() // 2 - quit_text.get_width() // 2, 350))