from models import Quote, Author
import connect
import re
from redis_cache import cache


def search_by_author(name: str):
    regex_pattern_author = re.compile(f'^{name}.*', re.IGNORECASE)
    author = Author.objects(fullname=regex_pattern_author).all()  # name:Steve Martin
    quotes = []
    for author in author:
        quotes = Quote.objects(author=author)
    return quotes


def search_by_tags(tags: str):
    tags = tags.split(',')
    pattern_tags = []
    for tag in tags:
        regex_pattern_tags = re.compile(f'^{tag}.*', re.IGNORECASE)
        pattern_tags.append(regex_pattern_tags)

    quotes = Quote.objects(tags__in=pattern_tags)
    return quotes


@cache
def search(search_query: str):
    print('Info not in cache')
    key, value = search_query.split(':')
    if key == 'name':
        return search_by_author(value)
    if key == 'tag' or key == 'tags':
        return search_by_tags(value)


if __name__ == '__main__':
    while True:
        try:
            query = input().encode('utf-8')
            utf_8_query = query.decode('utf-8')
            if utf_8_query == 'exit':
                exit(0)
            result = search(utf_8_query)
            [print(quote.quote) for quote in result]
            print('To escape type exit')
        except KeyboardInterrupt as err:
            print(err)
            exit(0)
        except ValueError as err:
            print(err)
            exit(0)
