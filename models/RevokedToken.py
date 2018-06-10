from models.models import MaintenanceDb


class RevokedTokenModel (MaintenanceDb):
    def __init__(self):
        pass

    def add_token(self,jti):
        db = MaintenanceDb()
        db.add_token(jti)

    @classmethod
    def is_jti_blacklisted(self,jti):
        db = MaintenanceDb()
        cur = db.getConnection().cursor()
        result = cur.execute("SELECT id,jti from revoked_tokens where jti = %(jti)s ", {'jti': jti})
        return bool(result)
