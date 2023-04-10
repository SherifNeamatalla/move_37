from langchain.document_loaders import YoutubeLoader

# This named from_youtube_channel but it actually expects a URL


def youtube_loader():
    return YoutubeLoader.from_youtube_channel("https://www.youtube.com/watch?v=QsYGlZkevEg",
                                              add_video_info=True)


langchain_indexing_tools = [
]