"""Module for manipulating SMPTE timecode. Supports 60, 59.94, 50, 30, 29.97, 25, 24, 23.98 frame rates in drop and non-drop where applicable, and milliseconds. It also supports
operator overloading for addition, subtraction, multiplication, and division.

iter_return sets the format that iterations return, the options are "tc" for a timecode string,
"frames" for a int total frames, and "tc_tuple" for a tuple of ints in the following format,
(hours, minutes, seconds, frames).

Notes: *There is a 24 hour SMPTE Timecode limit, so if your time exceeds that limit, it will roll over.
       *2 PyTimeCode objects of the same frame rate is the only supported way to combine PyTimeCode objects, 
            for example adding them together.

Copyright Joshua Banton"""


class PyTimeCode(object):
    def __init__(self, framerate, start_timecode = None, frames = None, drop_frame = False, iter_return="tc"):
        """frame rate can be string '60', '59.94', '50', '30', '29.97', '25', '24', '23.98', or 'ms'"""
        self.framerate = framerate
        self.int_framerate = self.set_int_framerate()
        self.drop_frame = drop_frame
        self.iter_return = iter_return
        self.hrs = None
        self.mins = None
        self.secs = None
        self.frs = None
        self.frames = None
        if start_timecode:
            self.set_timecode(start_timecode)
            self.tc_to_frames()
        elif not frames==None:#because 0==False, and frames can be 0
            self.frames = int(frames)
            self.frames_to_tc(frame_only=True)
        self.__check_drop_frame__()
        
    def set_timecode(self, timecode):
        """sets timecode to argument 'timecode'"""
        self.hrs, self.mins, self.secs, self.frs = self.parse_timecode(timecode)
        
    def tc_to_frames(self):
        """converts corrent timecode to frames"""
        frames = (((self.hrs * 3600) + (self.mins * 60) + self.secs) * self.int_framerate) + self.frs
        if self.drop_frame:
            del_frames = self.calc_drop_frames()
            frames = frames - del_frames
        self.frames = frames
        
    def frames_to_tc(self, frame_only=False):
        """converts frames back to timecode, if frame_only==True, it needs to
        calculate the drop frames without looking at self.hrs, etc."""
        if self.drop_frame:
            drop_frames = self.calc_drop_frames(frame_only)
            frames = self.frames + drop_frames
        else:
            frames = self.frames
        self.hrs = frames/(3600*self.int_framerate)
        #check to see if hours => 24. SMPTE Timecode only goes to 24 hours
        if self.hrs > 23:
            self.hrs = self.hrs % 24
            frames = frames - (24 * 3600 * self.int_framerate)
        self.mins = (frames%(3600*self.int_framerate))/(60*self.int_framerate)
        self.secs = ((frames%(3600*self.int_framerate))%(60*self.int_framerate))/self.int_framerate
        self.frs = ((frames%(3600*self.int_framerate))%(60*self.int_framerate))%self.int_framerate
        if self.drop_frame:
            if self.frs == 0 and (self.mins % 10): #tests to see if frames is 0 and if minutes is not an even 10, 20, 30, etc
                if self.framerate == '59.94':
                    self.frs = 4
                elif self.framerate == '29.97':
                    self.frs = 2
        self.tc_to_frames()
     
    def calc_drop_frames(self, frame_only=False):
        if frame_only:
            hours = self.frames/(3600*self.int_framerate)
            mins = (self.frames%(3600*self.int_framerate))/(60*self.int_framerate)
            if mins%10: #if the minutes is not a multiple of 10, there needs to be one more drop frame unit, 2 or 4
                extra = 1
            else:
                extra = 0
            if self.framerate == '59.94':
                return (hours * 6 * 36) + ((mins/10) *36) + (mins%10 * 4) + (extra * 4)
            elif self.framerate == '29.97':
                return (hours * 6 * 18) + ((mins/10) *18) + (mins%10 * 2) + (extra * 2)
        elif self.framerate == '59.94':
            return (self.hrs * 6 * 36) + ((self.mins/10) *36) + (self.mins%10 * 4)
        elif self.framerate == '29.97':
            return (self.hrs * 6 * 18) + ((self.mins/10) *18) + (self.mins%10 * 2)
        else:
            raise PyTimeCodeError('Drop frame with '+self.framerate+'fps not supported, only 29.97 & 59.94.') 
     
    def set_int_framerate(self):
        if self.framerate == '29.97':
            int_framerate = 30
        elif self.framerate == '59.94':
            int_framerate = 60
        elif self.framerate == '23.98':
            int_framerate = 24
        elif self.framerate == 'ms':
            int_framerate = 1000
        elif self.framerate == 'frames':
            int_framerate = 1
        else:
            int_framerate = int(self.framerate)
        return int_framerate
        
    def parse_timecode(self, timecode):
        """parses timecode string frames '00:00:00:00' or '00:00:00;00' or milliseconds '00:00:00:000'"""
        if len(timecode) == 11:
            frs = int(timecode[9:11])
        elif len(timecode) == 12 and self.framerate == 'ms':
            frs = int(timecode[9:12])
        else:
            raise PyTimeCodeError('Timecode string parsing error. ' + timecode)
        hrs = int(timecode[0:2])
        mins = int(timecode[3:5])
        secs = int(timecode[6:8])
        return hrs, mins, secs, frs
        
    def make_timecode(self):
        self.frames_to_tc()
        hr_str = self.__set_time_str(self.hrs)
        min_str = self.__set_time_str(self.mins)
        sec_str = self.__set_time_str(self.secs)
        frame_str = self.__set_time_str(self.frs)
        timecode_str = "%s:%s:%s:%s" % (hr_str, min_str, sec_str, frame_str)
        return timecode_str
        
    def __set_time_str(self, time):
        if len(str(time)) > 1:
            time_str = str(time)
        else:
            time_str = "0%s" % time
        return time_str
        
    def __iter__(self):
        return self
        
    def next(self):
        self.add_frames(1)
        return self.__return_item__()
        
    def back(self):
        self.sub_frames(1)
        return self.__return_item__()
                
    def __check_drop_frame__(self):
        if not self.drop_frame:
            return True
        elif self.framerate == "29.97" or self.framerate == "59.94":
            return True
        else:
            raise PyTimeCodeError('Drop frame with '+self.framerate+'fps not supported, only 29.97 & 59.94.')
    
    def __return_item__(self):
        if self.iter_return == 'tc':
            return self.make_timecode()
        elif self.iter_return == 'frames':
            return self.frames
        elif self.iter_return == 'tc_tuple':
            return (self.hrs, self.mins, self.secs, self.frs)
    
    def add_frames(self, frames):
        """adds or subtracts frames number of frames"""
        self.frames = self.frames + frames
        
    def sub_frames(self, frames):
        """adds or subtracts frames number of frames"""
        self.__add_timecode__(-frames)
        
    def mult_frames(self, frames):
        """adds or subtracts frames number of frames"""
        self.frames = self.frames * frames
        
    def div_frames(self, frames):
        """adds or subtracts frames number of frames"""
        self.frames = self.frames / frames
        
    def __add__(self, other):
        """returns new pytimecode object with added timecodes"""
        if type(other) == PyTimeCode:
            added_frames = self.frames + other.frames
        elif type(other) == int:
            added_frames = self.frames + other
        else:
            raise PyTimeCodeError('Type '+str(type(other))+' not supported for arithmetic.')
        newtc = PyTimeCode(self.framerate, start_timecode=None, frames=added_frames, drop_frame=self.drop_frame)
        return newtc
        
    def __sub__(self, other):
        """returns new pytimecode object with added timecodes"""
        if type(other) == PyTimeCode:
            subtracted_frames = self.frames - other.frames
        elif type(other) == int:
            subtracted_frames = self.frames - other
        else:
            raise PyTimeCodeError('Type '+str(type(other))+' not supported for arithmetic.')
        newtc = PyTimeCode(self.framerate, start_timecode=None, frames=subtracted_frames, drop_frame=self.drop_frame)
        return newtc
        
    def __mul__(self, other):
        """returns new pytimecode object with added timecodes"""
        if type(other) == PyTimeCode:
            mult_frames = self.frames * other.frames
        elif type(other) == int:
            mult_frames = self.frames * other
        else:
            raise PyTimeCodeError('Type '+str(type(other))+' not supported for arithmetic.')
        newtc = PyTimeCode(self.framerate, start_timecode=None, frames=mult_frames, drop_frame=self.drop_frame)
        return newtc 
        
    def __div__(self, other):
        """returns new pytimecode object with added timecodes"""
        if type(other) == PyTimeCode:
            div_frames = self.frames / other.frames
        elif type(other) == int:
            div_frames = self.frames /other
        else:
            raise PyTimeCodeError('Type '+str(type(other))+' not supported for arithmetic.')
        newtc = PyTimeCode(self.framerate, start_timecode=None, frames=div_frames, drop_frame=self.drop_frame)
        return newtc 
    
    def __repr__(self):
        return self.make_timecode()
        
class PyTimeCodeError(Exception):
    pass