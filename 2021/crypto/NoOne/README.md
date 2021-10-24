# NoOne

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
