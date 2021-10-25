# NoOne

### Author: [Phung Duc Thang](https://github.com/thangpd3160)

This is the last challenge, but actually the easiest challenge ever. The idea of this challenge is just fipping one bit, so that is the role from user (1) to admin (0), then we got the flag. Full source code can be found at [here](https://github.com/FPTU-Ethical-Hackers-Club/SVATTT/blob/main/2021/crypto/NoOne/src.py).

![image](https://user-images.githubusercontent.com/61876488/138581209-43c080c7-0e19-4143-97bd-1c37ea92d392.png)

### 1. Challenge analysis:

This challenge is same as the EasyOne challenge, we also need to login as admin, but can by normal register. The different is there is no `/logincert` anymore.

Follow the code, the `login_required` function tell us that it extract the user role from the `authtoken` value in cookies:

```python
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):

        try:
        
            ciphertext = request.cookies.get('authtoken')

            userid = request.cookies.get('userid')

            if not ciphertext or not userid:
                return redirect(url_for('login'))

            encryptkey = get_encryptkey(userid)

            plainbytes = decrypt(ciphertext, encryptkey)

            usernamelen = int.from_bytes(plainbytes[:2], "little")
            usernameencoded = plainbytes[2:usernamelen+2]
            username = usernameencoded.decode("utf-8")
            role = plainbytes[usernamelen+2]
            
            g.username = username
            g.role = role

        except:
            abort(401)
        
        return f(*args, **kwargs)
   
    return wrap
```

Follow the code, I see that the `authtokenvalue` is encrypted using AES in CFB mode:

```python
def encrypt(plainbytes, key):
    
    iv = Random.new().read(AES.block_size)
    
    cipher = AES.new(key, AES.MODE_CFB, iv)
    
    cipherbytes = cipher.encrypt(plainbytes)

    ciphertext = base64.b64encode(iv + cipherbytes)

    return ciphertext
```

And the value of `authtoken` is generated after we logon. I registered with username _thangpd11_, so that the role bytes value will lie in the first block.

```python
@app.route("/", methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Username and Password is required!')
        else:
            # verify login
            user = verify_login(username, password)

            if not user:
                flash('Username and Password is not correct!')
            else:
                
                userid = user[0]
                username = user[1]
                role = user[5]

                # get key
                key = base64.b64decode(user[4])

                # create authtoken
                usernamebytes = username.encode('utf-8')
                usernamelen = len(usernamebytes)
                plainbytes = len(usernamebytes).to_bytes(2, "little") + usernamebytes + role.to_bytes(1, "little")

                ciphertext = encrypt(plainbytes, key)

                response = make_response(redirect(url_for('index')))

                response.set_cookie('userid', str(userid))
                response.set_cookie('authtoken', ciphertext)

                return response

    return render_template('login.html')
```

### 2. Bit Flipping Attack on AES CFB

I take the folllowing from gooogle to help me easily illustrate the attack. The concept is actually very similar to the bit flipping attack on AES CBC (the classic one).

![image](https://user-images.githubusercontent.com/61876488/138589425-afa13bee-7a06-4a49-a116-e73802396f8b.png)

The decryption process of the first block can be interpreted in mathematic formula as **P₁ = E(IV) ⊕ C₁ or E(IV) = P₁ ⊕ C₁**.

The point is we wanna change **P₁** to **P₁'**. Simply, we just need to change the **C₁** value to another **C₁'** value, such that **E(IV)** value remains. In mathematical formula, we can interpret the above words as: 

**E(IV) = P₁ ⊕ C₁ = P₁' ⊕ C₁'**

or

**P₁ ⊕ C₁ = P₁' ⊕ C₁'**

#### 3. Exploit and get the flag

With that in mind, now I code the exploit tool as follow. As I'm so lazy, I don't code the full exploit, so I change the cookies value manually through Burp Suite:

```python
from Crypto import Random
from Crypto.Cipher import AES
from base64 import b64decode, b64encode

def xor(a: bytes, b: bytes):
    return bytes([_a ^ _b for _a, _b in zip(a, b)])

iv = Random.new().read(AES.block_size)
key = Random.new().read(AES.block_size)

cipher = AES.new(key, AES.MODE_CFB, iv)

username = 'thangpd11'
role = 1
usernamebytes = username.encode('utf-8')
usernamelen = len(usernamebytes)
plainbytes = len(usernamebytes).to_bytes(2, "little") + usernamebytes + role.to_bytes(1, "little")

cipherbytes = b64decode(b'tzRxbyN82l8uJK06ZdSQSI+kc1x1vnjPTLXL6w==') #authtoken in cookies value
iv = cipherbytes[:AES.block_size]
cipherbytes = cipherbytes[AES.block_size:]

new_role = 0
plainbytes_new = len(usernamebytes).to_bytes(2, "little") + usernamebytes + new_role.to_bytes(1, "little")

cipherbytes_new = xor(xor(plainbytes_new, plainbytes), cipherbytes)

ciphertext_new = b64encode(iv + cipherbytes_new)
print(ciphertext_new)
```

The new authtoken is **tzRxbyN82l8uJK06ZdSQSI+kc1x1vnjPTLXL6g==**. Let's submit it and get flag.

![image](https://user-images.githubusercontent.com/61876488/138590429-e19a91c7-2284-45d6-9621-d56a017b9022.png)
