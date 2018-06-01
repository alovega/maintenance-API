users={}
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




class Request(User):
    request_details = {}
    count=1
    def __init__(self,request_title,request_description,request_category):

        self.request_title = request_title
        self.request_description = request_description
        self.request_category = request_category
        self.request_id = Request.count
        Request.count += 1
    def add_request(self):
        self.request_details[self.request_id]=[self.request_title,self.request_description,self.request_category]

        return self.request_details

    
