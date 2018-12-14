# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class RlLinks(models.Model):
    _name = 'rl.links'
    name = fields.Char('Name', size=500)
    url = fields.Char('Link', size=1024)
    desc = fields.Char('Description', size=500)
    source = fields.Char('Source', size=100)
    subject_id = fields.Many2one('op.subject', 'Subject')


class RlStream(models.Model):
    _inherit = 'op.subject'
    subject_tag = fields.Char('Subject Tag', size=9999, required=False)

    subject_book_name = fields.Char('Book Name', size=9999, required=False)
    link_ids = fields.One2many('rl.links', 'subject_id', 'Links')
    google_link_ids = fields.One2many('rl.links', 'subject_id', string="Google Links",
                                      domain = [("source", "=", "google")])
    youtube_link_ids = fields.One2many('rl.links', 'subject_id', string="Google Links",
                                       domain =[("source", "=", "youtube")])
    amazon_link_ids = fields.One2many('rl.links', 'subject_id', string="Book Links",
                                      domain= [("source", "=", "amazon")])

    _sql_constraints = [
        ('unique_stream_code',
         'unique(code)', 'Code should be unique per stream!')]

    def get_youtube_search(self, keywords):
        search_items_no = 10
        try:
            from apiclient.discovery import build
            from apiclient.errors import HttpError
        except ImportError:
            print('Module not found - apiclient')
        for keyword in keywords:
            DEVELOPER_KEY = "AIzaSyAe3F13pvFK2LO7xE84vlbF5pdCx8qpKP0"
            YOUTUBE_API_SERVICE_NAME = "youtube"
            YOUTUBE_API_VERSION = "v3"
            youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                            developerKey=DEVELOPER_KEY,
                            cache_discovery=False)
            # Call the search.list method to retrieve results matching the specified query term.
            search_response = youtube.search().list(
                q=keyword,
                type="video",
                part="id,snippet",
                maxResults=search_items_no
            ).execute()
            for search_result in search_response.get("items", []):
                if search_result["id"]["kind"] == "youtube#video":
                    try:
                        video_id = search_result["id"]["videoId"]
                        source = "youtube"
                        yt = "www.youtube.com"
                        url = 'https://' + yt + '/watch?v=' + video_id
                        title = search_result["snippet"]["title"]
                        desc = search_result["snippet"]["description"]
                        res = self.env['rl.links'].search_count([('url', '=ilike', url)])
                    except KeyError:
                        pass
                    if (res <= 0):
                        self.env['rl.links'].create({
                            'name': title,
                            'url': url,
                            'source': source,
                            'desc': desc,
                            'subject_id': self.id
                        })

    def get_google_search(self, keywords):
        search_items_no = 10
        try:
            from googleapiclient.discovery import build
            import json
        except ImportError:
            print('Module not found - googleapiclient')

        for keyword in keywords:
            # This is the developer API Key from google
            dev_key = "AIzaSyAe3F13pvFK2LO7xE84vlbF5pdCx8qpKP0"
            # This is google custom search engine ID
            cse_id = "008912091836200069824:qi4hfz8ptsc"
            search_term = keyword
            service = build("customsearch", "v1",
                            developerKey=dev_key,
                            cache_discovery=False)

            res = service.cse().list(
                q=search_term,
                cx=cse_id,
                num = search_items_no,
            ).execute()
            itemsLists = res["items"]
            for dictionary in itemsLists:
                try:
                    url = dictionary['link']
                    title = dictionary['title']
                    source = 'google'
                    # source = dictionary['displayLink']
                    desc = dictionary['snippet']
                    res = self.env['rl.links'].search_count([('url', '=ilike', url)])
                except KeyError:
                    pass

                if (res <= 0):
                    self.env['rl.links'].create({
                        'name': title,
                        'url': url,
                        'source': source,
                        'desc': desc,
                        'subject_id': self.id
                    })

    def get_books(self, keywords): #search amazon in google
        search_items_no = 10
        try:
            from googleapiclient.discovery import build
            import json
        except ImportError:
            print('Module not found - googleapiclient')

        for keyword in keywords:
            # This is the developer API Key from google
            dev_key = "AIzaSyAe3F13pvFK2LO7xE84vlbF5pdCx8qpKP0"
            # This is google custom search engine ID
            cse_id = "008912091836200069824:vopgt_r1noo"
            search_term = 'book '+keyword
            service = build("customsearch", "v1",
                            developerKey=dev_key,
                            cache_discovery=False)

            res = service.cse().list(
                q=search_term,
                cx=cse_id,
                num=search_items_no,
            ).execute()
            itemsLists = res["items"]
            for dictionary in itemsLists:
                try:
                    url = dictionary['link']
                    title = dictionary['title']
                    source = 'amazon'
                    desc = dictionary['snippet']
                    res = self.env['rl.links'].search_count([('url', '=ilike', url)])
                except KeyError:
                    pass

                if (res <= 0):
                    self.env['rl.links'].create({
                        'name': title,
                        'url': url,
                        'source': source,
                        'desc': desc,
                        'subject_id': self.id
                    })

    @api.one
    def generate_materials(self):
        s = ','
        if self.subject_tag:
            keywords = self.subject_tag.split(s)
            self.get_google_search(keywords)
            self.get_youtube_search(keywords)
        if self.subject_book_name:
            book_names = self.subject_book_name.split(s)
            self.get_books(book_names)



