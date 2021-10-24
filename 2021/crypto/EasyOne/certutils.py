import base64
import hashlib
from logging import NullHandler, root
import sys
import os
from Crypto import Random
from Crypto.Cipher import AES
from werkzeug.exceptions import abort
from functools import wraps
from flask import Flask, render_template, request, url_for, flash, redirect, session, make_response, g
import mysql.connector
import werkzeug
import ssl
import OpenSSL
from OpenSSL import crypto
import datetime

class CertInfo:
    
    def __init__(
        self,
        cert=None,
        ):
        self.cert = cert
    def decode_x509name_obj(self, o):
        parts = []
        for c in o.get_components():
            parts.append(c[0].decode('utf-8') + '=' + c[1].decode('utf-8'))
        return ', '.join(parts)
    def cert_date_to_gmt_date(self, d):
        return datetime.datetime.strptime(d.decode('ascii'), '%Y%m%d%H%M%SZ')
    def cert_date_to_gmt_date_string(self, d):
        return self.cert_date_to_gmt_date(d).strftime("%Y-%m-%d %H:%M:%S GMT")
    def get_item(self, item, extension=None, return_as=None, algo=None):
        try:
            if item == 'subject':
                return self.decode_x509name_obj(self.cert.get_subject())

            elif item == 'subject_o':
                return self.cert.get_subject().O.strip()

            elif item == 'subject_cn':
                return self.cert.get_subject().CN.strip()

            elif item == 'extensions':
                ext_count = self.cert.get_extension_count()
                if extension is None:
                    ext_infos = []
                    for i in range (0, ext_count):
                        ext = self.cert.get_extension(i)
                        ext_infos.append(ext.get_short_name().decode('utf-8'))
                    return ext_infos

                for i in range (0, ext_count):
                    ext = self.cert.get_extension(i)
                    if extension in str(ext.get_short_name()):
                        return ext.__str__().strip()
                return None

            elif item == 'version':
                return self.cert.get_version()

            elif item == 'pubkey_type':
                pk_type = self.cert.get_pubkey().type()
                if pk_type == crypto.TYPE_RSA:
                    return 'RSA'
                elif pk_type == crypto.TYPE_DSA:
                    return 'DSA'
                return 'Unknown'

            elif item == 'pubkey_pem':
                return crypto.dump_publickey(crypto.FILETYPE_PEM, self.cert.get_pubkey()).decode('utf-8')

            elif item == 'serial_number':
                return self.cert.get_serial_number()

            elif item == 'not_before':
                not_before = self.cert.get_notBefore()
                if return_as == 'string':
                    return self.cert_date_to_gmt_date_string(not_before)
                return self.cert_date_to_gmt_date(not_before)

            elif item == 'not_after':
                not_after = self.cert.get_notAfter()
                if return_as == 'string':
                    return self.cert_date_to_gmt_date_string(not_after)
                return self.cert_date_to_gmt_date(not_after)

            elif item == 'has_expired':
                return self.cert.has_expired()

            elif item == 'issuer':
                return self.decode_x509name_obj(self.cert.get_issuer())

            elif item == 'issuer_o':
                return self.cert.get_issuer().O.strip()

            elif item == 'issuer_cn':
                return self.cert.get_issuer().CN.strip()

            elif item == 'signature_algorithm':
                return self.cert.get_signature_algorithm().decode('utf-8')

            elif item == 'digest':
                # ['md5', 'sha1', 'sha256', 'sha512']
                return self.cert.digest(algo)

            elif item == 'pem':
                return crypto.dump_certificate(crypto.FILETYPE_PEM, self.cert).decode('utf-8')

            else:
                return None

        except Exception as e:
            # logger.error('item = {}, exception, e = {}'.format(item, e))
            return None
    @property
    def subject(self):
        return self.get_item('subject')
    @property
    def subject_o(self):
        return self.get_item('subject_o')
    @property
    def subject_cn(self):
        return self.get_item('subject_cn')
    @property
    def subject_name_hash(self):
        return self.get_item('subject_name_hash')
    @property
    def extension_count(self):
        return self.get_item('extension_count')
    @property
    def extensions(self):
        return self.get_item('extensions')
    @property
    def extension_basic_constraints(self):
        return self.get_item('extensions', extension='basicConstraints')
    @property
    def extension_subject_key_identifier(self):
        return self.get_item('extensions', extension='subjectKeyIdentifier')
    @property
    def extension_authority_key_identifier(self):
        return self.get_item('extensions', extension='authorityKeyIdentifier')
    @property
    def extension_subject_alt_name(self):
        return self.get_item('extensions', extension='subjectAltName')
    @property
    def version(self):
        return self.get_item('version')
    @property
    def pubkey_type(self):
        return self.get_item('pubkey_type')
    @property
    def pubkey_pem(self):
        return self.get_item('pubkey_pem')
    @property
    def serial_number(self):
        return self.get_item('serial_number')
    @property
    def not_before(self):
        return self.get_item('not_before')
    @property
    def not_before_s(self):
        return self.get_item('not_before', return_as='string')
    @property
    def not_after(self):
        return self.get_item('not_after')
    @property
    def not_after_s(self):
        return self.get_item('not_after', return_as='string')
    @property
    def has_expired(self):
        return self.get_item('has_expired')
    @property
    def issuer(self):
        return self.get_item('issuer')
    @property
    def issuer_o(self):
        return self.get_item('issuer_o')
    @property
    def issuer_cn(self):
        return self.get_item('issuer_cn')
    @property
    def signature_algorithm(self):
        return self.get_item('signature_algorithm')
    @property
    def digest_sha256(self):
        return self.get_item('digest', algo='sha256')
    @property
    def pem(self):
        return self.get_item('pem')


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