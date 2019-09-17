#!/usr/bin/env python
# ~*~ encoding: utf-8 ~*~


#======
# name: process.py
# date: 2019SEP10
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
#======


import sys
import os.path
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


#---------
# name: process
# desc: given the parameters, process a list of urls
#       and upload them.
# TODO: find todays date in YYYY,YYYYMMM format and add as 
#       default tags
#---------
def process(src_fp, dest_fp, s_fn, d_fn):
    pil_resize(src_fp, dest_fp, s_fn, d_fn)
    pil_detail(dest_fp, d_fn)


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
        if len(afiles) > 0: 
            # loop through the list of files
            msg("processing")

 
            for s_fpn in afiles:
                s_fp, s_fn = filepath2title(s_fpn)
                msg("source <{}> <{}>".format(s_fp, s_fn))
                if s_fn:
                    if os.path.isfile(s_fpn):
                        # process the files one by one
                        d_fn = dt_build_fn()
           
                        # image processing using:
                        #    source filepath
                        #    destination filepath
                        #    source filename
                        #    destination filename
                        process(s_fp, dest_fp, s_fn, d_fn)

                    else:
                        print("warning: the source file is not found")
                        print("         <{}>".format(s_fn))
                        pass
                else:
                    break      
  
        else:
            # load all files found
            pass


#----- main cli entry point ------
if __name__ == "__main__":
    main()



# vim: ff=unix:ts=4:sw=4:tw=78:noai:expandtab

