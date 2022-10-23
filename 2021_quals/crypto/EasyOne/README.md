# EasyOne

### Author: [Phung Duc Thang](https://github.com/thangpd3160)

A challenge about digital certificate problem, just the basic things. Full source code can found at [here](https://github.com/FPTU-Ethical-Hackers-Club/SVATTT/tree/main/2021/crypto/EasyOne/source).

![image](https://user-images.githubusercontent.com/61876488/138579352-157d38db-e464-432d-a527-f46f64650f46.png)

### 1. Challenge analysis

Read the source code, I figured out that there is a route `/flag` which will tell us the flag of this challenge, but only admin can access content of flag:

```python
@app.route("/flag")
@login_required
def flag():
    flag = "You are not admin"
    if session["role"] == ROLE_ADMIN:
        flag = "ASCIS{xxxxxx}"
    return render_template('flag.html', flag=flag)
```

There is a register function, but we can't register as admin. It just allow us to register as a normal user:

```
@app.route("/register", methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        role = ROLE_USER

        if not username or not password:
            flash('Username and Password is required!')
        else:
            do_register(username, password, email, role)

            return redirect(url_for('login'))

    return render_template('register.html')
```

However, examine carefully the source code, I found that there is another way to login without admin account. It's the `/logincert` route:

```python
# This function only for admin
@app.route("/logincert", methods=('GET', 'POST'))
def logincert():
    if request.method == 'POST':
        username = None
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            split_tup = os.path.splitext(uploaded_file.filename)
            if split_tup[1] != ".pem":
                flash('Cert file is invalid')
                return render_template('logincert.html')
            else:    
                username = validate_certificate(uploaded_file)

        if username is None:
            flash('Login cert is invalid!')
            return render_template('logincert.html')
        else:    
            session["username"] = username
            session["role"] = ROLE_ADMIN

            return redirect(url_for('index'))

    return render_template('logincert.html')
 ```
 
 Notice the line code `username = validate_certificate(uploaded_file)`. Follow the code, it leads us to `verify_certificate_chain(cert_pem, trusted_certs)` function in file [certutils.py](https://github.com/thangpd3160/ASCIS_2021/blob/main/EasyOne/certutils.py).
 
 ```python
 def verify_certificate_chain(cert_pem, trusted_certs):
    certificate = crypto.load_certificate(crypto.FILETYPE_PEM, cert_pem)
    # parse ceritificate information
    clientcert = CertInfo(certificate)
    # get subject common name
    subject = clientcert.subject_cn
    issuer = clientcert.issuer_cn
    # Check if subject is admin user
    if subject != "admin":
        raise Exception("Not trusted user")
    # validate issuer 
    if issuer != "ca":
        raise Exception("Not trusted ca")
    thumbprint = clientcert.digest_sha256.decode('utf-8')
    #TODO: validate thumbprint
    #Create a certificate store and add your trusted certs
    try:
        store = crypto.X509Store()
        # Assuming the certificates are in PEM format in a trusted_certs list
        for _cert in trusted_certs:
            cert_file = open(_cert, 'r')
            cert_data = cert_file.read()
            client_certificate = crypto.load_certificate(crypto.FILETYPE_PEM, cert_data)
            store.add_cert(client_certificate)
        # Create a certificate context using the store 
        store_ctx = crypto.X509StoreContext(store, certificate)
        # Verify the certificate signature, returns None if it can validate the certificate
        store_ctx.verify_certificate()
        # verify success
        return subject
    except Exception as e:
        print("[+] Debug certificate validation failed")
        return False
 ```

For the one that does not really understand the detail code of digital certificate as me, I have been overwhelmed and confused a little bit. However, just pay attention to the output and the requirement in 2 `if` statements, I can draw out the 2 following conclusions:
- There are 2 requirements to successfully login by certificate: the subject must be `admin` and the issuers must be `ca`. It's really easy~~
- After passing these 2 requirements, it return us `subject`, which is actually the admin. Now we will a `admin` session, thus get the flag.
So, let's go on to create a digital ceritificate.

### 2. Create digital certificate

I use **openssl** on Kali Linux machine to create digital certiifcate. The ideas is simple:

- Create a certificate owned by `ca` \rightarrow→ **subject = ca** and **issuer = ca**.
- Create another certificate owned by `admin` \rightarrow→ **subject = admin** and **issuer = admin**.
- Sign the second certificate by the first certificate \rightarrow→ **subject = admin** and **issuer = ca**.

For the technical details, follow step by step as following:

- Create a RSA key pair for `ca` certificate:

```
thangpdhe141354@kali:~$ openssl genrsa -out ca.key 2048
Generating RSA private key, 2048 bit long modulus (2 primes)
.............+++++
...........................+++++
e is 65537 (0x010001)
```

- Create a certificate owned by `ca`. Left all other blanks and fill `Common Name` as `ca`:

```
thangpd3160@kali:~$ openssl req -new -x509 -days 1826 -key ca.key -out ca.crt
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:
State or Province Name (full name) [Some-State]:
Locality Name (eg, city) []:
Organization Name (eg, company) [Internet Widgits Pty Ltd]:
Organizational Unit Name (eg, section) []:
Common Name (e.g. server FQDN or YOUR name) []:ca
Email Address []:
```

After create, you can see the CA look like this:

![image](https://user-images.githubusercontent.com/61876488/138579930-7bd4845f-9f97-4618-9b32-0e60b9649710.png)

- Create a RSA key pair for admin certificate:

 ```
thangpd3160@kali:~$openssl genrsa -out ia.key 2048
Generating RSA private key, 2048 bit long modulus (2 primes)
.....+++++
.............+++++
e is 65537 (0x010001)
 ```
 
 - Create a certificate owned by `admin`. Left all other blanks and fill `Common Name` as `admin`:

```
thangpd3160@kali:~$ openssl req -new -key ia.key -out ia.csr
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:
State or Province Name (full name) [Some-State]:
Locality Name (eg, city) []:
Organization Name (eg, company) [Internet Widgits Pty Ltd]:
Organizational Unit Name (eg, section) []:
Common Name (e.g. server FQDN or YOUR name) []:admin
Email Address []:

Please enter the following 'extra' attributes
to be sent with your certificate request
A challenge password []:
An optional company name []:
```

The created certificate will look as following:

![image](https://user-images.githubusercontent.com/61876488/138580005-6c165763-ab39-4370-b9af-b0b89fc7dac4.png)

- Sign the second certificate by the first certificate:

```
thangpd3160@kali:~$ openssl x509 -req -days 730 -in ia.csr -CA ca.crt -CAkey ca.key -set_serial 01 -out ia.crt
Signature ok
subject=C = AU, ST = Some-State, O = Internet Widgits Pty Ltd, CN = admin
Getting CA Private Key
```

The signed certificate will look as following:

![image](https://user-images.githubusercontent.com/61876488/138580048-029a51e4-7400-4524-972a-307567318389.png)

- Finally, convert the certificate to .pem format to fit the code requirement:

```
thangpd3160@kali:~$ openssl x509 -in ia.crt -out ia.pem -outform PEM
```

### 3. Submit the digital certificate and get the flag

Submit file ia.pem to server:

![image](https://user-images.githubusercontent.com/61876488/138580152-2c8d5c49-9a00-4b7d-9c16-b74f9f023b6a.png)

Logon!

![image](https://user-images.githubusercontent.com/61876488/138580165-9afd7f4f-707b-4ce8-914e-28c0547c8039.png)

And get the flag!

![image](https://user-images.githubusercontent.com/61876488/138580195-0e67d5bf-47a7-4e4e-9943-58877fc9a7f6.png)

