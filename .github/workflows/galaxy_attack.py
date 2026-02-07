#!/usr/bin/env python3
"""
Galaxy Arcade Attack - Auto-playing SVG Game Animation
Generates an infinite-loop animated SVG for GitHub README
"""

import random
import math
from datetime import datetime

# Game Configuration
WIDTH = 800
HEIGHT = 600
SHIP_Y = HEIGHT - 80
NUM_ENEMIES = 8
NUM_STARS = 50
ANIMATION_DURATION = 20  # seconds for full loop

def generate_stars():
    """Generate background stars"""
    stars = []
    for i in range(NUM_STARS):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        size = random.uniform(1, 3)
        duration = random.uniform(1, 3)
        delay = random.uniform(0, 2)
        stars.append({
            'x': x,
            'y': y,
            'size': size,
            'duration': duration,
            'delay': delay
        })
    return stars

def generate_enemies():
    """Generate enemy ships with randomized paths"""
    enemies = []
    for i in range(NUM_ENEMIES):
        start_x = random.randint(50, WIDTH - 50)
        start_y = -50
        end_y = HEIGHT + 50
        duration = random.uniform(4, 8)
        delay = random.uniform(0, ANIMATION_DURATION * 0.7)
        
        # Zigzag pattern
        mid_x1 = start_x + random.randint(-100, 100)
        mid_x2 = start_x + random.randint(-100, 100)
        
        enemies.append({
            'id': i,
            'start_x': start_x,
            'start_y': start_y,
            'mid_x1': mid_x1,
            'mid_x2': mid_x2,
            'end_y': end_y,
            'duration': duration,
            'delay': delay
        })
    return enemies

def generate_lasers(enemies):
    """Generate laser shots timed with enemy positions"""
    lasers = []
    laser_id = 0
    
    for enemy in enemies:
        # Calculate when enemy reaches shootable position
        shoot_time = enemy['delay'] + (enemy['duration'] * 0.3)
        
        # Laser targeting enemy's position
        laser_start_y = SHIP_Y - 20
        laser_end_y = -20
        laser_duration = 0.5
        
        lasers.append({
            'id': laser_id,
            'x': enemy['start_x'],
            'start_y': laser_start_y,
            'end_y': laser_end_y,
            'duration': laser_duration,
            'delay': shoot_time
        })
        laser_id += 1
        
        # Add explosion at collision point
        explosion_time = shoot_time + laser_duration
        lasers.append({
            'type': 'explosion',
            'id': laser_id,
            'x': enemy['start_x'],
            'y': 200,
            'delay': explosion_time
        })
        laser_id += 1
    
    return lasers

def create_svg():
    """Generate the complete SVG animation"""
    
    stars = generate_stars()
    enemies = generate_enemies()
    lasers = generate_lasers(enemies)
    
    # Calculate score (enemies hit)
    score = len([l for l in lasers if l.get('type') == 'explosion'])
    
    svg = f'''<svg width="{WIDTH}" height="{HEIGHT}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Gradients -->
    <linearGradient id="spaceGradient" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#0a0a0a;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#1a0033;stop-opacity:1" />
    </linearGradient>
    
    <radialGradient id="explosionGradient" cx="50%" cy="50%" r="50%">
      <stop offset="0%" style="stop-color:#ff9900;stop-opacity:1" />
      <stop offset="50%" style="stop-color:#ff3300;stop-opacity:0.8" />
      <stop offset="100%" style="stop-color:#ff0000;stop-opacity:0" />
    </radialGradient>
    
    <!-- Filters -->
    <filter id="glow">
      <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  
  <!-- Background -->
  <rect width="{WIDTH}" height="{HEIGHT}" fill="url(#spaceGradient)"/>
  
  <!-- Stars -->
'''
    
    # Add twinkling stars
    for star in stars:
        svg += f'''  <circle cx="{star['x']}" cy="{star['y']}" r="{star['size']}" fill="#ffffff">
    <animate attributeName="opacity" values="0.3;1;0.3" dur="{star['duration']}s" begin="{star['delay']}s" repeatCount="indefinite"/>
  </circle>
'''
    
    # Add enemies
    svg += '\n  <!-- Enemy Ships -->\n'
    for enemy in enemies:
        path = f"M {enemy['start_x']},{enemy['start_y']} Q {enemy['mid_x1']},200 {enemy['mid_x2']},400 T {enemy['start_x']},{enemy['end_y']}"
        
        svg += f'''  <g id="enemy{enemy['id']}">
    <animateMotion dur="{enemy['duration']}s" begin="{enemy['delay']}s" repeatCount="indefinite">
      <mpath href="#enemyPath{enemy['id']}"/>
    </animateMotion>
    <!-- Enemy ship shape -->
    <polygon points="-15,-10 0,-20 15,-10 10,10 -10,10" fill="#ff3366" stroke="#ff0000" stroke-width="1" filter="url(#glow)"/>
    <circle cx="0" cy="0" r="3" fill="#ff0000"/>
  </g>
  <path id="enemyPath{enemy['id']}" d="{path}" fill="none"/>
'''
    
    # Add player ship
    svg += f'''
  <!-- Player Ship -->
  <g id="playerShip" transform="translate(400, {SHIP_Y})">
    <animateTransform attributeName="transform" type="translate"
      values="300,{SHIP_Y}; 500,{SHIP_Y}; 300,{SHIP_Y}"
      dur="6s" repeatCount="indefinite"/>
    <!-- Ship body -->
    <polygon points="0,-25 -20,15 20,15" fill="#00ff9c" stroke="#00cc7a" stroke-width="2" filter="url(#glow)"/>
    <!-- Cockpit -->
    <circle cx="0" cy="-5" r="5" fill="#00ccff" opacity="0.8"/>
    <!-- Engine glow -->
    <ellipse cx="0" cy="15" rx="8" ry="4" fill="#ff9900" opacity="0.6">
      <animate attributeName="opacity" values="0.6;1;0.6" dur="0.3s" repeatCount="indefinite"/>
    </ellipse>
  </g>
'''
    
    # Add lasers and explosions
    svg += '\n  <!-- Lasers & Explosions -->\n'
    for laser in lasers:
        if laser.get('type') == 'explosion':
            svg += f'''  <g opacity="0">
    <animate attributeName="opacity" values="0;1;1;0" dur="0.6s" begin="{laser['delay']}s" repeatCount="indefinite"/>
    <circle cx="{laser['x']}" cy="{laser['y']}" r="5" fill="url(#explosionGradient)">
      <animate attributeName="r" values="5;30;40" dur="0.6s" begin="{laser['delay']}s" repeatCount="indefinite"/>
    </circle>
    <circle cx="{laser['x']}" cy="{laser['y']}" r="3" fill="#ffffff">
      <animate attributeName="r" values="3;15;20" dur="0.6s" begin="{laser['delay']}s" repeatCount="indefinite"/>
    </circle>
  </g>
'''
        else:
            svg += f'''  <line x1="{laser['x']}" y1="{laser['start_y']}" x2="{laser['x']}" y2="{laser['start_y']}" 
        stroke="#00ff9c" stroke-width="3" filter="url(#glow)" opacity="0">
    <animate attributeName="y2" from="{laser['start_y']}" to="{laser['end_y']}" 
      dur="{laser['duration']}s" begin="{laser['delay']}s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0;1;1;0" 
      dur="{laser['duration']}s" begin="{laser['delay']}s" repeatCount="indefinite"/>
  </line>
'''
    
    # Add HUD
    svg += f'''
  <!-- HUD -->
  <rect x="10" y="10" width="200" height="80" fill="#0a0a0a" opacity="0.7" rx="5"/>
  <text x="20" y="35" font-family="'Courier New', monospace" font-size="16" fill="#00ff9c" font-weight="bold">
    GALAXY ATTACK
  </text>
  <text x="20" y="55" font-family="'Courier New', monospace" font-size="14" fill="#ffffff">
    SCORE: {score * 100}
  </text>
  <text x="20" y="75" font-family="'Courier New', monospace" font-size="12" fill="#00ff9c">
    HITS: {score}
  </text>
  
  <!-- Game Info -->
  <text x="{WIDTH - 180}" y="35" font-family="'Courier New', monospace" font-size="12" fill="#00ff9c" text-anchor="end">
    AUTO-PLAY MODE
  </text>
  <text x="{WIDTH - 180}" y="55" font-family="'Courier New', monospace" font-size="10" fill="#ffffff" text-anchor="end">
    Updated: {datetime.now().strftime("%Y-%m-%d")}
  </text>
  
</svg>'''
    
    return svg

if __name__ == "__main__":
    # Generate SVG
    svg_content = create_svg()
    
    # Save to file
    with open('galaxy_attack.svg', 'w', encoding='utf-8') as f:
        f.write(svg_content)
    
    print("✅ Galaxy Arcade Attack SVG generated successfully!")
    print("📁 Output: galaxy_attack.svg")
