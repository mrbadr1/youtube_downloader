# coding=utf-8
"""
"""
__author__ = 'Mrbadr1 <abroukbadre@gmail.com>'


from stylesheets import *

try:
    import os
    import requests,pytube,sys
    from PyQt5.QtWidgets import QApplication,QLabel,QStackedWidget,QCheckBox,QMessageBox,QStyledItemDelegate,QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, QLabel, QComboBox, QHeaderView
    from PyQt5.QtCore import Qt,QSize
    from PyQt5.QtWidgets import QFileDialog
    from pytube import exceptions
    from PyQt5.QtGui import QPixmap,QPainter,QColor
    from io import BytesIO
    from pytube import YouTube
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from pyqt_checkbox_table_widget.checkBoxTableWidget import CheckBoxTableWidget
except ImportError:
    import requests,pytube,sys
    from PyQt5.QtWidgets import QApplication,QLabel,QStackedWidget,QCheckBox,QMessageBox,QStyledItemDelegate,QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, QLabel, QComboBox, QHeaderView
    from PyQt5.QtCore import Qt,QSize
    from PyQt5.QtWidgets import QFileDialog

    from pytube import exceptions
    from PyQt5.QtGui import QPixmap,QPainter,QColor
    from io import BytesIO
    from pyqt_checkbox_table_widget.checkBoxTableWidget import CheckBoxTableWidget


video_info_dict = {}
row_position=0

class HoverZoomLabel(QLabel):
    def __init__(self, thumbnail_url, parent=None):
        super().__init__(parent)
        self.thumbnail_url = thumbnail_url
        self.setMouseTracking(True)
        self.large_pixmap = None  # Higher resolution thumbnail
        self.popup = QLabel(self)
        self.popup.setWindowFlags(self.popup.windowFlags() | Qt.ToolTip)
        self.popup.hide()

    def loadThumbnails(self):
        response = requests.get(self.thumbnail_url)
        thumbnail_data = BytesIO(response.content)
        pixmap = QPixmap()
        pixmap.loadFromData(thumbnail_data.getvalue())
        self.setPixmap(pixmap.scaledToWidth(100))  # Display small-sized thumbnail in the table cell

    def enterEvent(self, event):
        if self.large_pixmap is None:
            response = requests.get(self.thumbnail_url) 
            thumbnail_data = BytesIO(response.content)
            self.large_pixmap = QPixmap()
            self.large_pixmap.loadFromData(thumbnail_data.getvalue())
        popup_size = QSize(250, 200)  # Set the size of the popup window
        self.popup.setFixedSize(popup_size)  # Set the fixed size of the popup window
        scaled_pixmap = self.large_pixmap.scaled(popup_size, aspectRatioMode=Qt.KeepAspectRatio)  # Scale the pixmap to fit the popup size
        self.popup.setPixmap(scaled_pixmap)  # Set the scaled pixmap to the popup
        self.popup.move(self.mapToGlobal(self.rect().bottomRight()))
        self.popup.show()
    
    def leaveEvent(self, event):
        self.popup.hide()

class CenteredComboBoxDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.displayAlignment = Qt.AlignCenter
class YouTubeDownloaderApp(QWidget):
    def toggle_all_checkboxes(self, state):
        for i in range(self.table.rowCount()):
            checkbox_item = QTableWidgetItem()
            checkbox_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            checkbox_item.setCheckState(Qt.Checked if state == Qt.Checked else Qt.Unchecked)
            self.table.setItem(i, 0, checkbox_item)
    def __init__(self):
        super().__init__()
        self.old_pos = None  # Store the position of the mouse when the window is clicked
        self.setWindowTitle('YouTube Downloader')
        self.setWindowFlags(Qt.FramelessWindowHint)  # Set the window to be borderless
        self.setGeometry(300, 100, 750, 500)  # Set the initial position and size of the window
        self.setWindowOpacity(0.98)
        header = QLabel('youtube downloader', self)
        header.setStyleSheet(header_Style)
        close_button = QPushButton('X', self)
        close_button.clicked.connect(self.close)
        close_button.setStyleSheet(close_Botton_Style)
        
        header_layout = QHBoxLayout()
        header_layout.addStretch(1)  # Add a stretchable space to push the header to the center
        header_layout.addWidget(header, alignment=Qt.AlignCenter)  # Center align the header
        header_layout.addStretch(1)  # Add another stretchable space to center the header within the available space
        header_layout.addWidget(close_button)
        # Apply a modern style to the header
        header.setStyleSheet(heade_Label_Style)
        self.setStyleSheet(main_Style)

        self.url_label = QLabel('YouTube URL:')
        self.url_input = QLineEdit()
        self.url_input.setStyleSheet("QLineEdit {"
                        "border: 2px solid #ccc;"
                        "border-radius: 10px;"
                        "padding: 5px;"
                        "}")

        self.url_input.setAlignment(Qt.AlignCenter)
        self.search_button = QPushButton('Search')
        self.search_button.setStyleSheet(search_botton_style)


        self.search_button.clicked.connect(lambda: self.search(self.url_input.text()))
        allChkBox = QCheckBox('Check all')

        self.table = CheckBoxTableWidget()
        self.table.verticalScrollBar().setStyleSheet(table_style)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['Picture', 'Title', 'Quality', 'Size',"Duration"])
        self.table.verticalHeader().setDefaultSectionSize(38)  # Set the default row height to 100 pixels

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.table.setColumnWidth(1, 60)  # Set fixed size for the video thumbnail column
        self.table.setColumnWidth(0, 5)  # Set fixed size for the video thumbnail column
        self.table.setColumnWidth(3, 65)  # Set fixed size for the video quality column
        self.table.setColumnWidth(4, 60)  # Set fixed size for the video size column
        self.table.setColumnWidth(5, 60)  # Set fixed size for the video DURATION column
        self.table.setColumnWidth(2, 410)  # Set fixed size for the video title column
        self.table.verticalHeader().setVisible(False)
        allChkBox.stateChanged.connect(self.table.toggleState) # if allChkBox is checked, tablewidget checkboxes will also be checked 

        self.table.horizontalHeader().setStretchLastSection(True)  # Make the last column linked to the table


        input_layout = QHBoxLayout()
        input_layout.addWidget(self.url_label)
        input_layout.addWidget(self.url_input)
        input_layout.addWidget(self.search_button)

        self.download_video_button = QPushButton('Download Video')
        self.download_video_button.clicked.connect(self.download_video)
        self.download_video_button.setStyleSheet(download_botton_style)

        self.download_audio_button = QPushButton('Download Audio')
        self.download_audio_button.clicked.connect(self.download_audio)
        self.download_audio_button.setStyleSheet(download_audio_style)
        output_label = QLabel('Output:', self)
        self.output_textbox = QLineEdit(self)
        self.output_textbox.setStyleSheet("QLineEdit {"
                        "border: 2px solid #ccc;"
                        "border-radius: 10px;"
                        "padding: 3px;"
                        "}")
        browse_button = QPushButton('Browse')
        browse_button.setStyleSheet(search_botton_style)
        browse_button.clicked.connect(self.browse_output_directory)  

        output_layout = QHBoxLayout()  # Use QHBoxLayout to place the label and button on the same line
        output_layout.addWidget(output_label)
        output_layout.addWidget(self.output_textbox)
        output_layout.addWidget(browse_button)
        # Create a layout for the download buttons
        download_button_layout = QHBoxLayout()
        download_button_layout.addWidget(self.download_video_button)
        download_button_layout.addWidget(self.download_audio_button)

        # Add the download button layout to the main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(header_layout)
        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.table)

        self.setLayout(main_layout)

        lay = QVBoxLayout()
        lay.addWidget(allChkBox)
        lay.addWidget(self.table)
        #--------------------------------
        main_layout.addLayout(lay)
        main_layout.addLayout(output_layout)
        main_layout.addLayout(download_button_layout)

# Inside your class definition
    def browse_output_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if directory:
            self.output_textbox.setText(directory)
    def download_audio(self):
        # Add your logic for downloading audio here
        pass
        
    def search_video(self,url):
        try:       
            if url:
                yt = pytube.YouTube(url)
                videos = yt.streams.filter(adaptive=True, file_extension='mp4')
                videos = [video for video in videos if video.resolution] 
                if self.table.rowCount() > 0:
                    row_position = self.table.rowCount()
                    self.table.setRowCount(row_position + 1)
                else:
                    row_position = 0
                    self.table.setRowCount(1)  
                    self.search_button.setText('Add')  # Change the text of the search button to "Add"
                thumbnail_url = yt.thumbnail_url
                thumbnail_label = HoverZoomLabel(thumbnail_url)
                response = requests.get(thumbnail_url)
                thumbnail_data = BytesIO(response.content)
                thumbnail_pixmap = QPixmap()
                thumbnail_pixmap.loadFromData(thumbnail_data.getvalue())
                thumbnail_label.setPixmap(thumbnail_pixmap.scaledToWidth(100))
                thumbnail_label.loadThumbnails()  # Load the small-sized thumbnail for the table cell
                self.table.setCellWidget(row_position, 1, thumbnail_label)
                total_seconds = yt.length
                hours, minutes, seconds = transform_duration(total_seconds)
                duration_str = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
                duration_label = QLabel(duration_str)
                self.table.setCellWidget(row_position, 5, duration_label)
                self.quality_combobox = QComboBox()
                self.quality_combobox.setItemDelegate(CenteredComboBoxDelegate())
                self.quality_combobox.clear()
                for video in videos:
                    self.quality_combobox.addItem(video.resolution)  # Add the resolution of each video to the combobox
                self.table.setCellWidget(row_position, 3, self.quality_combobox)
                item = QTableWidgetItem(yt.title)
                item.setTextAlignment(Qt.AlignCenter)  # Set the alignment of the item to center
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Make the item not editable
                self.table.setItem(row_position, 2, item)  # Set the item in the table
                size_label = QLabel(str(round(videos[0].filesize / (1024 * 1024), 2)) + " Mb")  # Assuming all videos have the same size
                self.table.setCellWidget(row_position, 4, size_label)
                duration_label.setAlignment(Qt.AlignCenter)  # Center the content of the duration cell
                size_label.setAlignment(Qt.AlignCenter)  # Center the content of the size cell
                video_info_dict[row_position] = {
                           'url':url,
                           'thumbnail_url': yt.thumbnail_url,
                           'duration': yt.length,
                           'title': yt.title,
                           'sizes': {video.resolution: video.filesize for video in videos}
                       }

                self.quality_combobox.currentIndexChanged.connect(self.update_video_size)
        except exceptions.AgeRestrictedError as e:
            # Handle the age-restricted video error here
            error_message = f"The video is age restricted"
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText(error_message)
            msg.setWindowTitle("Age-Restricted Video")
            msg.exec_()
    def search(self,url):
        try:
            if 'list=' in url:
               self.download_youtube_playlist(url)
            else:
               self.search_video(url)
        except exceptions:
            print("error")
    def update_video_size(self, index):
        selected_quality = self.quality_combobox.itemText(index)
        row_index = self.table.currentRow()
        if row_index in video_info_dict:
            video_info = video_info_dict[row_index]
            size = video_info['sizes'][selected_quality]  # Get the size for the selected quality
            size_label=QLabel(str(round(size / (1024 * 1024), 2)) + " Mb")
            self.table.setCellWidget(row_index, 4,size_label)  # Update the size cell with the new size
            size_label.setAlignment(Qt.AlignCenter)  # Center the content of the size cell

    def download_video(self):
        selected_rows = []
        for i in range(self.table.rowCount()):
            item = self.table.item(i, 0)
            if item is not None and item.checkState() == Qt.Checked:
               selected_rows.append(i)        
        for row in selected_rows:
            url = video_info_dict[row][url]
            yt = pytube.YouTube(url)
            selected_quality = self.table.cellWidget(row, 3).currentText()
            videos = yt.streams.filter(progressive=True, file_extension='mp4', resolution=selected_quality)
            video_file_path = os.path.join(self.output_textbox.text(), f"downloaded_video_{row}.mp4")  # Construct the file path
            videos[0].download(output_path=self.output_textbox.text(), filename=f"downloaded_video_{row}")  # Download the video to the chosen directory
            print("vedio downloaded")
    def download_youtube_playlist(self, playlist_url):
        playlist = pytube.Playlist(playlist_url)
        video_urls = playlist.video_urls
        for url in video_urls:
            self.search_video(url)
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos()  # Save the current position of the mous         
    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = event.globalPos() - self.old_pos  # Calculate the delta movement of the mouse
            self.move(self.pos() + delta)  # Move the window by the delta
            self.old_pos = event.globalPos()  # Update the old positio         
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = None  # R

def transform_duration(seconds):
        hours = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        return hours, minutes, seconds

def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # Enable antialiasing for smooth rounded corners
        painter.setPen(Qt.NoPen)  # Set no pen for the border
        painter.setBrush(Qt.white)
        painter.drawRoundedRect(self.rect(), 10, 10)  # Draw a rounded rectangle to create the rounded corners

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = YouTubeDownloaderApp()
    window.show()
    sys.exit(app.exec_())
