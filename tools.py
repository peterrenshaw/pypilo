#!/usr/bin/env python
# ~*~ encoding: utf-8 ~*~


#======
# name: tools.py
# date: 2020AUG16
#       2019SEP21
#       2019SEP17
#       2019SEP06
#       2019AUG11
#       2016FEB03
# prog: pr
# desc: tools for image processing
# urls: 
#       datetime
#       <http://strftime.org/>
#       <http://pleac.sourceforge.net/pleac_python/datesandtimes.html>
#======


import sys
import glob
import time
import os.path
import datetime


#------ debug start ---------
DEBUG = False
def msg(msg, is_debug=DEBUG):
    if is_debug: print("> {}".format(msg))
#------ debug end ---------


#------ date time start -----
#------
# desc: datetime string in YYYY MMM DD HH MM SS format
#       and display as "YYYYMMMDDTHH:MM.SS", components
#       are the following:
#       YYYY = %Y  -- full 4 digit year
#       MMM  = %b  -- truncated month, UC
#       DD   = %d  -- day, zero padded
#       HH   = %H  -- 24 hour, zero padded
#       MM   = %M  -- minute, zero padded
#       SS   = %S  -- second, zero padded
#------
DTF_YYYYMMMDDTHHMMSS = "%Y%b%dT%H:%M.%S"
DTF_YYYYMMMDDTHHMMSS_FN = "%Y%b%d%H%M%S"

#---------
# dt_date2str: convert datetime to string format for filenames
#  
# desc: 2019SEP21 removed dot due to truncation on flickr        
#---------
def dt_date2str(dt, dt_format=DTF_YYYYMMMDDTHHMMSS):
    """convert a valid date time to a string format"""
    if dt_format:
        dts = dt.strftime(dt_format)
        time_delta = format(time.process_time(), '.3f')    # remove dot
        dts = "{}{}".format(dts, time_delta)              # remove dot
        dts = dts.upper()
        return dts 
    else:
        return ""
#---------
# dt_get_now: WARNING have set to local time not UTC
#---------
def dt_get_now(is_utc=False):
    """return current, now  date time"""
    if is_utc:
        return datetime.datetime.utcnow()
    else:
        return datetime.datetime.now()
def dt2epoch(dt):
    """
    given datetime object, return epoch
    be aware of the differences b/w now 
    utc_now (local time and UTC time)
    """
    e = time.mktime(dt.timetuple())
    return e
def dt_build_date(yyyy, mmm, dd, hh=0, mm=0, ss=0):
    """
    build datetime obj from year, month, day, hour, min, seconds 
    """
    dt = datetime.datetime(yyyy, mmm, dd, hh, mm, ss)
    return dt
def dt_build_fn(ext):
    """build extention type, build filename in date format"""
    dt = dt_get_now()
    fn = dt_date2str(dt, dt_format=DTF_YYYYMMMDDTHHMMSS_FN)
    msg("fn <{}.{}>".format(fn, ext)) 
    return "{}.{}".format(fn, ext)
def dt_build_fn_jpg():
    return dt_build_fn(ext='jpg')
def dt_build_fn_png():
    return dt_build_fn(ext='png')


#------ date time end ------

#------ filenames start ------
def get_filenames(filepathdirectory, file_type="*.*"):
    """
    given a valid filepath, gather all 
    the files in that directory as a list
    by globbing them using glob.glob. Use
    file_type to restrict or wild-card the 
    types of files to select.
    """
    fpd = filepathdirectory
    msg("tools.get_filenames.filepath <{}>".format(fpd))

    if os.path.isdir(fpd):
       fpn = os.path.join(fpd, file_type)
       files = glob.glob(fpn)

       msg("tools.get_filenames.fpn <{}>".format(fpn))
       msg("tools.get_filenames <{}>".format(files))
 
       return files
    else:
       return []
def get_fn_jpg(filepath):
    """build list of JPG files, upper and lowercase"""
    fn = get_filenames(filepath, "*.jpg") + get_filenames(filepath, "*.JPG")
    msg("fn <{}>".format(fn))
    return fn
def get_fn_png(filepath):
    """build list of PNG files, upper and lowercase"""
    fn = get_filenames(filepath, "*.png") +  get_filenames(filepath, "*.PNG")
    msg("fn <{}>".format(fn))
    return fn 

#---------
# name: filepath2title:
# desc: extract filename from VALID filepathname
#       check FPN valid, use os.path.basename to extract info
# rets: filepath, filename
#---------
def filepath2title(fpn):
    """
    convert filepath (unix) to a filename use os.path.basename 
    to extract info

      eg: convert from /some/filepath/filename.jpg
                  to   filename
    """
    msg("filepath2title")
    if os.path.isfile(fpn):
        fn = os.path.dirname(fpn)
        fp = os.path.basename(fpn)

        msg("filepath <{}>".format(fp))
        msg("filename <{}>".format(fn)

        return [filepath, filename]
    else:
        msg("Warning: <{}> is invalid")
        return ""
#------ filenames end ------

def main():
    """cli entry point"""
    pass

#----- main cli entry point ------
if __name__ == "__main__":
    main()


## vim: ff=unix:ts=4:sw=4:tw=78:noai:expandtab

