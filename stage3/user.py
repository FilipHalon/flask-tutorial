class User:
    def __init__(self, _id, username, password):
        # _id jest używane, żeby nie zacieniować magicznego id, metody wbudowanej pythona
        self.id = _id
        self.username = username
        self.password = password
