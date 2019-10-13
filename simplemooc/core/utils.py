from hashlib import sha224
from string import ascii_uppercase, digits
from random import choice

# Script para gerar a nova senha, do esqueceu senha.

def random_key(size=5):
	chars = ascii_uppercase + digits
	return ''.join(choice(chars) for x in range(size))

def generate_hash_key(salt, random_str_size=5):
	random_str = random_key(random_str_size)
	text = random_str + salt
	return sha224(text.encode('utf-8')).hexdigest()