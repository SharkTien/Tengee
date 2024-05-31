DATA_USERS_PATH = "./data/users/data_users.dat"
COURSES_PATH = "./data/courses/data.dat"
DATA_AMMOUNT_USER = "./data/id_u.dat"
DATA_AMMOUNT_COURSE = "./data/id_c.dat"
class DataManager:
    """
    DataManager:
        Class DataManager initiates list users = [], list courses = [] with basic method
        method:
            + __init__()

            + fetch_data(type: bool)
            
            + insert_data(type:bool)
            
            + get_data(type:bool)
    """
    def __init__(self):
        """
            __init__(): initiates original variables and const value 
        """
        self.__data_users = []
        self.__data_courses = []

    def insert_data(self, type, data):
        """
            insert_data(type: bool, data: list): insert a data (user/ course based on [type]) into user list/ course list
            data is a list with format: [accountname, password, username, role]
        """
        if type:
            id = int(open(DATA_AMMOUNT_USER, 'r').read().rstrip()[0]) + 1
            new_data = User(id, type, data[0], data[1], data[2], data[3])
            self.__data_users.append(new_data)
            open(DATA_AMMOUNT_USER, 'w').write(str(id))
            open(DATA_USERS_PATH,'a+',encoding='utf-8').write("%s\n%s\n%s\n%s\n%s\n" % (id, data[0], data[1], data[2], data[3]))
        return

    def fetch_data(self, type):
        """
            fetch_data(type: bool): get data from data file and add into user list/ course list
            user: [id, 1, accountname, password, username, role]
            course: [id, 0, title, author, description, price, oldprice, thumbnails url]
        """
        if type:
            data = open(DATA_USERS_PATH, 'r', encoding='utf-8').read().split("\n")[:-1]
            data = [data[i:i+5] for i in range(0,len(data), 5)]
            for item in data:
                self.__data_users.append(User(item[0], type, item[1], item[2], item[3], item[4]))
            return
        else:
            data = open(COURSES_PATH, 'r', encoding="utf-8").read().split("\n")[:-1]
            data = [data[i:i+7] for i in range(0, len(data), 7)]
            for item in data:
                self.__data_courses.append(Course(item[0], type, item[1], item[2], item[3], item[4], item[5], item[6]))
            return
        
    def get_data(self, data_type):
        """
            get_data(data_type): return list of users or courses based on [data_type]
        """
        if data_type:
            return self.__data_users
        else:
            return self.__data_courses
        
class Data:
    """
        class Data: generate a data storaging id and data_type, which is the familiar attributes of Course and User data.
        method:
            __init__(id, data_type)
    """
    def __init__(self, id, data_type):
        """
            __init__(id, data_type): initiates original variables
        """
        self.id = id
        self.data_type = data_type

class Course(Data):
    """
        class Course(Data): generate a data storaging title, author, description, price, oldprice and image then inherites id and data type
        method: 
            __init__(id, data_type, title, author, description, price, oldprice, image)
            
            get_this_course()
    """
    def __init__(self, id, data_type, title, author, description, price, oldprice, image):
        """           
            __init__(id, data_type, title, author, description, price, oldprice, image): initiates original variables and inherites variables from parent classes
        """
        super().__init__(id, data_type)
        self.title = title
        self.author = author
        self.description = description
        self.price = price
        self.oldprice = oldprice
        self.image = image
    def get_this_course(self):
        """
            get_this_course(): return a dictionary with keys including: title, author, description, price, oldprice and image
        """
        return {"title":self.title, 
                "author":self.author, 
                "description":self.description,
                "price":self.price,
                "oldprice":self.oldprice,
                "image":self.image}
    
class User(Data):
    """
        class User(Data): generate a data storaging accountname, password, username and role then inherites id and data type
        method: 
            __init__(id, data_type, accountname, password, username, role)
            
            get_this_user()
    """
    def __init__(self, id, data_type, accountname, password, username, role):
        """
            __init__(id, data_type, accountname, password, username, role): initiates original variables and inherites variables from parent classes
        """
        super().__init__(id, data_type)
        self.__accountname = accountname
        self.__password = password
        self.__username = username
        self.__role = role
        
    def get_this_user(self):
        """
            get_this_user(): return two value accountname, [password, username, role]
        """
        return self.__accountname,[self.__password, self.__username, self.__role]
    
