#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, ssl
from socketserver import ThreadingMixIn
from http.server import SimpleHTTPRequestHandler, HTTPServer

MYSERV_WORKDIR = "/media/kingdian/server_pub"
#MYSERV_CLIENTCRT = "/home/ran/keys/client.pem"
MYSERV_FULLCHAIN = "/home/ran/.acme.sh/example.noip.me_ecc/fullchain.cer"
MYSERV_PRIVKEY = "/home/ran/.acme.sh/example.noip.me_ecc/example.noip.me.key"

global sslcontext
sslcontext = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
sslcontext.options |= ssl.OP_NO_TLSv1
sslcontext.options |= ssl.OP_NO_TLSv1_1
#placeholder
sslcontext.protocol = ssl.PROTOCOL_TLSv1_2
#sslcontext.verify_mode = ssl.CERT_REQUIRED
sslcontext.set_ciphers("ECDHE-ECDSA-AES256-GCM-SHA384 ECDHE-ECDSA-CHACHA20-POLY1305")
sslcontext.set_ecdh_curve("secp384r1")
#sslcontext.load_verify_locations(MYSERV_CLIENTCRT)
sslcontext.load_cert_chain(MYSERV_FULLCHAIN, MYSERV_PRIVKEY)

class HSTSHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Strict-Transport-Security", "max-age=63072000; includeSubDomains; preload")
        self.send_header("Content-Security-Policy", "default-src 'self'")
        #self.send_header("Content-Security-Policy", "default-src 'none'; img-src 'self'; script-src 'self'; style-src 'self'; frame-ancestors 'self'; base-uri 'self'; form-action 'self'; object-src 'none'; require-trusted-types-for 'script'")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "SAMEORIGIN")
        self.send_header("X-XSS-Protection", "1; mode=block")
        self.send_header("Referrer-Policy", "no-referrer")
        SimpleHTTPRequestHandler.end_headers(self)

HSTSHandler.extensions_map['.avif'] = 'image/avif'
HSTSHandler.extensions_map['.webp'] = 'image/webp'

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True

def main():
    try:
        os.chdir(MYSERV_WORKDIR)#auto-change working directory
        SimpleHTTPRequestHandler.sys_version = "https://github.com/ran-sama"#display custom Python system version
        SimpleHTTPRequestHandler.server_version = "https://github.com/ran-sama"#display custom server software version
        my_server = ThreadedHTTPServer(('0.0.0.0', 443), HSTSHandler)
        my_server.socket = sslcontext.wrap_socket(my_server.socket, do_handshake_on_connect=False, server_side=True)
        print('Starting server, use <Ctrl-C> to stop')
        my_server.serve_forever()

    except KeyboardInterrupt:
        print(' received, shutting down server')
        my_server.shutdown()

if __name__ == '__main__':
    main()
