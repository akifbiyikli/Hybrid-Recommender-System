# Hybrid Recommender System
# İş Problemi
# ID'si verilen kullanıcı için item-based ve
# user-based recommender yöntemlerini
# kullanarak tahmin yapınız.

# Veri Seti Hikayesi
# Veri seti, bir film tavsiye hizmeti olan MovieLens tarafından sağlanmıştır.
# İçerisinde filmler ile birlikte bu filmlere yapılan derecelendirme puanlarını
# barındırmaktadır.
# 27.278 filmde 2.000.0263 derecelendirme içermektedir.
# Bu veriler 138.493 kullanıcı tarafından
# 09 Ocak 1995 ile 31 Mart 2015
# tarihleri arasında oluşturulmuştur. Bu veri seti ise 17 Ekim 2016 tarihinde
# oluşturulmuştur.
# Kullanıcılar rastgele seçilmiştir. Seçilen tüm kullanıcıların en az 20 filme oy
# verdiği bilgisi mevcuttur.



# Görev 1:
# Veri Hazırlama işlemlerini gerçekleştiriniz.
import pandas as pd
pd.set_option('display.max_columns', 5)
pd.set_option('display.width', 500)
pd.set_option('display.expand_frame_repr', False)


movie = pd.read_csv('movie.csv')
rating = pd.read_csv('rating.csv')
df = movie.merge(rating, how="left", on="movieId")



comment_counts = pd.DataFrame(df["title"].value_counts())
rare_movies = comment_counts[comment_counts["title"] <= 1000].index
common_movies = df[~df["title"].isin(rare_movies)]
user_movie_df = common_movies.pivot_table(index=["userId"], columns=["title"], values="rating")








# Görev 2:
# Öneri yapılacak kullanıcının izlediği filmleri
# belirleyiniz.
user_id = 108170

movie_id = rating[(rating["userId"] == user_id) & (rating["rating"] == 5.0)].\
    sort_values(by="timestamp", ascending=False)["movieId"][0:1].values[0]

movie_name = df[df["movieId"] == movie_id]["title"].values[0]

user_df = user_movie_df[user_movie_df.index == user_id]
movies_watched = user_df.columns[user_df.notna().any()].tolist()


# Görev 3:
# Aynı filmleri izleyen diğer kullanıcıların
# verisine ve Id'lerine erişiniz.
movies_watched_df = user_movie_df[movies_watched]
user_movie_count = movies_watched_df.T.notnull().sum()
user_movie_count = user_movie_count.reset_index()
user_movie_count.columns = ["userId", "movie_count"]
perc = len(movies_watched) * 60 / 100
users_same_movies = user_movie_count[user_movie_count["movie_count"] > perc]["userId"]
users_same_movies.head()


# Görev 4:
# Öneri yapılacak kullanıcı ile en benzer
# kullanıcıları belirleyiniz.
final_df = pd.concat([movies_watched_df[movies_watched_df.index.isin(users_same_movies.index)],
                      user_df[movies_watched]])
corr_df = final_df.T.corr().unstack().sort_values().drop_duplicates()
corr_df = pd.DataFrame(corr_df, columns=["corr"])
corr_df.index.names = ['user_id_1', 'user_id_2']
corr_df = corr_df.reset_index()
top_users = corr_df[(corr_df["user_id_1"] == user_id) & (corr_df["corr"] >= 0.65)][
    ["user_id_2", "corr"]].reset_index(drop=True)
top_users = top_users.sort_values(by='corr', ascending=False)
top_users.rename(columns={"user_id_2": "userId"}, inplace=True)
top_users_ratings = top_users.merge(rating[["userId", "movieId", "rating"]], how='inner')


# Görev 5:
# Weighted Average Recommendation Score'u
# hesaplayınız ve ilk 5 filmi tutunuz.
top_users_ratings['weighted_rating'] = top_users_ratings['corr'] * top_users_ratings['rating']
recommendation_df = top_users_ratings.groupby('movieId').agg({"weighted_rating": "mean"})
recommendation_df = recommendation_df.reset_index()
movies_to_be_recommend = recommendation_df[recommendation_df["weighted_rating"] > 4].\
    sort_values("weighted_rating", ascending=False)

# Görev 6:
# Kullanıcının izlediği filmlerden en son en yüksek puan verdiği
# filmin adına göre item-based öneri yapınız.
# ▪ 5 öneri user-based
# ▪ 5 öneri item-based
# olacak şekilde 10 öneri yapınız.




#  user = 108170
# movie = pd.read_csv('datasets/movie_lens_dataset/movie.csv')
# rating = pd.read_csv('datasets/movie_lens_dataset/rating.csv')
# #Öneri yapılacak kullanıcının 5 puan verdiği filmlerden puanı en güncel olan filmin id'sinin alınması:
# movie_id = rating[(rating["userId"] == user) & (rating["rating"] ==5.0)]. \
# sort_values(by="timestamp", ascending=Flase)["movieId"][0:1].values[0]


# User-Based için aşağıdaki çıktının elde edilmesi
# gerekmektedir.
#
#   0     Foxfire (1996)
#   1     Man from Earth, The (2007)
#   2     Primer (2004)
#   3     Pokémon the Movie 2000 (2000)
#   4     Selena (1997)

# movies_to_be_recommen.merge(movie[["movieId", "title"]])["title"]


# Item-Based için aşağıdaki çıktının elde edilmesi
# gerekmektedir:

#movies_from_item_based[1:6].index

#Index(['My Science Project (1985)', 'Mediterraneo (1991)',
#       'Old Man and the Sea, The (1958)',
#       'National Lampoon's Senior Trip (1995)', 'Clockwatchers (1997)'], dtype='object', name='title')

# 5 öneri user-based
movies_to_be_recommend.merge(movie[["movieId", "title"]])['title'][:5]

# 5 öneri item-based
def item_based_recommender(movie_name, user_movie_df):
    movie_name = user_movie_df[movie_name]
    return user_movie_df.corrwith(movie_name).sort_values(ascending=False).head(10)

movies_form_item_based = item_based_recommender(movie_name, user_movie_df)
movies_form_item_based[1:6].index
