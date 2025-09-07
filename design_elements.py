import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle
import numpy as np

COLOR_SCHEMES = {
    'professional': {
        'primary': '#2E4057',
        'secondary': '#048A81', 
        'accent': '#54C6EB',
        'bg': '#F8F9FA',
        'text': '#2C3E50',
        'light': '#E8F4F8'
    },
    'modern': {
        'primary': '#667eea',
        'secondary': '#764ba2',
        'accent': '#f093fb',
        'bg': '#ffecd2',
        'text': '#4a4a4a',
        'light': '#f8f1ff'
    },
    'tech': {
        'primary': '#0f0f23',
        'secondary': '#262640',
        'accent': '#7c3aed',
        'bg': '#f1f5f9',
        'text': '#1e293b',
        'light': '#e2e8f0'
    },
    'creative': {
        'primary': '#ff6b6b',
        'secondary': '#4ecdc4',
        'accent': '#45b7d1',
        'bg': '#fef7f7',
        'text': '#2d3748',
        'light': '#fef2f2'
    }
}

def create_gradient_background(ax, colors, direction='vertical'):
    if direction == 'vertical':
        gradient = np.linspace(0, 1, 256).reshape(256, -1)
    elif direction == 'horizontal':
        gradient = np.linspace(0, 1, 256).reshape(-1, 256)
    else:
        gradient = np.outer(np.linspace(0, 1, 256), np.linspace(0, 1, 256))
    ax.imshow(gradient, aspect='auto', cmap=plt.cm.colors.LinearSegmentedColormap.from_list('', colors),
              extent=[0, 10, 0, 10], alpha=0.3)

def draw_icon_computer(ax, x, y, size=0.8, color='#4ECDC4'):
    monitor = Rectangle((x-size/2, y-size/4), size, size/2, facecolor=color, edgecolor='white', linewidth=2)
    ax.add_patch(monitor)
    screen = Rectangle((x-size/2+0.1, y-size/4+0.1), size-0.2, size/2-0.3, facecolor='white', edgecolor=color, linewidth=1)
    ax.add_patch(screen)
    stand = Rectangle((x-0.1, y-size/2), 0.2, size/4, facecolor=color, edgecolor='white', linewidth=1)
    ax.add_patch(stand)
    base = Rectangle((x-size/3, y-size/2), size*2/3, 0.1, facecolor=color, edgecolor='white', linewidth=1)
    ax.add_patch(base)

def draw_icon_brain(ax, x, y, size=0.8, color='#FF6B6B'):
    brain = Circle((x, y), size/2, facecolor=color, edgecolor='white', linewidth=2, alpha=0.8)
    ax.add_patch(brain)
    for i in range(3):
        detail = Circle((x + (i-1)*0.15, y + 0.1), 0.08, facecolor='white', edgecolor=color, linewidth=1, alpha=0.7)
        ax.add_patch(detail)

def draw_icon_rocket(ax, x, y, size=0.8, color='#45B7D1'):
    rocket_body = FancyBboxPatch((x-size/6, y-size/2), size/3, size, boxstyle="round,pad=0.02", facecolor=color, edgecolor='white', linewidth=2)
    ax.add_patch(rocket_body)
    tip_x = [x-size/6, x, x+size/6]
    tip_y = [y+size/2, y+size/2+size/3, y+size/2]
    ax.plot(tip_x, tip_y, color='white', linewidth=3)
    ax.fill(tip_x, tip_y, color=color, alpha=0.8)
    flame_x = [x-size/8, x, x+size/8, x]
    flame_y = [y-size/2, y-size/2-size/4, y-size/2, y-size/2]
    ax.fill(flame_x, flame_y, color='#FFA500', alpha=0.8)

def draw_icon_chart(ax, x, y, size=0.8, color='#96CEB4'):
    chart_bg = Rectangle((x-size/2, y-size/2), size, size, facecolor='white', edgecolor=color, linewidth=2)
    ax.add_patch(chart_bg)
    bar_heights = [0.2, 0.5, 0.3, 0.7]
    bar_width = size/6
    for i, height in enumerate(bar_heights):
        bar_x = x - size/2 + 0.1 + i * bar_width * 1.2
        bar = Rectangle((bar_x, y-size/2+0.1), bar_width, height*size*0.6, facecolor=color, alpha=0.8)
        ax.add_patch(bar)

def draw_icon_gear(ax, x, y, size=0.8, color='#DDA0DD'):
    gear = Circle((x, y), size/3, facecolor=color, edgecolor='white', linewidth=2)
    ax.add_patch(gear)
    angles = np.linspace(0, 2*np.pi, 8, endpoint=False)
    for angle in angles:
        tooth_x = x + (size/3 + 0.1) * np.cos(angle)
        tooth_y = y + (size/3 + 0.1) * np.sin(angle)
        tooth = Circle((tooth_x, tooth_y), 0.05, facecolor=color, edgecolor='white', linewidth=1)
        ax.add_patch(tooth)
    center = Circle((x, y), size/8, facecolor='white', edgecolor=color, linewidth=2)
    ax.add_patch(center)

def draw_icon_lightbulb(ax, x, y, size=0.8, color='#FFEAA7'):
    bulb = Circle((x, y+size/6), size/3, facecolor=color, edgecolor='white', linewidth=2, alpha=0.9)
    ax.add_patch(bulb)
    base = Rectangle((x-size/6, y-size/3), size/3, size/4, facecolor='#E17055', edgecolor='white', linewidth=2)
    ax.add_patch(base)
    ray_length = size/4
    for angle in [45, 90, 135, 225, 270, 315]:
        angle_rad = np.radians(angle)
        start_x = x + (size/3 + 0.05) * np.cos(angle_rad)
        start_y = y + size/6 + (size/3 + 0.05) * np.sin(angle_rad)
        end_x = start_x + ray_length * np.cos(angle_rad)
        end_y = start_y + ray_length * np.sin(angle_rad)
        ax.plot([start_x, end_x], [start_y, end_y], color=color, linewidth=3, alpha=0.7)

def add_decorative_elements(ax, theme='professional'):
    colors = COLOR_SCHEMES[theme]
    corner1 = Circle((0.5, 9.5), 0.3, facecolor=colors['accent'], alpha=0.3)
    corner2 = Circle((9.5, 0.5), 0.25, facecolor=colors['secondary'], alpha=0.3)
    ax.add_patch(corner1)
    ax.add_patch(corner2)
    side_rect = Rectangle((0, 4), 0.1, 2, facecolor=colors['primary'], alpha=0.8)
    ax.add_patch(side_rect)

def create_title_banner(ax, title, theme='professional', y_pos=8.5):
    colors = COLOR_SCHEMES[theme]
    title_bg = FancyBboxPatch((0.5, y_pos-0.4), 9, 0.8, boxstyle="round,pad=0.1", facecolor=colors['primary'], edgecolor=colors['accent'], linewidth=2, alpha=0.9)
    ax.add_patch(title_bg)
    ax.text(5, y_pos, title, fontsize=24, fontweight='bold', color='white', ha='center', va='center',
            bbox=dict(boxstyle="round,pad=0.3", facecolor='none', edgecolor='none'))

ICON_FUNCTIONS = {
    'computer': draw_icon_computer,
    'brain': draw_icon_brain,
    'rocket': draw_icon_rocket,
    'chart': draw_icon_chart,
    'gear': draw_icon_gear,
    'lightbulb': draw_icon_lightbulb
  }
