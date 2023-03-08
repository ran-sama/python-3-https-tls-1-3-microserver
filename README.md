# python3-https-tls1-3-microserver
Threaded python3 HTTPS+TLS1.3 server w/ CryptCheck & SSL Labs 100% A+ rating.
```diff
!~ QuickStart ~!
```
[Click for setup instructions and guide](https://github.com/ran-sama/python3-https-tls1-3-microserver#setup-instructions-and-guide)
```diff
!~ QuickStart ~!
```
![alt text](https://raw.githubusercontent.com/ran-sama/python3_https_tls1_2_microserver/master/images/tls13_tls12_mixed_mode_new.png)
![alt text](https://raw.githubusercontent.com/ran-sama/python3_https_tls1_2_microserver/master/images/cryptcheck.png)
![alt text](https://raw.githubusercontent.com/ran-sama/python3_https_tls1_2_microserver/master/images/observatory_rating_new.png)

## TLS1.3 fully supported on OpenSSL 1.1.1a and higher

(Optional step for extra security) To disable the single AES128 cipher please edit your OpenSSL config:
```
sudo nano /etc/ssl/openssl.cnf
```

By adding this line at the very end:
```
Ciphersuites = TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256
```


So it will look like this:
```
[system_default_sect]
MinProtocol = TLSv1.2
CipherString = DEFAULT@SECLEVEL=2
Ciphersuites = TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256
```

This workaround is still required until either Python >3.7 or OpenSSL will fix the set_ciphers() function:
```
https://docs.python.org/3.8/library/ssl.html#tls-1-3
```

## Setup instructions and guide

The setup is straightforward and easy, as you only need certain directories and files to be present.

In the example we use:
```
/home/ran/.acmeweb/
/home/ran/.acme.sh/
/media/kingdian/server_pub/
```
And the servers:
```
port80_redirector_acme_ready.py
server-TLS1_3_ready.py
```
Feel free to just call them redirector.py and server.py for ease of use.
* Remember: You need superuser rights to bring up ports 80 and 443. 

In the beginning you probably will lack any form of certificates for your server to load into the openssl module of python.
Whilst in your home directory:
```
mkdir .acmeweb
```
We use this directory to do acme-challenges.
Also make appropriate changes to redirector.py:
```
MYSERV_ACMEWEBDIR = "/home/ran/.acmeweb"
```
For this we will bring up the redirector with python3 and make sure port 80 is forwarded in your WAN.
* Note: The redirector is only able to perform HTTP(301) redirects and answer GET and HEAD requests for the upcoming acme-challenge.

For the letsencrypt acme-challenge to work you also need the DNS entry of example.noip.me pointing to your servers IP.
Make yourself familiar with [acme.sh](https://github.com/acmesh-official/acme.sh) first and download it:

```
wget https://raw.githubusercontent.com/acmesh-official/acme.sh/master/acme.sh
chmod +x acme.sh
```
We run a shell one-liner to issue a certificate request, make appropriate changes according to your MYSERV_ACMEWEBDIR:
```
./acme.sh --issue -d example.noip.me --keylength ec-384 --accountkeylength 4096 -w /home/ran/.acmeweb --server letsencrypt --force
```
We want an EC-384 key, be able to authenticate us in future with a letsencrypt account key of 4096 bits and do the challenge in in the MYSERV_ACMEWEBDIR which you edited.

The acme.sh will inform you about the location where your key and fullchain files have been placed, like for the user "ran" it is:
```
/home/ran/.acme.sh/example.noip.me_ecc/fullchain.cer
/home/ran/.acme.sh/example.noip.me_ecc/example.noip.me.key
```

Make appropriate changes to server.py since your username will differ, please ignore the commented line:
```
MYSERV_WORKDIR = "/media/kingdian/server_pub"
#MYSERV_CLIENTCRT = "/home/ran/keys/client.pem"
MYSERV_FULLCHAIN = "/home/ran/.acme.sh/example.noip.me_ecc/fullchain.cer"
MYSERV_PRIVKEY = "/home/ran/.acme.sh/example.noip.me_ecc/example.noip.me.key"
```
* Note: Client certificates will prevent everyone from accessing your server, thus we leave them deactivated.

If all is configured correctly, bringing up server.py with python3 will make it serve all files located in MYSERV_WORKDIR using your private key and fullchain.

* Your future tasks: Set up an own cronjob to run every 90 days for auto-renewal of your certificates!

To help you with this I provide an example:
```
0 4 2 */2 * bash /home/ran/acme.sh --issue -d example.noip.me --keylength ec-384 --accountkeylength 4096 -w /home/ran/.acmeweb/ --server letsencrypt --force 1>/home/ran/acme_status.log 2>/home/ran/acme_error.log && sudo reboot
```
Do notice a system reboot is forced at the end, if you don't want this you can just restart the python server itself.
Please use a different day and time! I'm sure Let's entcrypt can handle the load to their servers, but randomize it a bit.

Every 2nd odd month:
[https://crontab.guru/#0_4_2_*/2_*](https://crontab.guru/#0_4_2_*/2_*)

Every 2nd even month:
[https://crontab.guru/#0_4_2_2-12/2_*](https://crontab.guru/#0_4_2_2-12/2_*)

## Automatic launching and cert renewal supported

https://github.com/ran-sama/python3-cert-renewer  
https://github.com/ran-sama/systemd-service-examples  


## License
Licensed under the WTFPL license.
