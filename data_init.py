from path import *

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
            insert_data(type: bool, data: list): insert a data (user/ course based on [type]) into user list/ course list. Data is a list with format: [id, type, accountname, password, username, role]
        """
        if type:
            try:
                id = str(int(open(DATA_AMMOUNT_USER,'r').read().rstrip()) + 1)
            except:
                id = '1'
            open(DATA_COURSES_OWNER, 'a+').write("%s\n%s\n" % (id, ""))
            if data[2]:
                new_data = Teacher(id, type, data[0], data[1], data[2], data[3]) #id, type=1, accountname, password, username, role
            else:
                new_data = Student(id, type, data[0], data[1], data[2], data[3]) #id, type=1, accountname, password, username, role
            self.__data_users.append(new_data)
            open(DATA_AMMOUNT_USER, 'w').write(id)
            open(DATA_USERS_PATH,'a+',encoding='utf-8').write("%s\n%s\n%s\n%s\n%s\n" % (id, data[0], data[1], data[2], data[3]))
        else:
            try:
                id = self.getID()
            except:
                id = '1'
            new_data = Course(id, type, data[0], data[1], data[2], data[3], data[4], data[5]) 
            self.__data_courses.append(new_data)
            open(DATA_AMMOUNT_COURSE, 'w').write(str(id))
            open(DATA_COURSES_PATH,'a+',encoding='utf-8').write("%s\n%s\n%s\n%s\n%s\n%s\n%s\n" % (id, data[0], data[1], data[2], data[3], data[4], data[5]))
            d = open(DATA_COURSES_OWNER,'r').read().split("\n")[:-1]
            d = {d[i]:d[i+1].split() for i in range(0, len(d), 2)}
            d[data[1]].append(str(id))
            with open(DATA_COURSES_OWNER, 'w') as f:
                for key,value in d.items():
                    f.write("%s\n%s\n" % (key, " ".join(value)))

    def fetch_data(self, type):
        """
            fetch_data(type: bool): get data from data file and add into user list/ course list
            user: [id, 1, accountname, password, username, role]
            course: [id, 0, title, author, description, price, oldprice, thumbnails url]
        """
        if type:
            data = open(DATA_USERS_PATH, 'r', encoding='utf-8').read().rstrip().split("\n")
            if data != [""]:
                data = [data[i:i+5] for i in range(0,len(data), 5)]
                for item in data:
                    if item[4]:
                        self.__data_users.append(Teacher(item[0], type, item[1], item[2], item[3], item[4]))
                    else:
                        self.__data_users.append(Student(item[0], type, item[1], item[2], item[3], item[4]))
        else:
            data = open(DATA_COURSES_PATH, 'r', encoding="utf-8").read().rstrip().split("\n")
            if data != [""]:
                data = [data[i:i+7] for i in range(0, len(data), 7)]
                for item in data:
                    self.__data_courses.append(Course(item[0], type, item[1], item[2], item[3], item[4], item[5], item[6]))
            
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
                for i in data:
                    f.write(f"{i[0]}\n")
                    f.write(f"{i[2]}\n")
                    f.write(f"{i[3]}\n")
                    f.write(f"{i[4]}\n")
                    f.write(f"{i[5]}\n")
        else:
            with open(DATA_COURSES_PATH, 'w', encoding='utf-8') as f:
                for item in data:
                    i = item.get_this_course()
                    f.write(f"{i["id"]}\n")
                    f.write(f"{i["title"]}\n")
                    f.write(f"{i["author"]}\n")
                    f.write(f"{i["description"]}\n")
                    f.write(f"{i["price"]}\n")
                    f.write(f"{i["oldprice"]}\n")
                    f.write(f"{i["image"]}\n")
    
    def find_data(self, typeData, id):
        """
            find_data(typeData, id): find data from data users [1] and data courses [0] based on [typeData] and [id].
            If type = -1, find accountname of users
        """
        if typeData == -1:
            items = []
            for item in self.__data_users:
                items.append(item.get_this_user()["accountname"])
            return self.__data_users[items.index(id)]
        elif typeData == 1:
            for item in self.__data_users:
                if item.get_this_user()["id"] == id:
                    return item
        elif typeData == 0:
           for item in self.__data_courses:
                if item.get_this_course()["id"] == id:
                    return item
        elif typeData == 2:
            for item in self.__data_users:
                if item.get_this_user()["id"] == id:
                    return item.get_this_user()["username"]
        
    def delete(self, data, type):
        """
           delete(data, type): function delete account or course based on [type] (bool)
        """
        if type:
            d = []
            for item in self.get_data(1):
                if item.id != data.id:
                    i = item.get_this_user()
                    d.append([i["id"], 1, i["accountname"], i["password"], i["username"], i["role"]])
            self.update_data(1, d)
        else:
            d = []
            for item in self.get_data(0):
                if item.id != data.id:
                    d.append(item)
            self.__data_courses = d
            self.update_data(0, d)
            d = open(DATA_COURSES_OWNER,'r').read().split("\n")[:-1]
            d = {d[i]:d[i+1].split() for i in range(0, len(d), 2)}
            for i in d.keys():
                if data.id in d[i]:
                    d[i].remove(data.id)
            with open(DATA_COURSES_OWNER, 'w') as f:
                for key,value in d.items():
                    f.write("%s\n%s\n" % (key, " ".join(value)))
    
    def getID(self):
        """
            getID(self): create new object's ID 
        """
        try:
            return str(int(open(DATA_AMMOUNT_COURSE, 'r').read().rstrip()) + 1)
        except:
            return '1'

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
            self.data_courses: storing the courses created or purchased by users
        """
        super().__init__(id, data_type)
        self.__accountname = accountname
        self.__password = password
        self.__username = username
        self.__role = role
        self.update_courses()

    def update_courses(self):
        """
            update_courses(): update the list courses of users
        """
        self.data_courses = open(DATA_COURSES_OWNER, 'r').read().split("\n")[:-1]
        self.data_courses = {self.data_courses[i]:[j for j in self.data_courses[i+1].split() if j != ""] for i in range(0,len(self.data_courses),2)}[self.id]
        
    def get_this_user(self):
        """
            get_this_user(): return a dict {id, accountname, password, username, role}
        """
        return {
            "id":self.id,
            "accountname":self.__accountname,
            "password":self.__password,
            "username":self.__username,
            "role":self.__role
        }
    
    def change_password(self, data):
        """
            change_password(data): get access to password and change it
        """
        self.__password = data

    def change_username(self, data):
        """
            change_username(data): get access to username and change it
        """
        self.__username = data
        
class Teacher(User):
    """
        class Teacher: generate a data storaging bank_account (-> Bank) then inherites id, data type, accountname, password, username and role
        method: 
            __init__(id, data_type, accountname, password, username, role)
            
            get_bank()
    """
    class Bank:
        """
            class Bank: generate a series data for bank account
            method:
                __init__(bank_name, cardholder, cardnumber)
        """
        def __init__(self, bank_name, recipient, cardnumber):
            """
                __init__(bank_name, cardholder, cardnumber): initiate attributes
            """
            self.__bank_name = bank_name
            self.__recipient = recipient
            self.__cardnumber = cardnumber

        def get_this_bank(self):
            """
                get_this_bank(): return a dictionary of Bank information
            """
            return {
                "bank_name": self.__bank_name,
                "recipient": self.__recipient,
                "cardnumber": self.__cardnumber
            }
        
    def __init__(self, id, data_type, accountname, password, username, role):
        """
            __init__(id, data_type, accountname, password, username, role): inherites and initiates attributes
        """
        super().__init__(id, data_type, accountname, password, username, role)
        self.bank_account = []
        self.fetch_bank()

    def insert_bank(self, bank_name, card_number, recipient):
        """
            insert_bank(bank_name, card_number, recipient): insert new bank value to this Teacher account
        """
        self.bank_account = Teacher.Bank(bank_name, card_number, recipient)
        d = open(DATA_BANKING, 'r', encoding='utf-8').read().rstrip().split("\n")
        data = []
        if d[0] != "":
            for i in d:
                if i.split('•')[0] != self.id:
                    data.append(i)
        data.append("%s•%s•%s•%s\n" % (self.id, bank_name, card_number, recipient))
        open(DATA_BANKING, 'w', encoding='utf-8').write("\n".join(data))

    def fetch_bank(self):
        """
            fetch_bank(self): get bank account data
        """
        d = open(DATA_BANKING, 'r', encoding='utf-8').read().rstrip().split("\n")
        if d[0] != "":
            for item in d:
                i = item.split('•')
                if i[0] == self.id:
                    self.bank_account = Teacher.Bank(i[1], i[2], i[3])

class Student(User):
    """
        class Student(User): inherites id, data type, accountname, password, username and role
        method: 
            __init__(id, data_type, accountname, password, username, role)
            
    """
    def __init__(self, id, data_type, accountname, password, username, role):
        """
            __init__(id, data_type, accountname, password, username, role): inherites and initiates attributes
        """
        super().__init__(id, data_type, accountname, password, username, role)
        




