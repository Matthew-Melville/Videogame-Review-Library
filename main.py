
from dataclasses import dataclass
from typing import Optional
from drafter import *

set_website_title("Videogame Library")
set_site_information(
    author="Matthew Melville",
    description="A Videogame Review Library",
    sources="Thanks to the Drafter docs and my study group.",
    planning=["plan.pdf", "design.pdf"],
    links=["https://github.com/Matthew-Melville/Videogame-Review-Library"]
)
hide_debug_information()
set_website_framed(False)

@dataclass
class Game:
    """
    Stores information about an individual video game.

    Attributes:
        title (str): The name of the game.
        platform (str): The platform the game is played on.
        genre (str): The game's genre.
        hours_played (float): The number of hours played.
        rating (float): The game's rating from 0 to 10.
        review (str): The written review of the game.
        status (str): The game's current status.
        favorite (bool): Whether the game is a favorite.
    """
    title: str
    platform: str
    genre: str
    hours_played: float
    rating: float
    review: str
    status: str
    favorite: bool


@dataclass
class State:
    """
    Stores the information used throughout the website.

    Attributes:
        games (list[Game]): The user's collection of games.
        selected_game_title (str): The currently selected game.
        search_query (str): The current search text.
        status_filter (str): The selected library filter.
        message (str): A message displayed to the user.
    """
    games: list[Game]
    selected_game_title: str
    search_query: str
    status_filter: str
    message: str


def find_game(state: State, title: str) -> Optional[Game]:
    """
    Finds a game using its title.

    Args:
        state (State): The current website state.
        title (str): The title to search for.

    Returns:
        Optional[Game]: The matching game, or None.
    """
    for game in state.games:
        if game.title == title:
            return game
    return None


def valid_rating(rating: str) -> bool:
    """
    Checks whether a rating is a number from 0 to 10.

    Args:
        rating (str): The rating entered by the user.

    Returns:
        bool: Whether the rating is valid.
    """
    try:
        number = float(rating)
        return 0 <= number <= 10
    except ValueError:
        return False


def valid_hours(hours: str) -> bool:
    """
    Checks whether the hours entered are a valid number.

    Args:
        hours (str): The hours entered by the user.

    Returns:
        bool: Whether the hours are valid.
    """
    if hours == "":
        return False
    return hours.replace(".", "", 1).isdigit()


def calculate_statistics(
    games: list[Game]
) -> tuple[int, float, float, int]:
    """
    Calculates statistics about the user's game collection.

    Args:
        games (list[Game]): The games in the user's collection.

    Returns:
        tuple[int, float, float, int]: Total games, average rating,
        total hours played, and completed games.
    """
    total_games = len(games)
    total_hours = 0.0
    total_rating = 0.0
    rated_games = 0
    completed_games = 0

    for game in games:
        total_hours += game.hours_played

        if game.rating > 0:
            total_rating += game.rating
            rated_games += 1

        if game.status == "Completed":
            completed_games += 1

    if rated_games > 0:
        average_rating = total_rating / rated_games
    else:
        average_rating = 0.0

    return total_games, average_rating, total_hours, completed_games


def test_helper_functions() -> None:
    """
    Tests the helper functions used by the website.
    """
    assert valid_rating("8")
    assert valid_rating("0")
    assert valid_rating("10")
    assert valid_rating("8.5")
    assert valid_rating("9.25")
    assert valid_rating("7.75")
    assert not valid_rating("11")
    assert not valid_rating("10.5")
    assert not valid_rating("-1")
    assert not valid_rating("abc")

    assert valid_hours("10")
    assert valid_hours("2.5")
    assert not valid_hours("")
    assert not valid_hours("abc")

    test_game = Game(
        "Terraria", "PC", "Adventure", 20.0, 9.5,
        "Great game!", "Completed", True
    )
    test_state = State([test_game], "", "", "All Games", "")

    assert find_game(test_state, "Terraria") == test_game
    assert find_game(test_state, "Minecraft") is None

    statistics = calculate_statistics([test_game])
    assert statistics[0] == 1
    assert statistics[1] == 9.5
    assert statistics[2] == 20.0
    assert statistics[3] == 1


# Drafter routes are tested through website interactions because
# they depend on information submitted through website input fields.


@route
def index(state: State) -> Page:
    """
    Displays the website's home page.
    """
    return Page(state, [
        Header("Personal Game Journal"),
        Text("Keep track of your video games, reviews, and playtime."),
        Button("Add a Game", "add_game"),
        Button("View Game Library", "library"),
        Button("View Favorites", "favorites"),
        Button("View Wishlist", "wishlist"),
        Button("View Statistics", "statistics")
    ])


@route
def add_game(state: State) -> Page:
    """
    Displays the form for adding a new game.
    """
    return Page(state, [
        Header("Add a New Game"),
        Text("Enter information about your game."),
        Text("Game Title:"),
        TextBox("title"),
        Text("Platform:"),
        TextBox("platform"),
        Text("Genre:"),
        TextBox("genre"),
        Text("Hours Played:"),
        TextBox("hours_played"),
        Text("Rating (0-10, decimals allowed):"),
        TextBox("rating"),
        Text("Review:"),
        TextArea("review"),
        Text("Status:"),
        SelectBox(
            "status",
            ["Playing", "Completed", "Dropped", "Wishlist"]
        ),
        Text("Favorite:"),
        CheckBox("favorite"),
        Button("Save Game", "save_game"),
        Button("Home", "index")
    ])


@route
def save_game(
    state: State,
    title: str,
    platform: str,
    genre: str,
    hours_played: str,
    rating: str,
    review: str,
    status: str,
    favorite: bool
) -> Page:
    """
    Checks the information and saves a new game.

    Args:
        state (State): The current website state.
        title (str): The game's title.
        platform (str): The game's platform.
        genre (str): The game's genre.
        hours_played (str): The hours played.
        rating (str): The game's rating.
        review (str): The written review.
        status (str): The game's current status.
        favorite (bool): Whether the game is a favorite.

    Returns:
        Page: A confirmation or validation message.
    """
    if title.strip() == "":
        state.message = "Please enter a game title."
        return Page(state, [
            Text(state.message),
            Button("Go Back", "add_game")
        ])

    if not valid_rating(rating):
        state.message = "Please enter a rating from 0 to 10."
        return Page(state, [
            Text(state.message),
            Button("Go Back", "add_game")
        ])

    if not valid_hours(hours_played):
        state.message = "Please enter valid hours played."
        return Page(state, [
            Text(state.message),
            Button("Go Back", "add_game")
        ])

    if find_game(state, title) is not None:
        state.message = "A game with that title already exists."
        return Page(state, [
            Text(state.message),
            Button("Go Back", "add_game")
        ])

    new_game = Game(
        title,
        platform,
        genre,
        float(hours_played),
        float(rating),
        review,
        status,
        favorite
    )

    state.games.append(new_game)
    state.message = title + " was successfully added!"

    return Page(state, [
        Header("Game Added!"),
        Text(state.message),
        Button("View Game Library", "library"),
        Button("Add Another Game", "add_game"),
        Button("Home", "index")
    ])


def build_library_page(state: State) -> Page:
    """
    Creates the game library using the current filter.

    Args:
        state (State): The current website state.

    Returns:
        Page: The game library page.
    """
    content = [
        Header("Game Library"),
        Text("Choose a category to filter your games."),
        SelectBox(
            "status_filter",
            [
                "All Games",
                "Playing",
                "Completed",
                "Dropped",
                "Wishlist",
                "Favorites"
            ],
            state.status_filter
        ),
        Button("Apply Filter", "filter_games"),
        Text("Search for a game:"),
        TextBox("search_query"),
        Button("Search", "search_games")
    ]

    found_games = False

    for game in state.games:
        if state.status_filter == "All Games":
            show_game = True
        elif state.status_filter == "Favorites":
            show_game = game.favorite
        else:
            show_game = game.status == state.status_filter

        if show_game:
            found_games = True
            content.append(Text(game.title + " - " + game.status))

            content.append(
                Button(
                    "View " + game.title,
                    "game_details",
                    {"title": game.title}
                )
            )

    if not found_games:
        content.append(Text("No games found in this category."))

    content.append(Button("Home", "index"))
    return Page(state, content)


@route
def library(state: State) -> Page:
    """
    Displays all games in the user's library.

    Args:
        state (State): The current website state.

    Returns:
        Page: The game library page.
    """
    state.status_filter = "All Games"
    return build_library_page(state)


@route
def filter_games(state: State, status_filter: str) -> Page:
    """
    Filters the game library by status or favorites.

    Args:
        state (State): The current website state.
        status_filter (str): The selected filter.

    Returns:
        Page: The filtered game library.
    """
    state.status_filter = status_filter
    return build_library_page(state)


@route
def search_games(state: State, search_query: str) -> Page:
    """
    Searches the game collection by title.

    Args:
        state (State): The current website state.
        search_query (str): The title or text to search for.

    Returns:
        Page: A page showing matching games.
    """
    state.search_query = search_query
    content = [
        Header("Search Results"),
        Text("Results for: " + search_query)
    ]

    found_games = False

    for game in state.games:
        if search_query.lower() in game.title.lower():
            found_games = True
            content.append(Text(game.title + " - " + game.status))

            content.append(
                Button(
                    "View " + game.title,
                    "game_details",
                    {"title": game.title}
                )
            )

    if not found_games:
        content.append(Text("No matching games were found."))

    content.append(Button("Back to Library", "library"))
    content.append(Button("Home", "index"))

    return Page(state, content)


@route
def game_details(state: State, title: str) -> Page:
    """
    Displays details about a selected game.

    Args:
        state (State): The current website state.
        title (str): The title of the selected game.

    Returns:
        Page: The selected game's details page.
    """
    game = find_game(state, title)

    if game is None:
        return Page(state, [
            Header("Game Not Found"),
            Text("That game could not be found."),
            Button("Back to Library", "library")
        ])

    state.selected_game_title = title

    return Page(state, [
        Header(game.title),
        Text("Platform: " + game.platform),
        Text("Genre: " + game.genre),
        Text("Hours Played: " + str(game.hours_played)),
        Text("Rating: " + str(game.rating) + "/10"),
        Text("Status: " + game.status),
        Text("Favorite: " + str(game.favorite)),
        Header("Review"),
        Text(game.review),
        Button(
            "Edit Game",
            "edit_game",
            {"title": game.title}
        ),
        Button(
            "Remove Game",
            "remove_game",
            {"title": game.title}
        ),
        Button("Back to Library", "library"),
        Button("Home", "index")
    ])


@route
def edit_game(state: State, title: str) -> Page:
    """
    Displays a form for editing an existing game.

    Args:
        state (State): The current website state.
        title (str): The title of the game being edited.

    Returns:
        Page: The edit game form.
    """
    game = find_game(state, title)

    if game is None:
        return Page(state, [
            Text("Game not found."),
            Button("Back to Library", "library")
        ])

    return Page(state, [
        Header("Edit " + game.title),
        Text("Game Title:"),
        TextBox("new_title", game.title),
        Text("Platform:"),
        TextBox("platform", game.platform),
        Text("Genre:"),
        TextBox("genre", game.genre),
        Text("Hours Played:"),
        TextBox("hours_played", str(game.hours_played)),
        Text("Rating (0-10, decimals allowed):"),
        TextBox("rating", str(game.rating)),
        Text("Review:"),
        TextArea("review", game.review),
        Text("Status:"),
        SelectBox(
            "status",
            ["Playing", "Completed", "Dropped", "Wishlist"],
            game.status
        ),
        Text("Favorite:"),
        CheckBox("favorite", game.favorite),
        Button(
            "Save Changes",
            "save_edit",
            {"original_title": game.title}
        ),
        Button(
            "Cancel",
            "game_details",
            {"title": game.title}
        )
    ])


@route
def save_edit(
    state: State,
    original_title: str,
    new_title: str,
    platform: str,
    genre: str,
    hours_played: str,
    rating: str,
    review: str,
    status: str,
    favorite: bool
) -> Page:
    """
    Validates and saves changes to an existing game.

    Args:
        state (State): The current website state.
        original_title (str): The game's original title.
        new_title (str): The updated title.
        platform (str): The updated platform.
        genre (str): The updated genre.
        hours_played (str): The updated hours played.
        rating (str): The updated rating.
        review (str): The updated review.
        status (str): The updated status.
        favorite (bool): Whether the game is a favorite.

    Returns:
        Page: A confirmation or validation message.
    """
    game = find_game(state, original_title)

    if game is None:
        return Page(state, [
            Text("Game not found."),
            Button("Back to Library", "library")
        ])

    if new_title.strip() == "":
        return Page(state, [
            Text("Please enter a game title."),
            Button(
                "Back to Edit",
                "edit_game",
                {"title": original_title}
            )
        ])

    if not valid_rating(rating):
        return Page(state, [
            Text("Please enter a rating from 0 to 10."),
            Button(
                "Back to Edit",
                "edit_game",
                {"title": original_title}
            )
        ])

    if not valid_hours(hours_played):
        return Page(state, [
            Text("Please enter valid hours played."),
            Button(
                "Back to Edit",
                "edit_game",
                {"title": original_title}
            )
        ])

    other_game = find_game(state, new_title)

    if other_game is not None and other_game != game:
        return Page(state, [
            Text("Another game already has that title."),
            Button(
                "Back to Edit",
                "edit_game",
                {"title": original_title}
            )
        ])

    game.title = new_title
    game.platform = platform
    game.genre = genre
    game.hours_played = float(hours_played)
    game.rating = float(rating)
    game.review = review
    game.status = status
    game.favorite = favorite

    state.selected_game_title = new_title
    state.message = "Game successfully updated!"

    return Page(state, [
        Header("Game Updated!"),
        Text(state.message),
        Button(
            "View Updated Game",
            "game_details",
            {"title": new_title}
        ),
        Button("Back to Library", "library")
    ])


@route
def remove_game(state: State, title: str) -> Page:
    """
    Removes a game from the user's collection.

    Args:
        state (State): The current website state.
        title (str): The title of the game to remove.

    Returns:
        Page: A confirmation message.
    """
    game = find_game(state, title)

    if game is not None:
        state.games.remove(game)
        state.message = title + " was removed."
    else:
        state.message = "Game not found."

    state.selected_game_title = ""

    return Page(state, [
        Header("Remove Game"),
        Text(state.message),
        Button("Back to Library", "library"),
        Button("Home", "index")
    ])


@route
def favorites(state: State) -> Page:
    """
    Displays the games marked as favorites.

    Args:
        state (State): The current website state.

    Returns:
        Page: The favorites page.
    """
    state.status_filter = "Favorites"
    return build_library_page(state)


@route
def wishlist(state: State) -> Page:
    """
    Displays the games on the user's wishlist.

    Args:
        state (State): The current website state.

    Returns:
        Page: The wishlist page.
    """
    state.status_filter = "Wishlist"
    return build_library_page(state)


@route
def statistics(state: State) -> Page:
    """
    Displays statistics about the user's game collection.

    Args:
        state (State): The current website state.

    Returns:
        Page: The statistics page.
    """
    total_games, average_rating, total_hours, completed_games = (
        calculate_statistics(state.games)
    )

    return Page(state, [
        Header("Game Statistics"),
        Text("Total Games: " + str(total_games)),
        Text("Average Rating: " + str(round(average_rating, 2))),
        Text("Total Hours Played: " + str(total_hours)),
        Text("Completed Games: " + str(completed_games)),
        Button("Back to Library", "library"),
        Button("Home", "index")
    ])


test_helper_functions()

start_server(State([], "", "", "All Games", ""))

