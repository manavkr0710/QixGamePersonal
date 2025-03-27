import pygame
import time
from player import Player
from enemies import Sparx, Qix
from ui import draw_instructions, draw_pause_menu, draw_game_over
from utils import calculate_polygon_area, line_intersects_circle

class Game:
    def __init__(self):
        pygame.init()
        self.screen_width, self.screen_height = 700, 700
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
        pygame.display.set_caption("Qix Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.invulnerable = False  # Player starts as vulnerable
        self.invulnerability_start_time = 0  # Track when invulnerability starts
        self.INVULNERABILITY_DURATION = 2  # Duration of invulnerability in seconds
        

        # Game states
        self.GAME_STATES = {
            'INSTRUCTIONS': 0,
            'INSTRUCTIONS_DETAIL': 3,
            'PLAY': 1,
            'END_GAME': 2,
            'PAUSE': 4
        }
        self.current_state = self.GAME_STATES['INSTRUCTIONS']
        self.menu_selection = 0
        self.pause_menu_selection = 0

        # Initialize game objects
        self.player = Player(self.screen_width, self.screen_height)
        self.sparx = [Sparx(50, 20)]
        self.qix = Qix(self.screen_width / 2, self.screen_height / 2)
        self.filled_areas = []
        self.level_passed = False
        self.level_pass_time = 0
        self.LEVEL_PASS_DURATION = 2

        # Board and movement variables
        self.push_enabled = False
        self.perimeter_path = [
            (50, 20), (self.screen_width - 50, 20),
            (self.screen_width - 50, self.screen_height - 50),
            (50, self.screen_height - 50)
        ]
        self.player_path = []

        # Hearts (lives)
        self.lives = 3  # Player starts with 3 lives

        # Initialize fonts
        self.title_font = pygame.font.Font(None, 64)
        self.font = pygame.font.Font(None, 36)
    def reset_game(self):
        """Reset all game variables to initial state."""
        self.player.reset(self.screen_width, self.screen_height)
        self.sparx = [Sparx(50, 20)]
        self.qix.reset(self.screen_width / 2, self.screen_height / 2)
        self.filled_areas = []
        self.level_passed = False
        self.level_pass_time = 0
        self.push_enabled = False
        self.player_path = []
        self.lives = 3  # Reset lives to 3
        self.current_state = self.GAME_STATES['PLAY']

    def run(self):
        """Main game loop."""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # Handle state-specific events
                if self.current_state == self.GAME_STATES['INSTRUCTIONS']:
                    self.handle_instructions_events(event)
                elif self.current_state == self.GAME_STATES['INSTRUCTIONS_DETAIL']:
                    self.handle_instructions_detail_events(event)
                elif self.current_state == self.GAME_STATES['PAUSE']:
                    self.handle_pause_events(event)
                elif self.current_state == self.GAME_STATES['PLAY']:
                    self.handle_play_events(event)
                elif self.current_state == self.GAME_STATES['END_GAME']:
                    self.handle_end_game_events(event)

            # Render the current state
            self.render()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def render(self):
        """Render the current game state."""
        if self.current_state == self.GAME_STATES['INSTRUCTIONS']:
            draw_instructions(self.screen, self.menu_selection, self.current_state)
        elif self.current_state == self.GAME_STATES['INSTRUCTIONS_DETAIL']:
            draw_instructions(self.screen, self.menu_selection, self.current_state)
        elif self.current_state == self.GAME_STATES['PAUSE']:
            draw_pause_menu(self.screen, self.pause_menu_selection)
        elif self.current_state == self.GAME_STATES['PLAY']:
            self.render_play()
        elif self.current_state == self.GAME_STATES['END_GAME']:
            draw_game_over(self.screen, self.calculate_territory_percentage())

    def render_play(self):
        """Render the play state."""
        self.screen.fill("white")

        # Draw claimed territories
        for area in self.filled_areas:
            pygame.draw.polygon(self.screen, (173, 216, 230), area)  # Light blue

        # Draw border
        pygame.draw.rect(self.screen, "black", (50, 20, self.screen_width - 100, self.screen_height - 70), 10)

        # Draw current path
        if self.player.push_enabled and len(self.player.path) > 1:
            pygame.draw.lines(self.screen, "green", False, self.player.path, 3)

        # Draw player with blinking effect during invulnerability
        if self.invulnerable:
            # Alternate between red and gray to create a blinking effect
            color = "gray" if int(time.time() * 10) % 2 == 0 else "red"
        else:
            color = "red"
        pygame.draw.rect(self.screen, color, (self.player.xpos, self.player.ypos, self.player.width, self.player.height))

        # Handle player movement
        keys = pygame.key.get_pressed()
        self.player.move(keys, self.screen_width, self.screen_height)

        # Move and draw Sparx
        for sparx in self.sparx:
            target_x, target_y = self.perimeter_path[sparx.path_index]
            if (sparx.x, sparx.y) == (target_x, target_y):
                sparx.path_index = (sparx.path_index + 1) % len(self.perimeter_path)

            if sparx.x < target_x:
                sparx.x += 5
            elif sparx.x > target_x:
                sparx.x -= 5
            if sparx.y < target_y:
                sparx.y += 5
            elif sparx.y > target_y:
                sparx.y -= 5

            sparx.draw(self.screen)

        # Move and draw Qix
        self.qix.x += self.qix.dx
        self.qix.y += self.qix.dy
        if self.qix.x <= 50 or self.qix.x >= self.screen_width - 50:
            self.qix.dx = -self.qix.dx
        if self.qix.y <= 20 or self.qix.y >= self.screen_height - 50:
            self.qix.dy = -self.qix.dy
        self.qix.draw(self.screen)

        # Check Sparx collision
        if self.check_sparx_collision():
            if self.lives <= 0:
                self.current_state = self.GAME_STATES['END_GAME']  # End the game if no lives are left

        # Draw UI Panel
        panel_width = 200
        panel_height = 150
        panel_x = self.screen_width - panel_width - 20
        panel_y = 20

        # Create a semi-transparent background for the panel
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        pygame.draw.rect(panel_surface, (200, 200, 200, 180), panel_surface.get_rect(), border_radius=10)
        self.screen.blit(panel_surface, (panel_x, panel_y))

        # Draw lives
        lives_text = self.font.render(f"Lives:", True, (0, 0, 0))
        lives_value = self.title_font.render(str(self.lives), True, (255, 0, 0))
        self.screen.blit(lives_text, (panel_x + 20, panel_y + 20))
        self.screen.blit(lives_value, (panel_x + 120, panel_y + 20))

        # Draw territory percentage
        percentage = self.calculate_territory_percentage()
        territory_text = self.font.render("Territory:", True, (0, 0, 0))
        territory_value = self.font.render(f"{percentage:.2f}%", True, (0, 128, 0))
        self.screen.blit(territory_text, (panel_x + 20, panel_y + 70))
        self.screen.blit(territory_value, (panel_x + 120, panel_y + 70))
        
    def calculate_territory_percentage(self):
        """Calculate the percentage of territory covered."""
        total_area = (self.screen_width - 100) * (self.screen_height - 90)
        covered_area = sum(calculate_polygon_area(area) for area in self.filled_areas if len(area) >= 3)
        return (covered_area / total_area) * 100 if total_area > 0 else 0
   

    def handle_instructions_events(self, event):
        """Handle events for the instructions menu."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.menu_selection = (self.menu_selection - 1) % 3
            elif event.key == pygame.K_DOWN:
                self.menu_selection = (self.menu_selection + 1) % 3
            elif event.key == pygame.K_RETURN:
                if self.menu_selection == 0:  # Start
                    self.reset_game()
                elif self.menu_selection == 1:  # Instructions
                    self.current_state = self.GAME_STATES['INSTRUCTIONS_DETAIL']
                elif self.menu_selection == 2:  # Exit
                    self.running = False

    def handle_instructions_detail_events(self, event):
        """Handle events for the detailed instructions screen."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.current_state = self.GAME_STATES['INSTRUCTIONS']

    def handle_pause_events(self, event):
        """Handle events for the pause menu."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.pause_menu_selection = (self.pause_menu_selection - 1) % 3
            elif event.key == pygame.K_DOWN:
                self.pause_menu_selection = (self.pause_menu_selection + 1) % 3
            elif event.key == pygame.K_RETURN:
                if self.pause_menu_selection == 0:  # Resume
                    self.current_state = self.GAME_STATES['PLAY']
                elif self.pause_menu_selection == 1:  # Main Menu
                    self.current_state = self.GAME_STATES['INSTRUCTIONS']
                elif self.pause_menu_selection == 2:  # Exit Game
                    self.running = False
            elif event.key == pygame.K_ESCAPE:
                self.current_state = self.GAME_STATES['PLAY']

    def handle_play_events(self, event):
        """Handle events for the play state."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.current_state = self.GAME_STATES['PAUSE']
                self.pause_menu_selection = 0
            elif event.key == pygame.K_SPACE:
                if self.player.push_enabled and len(self.player.path) >= 3:
                    self.filled_areas.append(self.player.path[:])  # Save the path as a polygon
                self.player.toggle_push()  # Toggle push mode
    def check_sparx_collision(self):
        """Check if the player collides with Sparx or if Sparx interferes with the pushed line."""
        if self.invulnerable:
            # Check if invulnerability duration has expired
            if time.time() - self.invulnerability_start_time > self.INVULNERABILITY_DURATION:
                self.invulnerable = False  # End invulnerability
            return False  # No collision during invulnerability

        # Check if Sparx collides with the player
        player_rect = pygame.Rect(self.player.xpos, self.player.ypos, self.player.width, self.player.height)
        for sparx in self.sparx:
            sparx_rect = pygame.Rect(sparx.x - 7, sparx.y - 7, 14, 14)  # Sparx is a circle with radius 7
            if player_rect.colliderect(sparx_rect):
                self.lives -= 1  # Lose a life
                self.player.reset(self.screen_width, self.screen_height)  # Reset player position
                self.invulnerable = True  # Enable invulnerability
                self.invulnerability_start_time = time.time()  # Record the start time
                return True

            # Check if Sparx interferes with the pushed line
            if len(self.player.path) >= 2:  # Ensure there are at least two points in the path
                for i in range(len(self.player.path) - 1):
                    line_start = self.player.path[i]
                    line_end = self.player.path[i + 1]
                    if line_intersects_circle(line_start, line_end, (sparx.x, sparx.y), 7):
                        self.lives -= 1  # Lose a life
                        self.player.reset(self.screen_width, self.screen_height)  # Reset player position
                        self.invulnerable = True  # Enable invulnerability
                        self.invulnerability_start_time = time.time()  # Record the start time
                        return True

        return False

    def handle_end_game_events(self, event):
        """Handle events for the game over screen."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.reset_game()
            elif event.key == pygame.K_ESCAPE:
                self.running = False