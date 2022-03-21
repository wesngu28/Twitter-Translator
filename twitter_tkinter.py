import pandas as pd
from google_trans_new import google_translator
import twint
from datetime import date
import pathlib

from tkinter import *
from PIL import Image, ImageTk
import requests
from io import BytesIO

translator = google_translator()
fileLocation = pathlib.Path(__file__).parent.resolve()

def displayAccountInfo(username):
    username = username[20:]
    c = twint.Config()
    c.Username = username
    c.Pandas = True
    twint.run.Lookup(c)
    Users_df = twint.storage.panda.User_df

    bio_string = Users_df.at[0,'bio']
    Users_df['bio'] = translator.translate(bio_string,lang_tgt='en')
    name_string = Users_df.at[0,'name']
    Users_df['name'] = translator.translate(name_string,lang_tgt='en')

    Users_df.drop(['id', 'join_datetime', 'join_time', 'likes', 'media', 'private', 'verified'], axis=1, inplace=True)

    image_url = Users_df.at[0,'avatar']

    response = requests.get(image_url)
    img_data = response.content
    img = Image.open(BytesIO(img_data))
    resized_img = img.resize((80,80))

    cover_img = ImageTk.PhotoImage(resized_img)
    img_label.pack(side=LEFT)
    img_label.configure(image=cover_img)
    img_label.image = cover_img

    handle = f"@{Users_df.at[0,'username']}"
    handle_label.config(text = handle)
    handle_label.pack(side=TOP)

    username = Users_df.at[0,'name']
    username_label.config(text = username)
    username_label.pack(side=TOP)

    join_date = Users_df.at[0,'join_date']
    joindate_label.config(text = str(join_date))
    joindate_label.pack(side=TOP)

    biography = Users_df.at[0,'bio']
    if biography == "":
        biography = "User has no bio set"
    bio_label.config(text = biography)
    bio_label.pack(side=TOP, pady=(0,15))

    banner_url = Users_df.at[0,'background_image']

    if banner_url != '':
        response = requests.get(banner_url)
        banner_data = response.content
        banner_img = Image.open(BytesIO(banner_data))
        banner_resize= banner_img.resize((250,83))

        banner = ImageTk.PhotoImage(banner_resize)
        banner_label.configure(image=banner)
        banner_label.image = banner
        banner_label.pack()

    start = entry1.get()
    if "optional" in start.lower():
        entry1.delete(0, END)
        entry1.insert(0,'2000-01-01')
    end_time = entry2.get()
    if "optional" in end_time.lower():
        entry2.delete(0, END)
    count = entry3.get()
    if ("optional" in count.lower()) or (type(count) == ""):
        count = int(Users_df.at[0,'tweets'])
        entry3.delete(0, END)
        entry3.insert(0,count)

    translateTweets(entry.get(),entry1.get(), entry2.get(), entry3.get())

def translateTweets(username, start_date, end_date, total_tweets):
    username = username[20:]
    c = twint.Config()
    c.Username = username
    c.Since = start_date
    c.Until = end_date
    c.Limit = total_tweets
    c.Pandas = True
    twint.run.Search(c)

    Tweets_df = twint.storage.panda.Tweets_df

    if Tweets_df.empty:
        tweet_result = "This user has no tweets!"
        no_tweets.config(text = tweet_result)
        no_tweets.pack(side=TOP)

    else:
        Tweets_df["english"] = ""

        translated_tweets = []
        for index, row in Tweets_df.iterrows():
            translated_tweets.append(translator.translate(row["tweet"], lang_tgt='en'))
        Tweets_df["english"] = translated_tweets

        Tweets_df.drop(['id','conversation_id', 'created_at', 'timezone', 'video', 'place', 'language', 'hashtags', 'cashtags', 'user_id',
        'user_id_str', 'day', 'hour', 'photos', 'search', 'near', 'geo', 'source', 'user_rt', 'retweet_id', 'retweet_date', 'user_rt_id','reply_to', 'translate', 'trans_src',
        'trans_dest'], axis=1, inplace=True)

        tweet1 = Tweets_df.at[0,'english']
        output_csv = username + "_tweets.csv"
        Tweets_df.to_csv(output_csv,encoding='utf-8-sig')
        output_label.config(text=f"File saved to: {str(fileLocation)}\{output_csv}")
        output_label.pack()

        tweet1 = Tweets_df.at[0,'english']
        tweet_1.config(text = tweet1)
        tweet_1.pack(side=TOP)
        dateTweet = Tweets_df.at[0, 'date']
        noLikes = Tweets_df.at[0,'nlikes']
        noReplies = Tweets_df.at[0,'nreplies']
        noRetweets = Tweets_df.at[0,'nretweets']
        quoteContent = Tweets_df.at[0, 'quote_url']

        tweet_1_info.config(text = f"{dateTweet}, {noReplies} Replies, {noRetweets} Retweets, {noLikes} Likes")
        if "https" in quoteContent.lower():
            tweet_1_media.config(text = "Quote Tweet")
            tweet_1_info.pack(pady=(0,0))
            tweet_1_media.pack(pady=(0,15))
        else:
            tweet_1_info.pack(pady=(0,15))

        if Tweets_df.shape[0] > 1:
            tweet2 = Tweets_df.at[1,'english']
            tweet_2.config(text = tweet2)
            tweet_2.pack(side=TOP)
            dateTweet = Tweets_df.at[1, 'date']
            noLikes = Tweets_df.at[1,'nlikes']
            noReplies = Tweets_df.at[1,'nreplies']
            noRetweets = Tweets_df.at[1,'nretweets']
            quoteContent = Tweets_df.at[1, 'quote_url']
            tweet_2_info.config(text = f"{dateTweet}, {noReplies} Replies, {noRetweets} Retweets, {noLikes} Likes")
            if "https" in quoteContent.lower():
                tweet_2_media.config(text = "Quote Tweet")
                tweet_2_info.pack(pady=(0,0))
                tweet_2_media.pack(pady=(0,15))
            else:
                tweet_2_info.pack(pady=(0,15))

        if Tweets_df.shape[0] > 2:
            tweet3 = Tweets_df.at[2,'english']
            tweet_3.config(text = tweet3)
            tweet_3.pack(side=TOP)
            dateTweet = Tweets_df.at[2, 'date']
            noLikes = Tweets_df.at[2,'nlikes']
            noReplies = Tweets_df.at[2,'nreplies']
            noRetweets = Tweets_df.at[2,'nretweets']
            quoteContent = Tweets_df.at[2, 'quote_url']
            tweet_3_info.config(text = f"{dateTweet}, {noReplies} Replies, {noRetweets} Retweets, {noLikes} Likes")
            if "https" in quoteContent.lower():
                tweet_3_media.config(text = "Quote Tweet")
                tweet_3_info.pack(pady=(0,0))
                tweet_3_media.pack(pady=(0,15))
            else:
                tweet_3_info.pack(pady=(0,15))

def on_click(event):
    event.widget.delete(0, END)

root = Tk()
root.title("Twitter Translator")
root.geometry("350x700")

input = Frame(root, bg='grey', bd=1)
input.pack(side="top", fill='x')

entry = Entry(input, font=('',10), width=41)
entry.insert(0,"Enter Twitter Profile Link")
entry.bind("<Button-1>", on_click)
entry.grid(row = 0, column = 1)

link_label = Label(input, text = "Link:", width=8)
link_label.grid(row=0, column=0)

entry1 = Entry(input, font=('',10), width=41)
entry1.insert(0,"Format: 2017-01-01 (optional)")
entry1.bind("<Button-1>", on_click)
entry1.grid(row=1, column=1)

start_label = Label(input, text = "Start date:", width=8)
start_label.grid(row=1,column=0)

entry2 = Entry(input, font=('',10), width=41)
entry2.insert(0,"Format: 2017-01-02 (optional)")
entry2.bind("<Button-1>", on_click)
entry2.grid(row=2, column=1)

end_label = Label(input, text = "End date:", width=8)
end_label.grid(row=2,column=0)

entry3 = Entry(input, font=('',10), width=41)
entry3.insert(0,"Ballpart # of tweets to export(optional)")
entry3.bind("<Button-1>", on_click)
entry3.grid(row=3, column=1)

total_label = Label(input, text = "Tweet Total:", width=8)
total_label.grid(row=3,column=0)

button = Button(input, text="Process Account", font=30, command=lambda:[displayAccountInfo(entry.get())])
button.grid(row=4, column=0, columnspan=2)

body = Frame(root, bg='grey', bd=1)
body.pack(side="top", fill='x')

image = Frame(body, bg='grey', bd=1)
image.pack(side="left", anchor='ne')

information = Frame(body, bg='grey', bd=1)
information.pack(side="right", anchor='nw')

bio = Frame(root, bg='grey', bd=1)
bio.pack()

name_label = Label(information, text = "", font=('',30))
img_label = Label(image)
img_label.config(image='')

handle_label = Label(information, text = "", width=200)
username_label = Label(information, text = "", width=200)
joindate_label = Label(information, text="", width=200)
bio_label = Label(bio, text="", width=300, wraplength=350, justify='left')

tweet_frame = Frame(root, bg='grey', bd=1)
tweet_frame.pack(side=TOP)

no_tweets = Label(tweet_frame, text = "", width=200)
tweet_1 = Label(tweet_frame, text = "", width=300, wraplength=350)
tweet_1_info = Label(tweet_frame, text = "", width=300, wraplength=350)
tweet_1_media = Label(tweet_frame, text = "", width=300, wraplength=350)
tweet_2 = Label(tweet_frame, text = "", width=300, wraplength=350)
tweet_2_info = Label(tweet_frame, text = "", width=300, wraplength=350)
tweet_2_media = Label(tweet_frame, text = "", width=300, wraplength=350)
tweet_3 = Label(tweet_frame, text="", width=300, wraplength=350)
tweet_3_info = Label(tweet_frame, text="", width=300, wraplength=350)
tweet_3_media = Label(tweet_frame, text = "", width=300, wraplength=350)

tweet_frame = Frame(root, bg='grey', bd=1)
tweet_frame.pack(side=TOP, fill='y')
banner_label = Label(tweet_frame)
banner_label.config(image='')
output_label = Label(tweet_frame, text="", width=300, wraplength=350)

root.mainloop()