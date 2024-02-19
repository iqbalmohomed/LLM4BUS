import requests
from bs4 import BeautifulSoup

season_urls = [
    "https://octonauts.fandom.com/wiki/Season_1",
    "https://octonauts.fandom.com/wiki/Season_2",
    "https://octonauts.fandom.com/wiki/Season_3",
    "https://octonauts.fandom.com/wiki/Season_4"]

def get_episode_urls(season_url):
    episode_urls = []
    soup = BeautifulSoup(requests.get(season_url).content, "lxml")
    for e in soup.find_all('a'):
        if e.has_attr('href') and e['href'].startswith("/wiki/") and e.parent.name == 'td' and e.parent.has_attr('class') and e.parent['class'] == ['summary']:
            episode_urls.append("https://octonauts.fandom.com" + e['href'])
    print(len(episode_urls))
    return episode_urls

def get_episode_id(soup):
    # Use beautifulsoup to find table with class infobox
    table = soup.find('table', {'class': 'infobox'})
    row = table.find_all('tr')[0]
    # Get text from row
    episode_title = row.get_text(strip=True)
    # Get third row from table
    row = table.find_all('tr')[2]
    # Get text from row
    episode_id = row.get_text(strip=True)
    return (episode_title, episode_id)

def make_episode_soup(url):
    return BeautifulSoup(requests.get(url).content, "lxml")

def get_episode_summaries(season_urls):
    episode_summaries = []
    for season_url in season_urls:
        episode_urls = get_episode_urls(season_url)
        for episode_url in episode_urls:
            episode_summaries.append(get_episode_summary(episode_url))
    return episode_summaries

def get_episode_summary(soup):
    result = []
    for e in soup.find_all('h2'):
        if 'Summary' in e.text:
            for s in e.find_next_siblings():
                if s.name == 'p':
                    result.append(s.get_text(strip=True))
                elif s.name == 'h2':
                    break
    return result


url = "https://octonauts.fandom.com/wiki/The_Undersea_Storm"
url2 = "https://octonauts.fandom.com/wiki/The_Giant_Squid"

#soup = make_episode_soup(url)
#print(get_episode_id(soup))
#print(get_episode_summary(soup))

def injest_episode(url):
    soup = make_episode_soup(url)
    (episode_title, episode_id) = get_episode_id(soup)
    episode_summary = get_episode_summary(soup)
    # save to file
    filename = url.split("/")[-1] + ".txt"
    with open(filename, "w") as file:
        file.write("Title:" + episode_title + "\n")
        file.write("Order:" + episode_id + "\n")
        file.write("Summary:\n")
        for s in episode_summary:
            file.write(s + "\n")
        file.close()

def injest_all_episodes(season_urls):
    for season_url in season_urls:
        episode_urls = get_episode_urls(season_url)
        for episode_url in episode_urls:
            injest_episode(episode_url)

injest_all_episodes(season_urls)