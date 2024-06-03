DATA_USERS_PATH = "./data/users/data_users.dat"
COURSES_PATH = "./data/courses/data_courses.dat"
DATA_AMMOUNT_USER = "./data/users/id_u.dat"
DATA_AMMOUNT_COURSE = "./data/courses/id_c.dat"
DATA_COURSES_OWNER = "./data/courses/courses_owner.dat"
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
            try:
                id = int(open(DATA_AMMOUNT_USER, 'r').read().rstrip()[0]) + 1
            except:
                id = 1
            open(DATA_COURSES_OWNER, 'a+').write("%s\n%s\n" % (id, ""))
            if data[2]:
                new_data = Teacher(id, type, data[0], data[1], data[2], data[3], data[4])
            else:
                new_data = Student(id, type, data[0], data[1], data[2], data[3], data[4])
            self.__data_users.append(new_data)
            open(DATA_AMMOUNT_USER, 'w').write(str(id))
            open(DATA_USERS_PATH,'a+',encoding='utf-8').write("%s\n%s\n%s\n%s\n%s\n%s\n" % (id, data[0], data[1], data[2], data[3], "•".join(data[4])))
        return

    def fetch_data(self, type):
        """
            fetch_data(type: bool): get data from data file and add into user list/ course list
            user: [id, 1, accountname, password, username, role]
            course: [id, 0, title, author, description, price, oldprice, thumbnails url]
        """
        if type:
            data = open(DATA_USERS_PATH, 'r', encoding='utf-8').read().rstrip().split("\n")
            data = [data[i:i+6] for i in range(0,len(data), 6)]
            for item in data:
                if item[4]:
                    self.__data_users.append(Teacher(item[0], type, item[1], item[2], item[3], item[4], item[5].split("•")))
                else:
                    self.__data_users.append(Student(item[0], type, item[1], item[2], item[3], item[4], item[5].split("•")))
        else:
            data = open(COURSES_PATH, 'r', encoding="utf-8").read().rstrip().split("\n")
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
        
    def update_data(self, data_type, data):
        """
            update_data(data_type): update list of users or courses based on [data_type]
        """
        if data_type:
            with open(DATA_USERS_PATH, 'w', encoding='utf-8') as f:
                for i in list(data.keys()):
                    f.write(f"{data[i][0]}\n")
                    f.write(f"{i}\n")
                    f.write(f"{data[i][1]}\n")
                    f.write(f"{data[i][2]}\n")
                    f.write(f"{data[i][3]}\n")
                    f.write(f"{data[i][4]}\n")

    def find_data(self, typeData, id):
        """
            class find_data: find data from data users [1] and data courses [0] based on [typeData] and [id].
            If id = -1, find accountname of users
        """
        if type(id) == str:
            items = []
            for item in self.__data_users:
                items.append(item.get_this_user()["accountname"])
            return [i for i in self.__data_users][items.index(id)]
        elif typeData == 1:
            for item in self.__data_users:
                if int(item.get_this_user()["id"]) == id:
                    return item
        elif typeData == 0:
           for item in self.__data_courses:
                if int(item.get_this_course()["id"]) == id:
                    return item
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
        return {
                "id":self.id,
                "title":self.title, 
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
        return {
            "id":self.id,
            "accountname":self.__accountname,
            "password":self.__password,
            "username":self.__username,
            "role":self.__role
        }

class Teacher(User):
    """
        class Teacher: generate a data storaging bank_account (-> Bank) then inherites id, data type, accountname, password, username and role
        method: 
            __init__(id, data_type, accountname, password, username, role, bank_account)
            
            get_bank()
    """
    class Bank:
        """
            class Bank: generate a series data for bank account
            method:
                __init__(bank_name, cardholder, cardnumber)
        """
        def __init__(self, bank_name, cardholder, cardnumber):
            """
                __init__(bank_name, cardholder, cardnumber): initiate attributes
            """
            self.bank_name = bank_name
            self.cardholder = cardholder
            self.cardnumber = cardnumber

    def __init__(self, id, data_type, accountname, password, username, role, bank_account):
        """
            __init__(id, data_type, accountname, password, username, role, bank_account): inherites and initiates attributes
        """
        super().__init__(id, data_type, accountname, password, username, role)
        self.bank_account = Teacher.Bank(bank_account[0], bank_account[1], bank_account[2])
        self.data_courses = open(DATA_COURSES_OWNER, 'r').read().split("\n")[:-1]
        self.data_courses = {self.data_courses[i]:[int(j) for j in self.data_courses[i+1].split()] for i in range(0,len(self.data_courses),2)}[id]
    
    def get_bank(self):
        """
            get_bank(): return a dictionary of Bank information
        """
        return {
            "bank_name": self.bank_account.bank_name,
            "cardholder": self.bank_account.cardholder,
            "cardnumber": self.bank_account.cardnumber
        }
    

class Student(User):
    """
        class Student(User): generate a data storaging more_information then inherites id, data type, accountname, password, username and role
        method: 
            __init__(id, data_type, accountname, password, username, role, more_information)
            
    """
    def __init__(self, id, data_type, accountname, password, username, role, more_information):
        """
            __init__(id, data_type, accountname, password, username, role, more_information): inherites and initiates attributes
        """
        super().__init__(id, data_type, accountname, password, username, role)
        data_courses = open(DATA_COURSES_OWNER, 'r').read().split("\n")[:-1]
        data_courses = {data_courses[i]:data_courses[i+1] for i in range(0,len(data_courses),2)}[id]
        





