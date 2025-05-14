import ssl
from django.core.mail.backends.smtp import EmailBackend

class UnverifiedEmailBackend(EmailBackend):
    """
    Email backend que desactiva la verificación de certificados SSL/TLS.
    Únicamente debe usarse en entornos de desarrollo.
    """
    def open(self):
        if self.connection:
            return False  

        local_hostname = getattr(self, 'local_hostname', None)
        timeout = getattr(self, 'timeout', None)
        ssl_keyfile = getattr(self, 'ssl_keyfile', None)
        ssl_certfile = getattr(self, 'ssl_certfile', None)

        try:
            if self.use_ssl:
                context = ssl._create_unverified_context()
                params = {
                    'host': self.host,
                    'port': self.port,
                    'local_hostname': local_hostname,
                    'timeout': timeout,
                    'context': context,
                }
                if ssl_keyfile is not None:
                    params['keyfile'] = ssl_keyfile
                if ssl_certfile is not None:
                    params['certfile'] = ssl_certfile

                self.connection = self.connection_class(**params)
            else:
                self.connection = self.connection_class(
                    self.host,
                    self.port,
                    local_hostname=local_hostname,
                    timeout=timeout,
                )
                if self.use_tls:
                    context = ssl._create_unverified_context()
                    starttls_params = {'context': context}
                    if ssl_keyfile is not None:
                        starttls_params['keyfile'] = ssl_keyfile
                    if ssl_certfile is not None:
                        starttls_params['certfile'] = ssl_certfile

                    self.connection.starttls(**starttls_params)
            if self.username and self.password:
                self.connection.login(self.username, self.password)
            return True
        except Exception:
            if not self.fail_silently:
                raise
