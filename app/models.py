import ldap3
from . import db
from flask_login import UserMixin


def get_ldap_connection():
    # conn = ldap.initialize(app.config['LDAP_PROVIDER_URL'])
    # conn = ldap.initialize('ldap://ldap-master.certesnetworks.com:389/')
    ldap_server = ldap3.Server(
        'ldap-server.certesnetworks.com', port=389)
    return ldap_server


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, username, password):
        self.username = username

    @staticmethod
    def try_login(username, password):
        try:
            # ldap_bind_dn = 'uid={},ou=Users,dc=certesnetworks,dc=com'.format(
            #     username)
            # ldap_server = get_ldap_connection()
            LDAP_BIND_DN = 'uid={},ou=Users,dc=certesnetworks,dc=com'.format(
                username)
            search_filter = '(&(CN=engineering)(uniqueMember=uid={},ou=users,dc=certesnetworks,dc=com))'.format(
                username)
            LDAP_BASE = 'ou=groups,dc=certesnetworks,DC=com'
            conn = ldap3.Connection('ldap-master.certesnetworks.com',
                                    LDAP_BIND_DN, password,
                                    auto_bind=True)
            print("Got conn")
            result = conn.search(LDAP_BASE, search_filter)
            # ldap_server.simple_bind_s(ldap_bind_dn, password)
            if not result:
                raise Exception("Invalid Username/Password")
        except Exception as e:
            print(str(e))
            raise Exception(str(e))

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    # def get_id(self):
    #     return unicode(self.id)
