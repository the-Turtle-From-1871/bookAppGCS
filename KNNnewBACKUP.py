import pandas as pd

# Load the ratings data in panda dataframe
ratings_df = pd.read_csv('/Users/cooperetheridge/Desktop/ratings.csv')
# Load the books data in panda dataframe
books_df = pd.read_csv('/Users/cooperetheridge/Desktop/books.csv')
     

# set display options
pd.set_option('display.max_columns', None) # display all columns
pd.set_option('display.width', 1000) # set display width
     

# Print dataset size and examine column data types
print("Number of ratings: ", len(ratings_df))
print(ratings_df.info())

print(ratings_df.head())

print(ratings_df.sort_values('book_id'))

books_df.drop(["goodreads_book_id", "best_book_id", "work_id", "books_count", "isbn", "isbn13", "language_code", "work_ratings_count", "work_text_reviews_count"], axis=1, inplace=True)

print(books_df)
     
     





# from surprise import KNNBaseline, Dataset, Reader
# from surprise.model_selection import cross_validate

# # Define the reader object for Surprise
# reader = Reader(rating_scale=(1, 5))

# # Load the merged dataframe into Surprise's Dataset object
# data = Dataset.load_from_df(ratings_df[['user_id', 'book_id', 'rating']], reader)

# # Set the similarity options for KNNBaseline
# sim_options = {'name': 'pearson_baseline', 'user_based': False}

# # Create the KNNBaseline model
# knn_model = KNNBaseline(sim_options=sim_options)

# # Perform k-fold cross-validation
# cv_results = cross_validate(knn_model, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)

# # Print the average RMSE and MAE scores
# average_rmse = sum(cv_results['test_rmse']) / len(cv_results['test_rmse'])
# average_mae = sum(cv_results['test_mae']) / len(cv_results['test_mae'])

# print(f"Average RMSE (5-fold CV): {average_rmse}")
# print(f"Average MAE (5-fold CV): {average_mae}")
     





# from surprise import KNNBaseline, Dataset, Reader
# from surprise.model_selection import cross_validate

# # Define the reader object for Surprise
# reader = Reader(rating_scale=(1, 5))

# # Load the merged dataframe into Surprise's Dataset object
# data = Dataset.load_from_df(ratings_df[['user_id', 'book_id', 'rating']], reader)

# # Set the similarity options for KNNBaseline
# sim_options = {'name': 'pearson_baseline', 'user_based': False}

# # Create the KNNBaseline model
# knn_model = KNNBaseline(sim_options=sim_options)

# # Perform k-fold cross-validation
# cv_results = cross_validate(knn_model, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)

# # Print the average RMSE and MAE scores
# average_rmse = sum(cv_results['test_rmse']) / len(cv_results['test_rmse'])
# average_mae = sum(cv_results['test_mae']) / len(cv_results['test_mae'])

# print(f"Average RMSE (5-fold CV): {average_rmse}")
# print(f"Average MAE (5-fold CV): {average_mae}")
     



from surprise import KNNBaseline, Reader, Dataset

# Define the reader object for Surprise
reader = Reader(rating_scale=(1, 5))

# Load the merged dataframe into Surprise's Dataset object
data = Dataset.load_from_df(ratings_df[['user_id', 'book_id', 'rating']], reader)

trainset = data.build_full_trainset()
sim_options = {"name": "pearson_baseline", "user_based": False}
algo = KNNBaseline(sim_options=sim_options)
algo.fit(trainset)
algo

print("Number of items in the trainset:", len(algo.trainset.all_items()))
     




     
def read_item_names(df):
    """Read book title and id from a csv file and return two dictionaries to
    convert raw ids into book titles and book titles into raw ids.
    """
    # Create dictionaries to convert raw ids into book titles and book titles
    # into raw ids
    rid_to_name = {}
    name_to_rid = {}
    for index, row in df.iterrows():
        rid = str(row["book_id"])
        name = row["title"]
        rid_to_name[rid] = name
        name_to_rid[name] = rid

    return rid_to_name, name_to_rid

# Read the mappings raw id <-> movie name
rid_to_name, name_to_rid = read_item_names(books_df)






# Retrieve inner id of the book
book_title = input("Book title: ")
raw_id = name_to_rid[book_title]
raw_id = int(raw_id)

inner_id = algo.trainset.to_inner_iid(raw_id)

neighbors_inner = algo.get_neighbors(inner_id, k=10)

# Get book information
book_data = books_df.loc[books_df['book_id'] == raw_id].iloc[0]

# Print book information and nearest neighbors
print()
print(f"Book title: {book_data['original_title']}")
print(f"Image URL: {book_data['image_url']}")
print(f"Authors: {book_data['authors']}")
print(f"Publication Year: {book_data['original_publication_year']}")
print()
print(f"The 10 nearest neighbors to {book_title} are:")
for neighbor_inner in neighbors_inner:
    neighbor_raw = algo.trainset.to_raw_iid(neighbor_inner)
    neighbor_name = rid_to_name[str(neighbor_raw)]
    neighbor_data = books_df.loc[books_df['book_id'] == neighbor_raw].iloc[0]
    print(f"Book title: {neighbor_data['original_title']}")
    print(f"Image URL: {neighbor_data['image_url']}")
    print(f"Authors: {neighbor_data['authors']}")
    print(f"Publication Year: {neighbor_data['original_publication_year']}")
    print()
     