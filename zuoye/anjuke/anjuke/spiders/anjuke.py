import json

from scrapy import Request
from scrapy.spiders import Spider
from scrapy.selector import Selector

from anjuke.items import AnjukeItem, AnjukeOldItem, AnjukeRenItem


class AnJuKeSpider(Spider):
    name = 'anjuke'

    anjuke_url = 'https://chengdu.anjuke.com/'
    def start_requests(self):
        yield Request(self.anjuke_url)

    # 获取3种房屋类型url和名称，并且跳转地区获取函数
    def parse(self, response):
        sel = Selector(response)
        new_house_href = sel.xpath('//*[@id="glbNavigation"]/div/ul/li[2]/a/@href').extract()[0]
        old_house_href = sel.xpath('//*[@id="glbNavigation"]/div/ul/li[3]/a/@href').extract()[0]
        ren_house_href = sel.xpath('//*[@id="glbNavigation"]/div/ul/li[4]/a/@href').extract()[0]
        new_house_name = sel.xpath('//*[@id="glbNavigation"]/div/ul/li[2]/a/text()').extract()[0]
        old_house_name = sel.xpath('//*[@id="glbNavigation"]/div/ul/li[3]/a/text()').extract()[0]
        ren_house_name = sel.xpath('//*[@id="glbNavigation"]/div/ul/li[4]/a/text()').extract()[0]
        # yield Request(new_house_href, callback=self.parse_new_house, meta={'name': new_house_name})
        yield Request(old_house_href, callback=self.parse_old_house, meta={'name': old_house_name})
        # yield Request(ren_house_href, callback=self.parse_ren_house, meta={'name': ren_house_name})

    # 获取房屋地区url，并且跳转类型获取函数
    def parse_new_house(self, response):
        sel = Selector(response)
        a_info = sel.xpath('//*[@id="container"]/div[1]/div/div[1]/div/div[2]/div[1]/div/a')[1:]
        for a in a_info:
            area_name = a.xpath('./text()').extract()[0]
            href = a.xpath('./@href').extract()[0]
            yield Request(href, callback=self.parse_area_new_house, meta={'name': response.meta.get('name'), 'href': href, 'area_name': area_name})

    # 获取房屋类型url，并且跳转爬取页面信息
    def parse_area_new_house(self, response):
        sel = Selector(response)
        if sel.xpath('//*[@id="container"]/div[1]/div/div[5]/div/a[1]/text()'):
            type_name1 = sel.xpath('//*[@id="container"]/div[1]/div/div[5]/div/a[1]/text()').extract()[0]
            href1 = 'w1/'
            type_name2 = sel.xpath('//*[@id="container"]/div[1]/div/div[5]/div/a[2]/text()').extract()[0]
            href2 = 'w2/'
            if sel.xpath('//*[@id="container"]/div[2]/div[1]/div[5]/div/span[@class="curr-page"]'):
                page = sel.xpath('//*[@id="container"]/div[2]/div[1]/div[5]/div/span[@class="curr-page"]/text()').extract()[0]
            else:
                page = '1'
            yield Request(response.meta.get('href') + href1, callback=self.parse_newHouse, meta={'name': response.meta.get('name'), 'href': response.meta.get('href')+ href1, 'area_name': response.meta.get('area_name'), 'type': type_name1, 'page': page})
            yield Request(response.meta.get('href') + href2, callback=self.parse_newHouse, meta={'name': response.meta.get('name'), 'href': response.meta.get('href')+ href2, 'area_name': response.meta.get('area_name'), 'type': type_name2, 'page': page})

    # 获取房屋地区url，并且跳转到爬取信息函数
    def parse_old_house(self, response):
        sel = Selector(response)
        a_info = sel.xpath('//*[@id="content"]/div[3]/div[1]/span[2]/a')[1:]
        if sel.xpath('//*[@id="content"]/div[4]/div[7]/i[@class="curr"]'):
            page = sel.xpath('//*[@id="content"]/div[4]/div[7]/i[@class="curr"]/text()').extract()[0]
        else:
            page = '1'
        for a in a_info:
            area_name = a.xpath('./text()').extract()[0]
            href = a.xpath('./@href').extract()[0]
            yield Request(href, callback=self.parse_oldHouse, meta={'name': response.meta.get('name'), 'href': href, 'area_name': area_name, 'page': page})

    # 获取房屋地区url，并且跳转类型获取函数
    def parse_ren_house(self, response):
        sel = Selector(response)
        a_info = sel.xpath('/html/body/div[5]/div[2]/div[1]/span[2]/div/a')[1:]
        for a in a_info:
            area_name = a.xpath('./text()').extract()[0]
            href = a.xpath('./@href').extract()[0]
            yield Request(href, callback=self.parse_area_ren_house, meta={'name': response.meta.get('name'), 'href': href, 'area_name': area_name})

    # 获取房子类型url，并且跳转爬取页面函数
    def parse_area_ren_house(self, response):
        sel = Selector(response)
        type_name1 = sel.xpath('/html/body/div[5]/div[2]/div[4]/span[2]/a[2]/text()').extract()[0]
        href1 = 'x1'
        type_name2 = sel.xpath('/html/body/div[5]/div[2]/div[4]/span[2]/a[3]/text()').extract()[0]
        href2 = 'x2'
        if sel.xpath('/html/body/div[5]/div[3]/div[3]/div/i[@class="curr"]'):
            page = sel.xpath('/html/body/div[5]/div[3]/div[3]/div/i[@class="curr"]/text()').extract()[0]
        else:
            page = '1'
        yield Request(response.meta.get('href') + href1, callback=self.parse_renHouse, meta={'name': response.meta.get('name'), 'href': response.meta.get('href') + href1, 'area_name': response.meta.get('area_name'), 'type': type_name1, 'page': page})
        yield Request(response.meta.get('href') + href2, callback=self.parse_renHouse, meta={'name': response.meta.get('name'), 'href': response.meta.get('href') + href2, 'area_name': response.meta.get('area_name'), 'type': type_name2, 'page': page})

    # 爬取出租房信息
    def parse_renHouse(self, response):
        sel = Selector(response)
        item = AnjukeRenItem()
        ren_houses = sel.xpath('//*[@id="list-content"]/div[@class="zu-itemmod  "]')
        href = response.meta.get('href')
        for ren_house in ren_houses:
            item['id'] = ren_house.xpath('./a/@href').extract()[0][-10:]
            item['img'] = ren_house.xpath('./a/img/@src').extract()[0]
            item['title'] = ren_house.xpath('./div[1]/h3/a/text()').extract()[0]
            item['address'] = ren_house.xpath('./div[1]/address/a/text()').extract()[0] + ren_house.xpath('./div[1]/address/text()').extract()[0].replace('\xa0', ' ').strip()
            item['tag'] = ','.join(ren_house.xpath('./div[1]/p[2]/span/text()').extract())
            item['house_type'] = ','.join(ren_house.xpath('./div[1]/p[1]/text()').extract()[:-1])
            item['price'] = ren_house.xpath('./div[2]/p/strong/text()').extract()[0] + ren_house.xpath('./div[2]/p/text()').extract()[0]
            item['name'] = response.meta.get('name')
            item['area_name'] = response.meta.get('area_name')
            item['type_name'] = response.meta.get('type')
            yield item
        if sel.xpath('/html/body/div[5]/div[3]/div[3]/div/a/text()'):
            if sel.xpath('/html/body/div[5]/div[3]/div[3]/div/a/text()').extract()[-1] == '下一页 >':
                yield Request(href[:-2] + 'p'+ str(int(response.meta.get('page'))+1) + '-' + href[-2:], callback=self.parse_renHouse,
                       meta={'href': href, 'name': response.meta.get('name'), 'area_name': response.meta.get('area_name'), 'type': response.meta.get('type'), 'page': str(int(response.meta.get('page'))+1)})

    # 爬取二手房信息
    def parse_oldHouse(self, response):
        sel = Selector(response)
        item = AnjukeOldItem()
        href = response.meta.get('href')
        old_houses = sel.xpath('//*[@id="houselist-mod-new"]/li')
        for old_house in old_houses:
            item['id'] = old_house.xpath('./div[2]/div[1]/a/@href').extract()[0][37:48]
            item['img'] = old_house.xpath('./div[1]/img/@src').extract()[0]
            item['title'] = old_house.xpath('./div[2]/div[1]/a/text()').extract()[0].encode().replace(b'\n',b'').decode().strip()
            item['address'] = old_house.xpath('./div[2]/div[3]/span/text()').extract()[0].replace('\xa0', ' ').replace(' ', '').encode().replace(b'\n',b'').decode()
            item['house_type'] = ','.join(old_house.xpath('./div[2]/div[2]/span/text()').extract()[:-1])
            if old_house.xpath('./div[2]/div[4]/span'):
                item['tag'] = ','.join(old_house.xpath('./div[2]/div[4]/span/text()').extract())
            item['price'] = old_house.xpath('./div[3]/span[1]/strong/text()').extract()[0] + old_house.xpath('./div[3]/span[1]/text()').extract()[0] + old_house.xpath('./div[3]/span[2]/text()').extract()[0]
            item['name'] = response.meta.get('name')
            item['area_name'] = response.meta.get('area_name')
            yield item
            if sel.xpath('//*[@id="content"]/div[4]/div[7]/a/text()'):
                if sel.xpath('//*[@id="content"]/div[4]/div[7]/a/text()').extract()[-1] == '下一页 >':
                    yield Request(href + 'p' + str(int(response.meta.get('page')) + 1),callback=self.parse_oldHouse,
                                  meta={'href': href, 'name': response.meta.get('name'), 'area_name': response.meta.get('area_name'), 'type': response.meta.get('type'), 'page': str(int(response.meta.get('page')) + 1)})

        # 爬取新房信息
    def parse_newHouse(self, response):
        sel = Selector(response)
        item = AnjukeItem()
        href = response.meta.get('href')
        # # 房屋信息
        new_houses = sel.xpath('//*[@id="container"]/div[2]/div[1]/div[4]/div')
        for new_house in new_houses:
            if new_house.xpath('./div/a[1]/h3/span/text()'):
                item['id'] = new_house.xpath('./@data-link').extract()[0][-11:-5]
                item['img'] = new_house.xpath('./a/img/@src').extract()[0]
                item['title'] = new_house.xpath('./div/a[1]/h3/span/text()').extract()[0]
                item['address'] = new_house.xpath('./div/a[2]/span/text()').extract()[0].replace('[', '').replace(']', '').replace('\xa0', ' ').strip()
                if new_house.xpath('./div/a[3]/span/text()'):
                    item['house_type'] = ','.join(new_house.xpath('./div/a[3]/span/text()').extract())
                else:
                    item['house_type'] = new_house.xpath('./div/a[3]/text()').extract()[0]
                item['status_icon'] = ','.join(new_house.xpath('./div/a[4]/div/i/text()').extract())
                item['tag'] = ','.join(new_house.xpath('./div/a[4]/div/span/text()').extract())
                item['name'] = response.meta.get('name')
                item['area_name'] = response.meta.get('area_name')
                item['type_name'] = response.meta.get('type')
                if new_house.xpath('./a[2]/p[1]/span/text()'):
                    item['price'] = new_house.xpath('./a[2]/p/text()').extract()[0] + new_house.xpath('./a[2]/p[1]/span/text()').extract()[0] + new_house.xpath('./a[2]/p[1]/text()').extract()[1]
                    if new_house.xpath('./a[2]/p[2]/text()'):
                        item['tel'] = new_house.xpath('./a[2]/p[2]/text()').extract()[0]
                else:
                    item['price'] = new_house.xpath('./a[2]/p/text()').extract()[0]
                    item['tel'] = new_house.xpath('./a[2]/p/text()').extract()[-1]
                yield item
        if sel.xpath('//*[@id="container"]/div[2]/div[1]/div[@class="list-page"]/div/a/text()'):
            if sel.xpath('//*[@id="container"]/div[2]/div[1]/div[@class="list-page"]/div/a/text()').extract()[-1] == '下一页':
                yield Request(href[:-3] + 'p'+ str(int(response.meta.get('page'))+1) + '_' + href[-3:], callback=self.parse_newHouse,
                       meta={'href': href, 'name': response.meta.get('name'), 'area_name': response.meta.get('area_name'), 'type': response.meta.get('type'), 'page': str(int(response.meta.get('page'))+1)})


