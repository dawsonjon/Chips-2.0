/* time.h Jonathan P Dawson 2015-10-21 */

#ifndef __time_h__
#define __time_h__

#include <stdlib.h>


///time.h
///------
///
///Macros
///******
///
///`time.h` defines the following macros:
///
///+ CLOCKS_PER_SEC
///
///`CLOCKS_PER_SEC` is the number per second of the value returned by the clock
///function. In chips, this value is a parameter
///passed to a component when it is instantiated.
///

#define NULL (int*)0xffffffffu

///Types
///*****
///
///`time.h` defines the following types:
///
///+ clock_t
///+ time_t
///+ tm
///
///`clock_t` is a type representing processor time in elapsed clock ticks.
///

#define clock_t unsigned long

///
///`time_t` is a type representing system time, as an integer number of seconds.
///

#define time_t unsigned long

//////`tm` is a struct which holds the components of a calendar time, called the
///broken-down time.  The structure contains the following members:
///
///.. code-clocks:: c
///
///         int tm_sec;   /*  seconds after the minute --- [0, 60] */
///         int tm_min;   /*  minutes after the hour --- [0, 59] */
///         int tm_hour;  /*  hours since midnight --- [0, 23] */
///         int tm_mday;  /*  day of the month --- [1, 31] */
///         int tm_mon;   /*  months since January --- [0, 11] */
///         int tm_year;  /*  years since 1900 */
///         int tm_wday;  /*  days since Sunday --- [0, 6] */
///         int tm_yday;  /*  days since January 1 --- [0, 365] */
///         int tm_isdst; /*  Daylight Saving Time flag */
///
///The value of tm_isdst is positive if Daylight Saving Time is in
///effect, zero if Daylight Saving Time is not in effect, and negative if
///the information is not available.
///

typedef struct {
	int tm_sec;   /*  seconds after the minute --- [0, 60] */
	int tm_min;   /*  minutes after the hour --- [0, 59] */
	int tm_hour;  /*  hours since midnight --- [0, 23] */
	int tm_mday;  /*  day of the month --- [1, 31] */
	int tm_mon;   /*  months since January --- [0, 11] */
	int tm_year;  /*  years since 1900 */
	int tm_wday;  /*  days since Sunday --- [0, 6] */
	int tm_yday;  /*  days since January 1 --- [0, 365] */
	int tm_isdst; /*  Daylight Saving Time flag */
} tm;

/* forward declarations */
tm *localtime(time_t *timer);
time_t mktime(tm *timeptr);

///Globals
///*****
///
///`time.h` defines the following variable:
///
///+ tz_offset *(Not part of C standard)
///
///`tz_offset` defines the offset in seconds from UTC.
///
int tz_offset = 0;

int _is_dst(tm t){

  time_t end_of_dst;
  tm last_sunday_in_october;
  last_sunday_in_october.tm_year = t.tm_year;
  last_sunday_in_october.tm_mon = 9;
  last_sunday_in_october.tm_mday = 31;
  last_sunday_in_october.tm_hour = 1;
  last_sunday_in_october.tm_min = 0;
  last_sunday_in_october.tm_sec = 0;
  last_sunday_in_october.tm_isdst = 0;
  mktime(&last_sunday_in_october);
  last_sunday_in_october.tm_mday -= last_sunday_in_october.tm_wday;
  end_of_dst = mktime(&last_sunday_in_october);

  time_t start_of_dst;
  tm last_sunday_in_march;
  last_sunday_in_march.tm_year = t.tm_year;
  last_sunday_in_march.tm_mon = 9;
  last_sunday_in_march.tm_mday = 31;
  last_sunday_in_march.tm_hour = 1;
  last_sunday_in_march.tm_min = 0;
  last_sunday_in_march.tm_sec = 0;
  last_sunday_in_october.tm_isdst = 0;
  mktime(&last_sunday_in_march);
  last_sunday_in_march.tm_mday -= last_sunday_in_march.tm_wday;
  start_of_dst = mktime(&last_sunday_in_march);

  time_t t0;
  t0 = mktime(&t);

  return start_of_dst < t0 && t0 < end_of_dst;

}

///
///The clock function
///******************
///
///Synopsis:
///
///    ..code-block:: c
///
///         #include <time.h>
///         clock_t clock(void);
///
///Description:
///
///   The clock function determines the processor time used.  
///
///Returns:
///
///   The clock function returns the processor time used by the program since
///   configuration/device reset in clock cycles.
///   To determine the time in seconds, the value returned by the clock
///   function should be divided by the value of the macro CLOCKS_PER_SEC.
///

clock_t clock(){

    unsigned long low = timer_low();
    unsigned long high = timer_high();
    unsigned long t;

    /*check for low half of timer wrapping round*/
    if(timer_low() < low) high = timer_high();

    /*calculate uptime in seconds*/
    t = high << 32 | low;
    return t;

}

///
///The difftime function
///*********************
///
///Synopsis:
///
///    ..code-block:: c
///
///         #include <time.h>
///         double difftime(time_t time1, time_t time0);
///
///Description:
///
///   The difftime function computes the difference between two calendar
///   times: time1 - time0.
///
///Returns:
///
///   The difftime function returns the difference expressed in seconds
///   as a double.
///

double difftime(time_t time1, time_t time0){
	return time1 - time0;
}

///
///The mktime function
///*******************
///
///Synopsis:
///
///    ..code-block:: c
///
///         #include <time.h>
///         time_t mktime(struct tm *timeptr);
///
///Description:
///
///   The mktime function converts the broken-down time, expressed as
///   local time, in the structure pointed to by timeptr into a calendar
///   time value with the same encoding as that of the values returned by
///   the time function.  The original values of the tm_wday and tm_yday
///   components of the structure are ignored, and the original values of
///   the other components are not restricted to the ranges indicated
///   above. On successful completion, the values of the tm_wday and
///   tm_yday components of the structure are set appropriately, and the
///   other components are set to represent the specified calendar time, but
///   with their values forced to the ranges indicated above; the final
///   value of tm_mday is not set until tm_mon and tm_year are determined.
///
///Returns:
///
///   The mktime function returns the specified calendar time encoded as
///   a value of type time_t.  If the calendar time cannot be represented,
///   the function returns the value (time_t)-1.
///

unsigned _is_leap_year(unsigned year){
    return year%4==0 && (year%100!=0 || year%400==0);
}

unsigned _days_in_year(unsigned year){
    return is_leap_year(year) ? 366 : 365;
}

unsigned _days_in_month(unsigned year, unsigned month){
    if (month == 3 || month == 8 || month == 5 || month == 10) return 30;
    if (month == 1) return is_leap_year(year) ? 29 : 28;
    return 31;
}

time_t mktime(tm *timeptr){

    time_t time;
    unsigned year, month, temp;

    time = 0;
    year = 1970;
    temp = timeptr->tm_year;
    while(1){
        if(year == temp+1900) break;
        time += _days_in_year(year) * 86400;
	year++;
    }
    month = 0;
    while(1){
        if(month == timeptr->tm_mon) break;
        time += _days_in_month(year, month) * 86400;
	month++;
    }
    time += (timeptr->tm_mday - 1) * 86400;
    time += timeptr->tm_hour * 3600;
    time += timeptr->tm_min * 60;
    time += timeptr->tm_sec;

    if (timeptr -> tm_isdst > 0){
        time += 3600;
    } else if (timeptr->tm_isdst < 0){
        time += _is_dst(*timeptr) ? 3600 : 0;
    }

    time -= tz_offset;
    *timeptr = *localtime(&time);

    return time;

}

///
///The time function
///*****************
///
///Synopsis:
///
///    ..code-block:: c
///
///         #include <time.h>
///         time_t time(time_t *timer);
///
///Description:
///
///   The time function determines the current calendar time.  The
///   encoding of the value is unspecified.
///
///Returns:
///
///   The time function returns the current calendar time.  
///   If timer is not a null pointer, the return value is also assigned to the
///   object it points to.
///

time_t set_time_ = 0;
time_t time(time_t *timer){

    unsigned long t;

    /*calculate uptime in seconds*/
    t = clock()/CLOCKS_PER_SEC;

    /*convert uptime to calender time*/
    t += set_time_;

    if (timer != (long*)NULL) {
	*timer = t;
    }

    return t;

}

///
///The set_time function (Not part of C standard)
///**********************************************
///
///Synopsis:
///
///    ..code-block:: c
///
///         #include <time.h>
///         void set_time(time_t t);
///
///Description:
///
///   Set the time of the system clock by supplying the current time.
///   The current time is expressed as seconds since the UNIX epoch.
///
///Returns:
///
///   None
///

void set_time(time_t t) {
   set_time_ = t - time((long*)NULL);
}

///
///The asctime function
///********************
///
///Synopsis:
///
///    ..code-block:: c
///
///         #include <time.h>
///         char *asctime(const struct tm *timeptr);
///
///Description:
///
///   The asctime function converts the broken-down time in the structure
///   pointed to by timeptr into a string in the form
///
///         Sun Sep 16 01:03:52 1973
///
///Returns:
///
///   The asctime function returns a pointer to the string.  
///

char result_[26];
char *asctime(tm *timeptr)
{
         const char wday_name[] = "SunMonTueWedThuFriSat";
         const char mon_name[] = "JanFebMarAprMayJunJulAugSepOctNovDec" ;
	 int i;
	 div_t ret;

	 for (i=0; i<3; i++){
	   result_[i] = wday_name[timeptr->tm_wday*3 + i];
         }
	 result_[3] = ' ';

	 for (i=0; i<3; i++){
	   result_[i+4] = mon_name[timeptr->tm_mon*3 + i];
         }
	 result_[7] = ' ';

	 ret = div(timeptr->tm_mday, 10);
	 result_[8] = ret.quot + '0';
	 result_[9] = ret.rem + '0';
	 result_[10] = ' ';

	 ret = div(timeptr->tm_hour, 10);
	 result_[11] = ret.quot + '0';
	 result_[12] = ret.rem + '0';
	 result_[13] = ':';
	 ret = div(timeptr->tm_min, 10);
	 result_[14] = ret.quot + '0';
	 result_[15] = ret.rem + '0';
	 result_[16] = ':';
	 ret = div(timeptr->tm_sec, 10);
	 result_[17] = ret.quot + '0';
	 result_[18] = ret.rem + '0';
	 result_[19] = ' ';

	 ret = div(timeptr->tm_year + 1900, 1000);
	 result_[20] = ret.quot + '0';
         ret = div(ret.rem, 100); 
	 result_[21] = ret.quot + '0';
         ret = div(ret.rem, 10); 
	 result_[22] = ret.quot + '0';
	 result_[23] = ret.rem + '0';
	 result_[24] = '\n';
	 result_[25] = 0;

         return result_;
}

///
///4.12.3.2 The ctime function
///
///Synopsis:
///
///    ..code-block:: c
///
///         #include <time.h>
///         char *ctime(const time_t *timer);
///
///Description:
///
///   The ctime function converts the calendar time pointed to by timer to local time in the form of a string.  It is equivalent to 
///
///         asctime(localtime(timer))
///
///Returns:
///
///   The ctime function returns the pointer returned by the asctime
///function with that broken-down time as argument.
///


///
///The gmtime function
///*******************
///
///Synopsis:
///
///    ..code-block:: c
///
///         #include <time.h>
///         struct tm *gmtime(const time_t *timer);
///
///Description:
///
///   The gmtime function converts the calendar time pointed to by timer
///   into a broken-down time, expressed as Coordinated Universal Time
///   (UTC).
///
///Returns:
///
///   The gmtime function returns a pointer to that object, or a null
///   pointer if UTC is not available.
///


tm time_;

tm *gmtime(time_t *timer){

    unsigned temp, days;
    time_t time = *timer;
    div_t res;

    time_.tm_year = 1970;
    time_.tm_wday = 4;
    while(1){
        temp = _days_in_year(time_.tm_year) * 86400;
        if(temp > time) break;
        time_.tm_year++;
        time_.tm_wday+=temp;
        time-=temp;
    }

    time_.tm_mon = 0;
    time_.tm_yday = 0;
    while(1){
        days = _days_in_month(time_.tm_year, time_.tm_mon);
        temp = days * 86400;
        if(temp > time) break;
        time_.tm_mon++;
        time_.tm_wday+=days;
        time_.tm_yday+=days;
        time -= temp;
    }
    time_.tm_year-=1900;

    res = div(time, 86400);
    time_.tm_mday = res.quot + 1;
    time_.tm_wday += res.quot;
    time_.tm_wday %= 7;
    time_.tm_yday += res.quot;
    time = res.rem;

    res = div(time, 3600);
    time_.tm_hour = res.quot;
    time = res.rem;

    res = div(time, 60);
    time_.tm_min = res.quot;
    time = res.rem;

    time_.tm_sec = time;

    return &time_;

}

///The localtime function
///**********************
///
///Synopsis:
///
///    ..code-block:: c
///
///         #include <time.h>
///         struct tm *localtime(const time_t *timer);
///
///Description:
///
///   The localtime function converts the calendar time pointed to by
///   timer into a broken-down time, expressed as local time.
///
///Returns:
///
///   The localtime function returns a pointer to that object.  
///

tm *localtime(time_t *timer){
 
    time_t local_time = *timer + tz_offset;
    return gmtime(&local_time);

}

///
///4.12.3.5 The strftime function
///
///Synopsis:
///
///    ..code-block:: c
///
///         #include <time.h>
///         size_t strftime(char *s, size_t maxsize,
///                  const char *format, const struct tm *timeptr);
///
///Description:
///
///   The strftime function places characters into the array pointed to
///by s as controlled by the string pointed to by format.  The format
///shall be a multibyte character sequence, beginning and ending in its
///initial shift state.  The format string consists of zero or more
///conversion specifications and ordinary multibyte characters.  A
///conversion specification consists of a % character followed by a
///character that determines the conversion specification's behavior.
///All ordinary multibyte characters (including the terminating null
///character) are copied unchanged into the array.  If copying takes
///place between objects that overlap, the behavior is undefined.  No
///more than maxsize characters are placed into the array.  Each
///conversion specification is replaced by appropriate characters as
///described in the following list.  The appropriate characters are
///determined by the program's locale and by the values contained in the
///structure pointed to by timeptr.
///
///"%a" is replaced by the locale's abbreviated weekday name.  
///"%A" is replaced by the locale's full weekday name.  
///"%b" is replaced by the locale's abbreviated month name.  
///"%B" is replaced by the locale's full month name.
///"%c" is replaced by the locale's appropriate date and time representation.
///"%d" is replaced by the day of the month as a decimal number (01-31).
///"%H" is replaced by the hour (24-hour clock) as a decimal number (00-23).
///"%I" is replaced by the hour (12-hour clock) as a decimal number (01-12). 
///"%j" is replaced by the day of the year as a decimal number (001-366 ).  
///"%m" is replaced by the month as a decimal number (01-12).  
///"%M" is replaced by the minute as a decimal number (00-59).  
///"%p" is replaced by the locale's equivalent of either AM or PM.  
///"%S" is replaced by the second as a decimal number (00-60).  
///"%U" is replaced by the week number of the year (ithe first Sunday as the 
///     first day of week 1) as a decimal number (00-53).  
///"%w" is replaced by the weekday as a decimal number (0-6), where Sunday is
///     0.
///"%W" is replaced by the week number of the year (the first Monday as the 
///     first day of week 1) as a decimal number (00-53). 
///"%x" is replaced by the locale's appropriate date representation.  
///"%X" is replaced by the locale's appropriate time representation.  
///"%y" is replaced by the year without century as a decimal number (00-99). 
///"%Y" is replaced by the year with century as a decimal number.  
///"%Z" is replaced by the time zone name, or by no characters if no time 
///     zone is determinable.  
///"%%" is replaced by %.
///
///   If a conversion specification is not one of the above, the behavior
///is undefined.
///
///Returns:
///
///   If the total number of resulting characters including the
///terminating null character is not more than maxsize , the strftime
///function returns the number of characters placed into the array
///pointed to by s not including the terminating null character.
///Otherwise, zero is returned and the contents of the array are
///indeterminate.

#endif
