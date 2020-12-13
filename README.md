#redditscrap

A tiny script that uses the Reddit API to download any number of the top submissions in a certain subreddit, along with the attached images.

The metadata is written into a **JSON** file, and the images are saved either as **JPEG** or **GIF** in the *home/username/Downloads/reddit/subreddit*

#Usage

You need to get your Reddit API credentials from [Old Reddit](https://old.reddit.com). 
Simply log into reddit and press **App** which is located in the top right corner next to your username. You will then be redirected to the App menu. In the App type choose script, and in the redirect url put (https://localhost:8080). 
You can put your app credentials in the script to authenticate it, or you can export them as environment variables which is more secure.

```bash
python redditscrap.py python -l 20
```
This command will download the top 20 submissions in the subreddit r/python. 
