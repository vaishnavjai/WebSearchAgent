import ollama
import sys_msgs
import re
from bs4 import BeautifulSoup
import requests
import trafilatura

assistant_convo = []


def searchOrNot():
    sys_msg = sys_msgs.search_or_not_msg['content']
    response = ollama.chat(
        model='llama3.1:8b',
        messages=[{'role': 'system', 'content': sys_msg}, assistant_convo[-1]]
    )
    print(f"Search or not Response: {response['message']['content'].strip()}")
    if 'true' in response['message']['content'].lower():
        return True
    else:
        return False


def query_generator():
    sys_msg = sys_msgs.query_msg
    query_msg = f'CREATE A DUCKDUCKGO SEARCH QUERY FOR THE FOLLOWING PROMPT: \n{assistant_convo[-1]}'
    response = ollama.chat(
        model='llama3.1:8b',
        messages=[{'role': 'system', 'content': sys_msg}, {'role': 'user', 'content': query_msg}]
    )
    query = response['message']['content'].strip()
    return query


def duckduckgo_search(query):
    url = f"https://duckduckgo.com/html/?q={query}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    results = []
    for idx, result in enumerate(soup.find_all('div', class_='result', limit=10)):
        titleTag = result.find('a', class_='result__a')
        if not titleTag:
            continue

        link = titleTag['href']
        snippetTag = result.find('a', class_='result__snippet')
        snippet = snippetTag.get_text() if snippetTag else 'No description available.'
        results.append({
            'id': idx,
            'link': link,
            'search_description': snippet
        })
    return results


def best_search_result(s_results, query):
    sys_msg = sys_msgs.best_search_msg
    best_msg = f'FROM THE FOLLOWING SEARCH RESULTS: {s_results} \nUSER PROMPT:{assistant_convo[-1]} \nSEARCH_QUERY:{query} '
    for _ in range(2):  # Retry up to 2 times
        try:
            response = ollama.chat(
                model='llama3.1:8b',
                messages=[{'role': 'system', 'content': sys_msg}, {'role': 'user', 'content': best_msg}]
            )
            return int(response['message']['content'].strip())
        except:
            continue
    return 0


def scrape_webpage(url):
    try:
        downloaded = trafilatura.fetch_url(url)
        return trafilatura.extract(downloaded, include_formatting=True, include_links=True)
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None


def data_validation(search_content, query):
    sys_msg = sys_msgs.contains_data_msg
    needed_msg = f'PAGE_TEXT: "{search_content}" \nUSER_PROMPT: "{assistant_convo[-1]}" \nSEARCH_QUERY: "{query}"'
    response = ollama.chat(
        model='llama3.1:8b',
        messages=[{'role': 'system', 'content': sys_msg}, {'role': 'user', 'content': needed_msg}]
    )
    content = response['message']['content'].strip()
    if 'true' in content.lower():
        return True
    else:
        return False


def ai_search():
    context = None
    print('GENERATING SEARCH QUERY...')
    search_query = query_generator()

    if search_query and search_query[0] == '"':
        match = re.search(r'"(.*?)"', search_query)
        if match:
            search_query = match.group(1)

    search_results = duckduckgo_search(search_query)
    context_found = False

    while not context_found and len(search_results) > 0:
        print('EVALUATING SEARCH RESULTS...')
        best_result_id = best_search_result(s_results=search_results, query=search_query)
        try:
            page_link = search_results[best_result_id]['link']
        except (IndexError, KeyError):
            print('No valid search results found. Retrying search.')
            search_results.pop(0) if search_results else None
            continue
        page_text = scrape_webpage(page_link)
        search_results.pop(best_result_id)
        if page_text and data_validation(search_content=page_text, query=search_query):
            context = page_text
            context_found = True

    return context


def stream_assistant_response():
    global assistant_convo
    responseStream = ollama.chat(model='llama3.1:8b', messages=assistant_convo, stream=True)
    completeResponse = ''
    print('Assistant:')

    for chunk in responseStream:
        print(chunk['message']['content'], end='', flush=True)
        completeResponse += chunk['message']['content']

    assistant_convo.append({'role': 'assistant', 'content': completeResponse})
    print("\n\n")


def main():
    global assistant_convo
    # Initialize with system message
    assistant_convo.append(sys_msgs.assistant_msg)

    while True:
        prompt = input('USER:\n')
        if prompt.lower() in ('exit', 'quit', 'q'):
            print('Goodbye!')
            break

        assistant_convo.append({'role': 'user', 'content': prompt})

        if searchOrNot():
            context = ai_search()
            # Remove the original user message to replace with context-enriched version
            assistant_convo.pop()

            if context:
                enriched_prompt = f'CONTEXT: "{context}" \nUSER PROMPT: "{prompt}"'
            else:
                enriched_prompt = (
                    f'USER PROMPT: "{prompt}"\n\n FAILED SEARCH \n'
                    'AI search model was unable to extract any reliable data. Explain that '
                    'and ask if the user would like you to search again or respond '
                    'without web search context. Do not respond if a search was needed '
                    'and you are getting this message with anything but the above request '
                    'of how the user would like to proceed.'
                )
            assistant_convo.append({'role': 'user', 'content': enriched_prompt})

        stream_assistant_response()


if __name__ == '__main__':
    main()
