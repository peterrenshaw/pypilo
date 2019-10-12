#!/usr/bin/env python
# ~*~ encoding: utf-8 ~*~


#======
# name: process.py
# date: 2019SEP21
#       2019SEP10
# prog: pr
# desc: process a file ready or flickr
# algo: 
#       given source directory
#           process all images
#           copy all images to destination directory
#       destination directory read for flickr.
#
# urls: <https://python-pillow.org>
#       <https://pillow.readthedocs.io/en/stable/handbook/tutorial.html>
#       <http://zetcode.com/python/pillow/>
#       <http://www.network-science.de/ascii/>
#       <https://stackoverflow.com/questions/493386/how-to-print-without-newline-or-space>
#======


import sys
import os.path
from shutil import copyfile        # copy big .mp4 files
from optparse import OptionParser


from tools import msg
from tools import DEBUG
from tools import get_fn_jpg
from tools import dt_get_now
from tools import dt_date2str
from tools import dt_build_fn
from tools import get_filenames
from tools import filepath2title
from tools import DTF_YYYYMMMDDTHHMMSS_FN 


from pil_tools import pil_detail
from pil_tools import pil_resize


IMG_JPG = 'jpg'
VID_M4V = 'm4v'



#---------
# name: process
# desc: wrapper for image and video processing
# args: afiles - list of filepathnames
#---------
def process(afiles, dest_fp):
    if len(afiles) > 0: 
        # loop through the list of files
        msg("processing")
  
        afs = sorted(afiles)
        for s_fpn in afs:
            s_fp, s_fn = filepath2title(s_fpn)
            msg("source <{}> <{}>".format(s_fp, s_fn))
            if s_fn:
                if os.path.isfile(s_fpn):
                    # process the files one by one
                    if is_file_jpg(s_fn):
                        print('.', end='', flush=True)
                        d_fn = dt_build_fn()
                        process_image(s_fp, dest_fp, s_fn, d_fn)

                    elif is_file_video(s_fn):
                        print('+', end='', flush=True)
                        d_fn = dt_build_fn(ext=VID_M4V)
                        process_video(s_fp, dest_fp, s_fn, d_fn)

                    else: 
                        print("Warning: file not processed")
                        print("\t<{}>".format(s_fn))

                else:
                    print("warning: the source file is not found")
                    print("         <{}>".format(s_fn))
                    pass
            else:
               break    
        print("")

        return True
    else:
        # load all files found
        return False


#---------
# name: process_image
# desc: given the parameters, process a list of urls
#       and upload them.
# TODO: find todays date in YYYY,YYYYMMM format and add as 
#       default tags
#---------
def process_image(src_fp, dest_fp, s_fn, d_fn):
    pil_resize(src_fp, dest_fp, s_fn, d_fn)
    pil_detail(dest_fp, d_fn)

def process_video(src_fp):
    """process all the videos"""
    # move the file (we still want to use it)
    sfpn = os.path.join(src_fp, s_fn)
    dfpn = os.path.join(dest_fp, d_fn)
    msg("move <{}> to <{}>".format(sfpn, dfpn))

    try: 
        copyfile(sfpn, dfpn)               
    except IOError:
        print("Error: unable to move image file")
        print("\tfilename  <{}>".format(s_fn))
        print("\tsource fp <{}>".format(src_fp))
        print("\tdest   fp <{}>".format(dest_fp))
        print("\tsfpn <{}>".format(sfpn))
        print("\tdfpn <{}>".format(dfpn))
     
        sys.exit(1)
 
    return True

def is_file_jpg(fn, ext=IMG_JPG):
    f = fn.lower()
    return (f.find(ext) > 0)
def is_file_video(fn, ext=VID_M4V):
    f = fn.lower()
    return (f.lower().find(ext) > 0)


#---------
# desc: main cli method
#---------
def main():
    """cli entry point"""
    usage = "usage: %prog -i -o [-s]"
    parser = OptionParser(usage)

    #------ in/out ------
    parser.add_option("-i", "--input", dest="input",
                      help="input source directory")
    parser.add_option("-o", "--output", dest="output",
                      help="output source directory"),
    parser.add_option("-j", "--jpg", dest="jpg",
                      action="store_true", 
                      help="process only jpg files")

    #------ options ------ 
    options, args = parser.parse_args()  

 
    #------ process ------
    if options.input:
        # only load 'jpg' images
        msg("path: <{}>".format(options.input))
        if options.jpg:
            
            afiles = get_fn_jpg(options.input)
        else:
            afiles = get_filenames(options.input)
        msg("files {}".format(afiles))

    
        # where do the processed files go? 
        if options.output:
            dest_fp = options.output
        else:
            dest_fp = os.curdir


        msg("destination: ({}) <{}>".format(len(afiles), afiles))
        if not process(afiles, dest_fp):
            print("Error: processing files has failed")
            sys.exit(1)
        

#----- main cli entry point ------
if __name__ == "__main__":
    main()



# vim: ff=unix:ts=4:sw=4:tw=78:noai:expandtab

