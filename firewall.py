# firewall.py
import random
import tkinter as tk
from tkinter import simpledialog
import string

def caesar_decrypt(ciphertext, shift):
    decrypted_text = ""
    for char in ciphertext:
        if char in string.ascii_lowercase:
            offset = ord('a')
            decrypted_text += chr((ord(char) - offset - shift) % 26 + offset)
        elif char in string.ascii_uppercase:
            offset = ord('A')
            decrypted_text += chr((ord(char) - offset - shift) % 26 + offset)
        else:
            decrypted_text += char
    return decrypted_text

def ask_question_firewall(difficulty):
    root = tk.Tk()
    root.withdraw()
    if difficulty == 'easy':
        user_input = simpledialog.askinteger("Firewall Challenge (Easy)", "Enter the number to bypass the firewall:")
        correct_number = 42
    elif difficulty == 'medium':
        user_input = simpledialog.askinteger("Firewall Challenge (Medium)", "Enter the number to bypass the firewall:")
        correct_number = 84
    elif difficulty == 'hard':
        user_input = simpledialog.askinteger("Firewall Challenge (Hard)", "Enter the number to bypass the firewall:")
        correct_number = 168
    else:
        return False
    
    root.destroy()
    if user_input is not None and user_input == correct_number:
        return True
    return False


def detect_collision(player_pos, node_pos, player_size, node_size):
    p_x, p_y = player_pos
    n_x, n_y = node_pos
    distance = ((p_x - n_x) ** 2 + (p_y - n_y) ** 2) ** 0.5
    if distance < player_size / 2 + node_size:
        return True
    return False
