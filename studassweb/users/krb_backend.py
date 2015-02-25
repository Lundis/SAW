try:
    # Linux
    import kerberos
except ImportError:
    # Windows
    import kerberos_sspi as kerberos

import logging

from django.conf import settings
from django.contrib.auth.backends import ModelBackend

from base.utils import generate_random_password

from .models import UserExtension, KerberosServer, KerberosLink

logger = logging.getLogger(__name__)


# Subclasses ModelBackend for permission support
class KrbBackend(ModelBackend):
    """
    Django Authentication backend using Kerberos for password checking.
    Originally based on https://github.com/02strich/django-auth-kerberos

    Modified to create UserExtensions for new users
    """

    def authenticate(self, username=None, password=None, **kwargs):
        """

        :param username: user@host.com. host.com uniquely decides the krb server
        :param password:
        :param kwargs: Nothing
        :return:
        """
        logger.debug("calling kerberos authenticate")
        if not "@" in username:
            return None
        username, hostname = username.split("@")
        # Check if a server with the specified hostname exists
        try:
            server = KerberosServer.objects.get(hostname=hostname)
            logger.debug("Found kerberos server")
        except KerberosServer.DoesNotExist:
            return None
        # Check if the credentials are correct
        if not self.check_password(server, username, password):
            #authentication failed
            return None
        logger.debug("Kerberos auth successful")
        # Next check if the user already exists
        try:
            krblink = KerberosLink.objects.get(server=server, username=username)
            logger.debug("kerberos user already exists")
            return krblink.user.user
        except KerberosLink.DoesNotExist:
            logger.info("Creating new User (%s)" % username)
            # Create a new user
            user_ext = UserExtension.create_user(username=username,
                                                 password=generate_random_password(),
                                                 email=username + "@" + hostname,
                                                 first_name="",
                                                 last_name="")
            # Not all fields have been filled out for this user, so mark him/her as incomplete
            user_ext.incomplete = True
            # Link the kerberos account to the user account
            KerberosLink.objects.create(user=user_ext, server=server, username=username)
            return user_ext.user

    @staticmethod
    def check_password(server, username, password):
        try:
            kerberos.checkPassword(username.lower(), password, server.service, server.realm)
            return True
        except kerberos.BasicAuthError as e:
            logger.info("Wrong krb credentials authentication (user %s): %s" % (username, e))
        except Exception as e:
            logger.error("Failure during krb authentication: %s", e)
            # for all other exceptions also deny access
            return False