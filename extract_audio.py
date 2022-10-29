import subprocess
import os.path
from pathlib import Path


def download_yt_video(yt_link):
    """
    Downloads a YouTube video using the program yt-dlp
    NOTE: you need to install it first if you don't have it
    Link: https://github.com/yt-dlp/yt-dlp
    """

    # Create tmp folder to store videos and audios
    tmp_folder = Path("tmp")
    tmp_folder.mkdir(exist_ok=True)

    # Download video
    list_files = subprocess.run(["yt-dlp", yt_link])
    print("The exit code was: %d" % list_files.returncode)

    # Move video to tmp folder
    for el in Path(".").iterdir():
        if el.suffix == ".webm":
            el.replace(tmp_folder / el.name)


def extract_audio(video_path):
    pass


if __name__ == "__main__":
    download_yt_video(
        "https://www.youtube.com/watch?time_continue=128&v=2WjMcUhsMAM&feature=emb_title"
    )
