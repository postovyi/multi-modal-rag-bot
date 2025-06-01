import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class TheBatchSpider(scrapy.Spider):
    name = 'the_batch'
    allowed_domains = ['deeplearning.ai']
    start_urls = ['https://www.deeplearning.ai/the-batch/']

    def parse(self, response):
        issue_links = response.css('a[href^="/the-batch/issue-"]::attr(href)').getall()

        for link in issue_links:
            issue_url = response.urljoin(link)
            yield scrapy.Request(issue_url, callback=self.parse_issue_page)

    def parse_issue_page(self, response):
        title = response.css('h1::text').get()
        date = response.xpath("//meta[@property='article:published_time']/@content").get()
        if not date:
            date_elements = response.css('div.blog-meta span::text').getall()
            if date_elements:
                for el in date_elements:
                    if any(
                        month in el
                        for month in [
                            'Jan',
                            'Feb',
                            'Mar',
                            'Apr',
                            'May',
                            'Jun',
                            'Jul',
                            'Aug',
                            'Sep',
                            'Oct',
                            'Nov',
                            'Dec',
                        ]
                    ):
                        date = el.strip()
                        break

        title_text = title.strip() if title else 'Title not found'
        date_text = date.strip() if date else 'Date not found'

        target_selector = 'div.prose--styled'
        content_container_list = response.css(target_selector)

        content = ''

        if content_container_list:
            actual_element_to_process = content_container_list[0]

            content_parts = []
            try:
                for element_text_node in actual_element_to_process.xpath(
                    './/*[self::p or self::h1 or self::h2 or self::h3 or self::h4 or self::h5 or '
                    'self::h6 or self::li or self::blockquote]//text() | '
                    './/figure/figcaption//text()'
                ):
                    text = element_text_node.get().strip()
                    if text:
                        content_parts.append(text)
                content = '\n\n'.join(content_parts).strip()

            except Exception:
                content = 'Content extraction error after finding container.'
        else:
            content = 'Content not extracted'

        yield {
            'url': response.url,
            'title': title_text,
            'publication_date': date_text,
            'content': content,
        }


def main() -> None:
    settings = get_project_settings()

    settings.set(
        'FEEDS', {'app/utils/output_programmatic.json': {'format': 'json', 'overwrite': True}}
    )

    process = CrawlerProcess(settings)

    process.crawl(TheBatchSpider)

    process.start()


if __name__ == '__main__':
    main()
    print('File written to: /app/utils/data/output_programmatic.json')
