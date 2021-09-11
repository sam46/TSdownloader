""" download segmented mpeg video (.ts files) from streaming websites """
import sys
import os
import requests

M3URL = "https://ts0-pl.tv.itself.cz/at/hls/media/vod_257_profile21.m3u8?start=1631362380&end=1631364000&device=f9bd99590153950fe5becdc4861279c6&auth=DVQqJQ5CUlNcV0ZFVEhQRlZcG1MIU0IXSQFDD1deRRlFXVZIUF5TXV9VEVRFRkFWRUdWWEAZRloHTQVeUAg"  # fill in: .m3u8 file url
REFERER = ""  # fill in: some websites require a specific referer website to allow the request

OUTNAME = 'video.ts'  # default output file name
LOC = ""  # default save location

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": REFERER,
    "DNT": "1",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache"
}


def getSegments(m3):
    """ figure out how many segments there are using the m3u8 file """
    lines = m3.text.split('\n')
    segments = []
    for line in lines:
        if 'https://' in line:
            segments.append(line)
    return segments


def dumpSegments(segments, path, append=False):
    """ downlaod and combine the .ts files
    the destination download path """
    with open(path, 'ab' if append else 'wb') as f:
        # i = 0
        n = len(segments)
        for i, segment in enumerate(segments):
            success = False
            while not success:
                try:
                    seg = requests.get(segment, headers=HEADERS)
                    success = True
                except:
                    print('retrying...')
            f.write(seg.content)
            print(('Downloading segment: %d' % i) + '  progress: %d%%\r' % (i * 100 / n), end="")


if __name__ == "__main__":
    DEST = LOC + OUTNAME
    if len(sys.argv) > 1:
        DEST = sys.argv[1]
    # validate destination:
    delim = ''
    if '\\' in DEST:
        delim = '\\'
    elif '/' in DEST:
        delim = '/'
    if delim:
        PATH = ''.join(DEST.split(delim)[:-1])
        if not os.path.isdir(PATH):
            print('INAVLID DESTINATION.')
            sys.exit(0)
    m3u8 = requests.get(M3URL, headers=HEADERS)
    segments = getSegments(m3u8)
    dumpSegments(segments, DEST)
