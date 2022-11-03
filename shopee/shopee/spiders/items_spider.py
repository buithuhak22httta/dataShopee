import scrapy

class ItemSpider(scrapy.Spider):
    name = "items"

    start_urls = [
        'https://shopee.vn/api/v4/shop/search_items?limit=50&offset=0&order=desc&shopid=179124960&sort_by=pop',
        'https://shopee.vn/api/v4/shop/search_items?limit=50&offset=50&order=desc&shopid=179124960&sort_by=pop',
        'https://shopee.vn/api/v4/shop/search_items?limit=50&offset=100&order=desc&shopid=179124960&sort_by=pop',
        'https://shopee.vn/api/v4/shop/search_items?limit=50&offset=150&order=desc&shopid=179124960&sort_by=pop',
    ]

    def parse(self, response):
        jsonresponse = response.json()    
        items = jsonresponse["items"]
        for item in items:
            item_basic = item["item_basic"]
            id = item_basic["itemid"]
            name = item_basic["name"]
            url_ = 'https://shopee.vn/api/v2/item/get_ratings?filter=0&flag=1&itemid='+str(id)+'&limit=6&offset=0&shopid=179124960&type=0'
            res = scrapy.Request(url=url_, callback=self.parse_rating, meta={'id': id, 'name': name})
            yield res
                                     
    def parse_rating(self,response):
        jsonres = response.json()
        rates = jsonres['data']
        summary = rates["item_rating_summary"]
        total = summary["rating_total"]
        rating = summary["rating_count"]
        rate1 = rating[0]
        rate2 = rating[1]
        rate3 = rating[2]
        rate4 = rating[3]
        rate5 = rating[4]
        id = response.meta["id"]
        name = response.meta["name"]
        link = 'https://shopee.vn/'+name.replace(' ', '-')+'-i.179124960.'+str(id)
        yield{
            'id': id,
            'name': name,
            'total': total,
            '1 sao': rate1,
            '2 sao': rate2,
            '3 sao': rate3,
            '4 sao': rate4,
            '5 sao': rate5,
            'link shopee': link
        }


