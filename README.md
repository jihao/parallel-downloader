# parallel-downloader
<pre>
$ python paralleldownloder.py -h
usage: paralleldownloder.py [-h] [--parallel PARALLEL] [--proxy-file PROXY]
                            [--user-agents-file UA] [--urls-file URLS]

Parallel Downloader supports proxy-file and user-agents-file. For each url in
urls.txt, this script will download it with a random selected http proxy and a
random selected user agent. It will retry 3 times until download succeed,
Otherwise failed url will be logged into failed_urls.log.

optional arguments:
  -h, --help            show this help message and exit
  --parallel PARALLEL   parallel download, default is 4
  --proxy-file PROXY    proxy file like sqlmap, random selected, default
                        proxy.txt
  --user-agents-file UA
                        user agents file like sqlmap, random selected, default
                        user-agents.txt
  --urls-file URLS      urls to download, one url per line, default urls.txt
</pre>

Notice: please change the save file logic for processing url to generate filename and save path issue for your case.
