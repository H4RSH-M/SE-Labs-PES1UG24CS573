import pygame
import random

TILE = 40
COLS, ROWS = 20, 15
WALL, FLOOR, CHEST, KEY, TRAP = 0, 1, 2, 3, 4
SPEED = 3
GUARD_SPEED = 2


def has_path(grid, start, target):
    if start is None or target is None:
        return False

    start_r, start_c = start[1], start[0]
    target_r, target_c = target[1], target[0]

    queue = [(start_r, start_c)]
    visited = {(start_r, start_c)}

    while queue:
        r, c = queue.pop(0)

        if (r, c) == (target_r, target_c):
            return True

        for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
            nr = r + dr
            nc = c + dc

            if not (0 <= nr < ROWS and 0 <= nc < COLS):
                continue

            if (nr, nc) in visited:
                continue

            # Only FLOOR, KEY and CHEST are considered safe
            # paths. TRAP tiles are deliberately excluded.
            if grid[nr][nc] not in (FLOOR, KEY, CHEST):
                continue

            visited.add((nr, nc))
            queue.append((nr, nc))

    return False


def generate_world():
    grid = [[WALL]*COLS for _ in range(ROWS)]
    rooms = []

    for _ in range(8):
        w = random.randint(3,6)
        h = random.randint(3,5)
        x = random.randint(1, COLS-w-1)
        y = random.randint(1, ROWS-h-1)
        room = pygame.Rect(x, y, w, h)
        overlap = any(room.inflate(2,2).colliderect(r) for r in rooms)

        if not overlap:
            rooms.append(room)
            for ry in range(y, y+h):
                for rx in range(x, x+w):
                    grid[ry][rx] = FLOOR

    for i in range(len(rooms)-1):
        ax, ay = rooms[i].centerx, rooms[i].centery
        bx, by = rooms[i+1].centerx, rooms[i+1].centery

        cx = ax
        while cx != bx:
            grid[ay][cx] = FLOOR
            cx += 1 if bx > cx else -1

        cy = ay
        while cy != by:
            grid[cy][bx] = FLOOR
            cy += 1 if by > cy else -1

    chest_pos = None
    key_pos = None

    if len(rooms) >= 2:
        cr, ck = rooms[-1], rooms[-2]

        chest_pos = (cr.centerx, cr.centery)
        key_pos = (ck.centerx, ck.centery)

        grid[cr.centery][cr.centerx] = CHEST
        grid[ck.centery][ck.centerx] = KEY

    start = rooms[0] if rooms else None

    # Add traps to random floor tiles.
    # A trap is only placed if a trap-free route still exists
    # from the starting area to the key and from the key to
    # the chest.
    trap_count = 8
    floor_tiles = []

    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] == FLOOR:
                # Don't place traps in the starting room.
                if start is not None and start.collidepoint(c, r):
                    continue

                floor_tiles.append((r, c))

    random.shuffle(floor_tiles)

    if start is not None and key_pos is not None and chest_pos is not None:
        start_pos = (start.centerx, start.centery)

        traps_added = 0

        for r, c in floor_tiles:
            if traps_added >= trap_count:
                break

            # Temporarily place the trap.
            grid[r][c] = TRAP

            # Check that both important routes still have
            # at least one safe path.
            start_to_key = has_path(
                grid,
                start_pos,
                key_pos
            )

            key_to_chest = has_path(
                grid,
                key_pos,
                chest_pos
            )

            if start_to_key and key_to_chest:
                traps_added += 1
            else:
                # This trap would make an important objective
                # inaccessible, so restore the floor.
                grid[r][c] = FLOOR

    return grid, start


COLORS = {
    WALL: (60,50,70),
    FLOOR: (200,190,170),
    CHEST: (200,160,30),
    KEY: (220,220,60),
    TRAP: (180,50,50),
}


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 28, 28)
        self.color = (60,120,220)
        self.has_key = False

    def move(self, keys, grid, rows, cols):
        dx=dy=0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx=-SPEED

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx=SPEED

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy=-SPEED

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy=SPEED

        self._try_move(dx,0,grid,rows,cols)
        self._try_move(0,dy,grid,rows,cols)

    def _try_move(self, dx, dy, grid, rows, cols):
        new = self.rect.move(dx,dy)

        for px,py in [
            (new.left,new.top),
            (new.right-1,new.top),
            (new.left,new.bottom-1),
            (new.right-1,new.bottom-1)
        ]:
            c,r=px//TILE,py//TILE

            if not(0<=r<rows and 0<=c<cols) or grid[r][c]==WALL:
                return

        self.rect=new

    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, self.rect)

        if self.has_key:
            pygame.draw.circle(
                screen,
                (220,220,60),
                (self.rect.right-6, self.rect.top+6),
                5
            )


class Guard:
    def __init__(self, x1, y1, x2, y2):
        self.rect = pygame.Rect(x1, y1, 28, 28)

        self.start_x = x1
        self.start_y = y1
        self.end_x = x2
        self.end_y = y2

        self.x = x1
        self.y = y1

        self.direction = 1
        self.speed = GUARD_SPEED
        self.color = (190,60,60)

    def update(self):
        if self.direction == 1:
            target_x = self.end_x
            target_y = self.end_y
        else:
            target_x = self.start_x
            target_y = self.start_y

        dx = target_x - self.x
        dy = target_y - self.y

        # Reach the endpoint exactly, then reverse.
        if abs(dx) + abs(dy) <= self.speed:
            self.x = target_x
            self.y = target_y
            self.direction *= -1
        else:
            if dx != 0:
                self.x += self.speed if dx > 0 else -self.speed
            elif dy != 0:
                self.y += self.speed if dy > 0 else -self.speed

        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            self.color,
            self.rect,
            border_radius=5
        )

        pygame.draw.circle(
            screen,
            (240,220,180),
            (self.rect.centerx-6, self.rect.centery-4),
            4
        )

        pygame.draw.circle(
            screen,
            (240,220,180),
            (self.rect.centerx+6, self.rect.centery-4),
            4
        )


WIDTH = COLS * TILE
HEIGHT = ROWS * TILE + 50
FPS = 60


class GameEngine:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Treasure Hunt")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 24)
        self.inventory_font = pygame.font.SysFont("monospace", 18)
        self.big_font = pygame.font.SysFont(
            "monospace",
            40,
            bold=True
        )

        self.reset()

    def reset(self):
        self.grid, start = generate_world()

        if start:
            sx = start.x * TILE + 6
            sy = start.y * TILE + 6
        else:
            sx, sy = TILE+6, TILE+6

        self.start_x = sx
        self.start_y = sy

        # Keep the starting room available for guard placement checks.
        self.start_room = start

        self.player = Player(sx, sy)
        self.guard = self.create_guard()

        self.won = False
        self.status = "Find the KEY, then the CHEST!"

    def create_guard(self):
        # Find the chest.
        chest_pos = None

        for r in range(ROWS):
            for c in range(COLS):
                if self.grid[r][c] == CHEST:
                    chest_pos = (c, r)
                    break

            if chest_pos is not None:
                break

        # If there is no chest, use the first valid FLOOR pair.
        if chest_pos is None:
            return self.find_fallback_guard()

        cx, cy = chest_pos

        start_col = self.start_x // TILE
        start_row = self.start_y // TILE

        horizontal_candidates = []
        vertical_candidates = []

        # Search nearby rows for short horizontal FLOOR patrols.
        for r in range(max(0, cy-3), min(ROWS, cy+4)):
            for c in range(max(0, cx-4), min(COLS-1, cx+5)):
                for length in (3, 2):
                    end_c = c + length - 1

                    if end_c >= COLS:
                        continue

                    valid = True

                    for pc in range(c, end_c+1):
                        if self.grid[r][pc] != FLOOR:
                            valid = False
                            break

                    if not valid:
                        continue

                    in_start_room = (
                        self.start_room is not None
                        and self.start_room.collidepoint(c, r)
                    )

                    near_start = (
                        abs(c - start_col) <= 1
                        and abs(r - start_row) <= 1
                    )

                    distance_to_chest = abs(c - cx) + abs(r - cy)

                    score = distance_to_chest

                    if in_start_room:
                        score += 100

                    if near_start:
                        score += 100

                    horizontal_candidates.append(
                        (score, c, r, end_c)
                    )

        # Prefer a short horizontal patrol.
        if horizontal_candidates:
            horizontal_candidates.sort(
                key=lambda item: item[0]
            )

            _, c1, r1, c2 = horizontal_candidates[0]

            x1 = c1 * TILE + 6
            y1 = r1 * TILE + 6

            x2 = c2 * TILE + 6
            y2 = r1 * TILE + 6

            return Guard(x1, y1, x2, y2)

        # No suitable horizontal patrol.
        # Search for a short vertical FLOOR patrol.
        for c in range(max(0, cx-3), min(COLS, cx+4)):
            for r in range(max(0, cy-4), min(ROWS-1, cy+5)):
                for length in (3, 2):
                    end_r = r + length - 1

                    if end_r >= ROWS:
                        continue

                    valid = True

                    for pr in range(r, end_r+1):
                        if self.grid[pr][c] != FLOOR:
                            valid = False
                            break

                    if not valid:
                        continue

                    in_start_room = (
                        self.start_room is not None
                        and self.start_room.collidepoint(c, r)
                    )

                    near_start = (
                        abs(c - start_col) <= 1
                        and abs(r - start_row) <= 1
                    )

                    distance_to_chest = abs(c - cx) + abs(r - cy)

                    score = distance_to_chest

                    if in_start_room:
                        score += 100

                    if near_start:
                        score += 100

                    vertical_candidates.append(
                        (score, c, r, end_r)
                    )

        if vertical_candidates:
            vertical_candidates.sort(
                key=lambda item: item[0]
            )

            _, c1, r1, r2 = vertical_candidates[0]

            x1 = c1 * TILE + 6
            y1 = r1 * TILE + 6

            x2 = c1 * TILE + 6
            y2 = r2 * TILE + 6

            return Guard(x1, y1, x2, y2)

        return self.find_fallback_guard()

    def find_fallback_guard(self):
        floor_pairs = []

        for r in range(ROWS):
            for c in range(COLS):
                if self.grid[r][c] != FLOOR:
                    continue

                if c + 1 < COLS and self.grid[r][c+1] == FLOOR:
                    floor_pairs.append(
                        ((c, r), (c+1, r))
                    )

                if r + 1 < ROWS and self.grid[r+1][c] == FLOOR:
                    floor_pairs.append(
                        ((c, r), (c, r+1))
                    )

        if floor_pairs:
            start_col = self.start_x // TILE
            start_row = self.start_y // TILE

            # Prefer a fallback away from the player's start.
            for p1, p2 in floor_pairs:
                if (
                    abs(p1[0] - start_col) > 1
                    or abs(p1[1] - start_row) > 1
                ):
                    x1 = p1[0] * TILE + 6
                    y1 = p1[1] * TILE + 6

                    x2 = p2[0] * TILE + 6
                    y2 = p2[1] * TILE + 6

                    return Guard(x1, y1, x2, y2)

            p1, p2 = floor_pairs[0]

            x1 = p1[0] * TILE + 6
            y1 = p1[1] * TILE + 6

            x2 = p2[0] * TILE + 6
            y2 = p2[1] * TILE + 6

            return Guard(x1, y1, x2, y2)

        return Guard(
            TILE+6,
            TILE+6,
            TILE+6+TILE,
            TILE+6
        )

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset()

        return True

    def update(self):
        if self.won:
            return

        # Guard moves automatically.
        self.guard.update()

        keys = pygame.key.get_pressed()

        self.player.move(
            keys,
            self.grid,
            ROWS,
            COLS
        )

        # Guard collision only resets the player.
        # The dungeon and key state remain unchanged.
        if self.player.rect.colliderect(self.guard.rect):
            self.player.rect.topleft = (
                self.start_x,
                self.start_y
            )
            self.status = "Guard caught you! Back to the start!"
            return

        pr = self.player.rect.centery // TILE
        pc = self.player.rect.centerx // TILE

        if 0<=pr<ROWS and 0<=pc<COLS:
            cell = self.grid[pr][pc]

            # Existing Task 1 trap behaviour.
            if cell == TRAP:
                self.player.rect.topleft = (
                    self.start_x,
                    self.start_y
                )
                self.status = "Trap triggered! Back to the start!"

            # Existing key behaviour.
            elif cell == KEY:
                self.player.has_key = True
                self.grid[pr][pc] = FLOOR
                self.status = "Got the key! Find the CHEST!"

            # Existing chest behaviour.
            elif cell == CHEST and self.player.has_key:
                self.won = True
                self.status = "Treasure found!"

    def draw_minimap(self):
        map_tile = 8
        map_width = COLS * map_tile
        map_height = ROWS * map_tile

        margin = 10
        map_x = WIDTH - map_width - margin
        map_y = margin

        border = pygame.Rect(
            map_x - 4,
            map_y - 4,
            map_width + 8,
            map_height + 8
        )

        pygame.draw.rect(
            self.screen,
            (15,15,25),
            border
        )

        for r in range(ROWS):
            for c in range(COLS):
                if self.grid[r][c] == WALL:
                    color = (45,40,55)
                else:
                    color = (180,170,150)

                rect = pygame.Rect(
                    map_x + c * map_tile,
                    map_y + r * map_tile,
                    map_tile,
                    map_tile
                )

                pygame.draw.rect(
                    self.screen,
                    color,
                    rect
                )

        player_col = self.player.rect.centerx // TILE
        player_row = self.player.rect.centery // TILE

        if 0 <= player_col < COLS and 0 <= player_row < ROWS:
            player_rect = pygame.Rect(
                map_x + player_col * map_tile + 1,
                map_y + player_row * map_tile + 1,
                map_tile - 2,
                map_tile - 2
            )

            pygame.draw.rect(
                self.screen,
                (50,140,255),
                player_rect
            )

    def draw_inventory(self):
        # Inventory panel is part of the existing HUD.
        inventory_rect = pygame.Rect(
            WIDTH - 260,
            ROWS*TILE + 5,
            250,
            40
        )

        pygame.draw.rect(
            self.screen,
            (35,35,50),
            inventory_rect,
            border_radius=5
        )

        pygame.draw.rect(
            self.screen,
            (90,90,110),
            inventory_rect,
            1,
            border_radius=5
        )

        if self.player.has_key:
            text = "Inventory: [KEY]"
        else:
            text = "Inventory: [EMPTY]"

        inventory_text = self.inventory_font.render(
            text,
            True,
            (230,230,230)
        )

        self.screen.blit(
            inventory_text,
            (
                inventory_rect.x + 10,
                inventory_rect.y + 10
            )
        )

    def draw(self):
        self.screen.fill((30,25,40))

        for r in range(ROWS):
            for c in range(COLS):
                cell = self.grid[r][c]

                rect = pygame.Rect(
                    c*TILE,
                    r*TILE,
                    TILE,
                    TILE
                )

                pygame.draw.rect(
                    self.screen,
                    COLORS[cell],
                    rect
                )

                if cell == KEY:
                    pygame.draw.circle(
                        self.screen,
                        (255,240,60),
                        (
                            c*TILE+TILE//2,
                            r*TILE+TILE//2
                        ),
                        10
                    )

                elif cell == CHEST:
                    pygame.draw.rect(
                        self.screen,
                        (180,120,20),
                        rect.inflate(-12,-12),
                        border_radius=4
                    )

        self.guard.draw(self.screen)
        self.player.draw(self.screen)

        # Task 3 mini-map.
        self.draw_minimap()

        hud = pygame.Rect(
            0,
            ROWS*TILE,
            WIDTH,
            50
        )

        pygame.draw.rect(
            self.screen,
            (20,20,35),
            hud
        )

        st = self.font.render(
            self.status + "  |  R=Restart",
            True,
            (200,200,200)
        )

        self.screen.blit(
            st,
            (8,ROWS*TILE+13)
        )

        # Task 4 inventory.
        self.draw_inventory()

        if self.won:
            ov=pygame.Surface(
                (WIDTH,ROWS*TILE),
                pygame.SRCALPHA
            )

            ov.fill((0,0,0,140))
            self.screen.blit(ov,(0,0))

            msg=self.big_font.render(
                "TREASURE FOUND!",
                True,
                (220,180,30)
            )

            sub=self.font.render(
                "Press R to Play Again",
                True,
                (180,180,180)
            )

            self.screen.blit(
                msg,
                (
                    WIDTH//2-msg.get_width()//2,
                    ROWS*TILE//2-30
                )
            )

            self.screen.blit(
                sub,
                (
                    WIDTH//2-sub.get_width()//2,
                    ROWS*TILE//2+20
                )
            )

        pygame.display.flip()

    def run(self):
        running=True

        while running:
            running=self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()


if __name__ == "__main__":
    engine = GameEngine()
    engine.run()