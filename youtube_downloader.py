from pytube import YouTube
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os

# Define the on_progress callback function
def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = int((bytes_downloaded / total_size) * 100)
    print(f"Downloading... {percentage_of_completion}% complete", end='\r')
    
def download_youtube_video_as_mp3(url, output_path):
    try:
        yt = YouTube(url)
        audio = yt.streams.filter(only_audio=True).first()
        print("Downloading audio...")
        audio.download(output_path=output_path, filename='audio')
        os.rename(os.path.join(output_path, 'audio.mp4'), os.path.join(output_path, 'audio.mp3'))
        print("Audio downloaded and converted to MP3 successfully!")
    except Exception as e:
        print("An error occurred: ", str(e))
# Function to download a YouTube video with a specific quality
def download_youtube_video(url, output_path, quality_choice):
    try:

        yt = YouTube(url, on_progress_callback=on_progress)
        if quality_choice=="":
           videos = yt.streams.filter(file_extension='mp4').order_by('resolution').desc()
           print("Available video qualities:")
           for i, video in enumerate(videos):
               print(f"{i+1}. {video.resolution} - {video.mime_type} - {video.filesize / (1024 * 1024):.2f} MB")
           choice = int(input("Enter the number of the video quality you want to download: "))
           video = videos[choice - 1]
           print("Parsing...")
           video.download(output_path=output_path)
           print("Video downloaded successfully!")
        elif quality_choice!="":
         videos = yt.streams.filter(file_extension='mp4', res=quality_choice)
         if videos:
            video = videos[0]  # Choose the first video with the specified quality
            print("Parsing...")
            video.download(output_path=output_path)
            print("Video downloaded successfully!")
        else:
            print(f"No video found with {quality_choice} quality for the URL: {url}")
    except Exception as e:
        print("An error occurred: ", str(e))

# Function to download a YouTube playlist with a specific quality
def download_youtube_playlist(playlist_url, output_path, quality_choice):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Enable headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU usage
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(playlist_url)
    
    # Find the anchor tags containing the video URLs
    playlist_items = driver.find_elements(By.ID, "wc-endpoint")
    href_links = [item.get_attribute('href') for item in playlist_items]
    
    for link in href_links:
        download_youtube_video(link, output_path, quality_choice)

    driver.quit()

if __name__ == "__main__":

    video_url = input("Enter the YouTube video URL: ")
    if 'list=' in video_url:
        output_folder = "downloaded_list"
        if not os.path.exists(output_folder):
         os.makedirs(output_folder)
        quality_choice = input("Enter the desired video quality (e.g., 720p, 1080p): ")
        download_youtube_playlist(video_url, output_folder, quality_choice)
    else:
        output_folder = "downloaded_videos"
        if not os.path.exists(output_folder):
         os.makedirs(output_folder)
        quality_choice = ""
        download_youtube_video(video_url, output_folder, quality_choice)


