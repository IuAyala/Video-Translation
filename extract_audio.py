import subprocess
import os.path


def download_yt_video(yt_link):
    """
    Downloads a YouTube video using the program yt-dlp
    NOTE: you need to install it first if you don't have it
    Link: https://github.com/yt-dlp/yt-dlp
    """

    if not os.path.exists("tmp"):
        os.mkdir("tmp")

    list_files = subprocess.run(["yt-dlp", yt_link])
    print("The exit code was: %d" % list_files.returncode)