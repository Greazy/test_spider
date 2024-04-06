import scrapy
import json

domen = "https://www.yelp.com"

home_services = ('Landscaping', 'Movers', 'Plumbers', 'Contractors', 'Electricians', 'Home Cleaners', 'HVAC', 'Locksmiths')
restaurants = ('Takeout', 'Burgers', 'Chinese', 'Italian', 'Reservations', 'Delivery', 'Mexican', 'Thai')
auto_services = ('Auto Repair', 'Auto Detailing', 'Body Shops', 'Car Wash', 'Car Dealers', 'Oil Change', 'Parking', 'Towing')
more = ('Dry Cleaning', 'Phone Repair', 'Bars', 'Nightlife', 'Hair Salons', 'Gyms', 'Massage', 'Shopping')


class ToScrapeCSSSpider(scrapy.Spider):
    name = "toscrape-css"
    category_name = 'Movers'
    location = 'San Francisco'

    start_urls = [
        f'https://www.yelp.com/search?find_desc={category_name}&find_loc={location}',
    ]

    def parse(self, response):
        for title in response.css("div.css-1u1p5a2"):
            business_name = title.css('a::text').get()

            if business_name is not None:
                business_page = domen + title.css('h3 > a::attr(href)').get()


                if business_page:
                    yield scrapy.Request(url=response.urljoin(business_page), callback=self.parse_page,  meta=response.meta)

        next_page = response.css('a.next-link::attr(href)').get()

        if next_page:
            yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)

    def parse_page(self, response):

        def extract_reviews():
            review = []

            for indx, el in enumerate(response.css('#reviews > section > div.css-1qn0b6x > ul > li')):
                name = el.css('a.css-19v1rkv::text').get()
                location = el.css('span.css-qgunke::text').get()
                date = el.css('div.css-1qn0b6x > span.css-chan6m::text').get()

                review.append({'name': name, 'location': location, 'date': date})

                if indx == 4:
                    break

            return review

        data = {
            'business_name': response.css('h1.css-hnttcw::text').get(),
            'business_rating': response.css('span.css-1p9ibgf::text').get(),
            'reviews': response.css('a.css-19v1rkv::text').get()[1:-1].split(' ')[0],
            'yelp_url': response.request.url,
            'website': response.css('p.css-1p9ibgf > a.css-1idmmu3::text').get(),
            'first_reviews': extract_reviews(),

        }

        with open('items.json', 'a') as f:
            json.dump(data, f, indent=4)
