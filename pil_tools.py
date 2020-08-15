#!/usr/bin/env python
# ~*~ encoding: utf-8 ~*~


#======
# name: pil_tools.py
# date: 2019SEP17
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
def calc_image_size(width, height, ratio, resize_width=WIDTH, resize_height=HEIGHT):
    """  
    given height, width and ration: resize image width, height 
    and known image ratio, resize width and height to fixed 
    dimensions.
    """
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
    msg("setting image w<{}> h<{}> r<{}>".format(w, h, ratio))

    return (w, h)

#---------- PIL start ----------
#

#----------
# pil_get_wh: get the image width and height using PIL
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
def pil_resize(src_fp, dest_fp, s_fn, d_fn, ext):
    msg("pil_resize")
    msg("source fp <{}>".format(src_fp))
    msg("dest   fp <{}>".format(dest_fp))

    # source filepath and nasrc_fp,me:
    sfpn = os.path.join(src_fp, s_fn)
    msg("1. sfpn <{}>".format(sfpn))

    if not os.path.isfile(sfpn):
        print("\n")
        print("Error: cannot find specificed file <>".format(dfpn))
        print("")
        sys.exit(1)
    else:
        msg("2. src <{}>".format(sfpn))

    # destination filepath and name
    dfpn = os.path.join(dest_fp, d_fn)  
    if not os.path.isdir(dest_fp):
        print("\n")
        print("Error: destination file directory not found <{}>".format(dest_fp))
        print("Error: cannot save file <{}>".format(dfpn))
        print("")
        sys.exit(1)
    else:
        msg("3. dest <{}>".format(dfpn))

    msg("4. open <{}>".format(sfpn))
    try:
        # original image
        i = Image.open(sfpn)
        msg("height <{}>".format(i.height))
        msg("width  <{}>".format(i.width))

        # find image ratio
        #r = c_image_ratio_hw(i.height, i.width)
        r = image_ratio(i.width, i.height)
        msg("ratio <{}>".format(r))


        # set new image width and height f
        w, h = calc_image_size(i.width, i.height, r)
        msg("{}:{}".format(w, h))

        msg("5. resize image")
        # resize image
        ir = i.resize((w, h))

        msg("6. save image by TYPE")
        # save image
        ir.save(dfpn, ext)

        i = None
        ir = None
   
    except IOError:
        # we haven't found a way to process this
        # file, skip but still WARN? -- Na kill
        print("\n")
        print("Warning: unable to resize image")
        print("Warning: unable to move image file at the moment")
        print("\tfilename  <{}>".format(s_fn))
        print("\tsource fp <{}>".format(src_fp))
        print("\tdest   fp <{}>".format(dest_fp))
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
