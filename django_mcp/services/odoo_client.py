import xmlrpc.client
import ssl
import os
from django.conf import settings

class OdooClient:
    """
    Robust XML-RPC Client for Odoo 18.0.
    Handles connection pooling, SSL context, and authentication.
    """

    def __init__(self):
        self.url = os.getenv('ODOO_URL', 'http://localhost:8069')
        self.db = os.getenv('ODOO_DB', 'odoo')
        self.username = os.getenv('ODOO_USERNAME', 'admin')
        self.password = os.getenv('ODOO_PASSWORD', 'admin')
        self.uid = None

        # SSL Context for HTTPS connections
        self._ssl_context = ssl.create_default_context()
        self._ssl_context.check_hostname = False
        self._ssl_context.verify_mode = ssl.CERT_NONE

        self.common = xmlrpc.client.ServerProxy(
            f'{self.url}/xmlrpc/2/common',
            context=self._ssl_context
        )
        self.models = xmlrpc.client.ServerProxy(
            f'{self.url}/xmlrpc/2/object',
            context=self._ssl_context
        )

    def authenticate(self):
        """
        Authenticate and cache UID.
        """
        if not self.uid:
            self.uid = self.common.authenticate(
                self.db,
                self.username,
                self.password,
                {}
            )
            if not self.uid:
                raise Exception("Odoo Authentication Failed")
        return self.uid

    def execute_kw(self, model, method, args=None, kwargs=None):
        """
        Wrapper for execute_kw with automatic authentication.
        """
        uid = self.authenticate()
        args = args or []
        kwargs = kwargs or {}

        try:
            return self.models.execute_kw(
                self.db,
                uid,
                self.password,
                model,
                method,
                args,
                kwargs
            )
        except xmlrpc.client.Fault as e:
            # Re-raise as clean application error
            raise Exception(f"Odoo Fault {e.faultCode}: {e.faultString}")
        except Exception as e:
            raise Exception(f"XML-RPC Connection Error: {str(e)}")
