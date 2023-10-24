#!/usr/bin/python3
# -*- coding: utf-8 -*-
# coding: utf8

"""
Copyright: © 2023, Streltsov Sergey
2023-10-22
https://www.bethowen.ru scraper
"""

import scrapy
import json
from scrapy.utils.project import get_project_settings


class BthRuSpider(scrapy.Spider):
    name = 'bth_ru'
    allowed_domains = ['bethowen.ru']
    p_settings = get_project_settings()
    start_urls = [p_settings.get('EP_START')]

    custom_settings = {
         # 'LOG_FILE': '/var/log/bth_ru.log',
         'LOG_LEVEL': 'INFO'
    }

    def __init__(self):
        # self.test_mode = True
        self.products_cache = set()
        super().__init__()

    def parse(self, response):
        jr = response.json()
        session_cookie = response.headers.get('Set-Cookie')
        session = [i for i in session_cookie.decode('utf-8').split(';') if 'PHPSESSID=' in i][0]
        self.logger.debug(f'Session: {session}')

        bth_auth_url = self.settings.get('EP_AUTH')
        auth_data = self.settings.get('AUTH_DATA')
        headers = self.settings.get('DEFAULT_REQUEST_HEADERS', dict())
        headers = headers.update({'Cookie': session})
        yield scrapy.Request(url=bth_auth_url, callback=self.btn_auth, headers=headers, method='POST',
                             body=json.dumps(auth_data), meta={'session': session})

    def btn_auth(self, response):
        session = response.meta.get('session')
        jr = response.json()
        access_token = jr.get('tokens', dict()).get('access_token')
        refresh_token = jr.get('tokens', dict()).get('refresh_token')
        user_id = jr.get('user', dict()).get('id')

        self.logger.debug(f'Access token: {access_token}')
        self.logger.debug(f'Refresh token: {refresh_token}')
        self.logger.debug(f'User id: {user_id}')

        def_headers = self.settings.get('DEFAULT_REQUEST_HEADERS', dict())
        headers = dict()
        headers['User-Agent'] = def_headers.get('User-Agent')
        headers['*****************'] = '247'
        headers['Authorization'] = access_token
        headers['************'] = user_id
        # ToDo: select city, now hardcoded Moscow=84
        headers['************'] = '84'
        headers['**************'] = def_headers.get('**************')
        headers['Host'] = def_headers.get('Host')
        headers['Connection'] = def_headers.get('Connection')
        headers['Accept-Encoding'] = 'gzip'
        headers['Cookie'] = session

        if access_token and captcha_token:
            bth_categories_url = self.settings.get('EP_PROD_CATEGORIES')
            self.logger.info(f'{bth_categories_url}')
            yield scrapy.Request(url=bth_categories_url, callback=self.bth_categories, headers=headers,
                                 meta={'session': session, 'headers': headers})

    def bth_categories(self, response):
        session = response.meta.get('session')
        headers = response.meta.get('headers')
        jr = response.json()
        categories = jr.get('categories', list())
        all_sub_categories = dict()
        while True:
            temp_lst = list()
            for category in categories:
                sub_categories = category.get('subcategories', None)
                if not sub_categories:
                    sub_category_id = category.get('id', None)
                    sub_category_name = category.get('name', None)
                    if sub_category_id and sub_category_name:
                        all_sub_categories[sub_category_id] = sub_category_name
                else:
                    temp_lst.extend(sub_categories)
            if len(temp_lst) == 0:
                break
            else:
                categories = temp_lst

        self.logger.info(f'Subcategories: {len(all_sub_categories)}')
        for sub_cat_id, sub_cat_name in all_sub_categories.items():
            offset = 0
            limit = 100
            bth_category_items_url = self.settings.get('EP_CATEGORY_ITEMS').format(sub_cat_id, offset, limit)
            yield scrapy.Request(url=bth_category_items_url, callback=self.bth_category_items, headers=headers,
                                 meta={'session': session, 'headers': headers, 'offset': offset, 'limit': limit,
                                       'sub_cat_id': sub_cat_id})

    def bth_category_items(self, response):
        session = response.meta.get('session')
        headers = response.meta.get('headers')
        offset = response.meta.get('offset')
        limit = response.meta.get('limit')
        sub_cat_id = response.meta.get('sub_cat_id')
        jr = response.json()

        metadata = jr.get('metadata', dict())
        md_count = metadata.get('count')
        md_limit = metadata.get('limit')
        md_offset = metadata.get('offset')
        products = jr.get('products', list())
        self.logger.info(f'Count: {md_count}, Limit: {md_limit}, Offset: {md_offset}, products: {len(products)}')

        for product in products:
            prd_id = product.get('id')
            if prd_id and (prd_id not in self.products_cache):
                self.products_cache.add(prd_id)
                offers = product.get('offers', list())
                item = dict()
                for offer in offers:
                    item['code'] = offer.get('code')
                    item['size'] = offer.get('size')
                    item['retail_price'] = offer.get('retail_price')
                yield item

                # for extended info with review, etc.

                # bth_item_url = self.settings.get('EP_ITEM_INFO').format(prd_id)
                # yield scrapy.Request(url=bth_item_url, callback=self.bth_item_info, headers=headers,
                #                      meta={'session': session, 'headers': headers, 'prd_id': prd_id})

        if md_offset+md_limit < md_count:
            offset = md_offset + md_limit
            bth_category_items_url = self.settings.get('EP_CATEGORY_ITEMS').format(sub_cat_id, offset, md_limit)
            yield scrapy.Request(url=bth_category_items_url, callback=self.bth_category_items, headers=headers,
                                 meta={'session': session, 'headers': headers, 'offset': offset, 'limit': md_limit,
                                       'sub_cat_id': sub_cat_id})

    def bth_item_info(self, response):
        jr = response.json()
        if self.test_mode:
            # short info
            offers = jr.get('offers')
            item = dict()
            for offer in offers:
                item['code'] = offer.get('code')
                item['size'] = offer.get('size')
                item['retail_price'] = offer.get('retail_price')
            yield item
        else:
            # complete info
            yield jr
