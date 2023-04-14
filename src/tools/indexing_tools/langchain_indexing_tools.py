from langchain.document_loaders import YoutubeLoader, DirectoryLoader


def directory_search(query: str):
    """Search a directory for a file"""
    return DirectoryLoader('/Users/sherifneamatalla/Desktop/personal/move_37', glob="**/*.md")


def youtube_loader(url: str):
    """Load info of a youtube video given its URL"""
    return YoutubeLoader.from_youtube_channel(url,
                                              add_video_info=True)


loaders_map = {
    "directory": directory_search,
    "youtube": youtube_loader,
}
