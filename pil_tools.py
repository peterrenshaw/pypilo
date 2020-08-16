#!/usr/bin/env python
# ~*~ encoding: utf-8 ~*~


#======
# name: pil_tools.py
# date: 2020AUG16
#       2019SEP17
# prog: pr
# desc: tools for image processing
# urls: PIL
#       <https://github.com/python-pillow/Pillow>
#       <https://pillow.readthedocs.org/en/latest/handbook/index.html>
#
#       modulo
#       <https://docs.python.org/3.3/reference/expressions.html>
#
#       image ratio
#       <https://stackoverflow.com/questions/1186414/whats-the-algorithm-to-calculate-aspect-ratio>
#======


import os
import sys
from shutil import copyfile   # copy big .mp4 files


import PIL
from PIL import Image
from PIL import ImageEnhance


from tools import msg


WIDTH = 1330    # hard coded width max
HEIGHT = 1000   # hard coded height max 

IMG_PNG = 'png' # png file ext
IMG_JPG = 'jpg' # jpg file ext
VID_M4V = 'm4v' # m4v file ext


#----------
# calc_image_size: resize height and width given ratio
#                  this is specifically for flickr
#----------
def calc_image_size(width, height, ratio, 
                    resize_width=WIDTH,
                    resize_height=HEIGHT):
    """  
    given height, width and ration: resize image 
    width, height and known image ratio, resize 
    width and height to fixed dimensions.
    """
    # image need to be resized?
    if resize_width < width and resize_height < height:

        # image is wider than higher
        if width > height:
            w = resize_width #WIDTH
            h = int(w / ratio)

        # image is taller than wider
        elif width < height:
            w = resize_height #HEIGHT
            h = int(w / ratio)

        # image is square
        else:
            w = int(height * ratio)
            h = int(width * ratio)
    else:
        w = int(width)
        h = int(height)

    msg("setting image w<{}> h<{}> r<{}>".format(w, h, ratio))

    return (w, h)

#---------- PIL start ----------
#

#----------
# pil_get_wh: get the image width and height using PIL
#             WARN on error, do not fail
#----------
def pil_get_wh(fp, fn):
    """extract image height and width using PIL"""
    fpn = os.path.join(fp, fn)
    if os.path.isfile(fpn):
        h = 0
        w = 0
        try:
            i = Image.open(fpn)
            (w, h) = (i.width, i.height)
        except IOError:
            msg("Warning: cannot determine image height and width")
            msg("Warning: problems with file <>".format(fpn))
    else:
        msg("Warning: could not find file <>".format(fpn))  
    return [w, h]
#----------
# image_ratio: find image ratio, width/height
#----------
def image_ratio(w, h):
    """calculate image ratio given width and height"""
    return w/h
#----------
# pil_image_ratio: find image ratio, width/height
#----------
def pil_image_ratio(fp, fn):
    """find image ratio given image"""
    height = 0
    width = 0

    height, width = pil_get_wh(fp, fn)

    ratio = width/height
    msg("ratio <{}>".format(ration))

    return ratio
#---------
# name: pil_resize
# desc: grab an image, 
#       resize the image to the supplied dimensions. we
#       assume the source directory is pre-edited so if 
#       we still handle .mp4s. Control is done by editing
#       which files are in the source file.
#
# warn: THIS FUNCTION MOVES THE FILES TO A DESTINATION DIR.
#
# bugs: if we find a filetype we do not support, we flag this
#       as an error and continue. It's also a good idea to 
#       modify the filename to reflect if you want to use
#       the file. If you want to use the file, you will 
#       have to copy the file over.
#---------
def pil_resize(sfp, dfp, sfn, dfn, ext):
    msg("pil_resize")
    msg("source fp <{}>".format(sfp))
    msg("dest   fp <{}>".format(dfp))

    # source filepath and nasrc_fp,me:
    sfpn = os.path.join(sfp, sfn)
    msg("1. sfpn <{}>".format(sfpn))
    msg("    sfp <{}>".format(sfp))
    msg("    sfn <{}>".format(sfn))

    # valid source filepath name?
    if not os.path.isfile(sfpn):
        print("\n")
        print("Error: cannot find specificed file <>".format(sfpn))
        print("")
        sys.exit(1)
    msg("2. src <{}>".format(sfpn))


    # destination filepath and name
    # fail if you cannot find destination
    # directory. Best not spew files all
    # over the place when most likely the
    # error is operator on CLI.
    dfpn = os.path.join(dfp, dfn)
    msg("3. dest <{}>".format(dfpn)) 
    if not os.path.isdir(dfp):
        print("\n")
        print("Error: destination file directory not found <{}>".format(dfp))
        print("Error: cannot save file <{}>".format(dfpn))
        print("")
        sys.exit(1)
        

    msg("4. open <{}>".format(sfpn))
    try:
        # original image
        i = Image.open(fp=sfpn)
        msg("height <{}>".format(i.height))
        msg("width  <{}>".format(i.width))

        # find image ratio
        #r = c_image_ratio_hw(i.height, i.width)
        r = image_ratio(i.width, i.height)
        msg("ratio <{}>".format(r))       

        # set new image width and height f
        w, h = calc_image_size(i.width, i.height, r)
        msg("w ({}) h ({})".format(w, h))

        msg("5. resize image")
        ir = i.resize((w, h))

        msg("6. save image by TYPE")
        msg("dfpn <{}>".format(dfpn))
        msg("ext <{}>".format(ext))

        ir.save(dfpn)

        i = None
        ir = None
   
    except IOError:
        # we haven't found a way to process this
        # file, skip but still WARN? -- Na kill
        print("\n")
        print("Warning: unable to resize image")
        print("Warning: unable to move image file at the moment")
        print("\tfilename  <{}>".format(sfn))
        print("\tsource fp <{}>".format(sfp))
        print("\tdest   fp <{}>".format(dfp))
        print("")
        sys.exit(1)

    return True

#---------
# name: pil_detail
# desc: grab an image, 
#       report details
#---------
def pil_detail(fp, fn):
    fpn = os.path.join(fp, fn)
    try:
        i = Image.open(fpn)
    except IOError:
        print("Unable to load image to find information")
        sys.exit(1)
    msg("<{}>\n\tformat({}) size({}) mode:({})".format(fn, i.format, i.size, i.mode))
#
#
#---------- PIL end ----------
    

#----- main cli entry point start ------
def main():
    """cli entry point"""
    pass
if __name__ == "__main__":
    main()
#----- main cli entry point end ------



## vim: ff=unix:ts=4:sw=4:tw=78:noai:expandtab
