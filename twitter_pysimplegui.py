import PySimpleGUI as sg
import twint
from google_trans_new import google_translator
import pathlib
import requests
from PIL import Image, ImageTk
import requests
from io import BytesIO
from datetime import date
import textwrap

sg.theme('DarkAmber')

translator = google_translator()
fileLocation = pathlib.Path(__file__).parent.resolve()

layout = [
  [sg.Text('Please enter your desired link. Optional fields: Starting date, ending date, number of tweets.')],
  [sg.Text('Twitter Profile Link:', size =(15, 1)), sg.InputText(key='url')],
  [sg.Text('Start Date', size =(15, 1)), sg.InputText(key='start_date')],
  [sg.Text('End Date', size =(15, 1)), sg.InputText(key='end_date')],
  [sg.Text('Number of Tweets', size =(15, 1)), sg.InputText(key='num_tweet')],
  [sg.OK(), sg.Button('Clear'), sg.Cancel()]]

def displayAccountInfo(values):
    username = values['url'][20:]
    c = twint.Config()
    c.Username = username
    c.Pandas = True
    twint.run.Lookup(c)
    Users_df = twint.storage.panda.User_df

    Users_df.drop(['id', 'join_datetime', 'join_time', 'likes', 'media', 'private', 'verified'], axis=1, inplace=True)

    image_url = Users_df.at[0,'avatar']
    response = requests.get(image_url)
    img_data = response.content
    img = Image.open(BytesIO(img_data))
    img.save("twitter_avatar.png", format="PNG")
    filename = "twitter_avatar.png"

    avatar = Image.open(filename)
    avatar = avatar.resize((80,80))
    avatar = ImageTk.PhotoImage(image=avatar)

    twitter_handle = f"@{Users_df.at[0,'username']}"

    bio_string = Users_df.at[0,'bio']
    Users_df['bio'] = translator.translate(bio_string,lang_tgt='en')
    biography = Users_df.at[0,'bio']
    biography = textwrap.fill(biography, 75)
    if biography == "":
        biography = "User has no bio set"

    name_string = Users_df.at[0,'name']
    Users_df['name'] = translator.translate(name_string,lang_tgt='en')
    twitter_username = Users_df.at[0,'name']

    join_date = "Account Created: " + Users_df.at[0,'join_date']

    banner_url = Users_df.at[0,'background_image']
    response = requests.get(banner_url)
    img_data = response.content
    img = Image.open(BytesIO(img_data))
    img.save("twitter_banner.png", format="PNG")
    filename = "twitter_banner.png"

    banner = Image.open(filename)
    banner = banner.resize((250,83))
    banner = ImageTk.PhotoImage(image=banner)

    if values['num_tweet'] == '':
      num_tweet = int(Users_df.at[0,'tweets'])
    else:
      num_tweet = values['num_tweet']

    if type(values['start_date']) == "":
      start_date = '2000-01-01'
    else:
      start_date = values['start_date']

    username = values['url'][20:]
    c = twint.Config()
    c.Username = username
    c.Since = start_date
    c.Until = values['end_date']
    c.Limit = num_tweet
    c.Pandas = True
    twint.run.Search(c)

    Tweets_df = twint.storage.panda.Tweets_df

    if Tweets_df.empty:
        tweet_result = "This user has no tweets!"

    else:
        tweet_result = "Displaying latest tweets:"
        Tweets_df["english"] = ""

        translated_tweets = []
        for index, row in Tweets_df.iterrows():
            translated_tweets.append(translator.translate(row["tweet"], lang_tgt='en'))
        Tweets_df["english"] = translated_tweets

        Tweets_df.drop(['id','conversation_id', 'created_at', 'timezone', 'video', 'place', 'language', 'hashtags', 'cashtags', 'user_id',
        'user_id_str', 'day', 'hour', 'photos', 'search', 'near', 'geo', 'source', 'user_rt', 'retweet_id', 'retweet_date', 'user_rt_id','reply_to', 'translate', 'trans_src',
        'trans_dest'], axis=1, inplace=True)

        output_csv = username + "_tweets.csv"
        Tweets_df.to_csv(output_csv,encoding='utf-8-sig')
        location_info =f"File saved to: {str(fileLocation)}\{output_csv}"

        tweet1 = Tweets_df.at[0,'english']
        tweet1 = textwrap.fill(tweet1, 75)
        dateTweet = Tweets_df.at[0, 'date']
        noLikes = Tweets_df.at[0,'nlikes']
        noReplies = Tweets_df.at[0,'nreplies']
        noRetweets = Tweets_df.at[0,'nretweets']
        quoteContent = Tweets_df.at[0, 'quote_url']
        tweet_1_info = f"{dateTweet}, {noReplies} Replies, {noRetweets} Retweets, {noLikes} Likes"
        if "https" in quoteContent.lower():
            tweet_1_info = tweet_1_info + "\nQuote:" + quoteContent

        if Tweets_df.shape[0] > 1:
            tweet2 = Tweets_df.at[1,'english']
            tweet2 = textwrap.fill(tweet2, 75)
            dateTweet = Tweets_df.at[1, 'date']
            noLikes = Tweets_df.at[1,'nlikes']
            noReplies = Tweets_df.at[1,'nreplies']
            noRetweets = Tweets_df.at[1,'nretweets']
            quoteContent = Tweets_df.at[1, 'quote_url']
            tweet_2_info = f"{dateTweet}, {noReplies} Replies, {noRetweets} Retweets, {noLikes} Likes"
            if "https" in quoteContent.lower():
              tweet_2_info = tweet_2_info + "\nQuote: " + quoteContent

        if Tweets_df.shape[0] > 2:
            tweet3 = Tweets_df.at[2,'english']
            tweet3 = textwrap.fill(tweet3, 75)
            dateTweet = Tweets_df.at[2, 'date']
            noLikes = Tweets_df.at[2,'nlikes']
            noReplies = Tweets_df.at[2,'nreplies']
            noRetweets = Tweets_df.at[2,'nretweets']
            quoteContent = Tweets_df.at[2, 'quote_url']
            tweet_3_info = f"{dateTweet}, {noReplies} Replies, {noRetweets} Retweets, {noLikes} Likes"
            if "https" in quoteContent.lower():
              tweet_3_info = tweet_3_info + "\nQuote: " + quoteContent

    layout = [
      [sg.Image(size=(80, 80), key='-IMAGE-')],
      [sg.Text(twitter_handle)],
      [sg.Text(biography)],
      [sg.Text(twitter_username)],
      [sg.Text(join_date)],
      [sg.HorizontalSeparator()],
      [sg.Image(size=(80, 80), key='-BG-')],
      [sg.Text(tweet_result)],
      [sg.Text(tweet1)],
      [sg.Text(tweet_1_info)],
      [sg.HorizontalSeparator()],
      [sg.Text(tweet2)],
      [sg.Text(tweet_2_info)],
      [sg.HorizontalSeparator()],
      [sg.Text(tweet3)],
      [sg.Text(tweet_3_info)],
      [sg.HorizontalSeparator()],
      [sg.Text(location_info)]
    ]

    window = sg.Window('Translated Account', layout, margins=(0, 0), finalize=True)
    window['-IMAGE-'].update(data=avatar)
    window['-BG-'].update(data=banner)

def clear_input():
  for key in values:
      window[key]('')
  return None

window = sg.Window('Twitter Translator', layout)

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Cancel'):
        break
    if event == "Clear":
      clear_input()
    if event == "OK":
      displayAccountInfo(values)
      clear_input()
window.close()