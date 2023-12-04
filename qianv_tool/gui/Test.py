from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QScrollArea, QSizePolicy
from PyQt5.QtCore import Qt

class DeviceInfoWindow(QMainWindow):
    def __init__(self, device_info):
        super().__init__()
        self.setWindowTitle("设备信息")
        self.setGeometry(100, 100, 400, 300)

        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        title_label = QLabel("设备信息")
        title_label.setAlignment(Qt.AlignLeft)
        main_layout.addWidget(title_label)

        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()
        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        main_layout.addWidget(scroll_area)

        for device in device_info:
            device_name_label = QLabel(f"设备名称: {device['name']}")
            scroll_layout.addWidget(device_name_label)

            device_info_widget = QWidget()
            device_info_layout = QVBoxLayout()  # 使用QHBoxLayout布局
            device_info_widget.setLayout(device_info_layout)
            device_info_widget.setStyleSheet("background-color: white;")
            device_info_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # 设置横向铺满

            app_info_label = QLabel("应用信息:")
            app_name_label = QLabel(f"应用名称: {device['app_name']}")
            screen_size_label = QLabel("屏幕尺寸:")
            screen_size_value_label = QLabel(f"{device['screen_size']}")

            device_info_layout.addWidget(app_info_label)
            device_info_layout.addWidget(app_name_label)
            device_info_layout.addWidget(screen_size_label)
            device_info_layout.addWidget(screen_size_value_label)

            scroll_layout.addWidget(device_info_widget)

        self.setCentralWidget(main_widget)

# 示例设备信息
device_info = [
    {
        'name': '设备1',
        'app_name': '应用1',
        'screen_size': '5.5寸'
    },
    {
        'name': '设备2',
        'app_name': '应用2',
        'screen_size': '6寸'
    },
    {
        'name': '设备3',
        'app_name': '应用3',
        'screen_size': '5寸'
    }
]

app = QApplication([])
window = DeviceInfoWindow(device_info)
window.show()
app.exec_()