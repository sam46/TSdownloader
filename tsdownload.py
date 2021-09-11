""" download segmented mpeg video (.ts files) from streaming websites """
import sys
import os
import requests

M3URL = ""  # fill in: .m3u8 file url
SEG1URL = ""  # fill in: first ts segment file url
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


def getSegsNum(m3):
    """ figure out how many segments there are using the m3u8 file """
    lines = m3.text.split('\n')
    nsegs = 0
    for line in lines:
        if '.ts' in line:
            # tokens = line.split('-')
            # idx = 0
            # for i, tok in enumerate(tokens):
            #     if 'seg' == tok[-3:]:
            #         idx = i + 1
            #         break
            # nsegs = int(tokens[idx])
            nsegs = nsegs + 1
    print(nsegs)
    return nsegs


def dumpSegs(initUrl, n, path, append=False):
    """ downlaod and combine the .ts files
    given the first seg's url, the number of segments and
    the destination download path """
    with open(path, 'ab' if append else 'wb') as f:
        for i in range(0, n):
            # segurl = initUrl.replace('seg-1-', 'seg-{:d}-'.format(i))
            segurl = initUrl.replace('/0/', '/{:d}/'.format(i))
            print(segurl)
            success = False
            while not success:
                try:
                    seg = requests.get(segurl, headers=HEADERS)
                    success = True
                except:
                    print('retrying...')
            f.write(seg.content)
            print(('dumped seg%d.ts' % i) + '  %d%%' % (i * 100 / n))


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
    nsegs = getSegsNum(m3u8)
    dumpSegs(SEG1URL, nsegs, DEST)
