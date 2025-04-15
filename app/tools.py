from langchain_core.tools import tool
from dataclasses import dataclass

@dataclass
class Tools:

    def __post_init__(self):
        pass

    @tool
    def get_youtube_link_according_to_the_song(song: str) -> str:
        """
        Retrieves the YouTube link for a given song name by searching it on YouTube.

        Parameters:
        - song (str): The name of the song or artist to search for on YouTube.

        Returns:
        - str: The URL of the first video result on YouTube for the given song name.

        Example:

        Note:
        - This tool is useful for returning a YouTube video link that best matches the input song title.
        - It assumes that the first result in the YouTube search is the most relevant.
        - If YouTube API is not used, scraping logic is applied instead.
        """
        from youtube_search import YoutubeSearch
        import webbrowser

        results = YoutubeSearch(f'{song}', max_results=1).to_dict()

        if not results:
            return "No video found for the given song."

        video_id = results[0]["id"]
        link = f"https://www.youtube.com/watch?v={video_id}"
        webbrowser.open(link)
        
        return link

    @tool
    def tool1(self):
        """
        """
        pass


