import base64
import string
import random
import hashlib
import time

ver = 1 #Hashcash format version, 1 (which supersedes version 0).
bits = int(input("Enter the difficulty (number of leading zeros): ")) # number of zero-bits at the start of the hashed code.
date = 201110163942 #in the format YYMMDD[hhmm[ss]] 
resourc = "me@moritzwalther.com" #resource data string being transmitted, e.g., an email address.
ext = "" #Extension (optional; ignored in version 1).
rand = "abcd" #String of random characters, encoded in base-64 format, must be 16 charectors in base64. 96bits
nonce_int  =  1 #Binary counter, encoded in base-64 format. max length 2 to the 24th power -1. 0 - 16777215

#function to create random string
def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

hs = "init"
start_time = time.time()

#generate a string of zeros based on number of leading zeroes desire to compare the hash with
zero_str = ""
while not len(zero_str) == int(bits):
    zero_str = zero_str + "0"
print("the number of leading zeros is: " + str(zero_str)+ " and the length is: "+ str(len(zero_str)))

while not hs[0:bits] == zero_str:
    #base64 module in python can only encode strings or bytes. Byte is limited to 0-256
    nonce_str = str(nonce_int) 
    #Base64 encode the nonce
    nonce = base64.b64encode(nonce_str.encode('ascii'))
    #generate random string
    rand = get_random_string(96)
    #assemble header
    header = str(ver)+":" +str(bits) +":"+str(date)+resourc+":"+ext+":"+rand+":"+str(nonce.decode('ascii'))
    #hash header
    hs = hashlib.sha256(header.encode('utf-8')).hexdigest()
    #increment the nonce
    nonce_int= nonce_int + 1
    
#calculate the time elapsed to find a fitting hash
current_time = time.time()
elapsed_time = current_time - start_time

print("the header is: " + header)
print("the hash is: " + hs)  
print ("the operation was run: " + str(nonce_int) +  " times")
print("this opertation took: " + str(elapsed_time) + " seconds")  