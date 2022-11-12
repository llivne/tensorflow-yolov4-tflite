import hashlib
import filecmp
import os
import time
import urllib
import requests
import magic
import progressbar
from urllib.parse import quote

MAIN_DIRECTORY = "simple_images/"

class simple_image_download:
    def __init__(self):
        pass

    @staticmethod
    def digest_file(file):
        hash_md5 = hashlib.md5()
        with open(file, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    # check if similar img was already downloaded
    def duplicate_img(self, file_name, path):
        downloaded_file = os.path.join(path, file_name)

        # I check against the main dir so if we use several keywords for the search it will compare with all of them to exclude duplicates
        for root, dirs, files in os.walk(MAIN_DIRECTORY):
            for name in files:
                test_file = os.path.join(root, name)
                if test_file != downloaded_file and filecmp.cmp(test_file, downloaded_file, shallow=True):
                    if self.digest_file(test_file) == self.digest_file(downloaded_file):
                        return True

        return False

    def urls(self, keywords, limit, extensions={'.jpg', '.png', '.ico', '.gif', '.jpeg'}):
        keyword_to_search = [str(item).strip() for item in keywords.split(',')]
        i = 0
        links = []

        things = len(keyword_to_search) * limit

        bar = progressbar.ProgressBar(maxval=things, \
                                      widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()]).start()

        while i < len(keyword_to_search):
            url = 'https://www.google.com/search?q=' + quote(
                keyword_to_search[i].encode(
                    'utf-8')) + '&biw=1536&bih=674&tbm=isch&sxsrf=ACYBGNSXXpS6YmAKUiLKKBs6xWb4uUY5gA:1581168823770&source=lnms&sa=X&ved=0ahUKEwioj8jwiMLnAhW9AhAIHbXTBMMQ_AUI3QUoAQ'
            raw_html = self._download_page(url)

            end_object = -1;
            google_image_seen = False;
            j = 0

            while j < limit:
                while (True):
                    try:
                        new_line = raw_html.find('"https://', end_object + 1)
                        end_object = raw_html.find('"', new_line + 1)

                        buffor = raw_html.find('\\', new_line + 1, end_object)
                        if buffor != -1:
                            object_raw = (raw_html[new_line + 1:buffor])
                        else:
                            object_raw = (raw_html[new_line + 1:end_object])

                        if any(extension in object_raw for extension in extensions):
                            break

                    except Exception as e:
                        break


                try:
                    r = requests.get(object_raw, allow_redirects=True, timeout=1)
                    if('html' not in str(r.content)):
                        mime = magic.Magic(mime=True)
                        file_type = mime.from_buffer(r.content)
                        file_extension = f'.{file_type.split("/")[1]}'
                        if file_extension == '.png' and not google_image_seen:
                            google_image_seen = True
                            raise ValueError();
                        links.append(object_raw)
                        bar.update(bar.currval + 1)
                    else:
                        j -= 1
                except Exception as e:
                    j -= 1
                j += 1

            i += 1

        bar.finish()
        return(links)


    def download(self, keywords, limit, extensions={'.jpg', '.png', '.ico', '.gif', '.jpeg'}):
        keyword_to_search = [str(item).strip() for item in keywords.split(',')]
        main_directory = MAIN_DIRECTORY
        i = 0

        things = len(keyword_to_search) * limit

        bar = progressbar.ProgressBar(maxval=things, \
                                      widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])

        bar.start()

        while i < len(keyword_to_search):
            self._create_directories(main_directory, keyword_to_search[i])
            url = 'https://www.google.com/search?q=' + quote(
                keyword_to_search[i].encode('utf-8')) + '&biw=1536&bih=674&tbm=isch&sxsrf=ACYBGNSXXpS6YmAKUiLKKBs6xWb4uUY5gA:1581168823770&source=lnms&sa=X&ved=0ahUKEwioj8jwiMLnAhW9AhAIHbXTBMMQ_AUI3QUoAQ'
            raw_html = self._download_page(url)

            end_object = -1;
            google_image_seen = False;
            download_attempts = 0
            j = 0
            while j < limit and download_attempts < 10:
                while (True):
                    try:
                        new_line = raw_html.find('"https://', end_object + 1)
                        end_object = raw_html.find('"', new_line + 1)

                        buffor = raw_html.find('\\', new_line + 1, end_object)
                        if buffor != -1:
                            object_raw = (raw_html[new_line+1:buffor])
                        else:
                            object_raw = (raw_html[new_line+1:end_object])

                        if any(extension in object_raw for extension in extensions):
                            break

                    except Exception as e:
                        break
                path = main_directory + keyword_to_search[i].replace(" ", "_")

                try:
                    r = requests.get(object_raw, allow_redirects=True, timeout=1)
                    if('html' not in str(r.content)):
                        mime = magic.Magic(mime=True)
                        file_type = mime.from_buffer(r.content)
                        file_extension = f'.{file_type.split("/")[1]}'
                        if file_extension not in extensions:
                            raise ValueError()
                        if file_extension == '.png' and not google_image_seen:
                            google_image_seen = True
                            raise ValueError()
                        if file_extension.lower() == '.jpeg':
                            file_extension = '.jpg'
                        file_name = str(keyword_to_search[i]) + "_" + str(j + 1) + file_extension
                        with open(os.path.join(path, file_name), 'wb') as file:
                            file.write(r.content)

                        if self.duplicate_img(file_name, path):
                            os.remove(os.path.join(path, file_name))
                            download_attempts += 1
                            j -= 1
                        else:
                            download_attempts = 0
                            bar.update(bar.currval + 1)
                    else:
                        j -= 1
                except Exception as e:
                    j -= 1
                j += 1

            i += 1
        bar.finish()


    def _create_directories(self, main_directory, name):
        name = name.replace(" ", "_")
        try:
            if not os.path.exists(main_directory):
                os.makedirs(main_directory)
                time.sleep(0.2)
                path = (name)
                sub_directory = os.path.join(main_directory, path)
                if not os.path.exists(sub_directory):
                    os.makedirs(sub_directory)
            else:
                path = (name)
                sub_directory = os.path.join(main_directory, path)
                if not os.path.exists(sub_directory):
                    os.makedirs(sub_directory)

        except OSError as e:
            if e.errno != 17:
                raise
            pass
        return

    def _download_page(self,url):

        try:
            headers = {}
            headers['User-Agent'] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
            req = urllib.request.Request(url, headers=headers)
            resp = urllib.request.urlopen(req)
            respData = str(resp.read())
            return respData

        except Exception as e:
            print(e)
            exit(0)


if __name__ == '__main__':
    response = simple_image_download

    # download_items = 'מכולת פסולת,' \
    #                  'dumpster rental,' \
    #                  'cubic yard dumpster,' \
    #                  'yard dumpster,' \
    #                  'פינוי פסולת בניין,' \
    #                  'dumpster in the street,' \
    #                  'yard dumpster in street,' \
    #                  'מכולה ברחוב'

    download_items = 'van'

    download_number = 200

    response().download(download_items, download_number)

    # print(response().urls('bear', 5))
