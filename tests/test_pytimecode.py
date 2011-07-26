"""Testing for pytimecode"""

import pytimecode

class TestPyTimeCode:        

    def setup_class(self):
        """ sets shit up for 
        """
        pass

    def teardown_class(self):
        """ teardown any state that was previously setup
            with a call to setup_class.
        """
        pass
        
    def test_instan(self):
        timeobj = pytimecode.PyTimeCode('24', '00:00:00:00')
        timeobj = pytimecode.PyTimeCode('23.98', '00:00:00:00')
        timeobj = pytimecode.PyTimeCode('29.97', '00:00:00:00')
        timeobj = pytimecode.PyTimeCode('30', '00:00:00:00')
        timeobj = pytimecode.PyTimeCode('60', '00:00:00:00')
        timeobj = pytimecode.PyTimeCode('59.94', '00:00:00:00')
        timeobj = pytimecode.PyTimeCode('ms', '03:36:09:230')
        timeobj = pytimecode.PyTimeCode('24', start_timecode=None, frames=12000)
        
    def test_repr_overload(self):
        timeobj = pytimecode.PyTimeCode('24', '01:00:00:00')
        assert timeobj.__repr__() == '01:00:00:00'
        timeobj = pytimecode.PyTimeCode('23.98', '20:00:00:00')
        assert timeobj.__repr__() == '20:00:00:00'
        timeobj = pytimecode.PyTimeCode('29.97', '00:09:00:00')
        assert timeobj.__repr__() == '00:09:00:00'
        timeobj = pytimecode.PyTimeCode('30', '00:10:00:00')
        assert timeobj.__repr__() == '00:10:00:00'
        timeobj = pytimecode.PyTimeCode('60', '00:00:09:00')
        assert timeobj.__repr__() == '00:00:09:00'
        timeobj = pytimecode.PyTimeCode('59.94', '00:00:20:00')
        assert timeobj.__repr__() == '00:00:20:00'
        timeobj = pytimecode.PyTimeCode('ms', '00:00:00:900')
        assert timeobj.__repr__() == '00:00:00:900'
        timeobj = pytimecode.PyTimeCode('24', start_timecode=None, frames=49)
        print timeobj.int_framerate
        assert timeobj.__repr__() == '00:00:02:01'
        
    def test_timecode_init(self):
        tc = pytimecode.PyTimeCode('29.97', '00:00:00:01', drop_frame=True)
        assert tc.frames == 1
        tc = pytimecode.PyTimeCode('29.97', '03:36:09:23', drop_frame=True)
        assert tc.frames == 388703
        tc = pytimecode.PyTimeCode('29.97', '03:36:09:23')
        assert tc.frames == 389093
        tc = pytimecode.PyTimeCode('30', '03:36:09:23')
        assert tc.frames == 389093
        tc = pytimecode.PyTimeCode('25', '03:36:09:23')
        assert tc.frames == 324248
        tc = pytimecode.PyTimeCode('59.94', '03:36:09:23')
        assert tc.frames == 778163
        tc = pytimecode.PyTimeCode('60', '03:36:09:23')
        assert tc.frames == 778163
        tc = pytimecode.PyTimeCode('59.94', '03:36:09:23', drop_frame=True)
        assert tc.frames == 777383
        tc = pytimecode.PyTimeCode('23.98', '03:36:09:23')
        assert tc.frames == 311279
        tc = pytimecode.PyTimeCode('24', '03:36:09:23')
        assert tc.frames == 311279
        tc = pytimecode.PyTimeCode('ms', '03:36:09:230')
        assert tc.hrs == 3
        assert tc.mins == 36
        assert tc.secs == 9
        assert tc.frs == 230
        tc = pytimecode.PyTimeCode('24', start_timecode=None, frames=12000)
        assert tc.make_timecode() == '00:08:20:00'
        tc = pytimecode.PyTimeCode('29.97', start_timecode=None, frames=2589407, drop_frame=True)
        assert tc.make_timecode() == '23:59:59:29'
        tc = pytimecode.PyTimeCode('29.97', start_timecode=None, frames=2589408, drop_frame=True)
        assert tc.make_timecode() == '00:00:00:00'
        tc = pytimecode.PyTimeCode('59.94', start_timecode=None, frames=5178815, drop_frame=True)
        assert tc.make_timecode() == '23:59:59:59'
        tc = pytimecode.PyTimeCode('59.94', start_timecode=None, frames=5178816, drop_frame=True)
        assert tc.make_timecode() == '00:00:00:00'
        
    def test_frame_to_tc(self):
        tc = pytimecode.PyTimeCode('29.97', '00:00:00:01', drop_frame=True)
        tc.frames_to_tc()
        print tc.hrs, tc.mins, tc.secs, tc.frs
        assert tc.hrs == 0
        assert tc.mins == 0
        assert tc.secs == 0
        assert tc.frs == 1
        assert tc.make_timecode() == '00:00:00:01'
        tc = pytimecode.PyTimeCode('29.97', '03:36:09:23', drop_frame=True)
        tc.frames_to_tc()
        print tc.hrs, tc.mins, tc.secs, tc.frs
        assert tc.hrs == 3
        assert tc.mins == 36
        assert tc.secs == 9
        assert tc.frs == 23
        tc = pytimecode.PyTimeCode('29.97', '03:36:09:23')
        print tc.hrs, tc.mins, tc.secs, tc.frs
        assert tc.hrs == 3
        assert tc.mins == 36
        assert tc.secs == 9
        assert tc.frs == 23
        tc = pytimecode.PyTimeCode('30', '03:36:09:23')
        print tc.hrs, tc.mins, tc.secs, tc.frs
        assert tc.hrs == 3
        assert tc.mins == 36
        assert tc.secs == 9
        assert tc.frs == 23
        tc = pytimecode.PyTimeCode('25', '03:36:09:23')
        print tc.hrs, tc.mins, tc.secs, tc.frs
        assert tc.hrs == 3
        assert tc.mins == 36
        assert tc.secs == 9
        assert tc.frs == 23
        tc = pytimecode.PyTimeCode('59.94', '03:36:09:23')
        print tc.hrs, tc.mins, tc.secs, tc.frs
        assert tc.hrs == 3
        assert tc.mins == 36
        assert tc.secs == 9
        assert tc.frs == 23
        tc = pytimecode.PyTimeCode('60', '03:36:09:23')
        print tc.hrs, tc.mins, tc.secs, tc.frs
        assert tc.hrs == 3
        assert tc.mins == 36
        assert tc.secs == 9
        assert tc.frs == 23
        tc = pytimecode.PyTimeCode('59.94', '03:36:09:23', drop_frame=True)
        print tc.hrs, tc.mins, tc.secs, tc.frs
        assert tc.hrs == 3
        assert tc.mins == 36
        assert tc.secs == 9
        assert tc.frs == 23
        tc = pytimecode.PyTimeCode('23.98', '03:36:09:23')
        print tc.hrs, tc.mins, tc.secs, tc.frs
        assert tc.hrs == 3
        assert tc.mins == 36
        assert tc.secs == 9
        assert tc.frs == 23
        tc = pytimecode.PyTimeCode('24', '03:36:09:23')
        print tc.hrs, tc.mins, tc.secs, tc.frs
        assert tc.hrs == 3
        assert tc.mins == 36
        assert tc.secs == 9
        assert tc.frs == 23
        tc = pytimecode.PyTimeCode('ms', '03:36:09:230')
        tc.frames_to_tc()
        print tc.hrs, tc.mins, tc.secs, tc.frs
        assert tc.hrs == 3
        assert tc.mins == 36
        assert tc.secs == 9
        assert tc.frs == 230
        tc = pytimecode.PyTimeCode('24', start_timecode=None, frames=12000)
        assert tc.make_timecode() == '00:08:20:00'
        assert tc.hrs == 0
        assert tc.mins == 8
        assert tc.secs == 20
        assert tc.frs == 0
        
    def test_drop_frame(self):
        tc = pytimecode.PyTimeCode('59.94', '13:36:59:59', drop_frame=True)
        timecode = tc.next()
        assert timecode == "13:37:00:04"
        tc = pytimecode.PyTimeCode('29.97', '13:36:59:29', drop_frame=True)
        timecode = tc.next()
        assert timecode == "13:37:00:02"
        tc = pytimecode.PyTimeCode('59.94', '13:39:59:59', drop_frame=True)
        timecode = tc.next()
        assert timecode == "13:40:00:00"
        tc = pytimecode.PyTimeCode('29.97', '13:39:59:29', drop_frame=True)
        timecode = tc.next()
        assert timecode == "13:40:00:00"
        
    def test_iteration(self):
        tc = pytimecode.PyTimeCode('29.97', '03:36:09:23', drop_frame=True)
        for x in range(60):
            t = tc.next()
            assert t
        assert t == "03:36:11:27"
        assert tc.frames == 388767
        tc = pytimecode.PyTimeCode('29.97', '03:36:09:23')
        for x in range(60):
            t = tc.next()
            assert t
        assert t == "03:36:11:23"
        assert tc.frames == 389153
        tc = pytimecode.PyTimeCode('30', '03:36:09:23')
        for x in range(60):
            t = tc.next()
            assert t
        assert t == "03:36:11:23"
        assert tc.frames == 389153
        tc = pytimecode.PyTimeCode('25', '03:36:09:23')
        for x in range(60):
            t = tc.next()
            assert t
        assert t == "03:36:12:08"
        assert tc.frames == 324308
        tc = pytimecode.PyTimeCode('59.94', '03:36:09:23')
        for x in range(60):
            t = tc.next()
            assert t
        assert t == "03:36:10:23"
        assert tc.frames == 778223
        tc = pytimecode.PyTimeCode('60', '03:36:09:23')
        for x in range(60):
            t = tc.next()
            assert t
        assert t == "03:36:10:23"
        assert tc.frames == 778223
        tc = pytimecode.PyTimeCode('59.94', '03:36:09:23', drop_frame=True)
        for x in range(60):
            t = tc.next()
            assert t
        assert t == "03:36:10:27"
        assert tc.frames == 777447
        tc = pytimecode.PyTimeCode('23.98', '03:36:09:23')
        for x in range(60):
            t = tc.next()
            assert t
        assert t == "03:36:12:11"
        assert tc.frames == 311339
        tc = pytimecode.PyTimeCode('24', '03:36:09:23')
        for x in range(60):
            t = tc.next()
            assert t
        assert t == "03:36:12:11"
        assert tc.frames == 311339
        tc = pytimecode.PyTimeCode('ms', '03:36:09:230')
        for x in range(60):
            t = tc.next()
            assert t
        assert t == '03:36:09:290'
        assert tc.frames == 12969290
        tc = pytimecode.PyTimeCode('24', start_timecode=None, frames=12000)
        for x in range(60):
            t = tc.next()
            assert t
        assert t == "00:08:22:12"
        assert tc.frames == 12060
        
    def test_op_overloads_add(self):
        tc = pytimecode.PyTimeCode('29.97', '03:36:09:23', drop_frame=True)
        tc2 = pytimecode.PyTimeCode('29.97', '00:00:29:23', drop_frame=True)
        d = tc + tc2
        f = tc + 893
        print tc.frames, tc2.frames
        assert d.make_timecode() == "03:36:39:18"
        assert d.frames == 389598
        assert f.make_timecode() == "03:36:39:18"
        assert f.frames == 389598
        tc = pytimecode.PyTimeCode('29.97', '03:36:09:23')
        tc2 = pytimecode.PyTimeCode('29.97', '00:00:29:23')
        d = tc + tc2
        f = tc + 893
        assert d.make_timecode() == "03:36:39:16"
        assert d.frames == 389986
        assert f.make_timecode() == "03:36:39:16"
        assert f.frames == 389986
        tc = pytimecode.PyTimeCode('30', '03:36:09:23')
        tc2 = pytimecode.PyTimeCode('30', '00:00:29:23')
        d = tc + tc2
        f = tc + 893
        assert d.make_timecode() == "03:36:39:16"
        assert d.frames == 389986
        assert f.make_timecode() == "03:36:39:16"
        assert f.frames == 389986
        tc = pytimecode.PyTimeCode('25', '03:36:09:23')
        tc2 = pytimecode.PyTimeCode('25', '00:00:29:23')
        d = tc + tc2
        f = tc + 748
        assert d.make_timecode() == "03:36:39:21"
        assert d.frames == 324996
        assert f.make_timecode() == "03:36:39:21"
        assert f.frames == 324996 
        tc = pytimecode.PyTimeCode('59.94', '03:36:09:23')
        tc2 = pytimecode.PyTimeCode('59.94', '00:00:29:23')
        d = tc + tc2
        f = tc + 1763
        assert d.make_timecode() == "03:36:38:46"
        assert d.frames == 779926
        assert f.make_timecode() == "03:36:38:46"
        assert f.frames == 779926 
        tc = pytimecode.PyTimeCode('60', '03:36:09:23')
        tc2 = pytimecode.PyTimeCode('60', '00:00:29:23')
        d = tc + tc2
        f = tc + 1763
        assert d.make_timecode() == "03:36:38:46"
        assert d.frames == 779926
        assert f.make_timecode() == "03:36:38:46"
        assert f.frames == 779926
        tc = pytimecode.PyTimeCode('59.94', '03:36:09:23', drop_frame=True)
        tc2 = pytimecode.PyTimeCode('59.94', '00:00:29:23', drop_frame=True)
        d = tc + tc2
        f = tc + 1763
        assert d.make_timecode() == "03:36:38:50"
        assert d.frames == 779150
        assert f.make_timecode() == "03:36:38:50"
        assert f.frames == 779150 
        tc = pytimecode.PyTimeCode('23.98', '03:36:09:23')
        tc2 = pytimecode.PyTimeCode('23.98', '00:00:29:23')
        d = tc + tc2
        f = tc + 719
        assert d.make_timecode() == "03:36:39:22"
        assert d.frames == 311998
        assert f.make_timecode() == "03:36:39:22"
        assert f.frames == 311998 
        tc = pytimecode.PyTimeCode('24', '03:36:09:23')
        tc = pytimecode.PyTimeCode('23.98', '03:36:09:23')
        tc2 = pytimecode.PyTimeCode('23.98', '00:00:29:23')
        d = tc + tc2
        f = tc + 719
        assert d.make_timecode() == "03:36:39:22"
        assert d.frames == 311998
        assert f.make_timecode() == "03:36:39:22"
        assert f.frames == 311998
        tc = pytimecode.PyTimeCode('ms', '03:36:09:230')
        tc2 = pytimecode.PyTimeCode('ms', '01:06:09:230')
        d = tc + tc2
        f = tc + 719
        print tc.frames, tc2.frames, d.frames
        assert d.make_timecode() == "04:42:18:460"
        assert d.frames == 16938460
        assert f.make_timecode() == "03:36:09:949"
        assert f.frames == 12969949
        tc = pytimecode.PyTimeCode('24', start_timecode=None, frames=12000)
        tc2 = pytimecode.PyTimeCode('24', start_timecode=None, frames=485)
        d = tc + tc2
        f = tc + 719
        assert d.make_timecode() == "00:08:40:05"
        assert d.frames == 12485
        assert f.make_timecode() == "00:08:49:23"
        assert f.frames == 12719
        
    def test_op_overloads_mult(self):
        tc = pytimecode.PyTimeCode('29.97', '00:00:09:23', drop_frame=True)
        tc2 = pytimecode.PyTimeCode('29.97', '00:00:29:23', drop_frame=True)
        d = tc * tc2
        f = tc * 4
        print tc.frames, tc2.frames
        assert d.make_timecode() == "02:25:30:13"
        assert d.frames == 261651
        assert f.make_timecode() == "00:00:39:02"
        assert f.frames == 1172
        tc = pytimecode.PyTimeCode('29.97', '00:00:09:23')
        tc2 = pytimecode.PyTimeCode('29.97', '00:00:29:23')
        d = tc * tc2
        f = tc * 4
        assert d.make_timecode() == "02:25:21:19"
        assert d.frames == 261649
        assert f.make_timecode() == "00:00:39:02"
        assert f.frames == 1172
        tc = pytimecode.PyTimeCode('30', '03:36:09:23')
        tc2 = pytimecode.PyTimeCode('30', '00:00:29:23')
        d = tc * tc2
        f = tc * 893
        assert d.make_timecode() == "01:13:21:19"
        assert d.frames == 132049
        assert f.make_timecode() == "01:13:21:19"
        assert f.frames == 132049
        tc = pytimecode.PyTimeCode('25', '03:36:09:23')
        tc2 = pytimecode.PyTimeCode('25', '00:00:29:23')
        d = tc * tc2
        f = tc * 748
        assert d.make_timecode() == "06:51:40:04"
        assert d.frames == 617504
        assert f.make_timecode() == "06:51:40:04"
        assert f.frames == 617504 
        tc = pytimecode.PyTimeCode('59.94', '03:36:09:23')
        tc2 = pytimecode.PyTimeCode('59.94', '00:00:29:23')
        d = tc * tc2
        f = tc * 1763
        assert d.make_timecode() == "15:23:42:49"
        assert d.frames == 3325369
        assert f.make_timecode() == "15:23:42:49"
        assert f.frames == 3325369 
        tc = pytimecode.PyTimeCode('60', '03:36:09:23')
        tc2 = pytimecode.PyTimeCode('60', '00:00:29:23')
        d = tc * tc2
        f = tc * 1763
        assert d.make_timecode() == "15:23:42:49"
        assert d.frames == 3325369
        assert f.make_timecode() == "15:23:42:49"
        assert f.frames == 3325369
        tc = pytimecode.PyTimeCode('59.94', '03:36:09:23', drop_frame=True)
        tc2 = pytimecode.PyTimeCode('59.94', '00:00:29:23', drop_frame=True)
        d = tc * tc2
        f = tc * 1763
        assert d.make_timecode() == "15:22:25:57"
        assert d.frames == 3317437
        assert f.make_timecode() == "15:22:25:57"
        assert f.frames == 3317437 
        tc = pytimecode.PyTimeCode('23.98', '03:36:09:23')
        tc2 = pytimecode.PyTimeCode('23.98', '00:00:29:23')
        d = tc * tc2
        f = tc * 719
        assert d.make_timecode() == "22:23:20:01"
        assert d.frames == 1934401
        assert f.make_timecode() == "22:23:20:01"
        assert f.frames == 1934401 
        tc = pytimecode.PyTimeCode('24', '03:36:09:23')
        tc = pytimecode.PyTimeCode('23.98', '03:36:09:23')
        tc2 = pytimecode.PyTimeCode('23.98', '00:00:29:23')
        d = tc * tc2
        f = tc * 719
        assert d.make_timecode() == "22:23:20:01"
        assert d.frames == 1934401
        assert f.make_timecode() == "22:23:20:01"
        assert f.frames == 1934401
        tc = pytimecode.PyTimeCode('ms', '03:36:09:230')
        tc2 = pytimecode.PyTimeCode('ms', '01:06:09:230')
        d = tc * tc2
        f = tc * 719
        print tc.frames, tc2.frames, d.frames
        assert d.make_timecode() == "12:39:52:900"
        assert d.frames == 45592900
        assert f.make_timecode() == "22:14:36:370"
        assert f.frames == 80076370
        tc = pytimecode.PyTimeCode('24', start_timecode=None, frames=12000)
        tc2 = pytimecode.PyTimeCode('24', start_timecode=None, frames=485)
        d = tc * tc2
        f = tc * 719
        assert d.make_timecode() == "19:21:40:00"
        assert d.frames == 1672800
        assert f.make_timecode() == "03:51:40:00"
        assert f.frames == 333600
        
    def test_24_hour_limit(self):
        tc = pytimecode.PyTimeCode('24', '00:00:00:21')
        tc2 = pytimecode.PyTimeCode('24', '23:59:59:23')
        assert (tc + tc2).make_timecode() == '00:00:00:20'
        assert (tc2 + 159840001).make_timecode() == '02:00:00:00'
        tc = pytimecode.PyTimeCode('29.97', '00:00:00:21')
        tc2 = pytimecode.PyTimeCode('29.97', '23:59:59:29')
        print (tc + tc2).frames
        assert (tc + tc2).make_timecode() == '00:00:00:20'
        assert (tc2 + 18360001).make_timecode() == '02:00:00:00'
        tc = pytimecode.PyTimeCode('29.97', '00:00:00:01', drop_frame=True)
        tc2 = pytimecode.PyTimeCode('29.97', '23:59:59:29', drop_frame=True)
        tc3 = (tc2+21)
        print 'yp1', tc.frames, tc2.frames, tc3.frames, tc.make_timecode()
        assert  tc3.make_timecode() == '00:00:00:20'
        tc = pytimecode.PyTimeCode('29.97', '00:00:00:21', drop_frame=True)
        tc2 = pytimecode.PyTimeCode('29.97', '23:59:59:29', drop_frame=True)
        tc3 = (tc+tc2)
        print 'yp2', tc.frames, tc2.frames, tc3.frames, tc.make_timecode()
        assert  tc3.make_timecode() == '00:00:00:20'
        tc = pytimecode.PyTimeCode('29.97', '04:20:13:21', drop_frame=True)
        tc2 = pytimecode.PyTimeCode('29.97', '23:59:59:29', drop_frame=True)
        tc3 = (tc+tc2)
        print 'yp2', tc.frames, tc2.frames, tc3.frames, tc.make_timecode()
        assert  tc3.make_timecode() == '04:20:13:20'
        tc = pytimecode.PyTimeCode('59.94', '04:20:13:21', drop_frame=True)
        tc2 = pytimecode.PyTimeCode('59.94', '23:59:59:59', drop_frame=True)
        tc3 = (tc+tc2)
        print 'yp2', tc.frames, tc2.frames, tc3.frames, tc.make_timecode()
        assert  tc3.make_timecode() == '04:20:13:20'
        
    def test_exceptions(self):
        e = None
        try:
            tc = pytimecode.PyTimeCode('24', '01:20:30:303')
        except pytimecode.PyTimeCodeError as e:
            pass
        print type(e), e
        assert e.__str__() == 'Timecode string parsing error. 01:20:30:303'
        try:
            tc = pytimecode.PyTimeCode('23.98', '01:20:30:303')
        except pytimecode.PyTimeCodeError as e:
            pass
        print type(e), e
        assert e.__str__() == 'Timecode string parsing error. 01:20:30:303'
        try:
            tc = pytimecode.PyTimeCode('29.97', '01:20:30:303')
        except pytimecode.PyTimeCodeError as e:
            pass
        print type(e), e
        assert e.__str__() == 'Timecode string parsing error. 01:20:30:303'
        try:
            tc = pytimecode.PyTimeCode('30', '01:20:30:303')
        except pytimecode.PyTimeCodeError as e:
            pass
        print type(e), e
        assert e.__str__() == 'Timecode string parsing error. 01:20:30:303'
        try:
            tc = pytimecode.PyTimeCode('60', '01:20:30:303')
        except pytimecode.PyTimeCodeError as e:
            pass
        print type(e), e
        assert e.__str__() == 'Timecode string parsing error. 01:20:30:303'
        try:
            tc = pytimecode.PyTimeCode('59.94', '01:20:30:303')
        except pytimecode.PyTimeCodeError as e:
            pass
        print type(e), e
        assert e.__str__() == 'Timecode string parsing error. 01:20:30:303'
        try:
            tc = pytimecode.PyTimeCode('ms', '01:20:30:3039')
        except pytimecode.PyTimeCodeError as e:
            pass
        print type(e), e
        assert e.__str__() == 'Timecode string parsing error. 01:20:30:3039'
        try:
            tc = pytimecode.PyTimeCode('60', '01:20:30:30', drop_frame=True)
        except pytimecode.PyTimeCodeError as e:
            pass
        print type(e), e
        assert e.__str__() == 'Drop frame with 60fps not supported, only 29.97 & 59.94.'
        tc = pytimecode.PyTimeCode('29.97', '00:00:09:23', drop_frame=True)
        tc2 = 'bum'
        try:
            d = tc * tc2
        except pytimecode.PyTimeCodeError as e:
            pass
        assert e.__str__() == "Type <type 'str'> not supported for arithmetic."
        tc = pytimecode.PyTimeCode('30', '00:00:09:23')
        tc2 = 'bum'
        try:
            d = tc + tc2
        except pytimecode.PyTimeCodeError as e:
            pass
        assert e.__str__() == "Type <type 'str'> not supported for arithmetic."
        tc = pytimecode.PyTimeCode('24', '00:00:09:23')
        tc2 = 'bum'
        try:
            d = tc - tc2
        except pytimecode.PyTimeCodeError as e:
            pass
        assert e.__str__() == "Type <type 'str'> not supported for arithmetic."
        tc = pytimecode.PyTimeCode('ms', '00:00:09:237')
        tc2 = 'bum'
        try:
            d = tc / tc2
        except pytimecode.PyTimeCodeError as e:
            pass
        assert e.__str__() == "Type <type 'str'> not supported for arithmetic."