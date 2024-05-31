from components import ui_controller
from ui_files import resource
from data_init import DataManager

if __name__ == "__main__":
    DataSystem = DataManager()
    DataSystem.fetch_data(1)
    DataSystem.fetch_data(0)
    data = DataSystem.get_data(1)
    for i in data:
        item = i.get_this_user()

    data = DataSystem.get_data(0)
    for i in data:
        item = i.get_this_course()
    
    ui_controller.main("0.0.0", DataSystem)
    