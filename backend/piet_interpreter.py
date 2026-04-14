import numpy as np
from PIL import Image
from collections import deque

class Direction:
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3

class CodelChooser:
    LEFT = 0
    RIGHT = 1

# Hex standard piet colors -> (Hue, Lightness)
# Hue: 0=Red, 1=Yellow, 2=Green, 3=Cyan, 4=Blue, 5=Magenta
# Lightness: 0=Light, 1=Normal, 2=Dark
PIET_COLORS_RGB = {
    (255, 192, 192): (0, 0), (255, 255, 192): (1, 0), (192, 255, 192): (2, 0), (192, 255, 255): (3, 0), (192, 192, 255): (4, 0), (255, 192, 255): (5, 0),
    (255, 0, 0): (0, 1),     (255, 255, 0): (1, 1),   (0, 255, 0): (2, 1),     (0, 255, 255): (3, 1),   (0, 0, 255): (4, 1),     (255, 0, 255): (5, 1),
    (192, 0, 0): (0, 2),     (192, 192, 0): (1, 2),   (0, 192, 0): (2, 2),     (0, 192, 192): (3, 2),   (0, 0, 192): (4, 2),     (192, 0, 192): (5, 2)
}
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def match_closest_color(r, g, b):
    color = (r, g, b)
    if color in PIET_COLORS_RGB:
        return color
    if color == WHITE or color == BLACK:
        return color
    
    # Simple Euclidean distance
    min_dist = float('inf')
    best_color = WHITE # default to white instead of failing
    colors = list(PIET_COLORS_RGB.keys()) + [WHITE, BLACK]
    for c in colors:
        dist = (r - c[0])**2 + (g - c[1])**2 + (b - c[2])**2
        if dist < min_dist:
            min_dist = dist
            best_color = c
    
    # If the distance is too high, treat as white
    if min_dist > 5000:
        return WHITE
    return best_color

class PietInterpreter:
    def __init__(self, image: Image.Image, codel_size: int = 1, in_data: str = ""):
        self.raw_image = image
        self.codel_size = codel_size
        self.width = image.width // codel_size
        self.height = image.height // codel_size
        self.in_data = list(in_data)
        
        self.dp = Direction.RIGHT
        self.cc = CodelChooser.LEFT
        self.stack = []
        self.output = []
        self.trace = []
        
        self.grid = self._parse_image()
        self.visited_blocks = {} # Stores block info

    def _parse_image(self):
        # Resize image by jumping codel_size
        img_np = np.array(self.raw_image)
        grid = np.empty((self.height, self.width), dtype=object)
        for y in range(self.height):
            for x in range(self.width):
                py = min(y * self.codel_size, self.raw_image.height - 1)
                px = min(x * self.codel_size, self.raw_image.width - 1)
                r, g, b = img_np[py, px][:3]
                grid[y, x] = match_closest_color(int(r), int(g), int(b))
        return grid

    def _get_block(self, start_x, start_y):
        color = self.grid[start_y, start_x]
        if color == BLACK or color == WHITE:
            return [(start_x, start_y)] # Treat single pixel as block for white/black for search simplicity
            
        if (start_x, start_y) in self.visited_blocks:
            # We already computed the region starting here OR region containing this
            # Actually we need an easy way to get the whole region from any pixel in it
            pass

        # Breadth first search
        queue = deque([(start_x, start_y)])
        visited_local = set([(start_x, start_y)])
        block = []
        
        while queue:
            cx, cy = queue.popleft()
            block.append((cx, cy))
            
            for nx, ny in [(cx+1, cy), (cx-1, cy), (cx, cy+1), (cx, cy-1)]:
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if (nx, ny) not in visited_local and self.grid[ny, nx] == color:
                        visited_local.add((nx, ny))
                        queue.append((nx, ny))
        return block

    def _find_edge(self, block, dp, cc):
        # 1. Find edge furthest in DP
        # 2. Find codel furthest in CC relative to DP
        if dp == Direction.RIGHT:
            max_x = max(b[0] for b in block)
            edge = [b for b in block if b[0] == max_x]
            if cc == CodelChooser.LEFT: return min(edge, key=lambda b: b[1]) # UP
            else: return max(edge, key=lambda b: b[1]) # DOWN
        elif dp == Direction.DOWN:
            max_y = max(b[1] for b in block)
            edge = [b for b in block if b[1] == max_y]
            if cc == CodelChooser.LEFT: return max(edge, key=lambda b: b[0]) # RIGHT
            else: return min(edge, key=lambda b: b[0]) # LEFT
        elif dp == Direction.LEFT:
            min_x = min(b[0] for b in block)
            edge = [b for b in block if b[0] == min_x]
            if cc == CodelChooser.LEFT: return max(edge, key=lambda b: b[1]) # DOWN
            else: return min(edge, key=lambda b: b[1]) # UP
        elif dp == Direction.UP:
            min_y = min(b[1] for b in block)
            edge = [b for b in block if b[1] == min_y]
            if cc == CodelChooser.LEFT: return min(edge, key=lambda b: b[0]) # LEFT
            else: return max(edge, key=lambda b: b[0]) # RIGHT

    def _step_dp(self, x, y, dp):
        if dp == Direction.RIGHT: return x+1, y
        if dp == Direction.DOWN: return x, y+1
        if dp == Direction.LEFT: return x-1, y
        if dp == Direction.UP: return x, y-1

    def _execute_op(self, old_color, new_color, block_size):
        if old_color == WHITE or new_color == WHITE:
            return None
            
        old_h, old_l = PIET_COLORS_RGB[old_color]
        new_h, new_l = PIET_COLORS_RGB[new_color]
        
        dh = (new_h - old_h) % 6
        dl = (new_l - old_l) % 3
        
        op = ""
        st = self.stack
        if dl == 0:
            if dh == 1: # add
                if len(st) >= 2: st.append(st.pop() + st.pop()); op="add"
            elif dh == 2: # divide
                if len(st) >= 2:
                    top, sec = st.pop(), st.pop()
                    if top != 0: st.append(sec // top); op="divide"
                    else: st.append(sec); st.append(top) # ignore
            elif dh == 3: # greater
                if len(st) >= 2:
                    top, sec = st.pop(), st.pop()
                    st.append(1 if sec > top else 0); op="greater"
            elif dh == 4: # duplicate
                if len(st) >= 1: st.append(st[-1]); op="duplicate"
            elif dh == 5: # in(char)
                if self.in_data:
                    c = self.in_data.pop(0)
                    st.append(ord(c)); op="in(char)"
        elif dl == 1:
            if dh == 0: # push
                st.append(block_size); op=f"push {block_size}"
            elif dh == 1: # subtract
                if len(st) >= 2:
                    top, sec = st.pop(), st.pop()
                    st.append(sec - top); op="subtract"
            elif dh == 2: # mod
                if len(st) >= 2:
                    top, sec = st.pop(), st.pop()
                    if top != 0: st.append(sec % top); op="mod"
                    else: st.append(sec); st.append(top)
            elif dh == 3: # pointer
                if len(st) >= 1:
                    val = st.pop()
                    self.dp = (self.dp + val) % 4; op=f"pointer {val}"
            elif dh == 4: # roll
                if len(st) >= 2:
                    rolls, depth = st.pop(), st.pop()
                    if depth > 0 and len(st) >= depth:
                        rolls = rolls % depth
                        if rolls < 0: rolls += depth
                        if rolls > 0:
                            sub = st[-depth:]
                            st[-depth:] = sub[-rolls:] + sub[:-rolls]
                    op="roll"
            elif dh == 5: # out(number)
                if len(st) >= 1:
                    val = st.pop()
                    self.output.append(str(val)); op=f"out(number) {val}"
        elif dl == 2:
            if dh == 0: # pop
                if len(st) >= 1: st.pop(); op="pop"
            elif dh == 1: # multiply
                if len(st) >= 2: st.append(st.pop() * st.pop()); op="multiply"
            elif dh == 2: # not
                if len(st) >= 1:
                    val = st.pop()
                    st.append(1 if val == 0 else 0); op="not"
            elif dh == 3: # switch
                if len(st) >= 1:
                    val = st.pop()
                    self.cc = (self.cc + val) % 2; op=f"switch {val}"
            elif dh == 4: # in(number)
                # Not fully implemented, just dummy
                op="in(number)"
                pass
            elif dh == 5: # out(char)
                if len(st) >= 1:
                    val = st.pop()
                    try:
                        self.output.append(chr(val))
                    except:
                        pass
                    op=f"out(char) {val}"

        return {"dh": dh, "dl": dl, "op": op}

    def execute(self, max_steps=-1):
        x, y = 0, 0
        step_count = 0
        
        while 0 <= x < self.width and 0 <= y < self.height and max_steps != 0:
            color = self.grid[y, x]
            
            if color == BLACK:
                self.trace.append({ "step": step_count, "error": "Start on black block" })
                break
                
            if color == WHITE:
                # Slide across white
                # TBD white block sliding
                nx, ny = self._step_dp(x, y, self.dp)
                
                # Check for bounds and black
                while 0 <= nx < self.width and 0 <= ny < self.height and self.grid[ny, nx] == WHITE:
                    nx, ny = self._step_dp(nx, ny, self.dp)
                
                if not (0 <= nx < self.width and 0 <= ny < self.height) or self.grid[ny, nx] == BLACK:
                    # Toggles CC, steps DP
                    self.cc = (self.cc + 1) % 2
                    self.dp = (self.dp + 1) % 4
                    # Don't step forward just change direction and we'll re-evaluate next loop
                else:
                    x, y = nx, ny
                    # Note: transition from white to a color has NO operation
                continue
                
            block = self._get_block(x, y)
            block_size = len(block)
            
            # Find next block
            edge_x, edge_y = self._find_edge(block, self.dp, self.cc)
            nx, ny = self._step_dp(edge_x, edge_y, self.dp)
            
            attempts = 0
            while attempts < 8:
                if not (0 <= nx < self.width and 0 <= ny < self.height) or self.grid[ny, nx] == BLACK:
                    if attempts % 2 == 0: self.cc = (self.cc + 1) % 2
                    else: self.dp = (self.dp + 1) % 4
                    edge_x, edge_y = self._find_edge(block, self.dp, self.cc)
                    nx, ny = self._step_dp(edge_x, edge_y, self.dp)
                    attempts += 1
                else:
                    break
                    
            if attempts == 8:
                # Terminate
                self.trace.append({ "step": step_count, "block": block, "color": color, "op": "terminate", "stack": list(self.stack) })
                break
            
            next_color = self.grid[ny, nx]
            op_res = self._execute_op(color, next_color, block_size)
            
            self.trace.append({
                "step": step_count,
                "block": block,
                "color": color,
                "next_color": next_color,
                "dp": self.dp,
                "cc": self.cc,
                "op": op_res["op"] if op_res else None,
                "stack": list(self.stack)
            })
            
            x, y = nx, ny
            step_count += 1
            max_steps -= 1
            if step_count > 10000: # safety break
                break
                
        return {
            "output": "".join(self.output),
            "trace": self.trace
        }
