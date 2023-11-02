import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

class Gridworld:
    def __init__(self, state_types, rewards, q_table,
                 slip=None, gamma=1, step_reward=-0.01):
        self.state_types = state_types
        self.rewards = rewards
        self.q_table = q_table
        self.slip = {
            'left': 0,
            'right': 0,
            'backward': 0,
            'forward': 1
        }
        self.gamma = gamma
        self.step_reward = step_reward

        if slip is not None:
            self.slip = slip
            forward_prob = 1 - self.slip['left'] - self.slip['right'] - self.slip['backward']
            self.slip['forward'] = forward_prob

    def render(self, policy=False):
        '''Render the gridworld with the current q-values'''
        step_size = 150

        # Initialize image
        height = self.state_types.shape[0] * step_size + 1
        width = self.state_types.shape[1] * step_size + 1
        image = Image.new(mode='RGBA', size=(width, height), color=(255, 255, 255))

        # Draw elements
        draw = ImageDraw.Draw(image)
        font_large = ImageFont.truetype("./FreeMono.ttf", step_size/3)
        font_mid = ImageFont.truetype("./FreeMono.ttf", step_size/7)
        font_small = ImageFont.truetype("./FreeMono.ttf", step_size/8)
        y_end, x_end = self.state_types.shape
        color_pos = (12, 107, 55)
        color_neg = (235, 68, 44)

        # Offsets for shapes and text
        rectangle_offset = step_size / 12
        text_offsets = {
            0: (step_size / 2, step_size / 5),
            1: (4 * step_size / 5, step_size / 2),
            2: (step_size / 2, 4 * step_size / 5),
            3: (step_size / 5, step_size / 2),
        }
        center = step_size / 2
        triangle_offsets = {
            0: [0, 0, step_size, 0, center, center],
            1: [step_size, 0, step_size, step_size, center, center],
            2: [0, step_size, step_size, step_size, center, center],
            3: [0, 0, 0, step_size, center, center]
        }
        arrow_offsets = {0: [center, step_size / 12,
                            center - step_size / 10, step_size / 4, 
                            center + step_size / 10, step_size / 4],
                        1: [11 * step_size / 12, center,
                            3 * step_size / 4, center - step_size / 10,
                            3 * step_size / 4, center + step_size / 10],
                        2: [center, 11 * step_size / 12,
                            center - step_size / 10, 3 * step_size / 4,
                            center + step_size / 10 , 3 * step_size / 4],
                        3: [step_size / 12, center,
                            step_size / 4, center - step_size / 10,
                            step_size / 4, center + step_size / 10]
                        }
        

        for x in range(x_end):
            for y in range(y_end):
                # Anchor position
                x_pos = x * step_size
                y_pos = y * step_size
                state_type = self.state_types[y, x]

                # Draw triangles/arrows and action values
                if state_type == 0:
                    if policy:
                        value = np.max(self.q_table[y, x])
                        best_actions = np.where(self.q_table[y, x] == value)[0]

                        if value >= 0:
                            fill = color_pos + (int(255 * value),)
                        else:
                            fill = color_neg + (int(-255 * value),)

                        rectangle = [(x_pos, y_pos), (x_pos + step_size, y_pos + step_size)]
                        draw.rectangle(rectangle, outline='black', fill=fill)

                        for action in best_actions:
                            xy = [x_pos, y_pos] * 3
                            arrow = [a + b for a, b in zip(xy, arrow_offsets[action])]
                            draw.polygon(arrow, fill='white', outline='black')
                        
                        text_xy = (x_pos + center, y_pos + center)
                        text = f'{value:.2f}'
                        draw.text(text_xy, text, anchor='mm', font=font_mid, fill='black')
                    else:
                        for action in range(4):
                            value = self.q_table[y, x, action]
                            xy = [x_pos, y_pos] * 3
                            triangle = [a + b for a, b in zip(xy, triangle_offsets[action])]
                            if value >= 0:
                                fill = color_pos + (int(255 * value),)
                            else:
                                fill = color_neg + (int(-255 * value),)
                            draw.polygon(triangle, fill=fill, outline='black')

                            text_offset_x, text_offset_y = text_offsets[action]
                            text_xy = (x_pos + text_offset_x, y_pos + text_offset_y)
                            text = f'{value:.2f}'
                            draw.text(text_xy, text, anchor='mm', font=font_small, fill='black')

                # Draw rectangle and reward
                elif state_type == 1:
                    reward = self.rewards[y, x]
                    if reward >= 0:
                        fill = color_pos + (int(255 * reward),)
                    else:
                        fill = color_neg + (int(-255 * reward),)

                    rectangle_outer = [(x_pos, y_pos), (x_pos + step_size, y_pos + step_size)]
                    draw.rectangle(rectangle_outer, outline='black', fill=fill)

                    rectangle_inner = [(x_pos + rectangle_offset, y_pos + rectangle_offset),
                    (x_pos + step_size - rectangle_offset, y_pos + step_size - rectangle_offset)]
                    draw.rectangle(rectangle_inner, outline='black', fill=fill)

                    text_xy = (x_pos + center, y_pos + center)
                    text = f'{reward:.2g}'
                    draw.text(text_xy, text, anchor='mm', fill='black', font=font_large)

                # Draw empty rectangle
                else:
                    rectangle = [(x_pos, y_pos), (x_pos + step_size, y_pos + step_size)]
                    draw.rectangle(rectangle, outline='black', fill='lightgrey')

        del draw
        
        return image
    
    def solve(self, theta=1e-18):
        '''Use value iteration to find optimal policy and q-table'''
        delta = theta
        i_max = self.state_types.shape[0]
        j_max = self.state_types.shape[1]

        direction_translate = {
            'left': -1,
            'right': 1,
            'backward': 2,
            'forward': 0
        }
        direction_to_offset = {
            0: (-1, 0),
            1: (0, 1),
            2: (1, 0),
            3: (0, -1),
        }

        delta = theta
        while delta >= theta:
            delta = 0

            for i in range(i_max):
                for j in range(j_max):
                    if self.state_types[i, j] == 0:
                        for a in range(4):
                            q_old = self.q_table[i, j, a]
                            action_value = 0

                            for slip_dir, prob in self.slip.items():
                                if prob != 0:
                                    actual_direction = (a + direction_translate[slip_dir]) % 4
                                    i_off, j_off = direction_to_offset[actual_direction]
                                    next_i = min(max(0, i + i_off), i_max - 1)
                                    next_j = min(max(0, j + j_off), j_max - 1)
                                    next_state = next_i, next_j

                                    if self.state_types[next_state] == 2:
                                        next_state = i, j

                                    reward = self.rewards[next_state]
                                    if reward == 0:
                                        reward = self.step_reward
                                    
                                    next_state_value = np.max(self.q_table[next_state])
                                    action_value += prob * (reward + self.gamma * next_state_value)

                            self.q_table[i, j, a] = action_value
                            delta = max(delta, abs(q_old - action_value))