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
    def __init__(self):
        home = os.environ['HOME']
        self.pymm_home = os.path.join(home, '.pymm')
        # check home, if none, warn and quit
        with open(os.path.join(self.pymm_home, 'config.json')) as config_file:
            self.config = json.load(config_file)

    def updata_database(self):
        def move_helper(old_path, path):
            dirpath = os.path.dirname(path)
            os.makedirs(dirpath, exist_ok=True)
            shutil.move(old_path, path)
        music_dir = self.config['music_dir']
        self.database = self.gen_database(music_dir)
        layout = self.config['layout']
        for entry in self.database:
            old_path = entry['path']
            _, extension = os.path.splitext(old_path)
            path = layout.format_map(entry) + extension
            path = os.path.join(music_dir, path)
            if path != old_path:
                move_helper(old_path, path)
                entry['path'] = path
        self.save_database()

    # def add_dir_do_database(self, mdir):
    #     self.load_database()
    #     metas = self.gen_database(mdir)
    #     for meta in metas:
    #         entry = self.search_database(meta)
    #         if entry:
    #             pass            # log
    #         else:
    #             self.database.append(meta)
    #     self.save_database()

    # def add_file_to_database(self, mfile):
    #     def copy_helper(old_path, path):
    #         dirpath = os.path.dirname(path)
    #         os.makedirs(dirpath, exist_ok=True)
    #         shutil.copyfile(old_path, path, follow_symlinks=False)
    #     self.load_database()
    #     meta = self.get_file_meta(mfile)
    #     if not meta:
    #         return None         # log
    #     entry = self.search_database(meta)
    #     if entry:
    #         return None         # log
    #     self.database.append(meta)
    #     self.save_database()

    # def search_database(self, meta):
    #     def meta_in_entry_helper(entry, meta):
    #         for k, v in meta:
    #             if k not in entry or entry[k] != v:
    #                 return False
    #         return True
    #     for entry in self.database:
    #         if meta_in_entry_helper(entry, meta):
    #             return entry
    #     return None

    def load_database(self):
        with open(os.path.join(self.pymm_home, self.config['database'])) as database_file:
            self.database = json.load(database_file)

    def save_database(self):
        with open(os.path.join(self.pymm_home, self.config['database']), mode='w') as database_file:
            json.dump(self.database, database_file, ensure_ascii=False, indent=4)
            database_file.write('\n')

    def gen_database(self, music_lib_path):
        if not os.path.isabs(music_lib_path):
            music_lib_path = os.path.abspath(music_lib_path)
        if not os.path.exists(music_lib_path):
            return False
        library = self.get_dir_meta(music_lib_path)
        return library

    def get_dir_meta(self, dirpath):
        meta = []
        subitems = os.listdir(dirpath)
        for item in subitems:
            # note dirpath must not be a root partition, e.x. 'C:'
            fullpath = os.path.join(dirpath, item)
            if os.path.isdir(fullpath):
                meta += self.get_dir_meta(fullpath)
            else:
                filemeta = self.get_file_meta(fullpath)
                if filemeta:
                    meta.append(filemeta)
        return meta

    def get_file_meta(self, mpath):
        mfile = mutagenx.File(mpath, easy=True)
        if not mfile:
            return None
        artist = mfile.get('artist')
        album = mfile.get('album')
        title = mfile.get('title')
        if artist and album and title:
            artist = artist[0]
            album = album[0]
            title = title[0]
            meta = {'artist': artist, 'album': album, 'title': title, 'path': mpath}
        else:
            return None
        return meta

def main():
    mm = pymm()
    mm.updata_database()
    # mm.gen_music_library('C:\\Users\\suxing\\Music\\BaiduMusicHD\\Songs')
    # print(mm.library)
    # mm.gen_music_library('C:\\Users\\suxing\\Downloads\\BaiduMusic\\Songs')
    # mm.gen_music_library('/home/suxing/Music')
    # print(mm.library)
    # print(len(mm.library))
    # mm.gen_music_library('/media/B23E0A2C3E09E9E5/Users/suxing/Music')
    # print(mm.library)
    # print(len(mm.library))
    # mm.gen_music_library('/media/B23E0A2C3E09E9E5/Users/suxing/Downloads/BaiduMusic')
    # print(mm.library)
    # print(len(mm.library))

import mutagenx
import os
import os.path
import json
import shutil
if __name__ == '__main__':
    main()

