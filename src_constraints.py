{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyNJRYfrG2drltXiHtHihyGv",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/BodikeChaithali/AI_GA2_Cognitive-Crew/blob/main/src_constraints.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "Qa8OYO9FPKFf"
      },
      "outputs": [],
      "source": [
        "import pandas as pd\n",
        "\n",
        "class MovieConstraintChecker:\n",
        "    def __init__(self, movies_df: pd.DataFrame):\n",
        "\n",
        "        self.movies_df = movies_df.set_index('movieId')\n",
        "\n",
        "    def apply_constraints(self, ranked_movies: dict, user_preferences: dict) -> dict:\n",
        "\n",
        "        filtered_movies = {}\n",
        "        franchise_counts = {}\n",
        "\n",
        "        excluded_genres = [g.lower() for g in user_preferences.get('excluded_genres', [])]\n",
        "        min_year = user_preferences.get('min_year', 1900)\n",
        "        max_year = user_preferences.get('max_year', 2030)\n",
        "        max_sequels = user_preferences.get('max_sequels', float('inf'))\n",
        "\n",
        "        for movie_id, score in ranked_movies.items():\n",
        "            if movie_id not in self.movies_df.index:\n",
        "                continue\n",
        "\n",
        "            movie = self.movies_df.loc[movie_id]\n",
        "            movie_genres = [g.lower() for g in str(movie.get('genres', '')).split('|')]\n",
        "            movie_year = int(movie.get('year', 1900))\n",
        "            franchise_id = movie.get('franchise_id', None)\n",
        "\n",
        "            if any(exc in movie_genres for exc in excluded_genres):\n",
        "                continue  # Violation: skip\n",
        "\n",
        "            if not (min_year <= movie_year <= max_year):\n",
        "                continue  # Violation: skip\n",
        "\n",
        "            if franchise_id is not None:\n",
        "                current_count = franchise_counts.get(franchise_id, 0)\n",
        "                if current_count >= max_sequels:\n",
        "                    continue  # Violation: skip\n",
        "                franchise_counts[franchise_id] = current_count + 1\n",
        "\n",
        "            filtered_movies[movie_id] = score\n",
        "\n",
        "        if not filtered_movies and ranked_movies:\n",
        "            print(\"[Warning] Constraints were too strict; returning top recommendations with relaxed rules.\")\n",
        "            return dict(list(ranked_movies.items())[:3])\n",
        "\n",
        "        return filtered_movies"
      ]
    }
  ]
}