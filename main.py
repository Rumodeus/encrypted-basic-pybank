import base64
import csv
import os
import random
import sys
import time
from math import sqrt
from random import randint as rand

#decoding public and private RSA keyhs
pub1 = int(base64.b64decode("MjkxMzc=").decode("ascii"))
pub2 = int(base64.b64decode("NjMxNTc=").decode("ascii"))
priv1 = int(base64.b64decode("NDQ5MTM=").decode("ascii"))
priv2 = int(base64.b64decode("NjMxNTc=").decode("ascii"))
public, private = ((pub1, pub2), (priv1, priv2))


#calculate the greatest common divisor for RSA
def gcd(a, b):
  if b == 0:
    return a
  else:
    return gcd(b, a % b)


#calculate the modular multiplicative inverse for RSA
def mod_inverse(a, m):
  for x in range(1, m):
    if (a * x) % m == 1:
      return x
  return -1


#check if number is prime
def isprime(n):
  if n < 2:
    return False
  elif n == 2:
    return True
  else:
    for i in range(2, int(sqrt(n)) + 1, 2):
      if n % i == 0:
        return False
  return True


#generate 2 random primes for RSA keys
p = rand(1, 1000)
q = rand(1, 1000)


#generate an RSA key pair given p, q, and keysize
def generate_keypair(p, q, keysize):
  nMin = 1 << (keysize - 1)
  nMax = (1 << keysize) - 1
  primes = [2]
  start = 1 << (keysize // 2 - 1)
  stop = 1 << (keysize // 2 + 1)

  if start >= stop:
    return []

  for i in range(3, stop + 1, 2):
    for p in primes:
      if i % p == 0:
        break
    else:
      primes.append(i)

  while (primes and primes[0] < start):
    del primes[0]

  while primes:
    p = random.choice(primes)
    primes.remove(p)
    q_values = [q for q in primes if nMin <= p * q <= nMax]
    if q_values:
      q = random.choice(q_values)
      break
  print(p, q)
  n = p * q
  phi = (p - 1) * (q - 1)

  e = random.randrange(1, phi)
  g = gcd(e, phi)

  while True:
    e = random.randrange(1, phi)
    g = gcd(e, phi)
    d = mod_inverse(e, phi)
    if g == 1 and e != d:
      break

  return ((e, n), (d, n))


def encrypt(msg_plaintext, package):
  e, n = package
  msg_ciphertext = [pow(ord(c), e, n) for c in msg_plaintext]
  return msg_ciphertext


def decrypt(msg_ciphertext, package):
  d, n = package
  msg_plaintext = [chr(pow(c, d, n)) for c in msg_ciphertext]
  return (''.join(msg_plaintext))


def caesar_cipher(text, shift):
  encrypted_text = ""

  for char in text:
    if char.isalpha():
      is_upper = char.isupper()
      char = char.lower()
      char_code = ord(char)
      shifted_char = chr(((char_code - ord('a') + shift) % 26) + ord('a'))
      if is_upper:
        shifted_char = shifted_char.upper()
    elif char.isnumeric():
      char_code = ord(char)
      shifted_char = chr(((char_code - ord('0') + shift) % 10) + ord('0'))
    else:
      shifted_char = char

    encrypted_text += shifted_char

  return encrypted_text


def caesar_decrypt(text, shift):
  return caesar_cipher(text, -shift)


split_parts = []
keyd = base64.b64decode("Nw==")
keydc = keyd.decode("ascii")
shift = int(keydc)
id = [1001, 4159, 7860, 10012, 6777]
user = [
    "Ahmed Hussain", "Uzair Hasnaan", "Arsalan Arsheed",
    "Abdullah Naanwanamak", "Jaden Clickube"
]
with open('balance.csv', 'r') as file1:
  csv_reader = csv.reader(file1)
  balance = []
  for row in csv_reader:
    for value in row:
      bal = float(value)
      balance.append(bal)

with open('count.csv', 'r') as file2:
  csv_reader = csv.reader(file2)
  counter = []
  for row in csv_reader:
    for value in row:
      cont = int(value)
      counter.append(cont)

with open('pin.csv', 'r') as file3:
  csv_reader = csv.reader(file3)
  pin_list = []
  for row in csv_reader:
    for value in row:
      pin = value
      pin_list.append(pin)

print("enter id")
ip = input()
if ip == "99999":
  print("Zǎo shang hǎo zhōng guó!")
  time.sleep(1)
  exit()
if ip == "":
  exit()
if any(char.isalpha() for char in ip):
  print("invalid")
  os.execl(sys.executable, sys.executable, *sys.argv)
if any(char.isalpha() is False and char.isnumeric() is False for char in ip):
  print("invalid")
  os.execl(sys.executable, sys.executable, *sys.argv)

else:
  if int(ip) not in id:
    print("wrong id")
    os.execl(sys.executable, sys.executable, *sys.argv)
  elif int(ip) in id:
    ip = int(ip)
    pos = id.index(ip)
    plaintext2 = ""
    cdcode = caesar_decrypt(pin_list[pos], shift)
    cdcode = cdcode.strip()
    for i in range(0, len(cdcode), 5):
      split_parts.append(cdcode[i:i + 5])
    for i in range(0, len(split_parts)):
      split_parts[i] = int(split_parts[i])
    decoded = decrypt(split_parts, private)
    pin_list[pos] = decoded

    def pina():
      if counter[pos] == 3:
        print("card is locked")
        time.sleep(1)
        exit()
      print("enter pin,", user[pos])
      pi = input()
      if pi == "":
        exit()
      if any(char.isalpha() for char in pi):
        print("no characters")
        counter[pos] += 1
        with open('count.csv', 'w', newline='') as csvfile:
          csvwriter = csv.writer(csvfile)
          csvwriter.writerow(counter)
        print(counter[pos])
        pina()
        return
      if any(char.isalpha() is False and char.isnumeric() is False
             for char in pi):
        print("invalid")
        counter[pos] += 1
        with open('count.csv', 'w', newline='') as csvfile:
          csvwriter = csv.writer(csvfile)
          csvwriter.writerow(counter)
        print(counter[pos])
        pina()
        return
      if pi == pin_list[pos]:
        print("correct")
        counter[pos] = 0
        with open('count.csv', 'w', newline='') as csvfile:
          csvwriter = csv.writer(csvfile)
          csvwriter.writerow(counter)
        return
      else:
        print("wrong pin")
        counter[pos] += 1
        with open('count.csv', 'w', newline='') as csvfile:
          csvwriter = csv.writer(csvfile)
          csvwriter.writerow(counter)
        print(counter[pos])
        pina()

    pina()
print("Welcome,", user[pos])
cd = balance[pos] / 10
cdc = int(cd)
cdef = cdc * 10


def menu():
  print(
      "Welcome to the PyBank\n1. Display Balance\n2. Withdraw Funds\n3. Deposit Funds\n4. Change pin\n9. Return Card"
  )
  op = input()

  if op == "1":
    print(f"You have £{balance[pos]}")
    cd = balance[pos] / 10
    cdc = int(cd)
    cdef = cdc * 10
    print(f"You can withdraw £{cdef}")
    menu()
  if op == "2":
    withdrawr = [10, 20, 40, 60, 80, 100]

    def withdrawing():
      print(
          "How much do you want to withdraw?\n£10\n£20\n£40\n£60\n£80\n£100\nOther\nReturn Card\nMenu"
      )
      withd = input()
      withd.lower()
      if "other" in withd:
        print("Enter amount")
        withd = input()
        if any(char.isalpha() is False and char.isnumeric() is False
               for char in withd):
          print("invalid")
          withdrawing()
        if any(char.isdigit() for char in withd):
          if any(char.isalpha() for char in withd):
            print("invalid amount (contains characters)")
            withdrawing()
          withd = int(withd)
          if withd % 10 != 0:
            print("invalid amount")
            withdrawing()
          else:
            balance[pos] = round(balance[pos] - withd, 2)
      else:
        if "return" in withd:
          exit()
        if "menu" in withd:
          menu()
        if any(char.isdigit() for char in withd):
          if any(char.isalpha() for char in withd):
            print("invalid amount (contains characters)")
            withdrawing()
          withd = int(withd)
          if withd not in withdrawr:
            print("invalid amount")
            withdrawing()
          else:
            balance[pos] = round(balance[pos] - withd, 2)
            with open('balance.csv', 'w', newline='') as csvfile:
              csvwriter = csv.writer(csvfile)
              csvwriter.writerow(balance)
        else:
          print("invalid statement")
          withdrawing()
      print(f"new balance is £{balance[pos]}")
      menu()

    withdrawing()
  if op == "3":

    def deping():
      print("Enter amount to deposit\nReturn Card\nMenu")
      depd = input()
      depd = depd.lower()
      if "return" in depd:
        exit()
      if "menu" in depd:
        menu()
      if any(char.isdigit() for char in depd):
        if any(char.isalpha() for char in depd):
          print("invalid amount (contains characters)")
          deping()

        else:
          depd = float(depd)
          balance[pos] = round(balance[pos] + depd, 2)
          with open('balance.csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(balance)
      else:
        print("invalid statement")
        deping()

    deping()
    print(f"new balance is £{balance[pos]}")
    menu()
  if op == "4":

    def pin():
      print("enter new pin")
      np = input()
      if len(np) < 4:
        print("too short")
        pin()
      if any(char.isalpha() for char in np):
        print("no characters")
        pin()
      if any(char.isalpha() is False and char.isnumeric() is False
             for char in np):
        print("invalid")
        pin()
      encrypte = encrypt(np, public)
      ence = (''.join((str(x) for x in encrypte)))
      encrypted = caesar_cipher(ence, shift)
      pin_list[pos] = encrypted
      with open('pin.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(pin_list)
      menu()

    pin()
  if op == "9":
    exit()
  else:
    print("Invalid statement")
    menu()


menu()
