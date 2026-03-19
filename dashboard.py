import pygame
import psutil
import socket
import time
import subprocess

pygame.init()
screen = pygame.display.set_mode((320, 240), pygame.FULLSCREEN)
pygame.display.set_caption("Dashboard")
pygame.mouse.set_visible(False)

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 80, 80)

font_big = pygame.font.SysFont("monospace", 22, bold=True)
font_med = pygame.font.SysFont("monospace", 16)
font_small = pygame.font.SysFont("monospace", 13)

def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except:
        return "No network"

def get_temp():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp") as f:
            return round(int(f.read()) / 1000, 1)
    except:
        return 0

def draw_bar(surface, x, y, w, h, pct, color):
    pygame.draw.rect(surface, (50, 50, 50), (x, y, w, h))
    pygame.draw.rect(surface, color, (x, y, int(w * pct / 100), h))
    pygame.draw.rect(surface, WHITE, (x, y, w, h), 1)

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill(BLACK)

    # Title
    now = time.strftime("%H:%M:%S  %d %b %Y")
    screen.blit(font_med.render(now, True, CYAN), (5, 5))
    pygame.draw.line(screen, CYAN, (0, 25), (320, 25), 1)

    # CPU
    cpu = psutil.cpu_percent(interval=None)
    temp = get_temp()
    screen.blit(font_med.render(f"CPU: {cpu}%  Temp: {temp}C", True, WHITE), (5, 32))
    draw_bar(screen, 5, 52, 310, 12, cpu, GREEN if cpu < 70 else RED)

    # RAM
    ram = psutil.virtual_memory()
    ram_pct = ram.percent
    ram_used = round(ram.used / 1024 / 1024)
    ram_total = round(ram.total / 1024 / 1024)
    screen.blit(font_med.render(f"RAM: {ram_used}/{ram_total} MB ({ram_pct}%)", True, WHITE), (5, 72))
    draw_bar(screen, 5, 92, 310, 12, ram_pct, YELLOW if ram_pct < 80 else RED)

    # Network
    ip = get_ip()
    screen.blit(font_med.render(f"IP: {ip}", True, WHITE), (5, 112))

    # Divider
    pygame.draw.line(screen, (80, 80, 80), (0, 132), (320, 132), 1)

    # App Status placeholder
    # screen.blit(font_med.render("App Status:", True, CYAN), (5, 138))
    # screen.blit(font_med.render("-- your app here --", True, YELLOW), (5, 158))

    pygame.display.flip()
    clock.tick(1)
