import pandas as pd

# Read the provided CSV file into a DataFrame
filepath = './imdb/imdb_data.csv'  # Replace with your actual file path
imdb_data = pd.read_csv(filepath)

# Initialize an empty DataFrame for the expanded data
all_data = pd.DataFrame()

# Iterate over each row in the DataFrame
for index, row in imdb_data.iterrows():
    movie_title = row['Movie Titles']
    
    # Iterate over each star rating column from 1 to 10
    for star in range(1, 11):
        # Get the count of the star rating
        count = row[str(star)]
        
        # Check if the count is not NaN and greater than 0
        if not pd.isna(count) and count > 0:
            # Create a new row for each star rating count
            temp_df = pd.DataFrame({
                'Movie Titles': [movie_title] * count,
                'Rating': [star] * count
            })
            # Append these rows to the expanded DataFrame
            all_data = pd.concat([all_data, temp_df], ignore_index=True)


movie_names = ['Barbie',
               'Oppenheimer',
               'Dune: Part Two',
               'The Marvels',
               'John Wick: Chapter 4',
               'Madame Web',
               'Spider-Man: Across the Spider-Verse',
               'Mission: Impossible - Dead Reckoning Part One',
               'Guardians of the Galaxy Vol. 3',
               'Ant Man and The Wasp',
               'The Hunger Games: The Ballad of Songbirds & Snakes',
               'Black Panther: Wakanda Forever']

outputs = ['barbie_imdb.csv',
          'oppenheimer_imdb.csv',
          'dune2_imdb.csv',
          'the_marvels_imdb.csv',
          'john_wick_4_imdb.csv',
          'madame_web_imdb.csv',
          'spider_verse_imdb.csv',
          'mission_impossible_imdb.csv',
          'guardians_of_the_galaxy_imdb.csv',
          'ant_man_imdb.csv',
          'hunger_games_imdb.csv',
          'black_panther_imdb.csv'
]

for movie, output in zip(movie_names, outputs):
    data = all_data[all_data['Movie Titles'] == movie]
    data = data.drop('Movie Titles', axis=1)
    data.to_csv(output, index=False)
