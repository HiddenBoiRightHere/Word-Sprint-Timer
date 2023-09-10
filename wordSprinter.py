import os
import tkinter as tk
import time
from pygame import mixer
from tkinter import filedialog as fd






def final_calculations(time_limit, begin_word_count, final_word_count):
    try:
        total_change = float(final_word_count) - float(begin_word_count)
        rate_of_change = float(total_change) / float(time_limit)

        wpm_result.config(state="normal")
        wpm_result.delete(0, tk.END)
        wpm_result.insert(0, string=f"{rate_of_change}")
        wpm_result.config(state="disabled")

        prev_time.config(state="normal")
        prev_time.delete(0, tk.END)
        prev_time.insert(0, string=f"{time_limit}")
        prev_time.config(state="disabled")

        prev_words.config(state="normal")
        prev_words.delete(0, tk.END)
        prev_words.insert(0, string=f"{final_word_count}")
        prev_words.config(state="disabled")

        prev_inc_dec.config(state="normal")
        prev_inc_dec.delete(0, tk.END)
        prev_inc_dec.insert(0, string=f"{total_change}")
        prev_inc_dec.config(state="disabled")

        word_start.config(state="normal")
        word_start.delete(0, tk.END)
        word_start.insert(0, f"{final_word_count}")


        limit_entry.config(state="normal")

        submit_button.config(state="disabled")
        word_end.config(state="disabled")
        button.config(state="normal")
        fail_label.forget()
    except:
        fail_label.pack()

def change_music():
    """
    Allows user to change the timer-end music
    :return:
    """
    filename = fd.askopenfilename(filetypes=(('WAV Files', '*.wav'), ('MP3 Files', '*.mp3'), ('All files', '*.*')))
    try:
        mixer.music.load(filename)
        filename_split = filename.split(sep="/")
        current_music_label.config(text=f"Current Music: \n{filename_split[-1]}")
        fail_label.forget()
    except:
        fail_label.config(text="Music format not acceptable. Default file chosen!")
        filename = "default.wav"
        mixer.music.load(filename)
        current_music_label.config(text=f"Current Music: \n{filename}")
        fail_label.pack()



def update_color(time_remaining, timer_limit, update_color_id):
    """
    Changes circle color and fill based on time currently passed.
    :param time_remaining: Current time remaining from beginning of the run
    :param timer_limit: Total time limit allowed
    :param update_color_id: reruns function until done
    :return: none
    """
    #disable execute button because it absolutely wrecks timer
    button.config(state="disabled")
    word_start.config(state="disabled")
    limit_entry.config(state="disabled")
    if time_remaining > 0:
        # Calculate the angle based on the remaining time
        angle = 360 - (360 * (time_remaining / timer_limit))

        # Calculate the RGB values for the color
        red = int(255 * (1 - time_remaining / timer_limit))
        green = int(255 * (time_remaining / timer_limit))
        blue = 0

        # in case of abnormal times
        try:
            # Convert RGB to hexadecimal color code
            color = '#%02x%02x%02x' % (red, green, blue)
            canvas.itemconfig(arc, fill=color, start=90, extent=angle)
        except:
            color="#bd2417"
        # Update the arc on the canvas
            canvas.itemconfig(arc, fill=color, start=90, extent=angle)

        # Decrease the time remaining
        time_remaining -= 1

        # Schedule the update after 1 second (1000 milliseconds)
        update_color_id = root.after(1000, update_color, time_remaining, timer_limit, update_color_id)
    else:
        # Calculate the RGB values for the color
        red = int(255 * (1 - time_remaining / timer_limit))
        green = int(255 * (time_remaining / timer_limit))
        blue = 0

        #in case of abnormal times
        try:
            # Convert RGB to hexadecimal color code
            color = '#%02x%02x%02x' % (red, green, blue)
            canvas.itemconfig(circle, fill=color)
        except:
            color="#bd2417"
            canvas.itemconfig(circle, fill=color)


        #ALlow user to input final word count.
        word_end.config(state="normal")
        word_end.delete(0,tk.END)

        submit_button.config(state="normal")

        # Start playing the song
        mixer.music.play()









def WordTimer(timer_limit, word_start):
    """
    Begins the timer and will stop it once timer_limit is reached.
    :param timer_limit: The amount of time the timer will run.
    :return: N/A
    """
    start_time = time.time()
    while time.time() - start_time < timer_limit:
        pass
    print("End!")
    last_words = input("Please input your final word count.")
    last_words = int(last_words.strip())
    wpm = timer_limit/60 * (last_words - word_start)
    print(f"Your final wpm is {wpm}, and you increased your word count by {last_words - word_start} words!")


def execute_command(limit_entry, word_start):
    """
    Collects information from Tkinter window as to how much time they wish to spend and their first word count.
    :param limit_entry: Time Limit that user has put in seconds
    :param word_entry: Current word count from user.
    :return:
    """
    #Flag for determining whether user has input correct values
    fail = False

    try:
        # Get the number entered by the user
        timer_limit = float(limit_entry.get())
        timer_limit = timer_limit * 60

        # Replace the print statement with your desired command
        #print(f"The entered number is: {timer_limit} seconds.")
    except ValueError:
        # In case the user enters a non-numeric value
        #print("Please enter a valid number.")
        fail = True

    try:
        # Get number for word count beginning.
        word_start_count = float(word_start.get())

        # Replace the print statement with your desired command
        #print(f"You are beginning with {word_start_count}.")
    except ValueError:
        # In case non-numeric value
        #print("You did not enter valid number in word start count.")
        fail = True

    #Edit to avoid constant error re-packing later.
    if fail == True:
        fail_label = tk.Label(root, text="Something is wrong. Please check your inputs and try again.")
        fail_label.pack()
    else:
        fail_label = tk.Label(root, text="Something is wrong. Please check your inputs and try again.")
        fail_label.forget()
        canvas.itemconfig(circle, fill='')
        # Variable to hold the update_color_id
        update_color_id = None
        update_color(timer_limit, timer_limit, update_color_id)


# Create the main application window
root = tk.Tk()
root.title("Word Sprint Timer")
#root.geometry("700x700")
root.minsize(width=475, height=725)
root.maxsize(width=475, height=725)
filename = "default.wav"

#Start music mixer
# Starting the mixer
mixer.init()

# Loading the song
mixer.music.load(filename)

# Setting the volume
mixer.music.set_volume(1)

#Window design
# Add a label to prompt the user
label = tk.Label(root, text="Please enter the time in minutes you wish to spend:")
label.pack(pady=10)

# Add an entry widget for number input
limit_entry = tk.Entry(root)
limit_entry.pack(pady=5)

# Add a label to prompt the user
enter_wc = tk.Label(root, text="Please enter your beginning word count:")
enter_wc.pack(pady=10)


word_start = tk.Entry(root)
word_start.pack(pady=5)

# Add a button to execute the command
button = tk.Button(root, text="Execute", command=lambda: execute_command(limit_entry, word_start))
button.pack(pady=10)


#Place to put final word count when done:
word_end_desc = tk.Label(root, text="When the timer is complete, please place your final word count below.")
word_end_desc.pack(pady=10)

word_end = tk.Entry(root)
word_end.pack(pady=10)
word_end.insert(0, string="Wait until done.")
word_end.config(state="disabled")

current_music_label = tk.Label(root, text=f"Current Music: \n{filename}")
current_music_label.pack(side="top")

change_music_button = tk.Button(root, text="Change Music", command=lambda: change_music())
change_music_button.pack(side="left", padx=15)

stop_music_button = tk.Button(root, text="Stop Music", command=lambda: mixer.music.stop())
stop_music_button.pack(side="right", padx=15)

submit_button = tk.Button(root, text="Submit.", command=lambda: final_calculations(limit_entry.get(), word_start.get(), word_end.get()))
submit_button.pack()
submit_button.config(state="disabled")


#Create canvas for circle
# Create a canvas to draw the circle/oval
canvas = tk.Canvas(root, width=200, height=200, bg='white')
canvas.pack()

# Draw the initial circle/oval (gray color)
arc = canvas.create_arc(50, 50, 150, 150, fill='gray', start=90, extent=360)
circle = canvas.create_oval(50, 50, 150, 150, outline="black", width=1)



#Add Calculated Words Per Minute, Previous Time Spent, Previous Words (begin, end, increase/decrease)

wpm_result_label = tk.Label(text="Previous Words Per Minute (WPM)")
wpm_result_label.pack()

wpm_result = tk.Entry(root)
wpm_result.pack()
wpm_result.insert(0, string="No history.")
wpm_result.config(state="disabled")

prev_time_label = tk.Label(text="Previous Time Limit")
prev_time_label.pack()

prev_time = tk.Entry(root)
prev_time.pack()
prev_time.insert(0, string="No history.")
prev_time.config(state="disabled")

prev_words_label = tk.Label(text="Previous Ending Word Count")
prev_words_label.pack()

prev_words = tk.Entry(root)
prev_words.pack()
prev_words.insert(0, string="No history.")
prev_words.config(state="disabled")

prev_inc_dec_label = tk.Label(text="Previous Change in Words")
prev_inc_dec_label.pack()

prev_inc_dec = tk.Entry(root)
prev_inc_dec.pack()
prev_inc_dec.insert(0, string="No history.")
prev_inc_dec.config(state="disabled")

fail_label = tk.Label(root, text="Something is wrong. Please check your inputs and try again.")

# Run the main Tkinter event loop
root.mainloop()