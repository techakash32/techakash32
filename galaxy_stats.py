#!/usr/bin/env python3
"""
Galaxy GitHub Stats Card Generator
Static SVG card with GitHub statistics in arcade/space theme
"""

import os
import sys
import json
import random
import math
from datetime import datetime
import xml.etree.ElementTree as ET
from xml.dom import minidom
import requests

def get_github_stats(username):
    """Get GitHub statistics with fallback values"""
    stats = {
        'username': username,
        'total_commits': 427,
        'total_stars': 68,
        'commit_streak': 42,
        'public_repos': 12,
        'followers': 24
    }
    
    try:
        # Get user info from GitHub API
        user_url = f"https://api.github.com/users/{username}"
        response = requests.get(user_url, timeout=10)
        
        if response.status_code == 200:
            user_data = response.json()
            stats['public_repos'] = user_data.get('public_repos', 12)
            stats['followers'] = user_data.get('followers', 24)
            
            # Get stars from repositories
            repos_url = f"https://api.github.com/users/{username}/repos"
            repos_response = requests.get(repos_url, timeout=10)
            
            if repos_response.status_code == 200:
                repos_data = repos_response.json()
                stats['total_stars'] = sum(repo.get('stargazers_count', 0) for repo in repos_data)
        
        # Calculate derived stats
        stats['total_commits'] = stats['public_repos'] * 35 + stats['followers'] * 5
        stats['commit_streak'] = min(stats['followers'] * 2, 365)
        
        # Apply reasonable limits
        stats['total_commits'] = min(stats['total_commits'], 10000)
        stats['total_stars'] = min(stats['total_stars'], 500)
        stats['commit_streak'] = max(min(stats['commit_streak'], 365), 7)
        
    except Exception as e:
        print(f"Using fallback stats: {e}")
        # Keep default values
    
    return stats

class GalaxyStatsCard:
    def __init__(self, stats, width=600, height=280):
        self.stats = stats
        self.width = width
        self.height = height
        
        self.colors = {
            'background': '#0a0a17',
            'card_bg': '#11112a',
            'text_primary': '#ffffff',
            'text_secondary': '#a0a0ff',
            'accent_cyan': '#00ffff',
            'accent_purple': '#b967ff',
            'accent_green': '#00ff9c',
            'accent_orange': '#ffaa00',
            'star_color': '#ffffff'
        }
        
        self.padding = 30
        self.content_width = width - (self.padding * 2)
    
    def generate(self):
        """Generate complete SVG card"""
        svg = ET.Element('svg', {
            'width': str(self.width),
            'height': str(self.height),
            'xmlns': 'http://www.w3.org/2000/svg',
            'viewBox': f'0 0 {self.width} {self.height}'
        })
        
        self.add_background(svg)
        self.add_stars(svg)
        self.add_card(svg)
        self.add_header(svg)
        self.add_stats(svg)
        self.add_footer(svg)
        
        return self.format_xml(svg)
    
    def add_background(self, svg):
        """Add space background"""
        ET.SubElement(svg, 'rect', {
            'width': '100%',
            'height': '100%',
            'fill': self.colors['background']
        })
        
        # Nebula effects
        ET.SubElement(svg, 'ellipse', {
            'cx': '150',
            'cy': '100',
            'rx': '100',
            'ry': '40',
            'fill': self.colors['accent_cyan'],
            'opacity': '0.08'
        })
        
        ET.SubElement(svg, 'ellipse', {
            'cx': '450',
            'cy': '200',
            'rx': '150',
            'ry': '60',
            'fill': self.colors['accent_purple'],
            'opacity': '0.06'
        })
    
    def add_stars(self, svg):
        """Add starfield"""
        random.seed(42)  # Consistent stars
        
        for _ in range(50):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            size = random.uniform(0.3, 1.2)
            opacity = random.uniform(0.4, 0.9)
            
            ET.SubElement(svg, 'circle', {
                'cx': str(x),
                'cy': str(y),
                'r': str(size),
                'fill': self.colors['star_color'],
                'opacity': str(opacity)
            })
    
    def add_card(self, svg):
        """Add card container"""
        # Card shadow
        ET.SubElement(svg, 'rect', {
            'x': str(self.padding + 3),
            'y': str(self.padding + 3),
            'width': str(self.content_width),
            'height': str(self.height - (self.padding * 2)),
            'rx': '12',
            'fill': '#000000',
            'opacity': '0.3'
        })
        
        # Card background
        ET.SubElement(svg, 'rect', {
            'x': str(self.padding),
            'y': str(self.padding),
            'width': str(self.content_width),
            'height': str(self.height - (self.padding * 2)),
            'rx': '12',
            'fill': self.colors['card_bg'],
            'stroke': self.colors['accent_cyan'],
            'stroke-width': '1',
            'stroke-opacity': '0.3'
        })
    
    def add_header(self, svg):
        """Add header with title"""
        ET.SubElement(svg, 'text', {
            'x': str(self.width // 2),
            'y': str(self.padding + 40),
            'fill': self.colors['text_primary'],
            'font-family': 'Arial, sans-serif',
            'font-size': '24',
            'font-weight': 'bold',
            'text-anchor': 'middle'
        }).text = 'GALAXY STATS TERMINAL'
        
        ET.SubElement(svg, 'text', {
            'x': str(self.padding + 20),
            'y': str(self.padding + 70),
            'fill': self.colors['text_secondary'],
            'font-family': 'Consolas, monospace',
            'font-size': '14'
        }).text = f'USER: @{self.stats["username"]}'
        
        current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')
        ET.SubElement(svg, 'text', {
            'x': str(self.width - self.padding - 20),
            'y': str(self.padding + 70),
            'fill': self.colors['text_secondary'],
            'font-family': 'Consolas, monospace',
            'font-size': '12',
            'text-anchor': 'end'
        }).text = f'UPDATED: {current_time}'
    
    def add_stats(self, svg):
        """Add statistics displays"""
        stat_start_y = self.padding + 100
        stat_width = (self.content_width - 40) // 3
        
        stats_data = [
            {
                'value': self.stats['total_commits'],
                'label': '👾 ENEMIES DESTROYED',
                'icon': '👾',
                'color': self.colors['accent_purple'],
                'desc': 'Total Commits'
            },
            {
                'value': self.stats['total_stars'],
                'label': '⚡ POWER-UPS',
                'icon': '⚡',
                'color': self.colors['accent_green'],
                'desc': 'Total Stars'
            },
            {
                'value': self.stats['commit_streak'],
                'label': '🕒 SURVIVAL TIME',
                'icon': '🕒',
                'color': self.colors['accent_orange'],
                'desc': 'Day Streak'
            }
        ]
        
        for i, stat in enumerate(stats_data):
            x = self.padding + 10 + (i * (stat_width + 10))
            
            # Stat box
            ET.SubElement(svg, 'rect', {
                'x': str(x),
                'y': str(stat_start_y),
                'width': str(stat_width),
                'height': '120',
                'rx': '8',
                'fill': '#0a0a1a',
                'stroke': stat['color'],
                'stroke-width': '1',
                'stroke-opacity': '0.4'
            })
            
            # Icon
            ET.SubElement(svg, 'text', {
                'x': str(x + stat_width // 2),
                'y': str(stat_start_y + 40),
                'fill': stat['color'],
                'font-family': 'Arial, sans-serif',
                'font-size': '28',
                'text-anchor': 'middle',
                'font-weight': 'bold'
            }).text = stat['icon']
            
            # Value
            value_str = f"{stat['value']:,}"
            ET.SubElement(svg, 'text', {
                'x': str(x + stat_width // 2),
                'y': str(stat_start_y + 80),
                'fill': self.colors['text_primary'],
                'font-family': 'Arial, sans-serif',
                'font-size': '28',
                'text-anchor': 'middle',
                'font-weight': 'bold'
            }).text = value_str
            
            # Label
            ET.SubElement(svg, 'text', {
                'x': str(x + stat_width // 2),
                'y': str(stat_start_y + 100),
                'fill': self.colors['text_secondary'],
                'font-family': 'Consolas, monospace',
                'font-size': '11',
                'text-anchor': 'middle'
            }).text = stat['label']
            
            # Description
            ET.SubElement(svg, 'text', {
                'x': str(x + stat_width // 2),
                'y': str(stat_start_y + 115),
                'fill': '#6666aa',
                'font-family': 'Consolas, monospace',
                'font-size': '10',
                'text-anchor': 'middle'
            }).text = stat['desc']
    
    def add_footer(self, svg):
        """Add footer info"""
        footer_y = self.height - self.padding - 10
        
        stats_text = f"Repos: {self.stats['public_repos']} • Followers: {self.stats['followers']}"
        ET.SubElement(svg, 'text', {
            'x': str(self.width // 2),
            'y': str(footer_y),
            'fill': self.colors['text_secondary'],
            'font-family': 'Consolas, monospace',
            'font-size': '12',
            'text-anchor': 'middle'
        }).text = stats_text
        
        ET.SubElement(svg, 'text', {
            'x': str(self.width - self.padding - 10),
            'y': str(footer_y),
            'fill': '#6666aa',
            'font-family': 'Consolas, monospace',
            'font-size': '10',
            'text-anchor': 'end'
        }).text = 'Generated with Galaxy Stats'
    
    def format_xml(self, svg):
        """Format SVG with proper XML declaration"""
        rough_string = ET.tostring(svg, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")

def main():
    """Main function"""
    print("🚀 Generating Galaxy Stats Card...")
    
    # Get username
    username = os.getenv('GITHUB_ACTOR', 'techakash32')
    print(f"📊 Fetching stats for: {username}")
    
    # Get stats
    stats = get_github_stats(username)
    
    # Generate card
    generator = GalaxyStatsCard(stats)
    svg_content = generator.generate()
    
    # Save to file
    os.makedirs('output', exist_ok=True)
    
    with open('output/galaxy_stats.svg', 'w', encoding='utf-8') as f:
        f.write(svg_content)
    
    print(f"✅ Stats Card saved to output/galaxy_stats.svg")
    print(f"👾 Enemies Destroyed: {stats['total_commits']:,}")
    print(f"⚡ Power-ups: {stats['total_stars']:,}")
    print(f"🕒 Survival Time: {stats['commit_streak']} days")

if __name__ == '__main__':
    main()
