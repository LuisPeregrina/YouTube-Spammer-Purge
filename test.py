import re

def youtube_url_validation(url):
    for pattern in [
        r'.*/c(?:hannel)*/([\S]+)',
        r'.*/'
    ]:
        youtube_regex_match = re.match(
            pattern,
            url,
            flags=re.DOTALL+re.IGNORECASE
        )
        if youtube_regex_match is not None:
            return youtube_regex_match.group(1)
    return False


print(youtube_url_validation('youtube.com/channel/UCUZHFZ9jIKrLroW8LcyJEQQ'))
print(youtube_url_validation('https://youtube.com/c/YouTubeCreators'))
print(youtube_url_validation('YouTubeCreators'))
