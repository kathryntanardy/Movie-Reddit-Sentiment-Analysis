import praw
import pandas as pd
import datetime
import time

start_time = time.time()

reddit = praw.Reddit(user_agent=True, client_id="3kz44HY1whW5l0h35TZWxA", 
                     client_secret="uQATPvCSczHiL6oJhDUVUNEnJZmHBA", username='movieratings',
                     password="cmptproject123")

url_array = ["https://www.reddit.com/r/movies/comments/155afzv/official_discussion_barbie_spoilers/",
             "https://www.reddit.com/r/movies/comments/155ag1m/official_discussion_oppenheimer_spoilers/",
             "https://www.reddit.com/r/movies/comments/1b3jo9s/official_discussion_dune_part_two_spoilers/",
             "https://www.reddit.com/r/movies/comments/18gmic3/official_poster_for_madame_web/",
             "https://www.reddit.com/r/movies/comments/17rujx8/official_discussion_the_marvels_spoilers/",
             "https://www.reddit.com/r/movies/comments/13y03dr/official_discussion_spiderman_across_the/",
             "https://www.reddit.com/r/movies/comments/14xasdx/official_discussion_mission_impossible_dead/",
             "https://www.reddit.com/r/movies/comments/1205lx8/official_discussion_john_wick_chapter_4_spoilers/",
             "https://www.reddit.com/r/movies/comments/13878rl/official_discussion_guardians_of_the_galaxy_vol_3/",
             "https://www.reddit.com/r/movies/comments/8wg5o3/official_discussion_ant_man_and_the_wasp_spoilers/",
             "https://www.reddit.com/r/movies/comments/yrzhen/official_discussion_black_panther_wakanda_forever/",
             "https://www.reddit.com/r/movies/comments/17x5dqy/official_discussion_the_hunger_games_the_ballad/"]

output_file_array = ["./data_scraped/barbie_comments.csv",
                     "./data_scraped/oppenheimer_comments.csv",
                     "./data_scraped/dune2_comments.csv",
                     "./data_scraped/madame_web_comments.csv",
                     "./data_scraped/the_marvels_comments.csv",
                     "./data_scraped/spider_verse_comments.csv",
                     "./data_scraped/mission_impossible_comments.csv",
                     "./data_scraped/john_wick_4_comments.csv",
                     "./data_scraped/guardians_of_the_galaxy_comments.csv",
                     "./data_scraped/ant_man_comments.csv",
                     "./data_scraped/black_panther_comments.csv",
                     "./data_scraped/hunger_games_comments.csv"]


for url, output_file in zip(url_array, output_file_array):
    # Get data of the post from the link
    post = reddit.submission(url=url)

    comments_data = []

    post.comments.replace_more(limit=600)  # This line removes MoreComments objects that represent hidden comments
    for comment in post.comments.list():
        # Convert timestamp data to date
        # print(datetime.datetime.utcfromtimestamp(comment.created_utc))
        # comment_date = datetime.datetime.fromtimestamp(comment.created_utc, tz=datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        comment_date = datetime.datetime.utcfromtimestamp(comment.created_utc)

        # Append the data into the array
        comments_data.append({
            "comment": comment.body,
            "date": comment_date})
    
    df_comments = pd.DataFrame(comments_data)
    df_comments.to_csv(output_file, index=False)

    # Feedback message
    print(output_file + " SUCCESSFUL")

    time.sleep(60)



# ------------------------------ Oppenheimer & Dune 2 ------------------------------

url_array2 = ["https://www.reddit.com/r/movies/comments/155ag1m/official_discussion_oppenheimer_spoilers/",
              "https://www.reddit.com/r/movies/comments/1b3jo9s/official_discussion_dune_part_two_spoilers/"]

output_file_array2 = ["oppenheimer_comments.csv",
                     "dune2_comments.csv"]