import pygame

class Player:
    def __init__(self, screen_width, screen_height):
        self.width, self.height = 10, 10
        self.xpos = screen_width / 2
        self.ypos = screen_height - self.height - 50
        self.speed = 5
        self.path = []  # Tracks the player's path while pushing
        self.push_enabled = False

    def reset(self, screen_width, screen_height):
        self.xpos = screen_width / 2
        self.ypos = screen_height - self.height - 50
        self.path = []
        self.push_enabled = False

    def toggle_push(self):
        """Toggle the push mode and reset the path if disabled."""
        self.push_enabled = not self.push_enabled
        if self.push_enabled:
            # Add the player's current position to the path when pushing starts
            self.path = [(self.xpos + self.width // 2, self.ypos + self.height // 2)]
        else:
            # Reset the path when pushing is disabled
            self.path = []
    def draw(self, screen):
        """Draw the player on the screen."""
        color = "red" if not self.push_enabled else "green"
        pygame.draw.rect(screen, color, (self.xpos, self.ypos, self.width, self.height))

    def move(self, keys, screen_width, screen_height):
        """Move the player based on the provided movement logic."""
        if self.push_enabled:
            # Prevent diagonal movement by prioritizing one direction
            if keys[pygame.K_LEFT] and not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
                self.xpos -= self.speed
                if self.xpos < 50:
                    self.xpos = 50
                self.path.append((self.xpos + self.width // 2, self.ypos + self.height // 2))  # Track path

            elif keys[pygame.K_RIGHT] and not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
                self.xpos += self.speed
                if self.xpos > screen_width - self.width - 50:
                    self.xpos = screen_width - self.width - 50
                self.path.append((self.xpos + self.width // 2, self.ypos + self.height // 2))  # Track path

            elif keys[pygame.K_UP] and not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
                self.ypos -= self.speed
                if self.ypos < 20:
                    self.ypos = 20
                self.path.append((self.xpos + self.width // 2, self.ypos + self.height // 2))  # Track path

            elif keys[pygame.K_DOWN] and not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
                self.ypos += self.speed
                if self.ypos > screen_height - self.height - 50:
                    self.ypos = screen_height - self.height - 50
                self.path.append((self.xpos + self.width // 2, self.ypos + self.height // 2))  # Track path
        else:
            # Movement along the border
            if keys[pygame.K_LEFT] and self.ypos in [20, screen_height - self.height - 50]:
                self.xpos = max(50, self.xpos - self.speed)
            elif keys[pygame.K_RIGHT] and self.ypos in [20, screen_height - self.height - 50]:
                self.xpos = min(screen_width - self.width - 50, self.xpos + self.speed)
            elif keys[pygame.K_UP] and self.xpos in [50, screen_width - self.width - 50]:
                self.ypos = max(20, self.ypos - self.speed)
            elif keys[pygame.K_DOWN] and self.xpos in [50, screen_width - self.width - 50]:
                self.ypos = min(screen_height - self.height - 50, self.ypos + self.speed)
    def is_on_perimeter(self, screen_width, screen_height):
        """Check if the player is on the perimeter."""
        return (
            (self.ypos == 20 or self.ypos == screen_height - self.height - 50) and
            (50 <= self.xpos <= screen_width - self.width - 50)
        ) or (
            (self.xpos == 50 or self.xpos == screen_width - self.width - 50) and
            (20 <= self.ypos <= screen_height - self.height - 50)
        )