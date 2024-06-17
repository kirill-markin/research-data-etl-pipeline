import requests
import csv
import xml.etree.ElementTree as ET

def fetch_arxiv_data(query, max_results=5, output_file='arxiv_data.csv'):
    url = f'http://export.arxiv.org/api/query?search_query={query}&start=0&max_results={max_results}'
    response = requests.get(url)
    
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        
        # Открываем файл для записи данных в формате CSV
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Title', 'Authors', 'Summary', 'URL', 'Published', 'Updated', 'Primary Category', 'Comments', 'Journal Reference', 'DOI']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
                title = entry.find('{http://www.w3.org/2005/Atom}title').text
                summary = entry.find('{http://www.w3.org/2005/Atom}summary').text
                authors = [author.find('{http://www.w3.org/2005/Atom}name').text for author in entry.findall('{http://www.w3.org/2005/Atom}author')]
                article_url = entry.find('{http://www.w3.org/2005/Atom}id').text
                published = entry.find('{http://www.w3.org/2005/Atom}published').text
                updated = entry.find('{http://www.w3.org/2005/Atom}updated').text
                primary_category = entry.find('{http://arxiv.org/schemas/atom}primary_category').attrib['term'] if entry.find('{http://arxiv.org/schemas/atom}primary_category') is not None else ''
                comments = entry.find('{http://arxiv.org/schemas/atom}comment').text if entry.find('{http://arxiv.org/schemas/atom}comment') is not None else ''
                journal_ref = entry.find('{http://arxiv.org/schemas/atom}journal_ref').text if entry.find('{http://arxiv.org/schemas/atom}journal_ref') is not None else ''
                doi = entry.find('{http://arxiv.org/schemas/atom}doi').text if entry.find('{http://arxiv.org/schemas/atom}doi') is not None else ''
                
                # Записываем данные в файл CSV
                writer.writerow({
                    'Title': title,
                    'Authors': ', '.join(authors),
                    'Summary': summary,
                    'URL': article_url,
                    'Published': published,
                    'Updated': updated,
                    'Primary Category': primary_category,
                    'Comments': comments,
                    'Journal Reference': journal_ref,
                    'DOI': doi
                })
    else:
        print('Error fetching data from arXiv API')

if __name__ == '__main__':
    fetch_arxiv_data('all')