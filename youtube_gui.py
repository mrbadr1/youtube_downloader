import sys
import urllib.request
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QComboBox, QFrame
from PyQt5.QtGui import QPixmap
from pytube import YouTube
from pytube import YouTube
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
class YouTubeDownloaderGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("Enter YouTube URL")
        layout.addWidget(self.url_input)

        self.search_button = QPushButton('Search', self)
        self.search_button.clicked.connect(self.searchYouTube)
        layout.addWidget(self.search_button)

        self.video_containers = QVBoxLayout()  # Main container for video items
        layout.addLayout(self.video_containers)

        self.setLayout(layout)
        self.setWindowTitle('YouTube Downloader')

        # Apply styles
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                font-family: Arial, sans-serif;
            }
            QLineEdit, QPushButton, QComboBox {
                padding: 8px;
                font-size: 14px;
            }
            
            QPushButton {
                background-color: #ff0000;
                color: #fff;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #cc0000;
            }
            QFrame {
                border: 2px solid #ccc;
                padding: 10px;
                margin: 10px 0;
                background-color: #fff;
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
            }
            QComboBox {
                padding: 8px;
                font-size: 14px;
            }
            QPushButton#downloadButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton#downloadButton:hover {
                background-color: #45a049;
            }
        """)

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clearLayout(child.layout())

    def searchYouTube(self):
        url = self.url_input.text()
        if 'list=' in url:
            self.clearLayout(self.video_containers)  # Clear the existing video containers
            try:
                 playlist_videos = self.get_playlist_videos(url)  # Function to get videos from the playlist
                 print(playlist_videos)
                 for video_url in playlist_videos:
                    yt = YouTube(video_url)
                    video_title = yt.title
                    videos = yt.streams.filter(file_extension='mp4').order_by('resolution').desc()
                    video_container = self.createVideoContainer(video_title, videos, yt.thumbnail_url)
                    self.video_containers.addWidget(video_container)  # Use addWidget to add the video container frame

            except Exception as e:
             print("An error occurred: ", str(e))
        else:
            self.clearLayout(self.video_containers)  # Clear the existing video containers
            try:
                yt = YouTube(url)
                video_title = yt.title
                videos = yt.streams.filter(file_extension='mp4').order_by('resolution').desc()
                video_container = self.createVideoContainer(video_title, videos, yt.thumbnail_url)
                self.video_containers.addLayout(video_container)
            except Exception as e:
                print("An error occurred: ", str(e))
    @staticmethod
    def get_playlist_videos(playlist_url):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Enable headless mode
        chrome_options.add_argument("--disable-gpu")  # Disable GPU usage
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(playlist_url)
        # Find the anchor tags containing the video URLs
        playlist_items = driver.find_elements(By.ID, "wc-endpoint")
        href_links = [item.get_attribute('href') for item in playlist_items]
        driver.quit()
        return href_links


    def createVideoContainer(self, video_title, videos, thumbnail_url):
       container_frame = QFrame()
       container_layout = QHBoxLayout()
       container_frame.setLayout(container_layout)
    
       # Add video thumbnail
       thumbnail_label = QLabel(self)
       thumbnail_pixmap = QPixmap()
       thumbnail_pixmap.loadFromData(urllib.request.urlopen(thumbnail_url).read())
       thumbnail_label.setPixmap(thumbnail_pixmap.scaledToWidth(50))  # Set the width as needed
       container_layout.addWidget(thumbnail_label)
    
       video_info_layout = QVBoxLayout()
    
       video_title_label = QLabel(video_title, self)
       video_info_layout.addWidget(video_title_label)
    
       button_and_combobox_layout = QHBoxLayout()
    
       quality_combobox = QComboBox(self)
       quality_combobox.setStyleSheet("padding: 5px; font-size: 12px;")  # Apply styles to the combobox
       for stream in videos:
           quality_info = f"{stream.resolution} - {stream.filesize / (1024 * 1024):.2f} MB"
           quality_combobox.addItem(quality_info)
    
       download_button = QPushButton('Download', self)
       download_button.setObjectName("downloadButton")
       download_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 5px; border: none; border-radius: 5px;")  # Apply styles to the download button
    
       button_and_combobox_layout.addWidget(quality_combobox)
       button_and_combobox_layout.addWidget(download_button)
    
       video_info_layout.addLayout(button_and_combobox_layout)
    
       container_layout.addLayout(video_info_layout)
    
       self.video_containers.addWidget(container_frame)  # Add the container frame to the main video containers layout
    
       return container_frame
    


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = YouTubeDownloaderGUI()
    window.show()
    sys.exit(app.exec_())
