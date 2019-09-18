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


import PIL
from PIL import Image
from PIL import ImageEnhance


from tools import msg


WIDTH = 1330    # hard coded width max
HEIGHT = 1000   # hard coded height max 


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
    h = 0
    w = 0
    try:
        i = Image.open(fpn)
        (w, h) = (i.width, i.height)
    except IOError:
        msg("Error: unable to resize image")
        sys.exit(1)
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
#       resize the image to the supplied dimensions
#---------
def pil_resize(src_fp, dest_fp, s_fn, d_fn):
    msg("source fp <{}>".format(src_fp))
    msg("dest   fp <{}>".format(dest_fp))
    try:
        # source filepath and nasrc_fp,me:
        sfpn = os.path.join(src_fp, s_fn)
        msg("src <{}>".format(sfpn))

        # destination filepath and name
        dfpn = os.path.join(dest_fp, d_fn)   
        msg("dest <{}>".format(dfpn))

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

        # resize image
        ir = i.resize((w, h))

        # save image
        ir.save(dfpn, "JPEG")

        i = None
        ir = None
    except IOError:
        print("Error: unable to resize image")
        sys.exit(1)
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
        print("Unable to load image")
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
