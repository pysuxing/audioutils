#! /usr/bin/python

# description
#     a small utility designed to help to manage the author's music library. 
#     Read mp3 media tags, mv mp3 files to music directories
#     according to the music library structure.
#     The music library structure is descripted below.
#     ${MusicLibrary}/Artist/Album/"Artist - Title"
# author
#     SuXing, pysuxing@gmail.com

class pymm():
    def gen_music_library(self, music_lib_path):
        if not os.path.isabs(music_lib_path):
            music_lib_path = os.path.abspath(music_lib_path)
        if not os.path.exists(music_lib_path):
            return False
        self.library = self.get_dir_meta(music_lib_path)

    def get_dir_meta(self, dirpath):
        meta = []
        subitems = os.listdir(dirpath)
        for item in subitems:
            # note dirpath must not be a root partition, e.x. 'C:'
            fullpath = os.path.join(dirpath, item)
            if os.path.isdir(item):
                meta += self.get_dir_meta(fullpath)
            else:
                filemeta = self.get_file_meta(fullpath)
                if filemeta:
                    meta.append(filemeta)
        return meta

    def get_file_meta(self, mpath):
        # if not os.path.isabs(mpath):
        #     mpath = os.path.abspath(mpath)
        # if not os.path.exists(mpath):
        #     return False
        meta = {}
        mfile = mutagenx.File(mpath, easy=True)
        if mfile:
            meta = {'artist': mfile.get('artist'),
                    'album': mfile.get('album'),
                    'title': mfile.get('title')}
        return meta

def main():
    mm = pymm()
    # mm.gen_music_library('C:\\Users\\suxing\\Music\\BaiduMusicHD\\Songs')
    # print(mm.library)
    # mm.gen_music_library('C:\\Users\\suxing\\Downloads\\BaiduMusic\\Songs')
    mm.gen_music_library('E:\\Music')
    print(mm.library)

import mutagenx
import os
import os.path
import shutil
if __name__ == '__main__':
    main()

