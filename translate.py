# -*- coding: utf-8 -*-

from os import environ
import uuid
from json import load, dump
from os.path import abspath, dirname, join

import requests
from dotenv import load_dotenv

LANGS = ['af', 'ar', 'bn', 'bs', 'bg', 'zh-Hans', 'zh-Hant', 'hr', 'cs', 'da', 'nl', 'et', 'fi', 'fr', 'de', 'el', 'he', 'hi', 'hu', 'is', 'it', 'ja', 'ko', 'lv', 'lt', 'nb', 'fa', 'pl', 'pt', 'ro', 'ru', 'sk', 'sl', 'es', 'sv', 'te', 'th', 'tr', 'uk', 'vi', 'cy']

load_dotenv(dotenv_path=join(dirname(abspath(__file__)), '.env'))
KEY = environ['TRANSLATOR_TEXT_KEY']
base_url = 'https://api.cognitive.microsofttranslator.com'


def detect(text):
    path = '/detect?api-version=3.0'
    headers = {
        'Ocp-Apim-Subscription-Key': KEY,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }
    body = [{
        'text' : text
    }]
    constructed_url = base_url + path
    request = requests.post(constructed_url, headers=headers, json=body)
    return request.json()

def translate(text, _from, to):
    path = '/translate?api-version=3.0'
    headers = {
        'Ocp-Apim-Subscription-Key': KEY,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }
    body = [{
        'text' : text
    }]
    params = '&from={}&to={}'.format(_from, to)
    constructed_url = base_url + path + params
    request = requests.post(constructed_url, headers=headers, json=body)
    return request.json()

def run():
    try:
        with open('in/input.json') as infile:
            data = load(infile)
            for lang in LANGS:
                out = {}
                for key in data.keys():
                    text1 = data[key]
                    if type(text1) == type({}):
                        out[key] = {}
                        for key2 in text1.keys():
                            text2 = data[key][key2]
                            _translated = translate(text2, 'en', lang)
                            translated = _translated[0]['translations'][0]['text']
                            out[key][key2] = translated
                    else:
                        _translated = translate(text1, 'en', lang)
                        translated = _translated[0]['translations'][0]['text']
                        out[key] = translated
                with open('out/{}.json'.format(lang), 'w') as outfile:
                    dump(out, outfile)

    except Exception as e:
        print('run: {}'.format(e))

if __name__ == '__main__':
    run()
