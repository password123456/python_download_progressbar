__author__ = 'https://github.com/password123456/'

import os
import requests
import hashlib
import importlib
import sys
import time

importlib.reload(sys)


class Bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def download_file(url):
    saved_path = '/home/download/'
    file_name = '%s/%s' % (saved_path, url.split('/')[-1])

    try:
        header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36', 
                  'Connection': 'keep-alive'}

        with open(file_name, 'wb') as f:
            print('%s Download URL: %s %s' % (Bcolors.OKGREEN, url, Bcolors.ENDC))

            r = requests.get(url, headers=header, stream=True)
            download_file_length = r.headers.get('Content-Length')
            print('%s Downloading: %s / %.2f MB %s'
                  % (Bcolors.OKGREEN, file_name, (float(download_file_length) / (1024.0 * 1024.0)), Bcolors.ENDC))

            if download_file_length is None:
                f.write(r.content)
            else:
                dl = 0
                total_length = int(download_file_length)
                start = time.perf_counter()
                for data in r.iter_content(chunk_size=8092):
                    dl += len(data)
                    f.write(data)
                    done = int(100 * dl / total_length)
                    sys.stdout.write('\r [%s%s] %s/%s (%s%%) - %.2f seconds '
                                     % ('>' * done, ' ' * (100 - done), total_length, dl,
                                        done, (time.perf_counter() - start)))
                    sys.stdout.flush()
        f.close()

        if os.path.isfile(file_name):
            f = open(file_name, 'rb')
            download_file_read = f.read()

            file_hash = hashlib.sha256(download_file_read).hexdigest()
            print('\n')
            print('%s SHA-256: %s%s' % (Bcolors.OKGREEN, file_hash, Bcolors.ENDC))
            f.close()

    except Exception as e:
        print('%s[-] Exception::%s%s' % (Bcolors.WARNING, e, Bcolors.ENDC))

    else:
        r.close()


def main():
    url = 'download file url'
    download_file(url)


if __name__ == '__main__':
    main()
