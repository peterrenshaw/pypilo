#!/usr/bin/env python3
# ~*~ encoding: utf-8 ~*~


#======
# name: process.py
# date: 2020AUG16
#       2019NOV28
#       2019NOV03
#       2019OCT29
#       2019SEP21
#       2019SEP10
# prog: pr
# desc: process a file ready for flickr
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
from tools import get_fn_png 
from tools import dt_get_now
from tools import dt_date2str
from tools import dt_build_fn
from tools import dt_build_fn_png
from tools import dt_build_fn_jpg
from tools import get_filenames
from tools import filepath2title
from tools import DTF_YYYYMMMDDTHHMMSS_FN 


from pil_tools import IMG_PNG
from pil_tools import IMG_JPG
from pil_tools import VID_M4V
from pil_tools import pil_detail
from pil_tools import pil_resize


#---------
# is_file_xxx: input a filename, ext
#              can the file be found?
#---------
def get_file_ext(fnp):
    ext = os.path.splitext(fnp)[1].lower()
    ext = ext.replace(".","")
    return ext
def is_file_ext(fn, ext):
    fn = fn.lower()
    e = get_file_ext(fn)
    msg("fn=<{}> ext=<{}> ({})".format(fn, e,  (e == ext)))
    return (e == ext)
def is_file_jpg(fn, ext=IMG_JPG):
    return is_file_ext(fn, ext)
def is_file_png(fn, ext=IMG_PNG):
    return is_file_ext(fn, ext)
def is_file_video(fn, ext=VID_M4V):
    return is_file_ext(fn, ext)

#---------
# name: process
# desc: wrapper for image and video processing
# args: afiles - list of filepathnames
#---------
def process(afiles, dfp):
    msg("process")
    if len(afiles) > 0: 
        # loop through the list of files
        msg("processing")
  
        afs = sorted(afiles)
        for sfpn in afs:
            msg("sfpn <{}>".format(sfpn))

            # extract filepath and filename
            sfp, sfn = filepath2title(sfpn)
            msg("source filepath <{}>".format(sfp))
            msg("source filename <{}>".format(sfn))

            if sfn:
                isf = os.path.isfile(sfpn)
                msg("file exist: <{}> is {}".format(sfpn, isf ))

                # process file depending on file extension
                # if supported, process otherwise flag and
                # continue.
                if os.path.isfile(sfpn):
                    # process the files one by one
                    if is_file_jpg(sfn):

                        print('>', end='', flush=True)
                        dfn = dt_build_fn_jpg()
                        process_image(sfp, dfp, sfn, dfn, IMG_JPG)
                    elif is_file_png(sfn):

                        print('<', end='', flush=True)
                        dfn = dt_build_fn_png()
                        process_image(sfp, dfp, sfn, dfn, IMG_PNG)
                    elif is_file_video(sfn):

                        print('|', end='', flush=True)
                        dfn = dt_build_fn(ext=VID_M4V)
                        process_video(sfp, dfp, sfn, dfn)
                    else: 
                        msg("Warning: file not processed")
                        msg("source filename <{}>".format(sfn))
                        print("?")

                else:
                    print("warning: the source file is not found")
                    print("         <{}>".format(sfn))
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
def process_image(sfp, dfp, sfn, dfn, ext):
    msg("sr_fp {}".format(sfp))
    msg("dest_fp {}".format(dfp))
    msg("s_fn {}".format(sfn))
    msg("d_fn {}".format(dfn))

    # resize or fail
    # TODO: Why is this happening
    if not pil_resize(sfp, dfp, sfn, dfn, ext):
      sfpn = os.path.join(sfp, sfn)
      dfpn = os.path.join(dfp, dfn)
      msg("warning: image <{}> cannot be resized".format(sfpn))
      msg("move <{}> to <{}>".format(sfpn, dfpn))
      copyfile(sfpn, dfpn) 
      #sys.exit(1)

      return False
    else:
      return True

def process_video(sfp, dfp, sfn, dfn):
    """process all the videos"""
    # move the file (we still want to use it)
    sfpn = os.path.join(sfp, sfn)
    dfpn = os.path.join(dfp, dfn)
    msg("move <{}> to <{}>".format(sfpn, dfpn))

    try: 
        copyfile(sfpn, dfpn)               
    except IOError:
        print("Error: unable to move video file")
        print("\tfilename  <{}>".format(sfn))
        print("\tsource fp <{}>".format(sfp))
        print("\tdest   fp <{}>".format(dfp))
        print("\tsfpn <{}>".format(sfpn))
        print("\tdfpn <{}>".format(dfpn))
     
        sys.exit(1)
 
    return True

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
    parser.add_option("-p", "--png", dest="png",
                      action="store_true", 
                      help="process only png files")

    #------ options ------ 
    options, args = parser.parse_args()  

 
    #------ process ------
    if options.input:
        # input directory must exist
        if not os.path.isdir(options.input):
            print("Error:   processing input files has failed")
            print("Warning: <{}> is ({})".format(options.input, os.path.isdir(options.input)))
            print("")
            sys.exit(1)
        else:
            msg("source: <{}> is dir {}".format(options.input, os.path.isdir(options.input)))

        # only load 'jpg' images
        if options.jpg:
            afiles = get_fn_jpg(options.input)

        # only load 'png' images
        elif options.png:
            afiles = get_fn_png(options.input)

        # load all the files, skip the ones we can't work with
        else:
            afiles = get_filenames(options.input)
        msg("files {}".format(afiles))
    
        # where do the processed files go?
        dest_fp = ""
        if options.output:
            if os.path.isdir(options.output):
                dest_fp = options.output
            else:
                print("Warning: Trying to save files to an invalid directory")
                print("         I suggest manually creating the directory")
                print("")
                sys.exit(1)
        else:
            print("Error: Destination path must be supplied")
            print("")
            sys.exit(1)
            
        # process the files
        if process(afiles, dest_fp):
            msg("destination: ({}) <{}>".format(len(afiles), afiles))
        else:
            print("Error:   processing files has failed")
            print("Warning: <{}> is ({})".format(dest_fp, os.path.isdir(dest_fp)))
            print("")
            sys.exit(1)

        

#----- main cli entry point ------
if __name__ == "__main__":
    main()



# vim: ff=unix:ts=4:sw=4:tw=78:noai:expandtab

