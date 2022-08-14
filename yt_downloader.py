from tkinter import *
from tkinter import filedialog
from moviepy import *
from moviepy.editor import VideoFileClip
from pytube import YouTube
from tkinter.ttk import *
import time
from pytube.cli import on_progress

import shutil  # a module that allows us to copy files and folders and move them to whatever location we want
import asyncio
import threading
screen = Tk()

flag = False


# functions
def select_path():
    global flag
    """

    :return:
    """

    path = filedialog.askdirectory()  # the filedialog will allow the user to select a path from the file explorer
    # askdirectory() allows the user to select any directory using the explorer
    if path is None or path == "":
        return False
    path_label.config(text=path)
    flag = True
    return True


# progress = Progressbar(screen, orient = HORIZONTAL,length = 400, mode='determinate')

# def bar(stream, _chunk, _file_handle, bytes_remaining):
#     current = ((stream.filesize - bytes_remaining)/stream.filesize)
#     percent = ('{0:.1f}').format(current*100)
#     prog = int(50*current)
#     status = '█' * prog + '-' * (50 - prog)
#     sys.stdout.write(' ↳ |{bar}| {percent}%\r'.format(bar=status, percent=percent))
#     sys.stdout.flush()




def download_file():
    global flag
    # get user path
    get_link = link_field.get()
    if screen.title == "Downloading....":
        return
    elif get_link is None or get_link == "":
        return
    if flag == False:
        if not select_path():
            return

    # get the selected path
    user_path = path_label.cget("text")
    if user_path is None or user_path == "":
        return

    # when the file is being downloaded we're gonna change the title of the screen to 'downloading'
    screen.title("Downloading....")
    # Download video
    try:
        mp4_vid = YouTube(get_link).streams.get_by_resolution(variable.get()).download()

    except:
        print("Running Except")
        try:
            mp4_vid = YouTube(get_link).streams.get_highest_resolution().download()

        except:
            return

    # mp4_vid = YouTube(get_link).streams.all().download()
    # mp4_vid = YouTube(get_link).streams.get_by_resolution().download()
    video_clip = VideoFileClip(mp4_vid)
    video_clip.close()
    # move the downloaded video to a selected directory
    shutil.move(mp4_vid, user_path)
    # If the download is complete, we change the title of the screen
    screen.title("Download Completed!")
    flag = False


res_list = [""]


def get_res():
    global res_list
    global res_dropdown
    if screen.title == "Getting resolutions....":
        return
    screen.title("Getting resolutions....")
    # Get resolutions
    mp4_vid_res = YouTube(link_field.get()).streams.all()
    # print(mp4_vid_res[0])
    # get the video resolution
    for i in mp4_vid_res:
        if i.resolution is None:
            pass
        else:
            res_list.append(i.resolution)

    res_list = set(res_list)
    res_list = list(res_list)
    variable.set(res_list[1])

    res_dropdown = OptionMenu(screen, variable, *res_list)
    # canvas.update()
    canvas.create_window(190, 280, window=res_dropdown)
    screen.title("YouTube video downloader")


def down_thread():
    t1 = threading.Thread(target=download_file)
    t1.start()


def get_res_thread():
    t1 = threading.Thread(target=get_res)
    t1.start()


def debug_fun():
    print(variable.get())


title = screen.title("YouTube video downloader")
canvas = Canvas(screen, width=600, height=600)
canvas.pack()

# canvas.create_window(50, 300, window=progress)

# image logo
logo_img = PhotoImage(file='YouTube_logo_pngtype.png')

# resizing the image
logo_img = logo_img.subsample(2, 2)

canvas.create_image(290, 80, image=logo_img)

# link field
link_field = Entry(screen, width = 50)
link_label = Label(screen, text="Enter the video link : ", font=("Arial", 15))

# select the path for saving the file
path_label = Label(screen, text="Select path for Download", font=("Arial", 15))
select_btn = Button(screen, text="SELECT", command=select_path)

# Adding the buttons to the window
canvas.create_window(290, 220, window=path_label)
canvas.create_window(290, 280, window=select_btn)

# Add widgets to window
canvas.create_window(290, 170, window=link_label)  # the coordinates of the widget in the window
canvas.create_window(290, 250, window=link_field)

# download buttons
download_btn = Button(screen, text="Download file", command=down_thread)

# add download button to canvas
canvas.create_window(290, 390, window=download_btn)

# Resolution buttons
res_btn = Button(screen, text="Get Resolution", command=get_res_thread)

# add resolution button to canvas
canvas.create_window(190, 390, window=res_btn)

# progress.pack(pady=10)


# Resolution buttons
#debug_btn = Button(screen, text="debug", command=debug_fun)

# add resolution button to canvas
#canvas.create_window(90, 390, window=debug_btn)

# add dropdown list
#res_list = ["", "240p", "360p", "1080p"]

#res_list = set(res_list)

variable = StringVar(screen)
#variable.set(res_list[0])  #default value

print(res_list)
res_dropdown = OptionMenu(screen, variable, *res_list)


screen.mainloop()
