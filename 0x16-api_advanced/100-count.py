from requests import get

def count_words(subreddit, word_list, word_count=[], page_after=None):
    """
    Prints the count of the given words present in the title of the
    subreddit's hottest articles.
    """
    headers = {'User-Agent': 'HolbertonSchool'}

    word_list = [word.lower() for word in word_list]

    if not word_count:
        word_count = [0] * len(word_list)

    if page_after is None:
        url = f'https://www.reddit.com/r/{subreddit}/hot.json'
    else:
        url = f'https://www.reddit.com/r/{subreddit}/hot.json?after={page_after}'

    response = get(url, headers=headers, allow_redirects=False)
    if response.status_code == 200:
        data = response.json()['data']
        for child in data['children']:
            title_words = child['data']['title'].lower().split()
            for i, word in enumerate(word_list):
                if word in title_words:
                    word_count[i] += title_words.count(word)

        if data['after'] is not None:
            count_words(subreddit, word_list, word_count, data['after'])
        else:
            word_dict = {}
            for word, count in zip(word_list, word_count):
                if count != 0:
                    word_dict[word] = count * word_list.count(word)

            for key, value in sorted(word_dict.items(), key=lambda x: (-x[1], x[0])):
                print(f'{key}: {value}')

# Example usage
count_words('programming', ['python', 'java', 'code'])
