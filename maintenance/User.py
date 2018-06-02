class User(object):
    count = 0
    users_details = {}
    def __init__(self,name,username,password):
        self.name=name
        self.username=username
        self.password=password
        self.id = User.count
        User.count += 1
    def add_user(self):
        self.users_details[self.id]=[self.name,self.username,self.password]