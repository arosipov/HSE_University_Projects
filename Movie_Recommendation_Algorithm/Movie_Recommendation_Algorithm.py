from collections import defaultdict


def build_graph(movies, similarities):
    """
    Builds a graph of movies and their similarities.

    Input:
        movies (List[str]): A list of movie names.
        similarities (List[List[str]]): A list of pairs of similar movies.

    Output:
        defaultdict: A default dictionary representing the graph, where keys
        are movie names and values are sets of similar movies
        (including the movie itself).
    """
    graph = defaultdict(set)
    for a, b in similarities:
        graph[a].add(b)
        graph[b].add(a)
        graph[a].add(a)
        graph[b].add(b)
    for movie in movies:
        if movie not in graph:
            graph[movie].add(movie)
    return graph


def dfs(node, graph, visited):
    """
    Performs a Depth-First Search to find all connected nodes in the graph.

    Input:
        node (str): The current movie name.
        graph (defaultdict): A default dictionary representing the graph,
        where keys are movie names and values are sets of similar movies.
        visited (Set[str]): A set of visited movie names.

    Output:
        Set[str]: A set of all connected movie names, including the current
        movie.
    """
    if node in visited:
        return set()
    visited.add(node)
    result = set([node])
    for neighbor in graph[node]:
        result |= dfs(neighbor, graph, visited)
    return result


def calculate_score(movie, friends, graph):
    """
    Calculates the score and uniqueness of a movie based on the number of
    friends who have seen it and the mean number of similar movies seen
    by friends.

    Input:
        movie (str): The current movie name.
        friends (List[List[str]]): A list of lists, where each inner list
        contains the movies seen by a friend.
        graph (defaultdict): A default dictionary representing the graph,
        where keys are movie names and values are sets of similar movies.

    Output:
        Tuple[int, float]: A tuple containing the score (number of friends
        who have seen the movie) and the uniqueness (1 divided by the mean
        number of similar movies seen by friends).
    """
    seen_friends = sum([1 for friend in friends if movie in friend])
    if seen_friends == 0:
        return 0, 0

    similar_movies = dfs(movie, graph, set())
    similar_movies.remove(movie)

    total_similar_seen = 0
    friends_counted = 0

    for friend in friends:
        similar_seen = len(set(friend) & similar_movies)
        if similar_seen > 0:
            total_similar_seen += similar_seen
            friends_counted += 1

    if friends_counted == 0:
        return 0, 0

    mean_similar_seen = total_similar_seen / friends_counted
    return seen_friends, 1 / mean_similar_seen


def recommend_movie(movies, similarities, friends):
    """
    Recommends a movie with the highest score/uniqueness ratio.

    Input:
        movies (List[str]): A list of movie names.
        similarities (List[List[str]]): A list of pairs of similar movies.
        friends (List[List[str]]): A list of lists, where each inner list
        contains the movies seen by a friend.

    Output:
        str: The recommended movie name, or "No movie to recommend" if no
        movie meets the criteria.
    """
    graph = build_graph(movies, similarities)
    recommendations = []

    for movie in movies:
        score, uniqueness = calculate_score(movie, friends, graph)
        if uniqueness != 0:
            recommendations.append((movie, score / uniqueness))

    if not recommendations:
        return "No movie to recommend"

    best_recommendation = max(recommendations, key=lambda x: x[1])
    return best_recommendation[0]


# def unit_test():
#     # Test 1: Normal case
#     movies = [
#         "Snatch",
#         "Lock, Stock and Two Smoking Barrels",
#         "The Hateful Eight",
#         "Pain & Gain",
#         "Reservoir Dogs",
#     ]
#     similarities = [
#         ["Snatch", "Lock, Stock and Two Smoking Barrels"],
#         ["Snatch", "Pain & Gain"],
#         ["Reservoir Dogs", "The Hateful Eight"],
#     ]
#     friends = [
#         ["Reservoir Dogs"],
#         ["Reservoir Dogs", "Lock, Stock and Two Smoking Barrels"],
#         ["Reservoir Dogs"],
#         ["Snatch"],
#         ["Lock, Stock and Two Smoking Barrels"],
#         ["Pain & Gain", "Reservoir Dogs"],
#     ]
#     assert (
#         recommend_movie(movies, similarities, friends)
#         == "Lock, Stock and Two Smoking Barrels"
#     )

#     # Test 2: No friends have seen any movie
#     movies = [
#         "Snatch",
#         "Lock, Stock and Two Smoking Barrels",
#         "The Hateful Eight",
#         "Pain & Gain",
#         "Reservoir Dogs",
#     ]
#     similarities = [
#         ["Snatch", "Lock, Stock and Two Smoking Barrels"],
#         ["Snatch", "Pain & Gain"],
#         ["Reservoir Dogs", "The Hateful Eight"],
#     ]
#     friends = []
#     assert (
#         recommend_movie(movies, similarities, friends)
#         == "No movie to recommend"
#     )

#     # Test 3: No similar movies
#     movies = [
#         "Snatch",
#         "Lock, Stock and Two Smoking Barrels",
#         "The Hateful Eight",
#         "Pain & Gain",
#         "Reservoir Dogs",
#     ]
#     similarities = []
#     friends = [
#         ["Reservoir Dogs"],
#         ["Reservoir Dogs", "Lock, Stock and Two Smoking Barrels"],
#         ["Reservoir Dogs"],
#         ["Snatch"],
#         ["Lock, Stock and Two Smoking Barrels"],
#         ["Pain & Gain", "Reservoir Dogs"],
#     ]
#     assert (
#         recommend_movie(movies, similarities, friends)
#         == "No movie to recommend"
#     )

#     # Test 4: No movies
#     movies = []
#     similarities = []
#     friends = []
#     assert (
#         recommend_movie(movies, similarities, friends)
#         == "No movie to recommend"
#     )

#     # Test 5: All movies are similar
#     movies = [
#         "Snatch",
#         "Lock, Stock and Two Smoking Barrels",
#         "The Hateful Eight",
#         "Pain & Gain",
#         "Reservoir Dogs",
#     ]
#     similarities = [
#         ["Snatch", "Lock, Stock and Two Smoking Barrels"],
#         ["Snatch", "The Hateful Eight"],
#         ["Snatch", "Pain & Gain"],
#         ["Snatch", "Reservoir Dogs"],
#         ["Lock, Stock and Two Smoking Barrels", "The Hateful Eight"],
#         ["Lock, Stock and Two Smoking Barrels", "Pain & Gain"],
#         ["Lock, Stock and Two Smoking Barrels", "Reservoir Dogs"],
#         ["The Hateful Eight", "Pain & Gain"],
#         ["The Hateful Eight", "Reservoir Dogs"],
#         ["Pain & Gain", "Reservoir Dogs"],
#     ]
#     friends = [
#         ["Reservoir Dogs"],
#         ["Reservoir Dogs", "Lock, Stock and Two Smoking Barrels"],
#         ["Reservoir Dogs"],
#         ["Snatch"],
#         ["Lock, Stock and Two Smoking Barrels"],
#         ["Pain & Gain", "Reservoir Dogs"],
#     ]
#     assert recommend_movie(movies, similarities, friends) in movies

#     # Test 6: All friends have seen all movies
#     movies = [
#         "Snatch",
#         "Lock, Stock and Two Smoking Barrels",
#         "The Hateful Eight",
#         "Pain & Gain",
#         "Reservoir Dogs",
#     ]
#     similarities = [
#         ["Snatch", "Lock, Stock and Two Smoking Barrels"],
#         ["Snatch", "Pain & Gain"],
#         ["Reservoir Dogs", "The Hateful Eight"],
#     ]
#     friends = [movies, movies, movies, movies, movies]
#     assert recommend_movie(movies, similarities, friends) in movies

# unit_test()

if __name__ == "__main__":
    movies = [
        "Snatch",
        "Lock, Stock and Two Smoking Barrels",
        "The Hateful Eight",
        "Pain & Gain",
        "Reservoir Dogs",
    ]

    similarities = [
        ["Snatch", "Lock, Stock and Two Smoking Barrels"],
        ["Snatch", "Pain & Gain"],
        ["Reservoir Dogs", "The Hateful Eight"],
    ]

    friends = [
        ["Reservoir Dogs"],
        ["Reservoir Dogs", "Lock, Stock and Two Smoking Barrels"],
        ["Reservoir Dogs"],
        ["Snatch"],
        ["Lock, Stock and Two Smoking Barrels"],
        ["Pain & Gain", "Reservoir Dogs"],
    ]

    print(recommend_movie(movies, similarities, friends))
