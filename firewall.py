# firewall.py
import random
import pygame
import tkinter as tk
from tkinter import simpledialog
import string

def caesar_cipher(text, shift):
    encrypted_text = []
    for char in text:
        if char.isalpha():
            shift_base = ord('A') if char.isupper() else ord('a')
            encrypted_text.append(chr((ord(char) - shift_base + shift) % 26 + shift_base))
        else:
            encrypted_text.append(char)
    return ''.join(encrypted_text)

def caesar_decipher(text, shift):
    return caesar_cipher(text, -shift)

def ask_question_firewall(difficulty):
    root = tk.Tk()
    root.withdraw()
    
    # Determine the shift value based on difficulty
    shift = {"easy": 3, "medium": 7, "hard": 13}[difficulty]
    
    # Generate a random message and cipher it
    message = "SECURE THIS FIREWALL"
    ciphered_message = caesar_cipher(message, shift)
    
    user_input = simpledialog.askstring("Firewall Challenge", f"Decipher this message: {ciphered_message}")
    root.destroy()
    
    if user_input is not None and user_input.upper() == message:
        return True
    return False

    
    root.destroy()
    if user_input is not None and user_input == correct_number:
        return True
    return False


def detect_rectangle_collision(player_pos, player_size, rect_pos, rect_width, rect_height):
    player_rect = pygame.Rect(player_pos[0] - player_size // 2, player_pos[1] - player_size // 2, player_size, player_size)
    firewall_rect = pygame.Rect(rect_pos[0], rect_pos[1], rect_width, rect_height)
    return player_rect.colliderect(firewall_rect)
