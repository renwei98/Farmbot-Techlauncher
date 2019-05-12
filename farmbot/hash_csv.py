import hashlib

#hash current csv
def hash_this_csv(current_csv):
    hasher = hashlib.md5()
    with open(current_csv, 'rb') as cfile:
        buf = cfile.read()
        hasher.update(buf)
    global hashed_value
    hashed_value = hasher.hexdigest()
    
#hash new csv and compare with hashed csv value
def csv_changed(path):
    global hasher1
    hasher1 = hashlib.md5()
    with open(path, 'rb') as rfile:
        buf1 = rfile.read()
        hasher1.update(buf1)
    if hashed_value == hasher1.hexdigest():
        return False
    else:
        return True
    
#sign new hash value to current value
def update_hash():
    global hashed_value
    hashed_value = hasher1.hexdigest()

#test purpose print out values
def print_hash_values():
    print(hashed_value + "\n" + hasher1.hexdigest())