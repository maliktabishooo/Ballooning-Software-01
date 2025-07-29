import cv2
import numpy as np
from dataclasses import dataclass
from config import Config

@dataclass
class Balloon:
    id: int
    position: tuple  # (x, y)
    dimension: dict
    radius: int = Config.BALLOON_RADIUS

class BalloonEngine:
    def __init__(self, img_width, img_height):
        self.balloons = []
        self.next_id = 1
        self.img_width = img_width
        self.img_height = img_height
        self.occupied_map = np.zeros((img_height, img_width), dtype=bool)
    
    def place_balloon(self, dimension):
        """Intelligent balloon placement with collision avoidance"""
        # Initial position near dimension text
        x, y, w, h = dimension['coords']
        candidate_pos = (x + w + Config.BALLOON_RADIUS + 10, y + h//2)
        
        # Adjust position to avoid collisions
        final_pos = self.find_optimal_position(candidate_pos, dimension)
        
        # Create balloon
        balloon = Balloon(id=self.next_id, position=final_pos, dimension=dimension)
        self.balloons.append(balloon)
        self.next_id += 1
        
        # Mark area as occupied
        self.mark_occupied_area(final_pos)
        
        return balloon
    
    def find_optimal_position(self, start_pos, dimension):
        """Find optimal position avoiding collisions"""
        x, y = start_pos
        directions = [
            (1, 0),   # Right
            (0, 1),   # Down
            (-1, 0),  # Left
            (0, -1),  # Up
            (1, 1),   # Down-right
            (1, -1),  # Up-right
            (-1, 1),  # Down-left
            (-1, -1)  # Up-left
        ]
        
        # Try initial position
        if self.is_position_available(start_pos):
            return start_pos
        
        # Spiral search for available position
        step = Config.BALLOON_RADIUS * 2
        max_steps = 10
        
        for distance in range(1, max_steps + 1):
            for dx, dy in directions:
                candidate = (
                    x + dx * distance * step,
                    y + dy * distance * step
                )
                
                # Check bounds
                if not (0 <= candidate[0] < self.img_width and 
                        0 <= candidate[1] < self.img_height):
                    continue
                
                if self.is_position_available(candidate):
                    return candidate
        
        # Fallback to initial position if no space found
        return start_pos
    
    def is_position_available(self, position):
        """Check if position is available"""
        x, y = position
        r = Config.BALLOON_RADIUS + Config.BALLOON_PADDING
        
        # Check boundaries
        if (x - r < 0 or x + r >= self.img_width or
            y - r < 0 or y + r >= self.img_height):
            return False
        
        # Check occupied map
        y_start = max(0, int(y - r))
        y_end = min(self.img_height, int(y + r))
        x_start = max(0, int(x - r))
        x_end = min(self.img_width, int(x + r))
        
        return not np.any(self.occupied_map[y_start:y_end, x_start:x_end])
    
    def mark_occupied_area(self, position):
        """Mark area around balloon as occupied"""
        x, y = position
        r = Config.BALLOON_RADIUS + Config.BALLOON_PADDING
        
        y_start = max(0, int(y - r))
        y_end = min(self.img_height, int(y + r))
        x_start = max(0, int(x - r))
        x_end = min(self.img_width, int(x + r))
        
        self.occupied_map[y_start:y_end, x_start:x_end] = True
    
    def draw_balloons(self, img):
        """Draw balloons on image"""
        img_with_balloons = img.copy()
        
        for balloon in self.balloons:
            # Draw balloon circle
            cv2.circle(
                img_with_balloons, 
                balloon.position, 
                balloon.radius, 
                (0, 0, 255),  # Red color
                2  # Thickness
            )
            
            # Draw balloon ID
            text_size = cv2.getTextSize(
                str(balloon.id), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.8,  # Font scale
                2     # Thickness
            )[0]
            
            text_x = balloon.position[0] - text_size[0] // 2
            text_y = balloon.position[1] + text_size[1] // 2
            
            cv2.putText(
                img_with_balloons,
                str(balloon.id),
                (text_x, text_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2
            )
            
            # Draw line from balloon to dimension text
            text_x, text_y, w, h = balloon.dimension['coords']
            text_center = (text_x + w // 2, text_y + h // 2)
            
            cv2.line(
                img_with_balloons,
                balloon.position,
                text_center,
                (0, 255, 0),  # Green color
                1
            )
        
        return img_with_balloons
