from components import ui_controller
from ui_files import resource
from data_init import DataManager

if __name__ == "__main__":
    DataSystem = DataManager()
    DataSystem.fetch_data(1)
    DataSystem.fetch_data(0)
    
    ui_controller.main("0.0.0", DataSystem)
    