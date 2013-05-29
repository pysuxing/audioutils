#! /usr/bin/python

# filename:
#     mp3tag2musiclib.py
# description
#     a small utility designed to help to manage the author's music library. 
#     Read mp3 media tags, mv mp3 files to music directories
#     according to the music library structure.
#     The music library structure is descripted below.
#     ${MusicLibrary}/Artist/Album/"Artist - Title"
# author
#     SuXing, pysuxing@gmail.com


# process single mp3 file
def process_single_mp3file(music_lib_root, mp3file_name):
    print 'process_single_mp3file %s' % mp3file_name
    if not os.path.exists(mp3file_name):
        print 'file "%s" doesn\'t exist!' % mp3file_name
        return False
    origin_file_name = mp3file_name
    mp3file = mutagen.mp3.Open(origin_file_name)
    mp3file_name = os.path.basename(origin_file_name)
    (name, ext) = os.path.splitext(mp3file_name)
    if not ext == '.mp3':
        print '%s is not a mp3 file!' % mp3file_name
        return False
    if 'TIT2' not in mp3file:
        print 'No title info in mp3 file "%s"' % origin_file_name
        return False
    title = mp3file['TIT2']         # title
    title_text = title.text[0]
    if 'TPE1' not in mp3file:
        print 'No artist info in mp3 file "%s"' % origin_file_name
        return False
    artist = mp3file['TPE1']        # artist
    artist_text = artist.text[0]
    if 'TALB' not in mp3file:
        print 'No album info in mp3 file "%s"' % origin_file_name
        return False
    album = mp3file['TALB']         # album
    album_text = album.text[0]
    # generate target path
    artist_path = music_lib_root + os.sep + artist_text
    if not os.path.exists(artist_path):
        os.mkdir(artist_path)
    album_path = artist_path + os.sep + album_text
    if not os.path.exists(album_path):
        os.mkdir(album_path)
    file_name = artist_text + ' - ' + title_text + ext
    target_path = album_path + os.sep + file_name
    # rename mp3 file
    #shutil.copy(origin_file_name, target_path) # debug mode
    shutil.move(origin_file_name, target_path) # release mode
    return True

def process_directory(music_lib_root, directory, is_recursively = False):
    print 'process_directory %s' % directory
    if not os.path.exists(directory):
        print 'directory "%s" doesn\'t exist!' % directory
        return False
    # walk through the directory and check its sub items
    directory = directory.rstrip(os.sep)
    sub_items = os.listdir(directory)
    for filename in sub_items:
        # if in recursive mode, check all subdirectories
        if is_recursively:
            if os.path.isdir(directory+os.sep+filename):
                if not process_directory(music_lib_root, directory+os.sep+filename, is_recursively):
                    return False
        if filename.endswith('.mp3'):
            if not process_single_mp3file(music_lib_root, directory+os.sep+filename):
                return False
    return True

# main process
def main():
    allowed_options = 'd:r'
    allowed_long_options = 'directory= recursively'.split()
    try:
        opts, args = getopt.getopt(sys.argv[1:], allowed_options, allowed_long_options)
    except getopt.GetoptError, err:
        print str(err)
        print 'usage: %s [-d][-r] directory mp3file [mp3file2 ...]' % sys.argv[0]
        sys.exit(1)
    home_director = os.getenv('HOME')
    if home_director != None:
        music_lib_root = home_director + os.sep + 'Music'
    else:
        music_lib_root = '.'
    directorys = []
    files = []
    is_recursively = False
    for opt, value in opts:
        if opt == '-d' or opt == '--directory':
            directorys.append(value)
        elif opt == '-r' or opt == '--recursively':
            is_recursively = True
        else:
            assert False, 'unhandled option'
    for file_item in args:
        process_single_mp3file(music_lib_root, file_item)
    for dir_item in directorys:
        process_directory(music_lib_root, dir_item, is_recursively)
    return

import mutagen.mp3
import os
import sys
import shutil
import getopt
if __name__ == '__main__':
    main()

