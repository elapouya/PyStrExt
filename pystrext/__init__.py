# -*- coding: utf-8 -*-
"""
| Python String Extension
| 
| With pystrext module, you will be able to manipulate strings.
| 
| Created on 2 Feb. 2010
| @author: elapouya
"""

import cStringIO, gzip
import re
import random
import unicodedata

def compress(s):
    """ Compress a string with gzip
    
    It could be useful to compress some data without creating a file, this function do that.
    
    Args:
        s (str) : The strings to compress
        
    Returns:
        str : The compressed string
        
    Examples:
        >>> s = "monty python" * 80
        >>> len(s)
        960
        >>> c = compress(s)
        >>> len(c)
        41
        >>> u = uncompress(c)
        >>> len(u)
        960
        >>> s == u
        True
    """
    zbuf = cStringIO.StringIO()
    zfile = gzip.GzipFile(mode='wb', compresslevel=6, fileobj=zbuf)
    zfile.write(s)
    zfile.close()
    output=zbuf.getvalue()
    zbuf.close()
    return output

def uncompress(s):
    """ Uncompress a gzipped string
    
    You can uncompress both strings compressed with pystrext.compress() but also
    a .gz file that has been read with open() and read().
    
    Args:
        s (str) : The gzipped string to uncompress
        
    Returns:
        str : The uncompressed string
        
    Examples:
        see pystrext.compress()
    """
    zbuf = cStringIO.StringIO(s)
    zfile = gzip.GzipFile(mode='rb', compresslevel=6, fileobj=zbuf)
    output=zfile.read(s)
    zfile.close()
    zbuf.close()
    return output

def get_col(str,**kwargs):
    """ Extract a column from a string
    
    Some strings have got many columns seperated with a separator.
    Some strings may also have some sub-columns seperated with another separator.
    get_col() can extract **one** column/sub-column at any depth level.
    You have to specify one separator and one column number for each depth level you want to select.
    
    | Arguments name is important, it must be : col<n> and sep<n>. 
    | Arguments are sorted so sep1/col1 is searched before sep2/col2
    | The separator can be a regular expression (by default will be '\W+')
    
    Args:
        str (str) : The listing row to parse
        sep1 (str) : sperator 1 
        col1 (str) : column number 1
        sepn (str) : sperator n
        coln (str) : column number n
        
    Returns:
        str : The column/sub-column requested
        
    Examples:
        >>> get_col("  4   0  95   0   0   0|   0    72k| 352k   40k|   0     0 | 435   138 ",col1=2,sep1='\|',col2=-1,sep2='\W+')
        '40k'
        >>> get_col("/a/b/c/basename.date.jpg",col1=-1,sep1='/',col2=1,sep2='\.')
        'date'
    """
    try:
        for k,v in sorted(kwargs.items()):
            if k[:3] == 'col':
                sep = kwargs.get('sep%s' % k[3:],'\W+')
                str = re.split(sep, str, flags=re.IGNORECASE)[v]
    except IndexError:
        str = ''
        
    return str

def extract(str,pattern):
    """ Search a pattern and return the first group of the first match.
    
    The pattern must include a group selection, ie : it must include parentheses. 
    Only the part inside the parentheses will be returned. 
        
    Args:
        str (str) : The string to search a pattern
        pattern (RegexObject or str) : A regular expression object or a string for the pattern to search 
        
    Returns:
        str : The extracted strings that matches the pattern or **None** if no match.
        
    Examples:
        >>> extract('the full monty python','(\w+) python')
        'monty'
        >>> r=re.compile('>([^<]*)<')
        >>> extract('this is text form : >the answer<',r)
        'the answer'
    """
    if isinstance(pattern, basestring):
        pattern = re.compile(pattern)
    m = pattern.search(str)
    if m:
        return m.group(1)
    return None

def extracts(str,pattern,default):
    """ Search a pattern and return groups of the first match.
    
    The pattern must include a group selections, ie : it must include parentheses. 
    Only the part inside the parentheses will be returned. 
        
    Args:
        str (str) : The string to search a pattern
        pattern (RegexObject or str) : A regular expression object or a string for the pattern to search 
        
    Returns:
        list : The extracted string for each group that matches the pattern or *default* argument if no match.
        
    Examples:
        >>> h,m,s = extracts('elapse time : 5h 7m 36s','(\d+)h (\d+)m (\d+)s',['0']*3)
        >>> h,m,s
        ('5', '7', '36')
    """
    if isinstance(pattern, basestring):
        pattern = re.compile(pattern)
    m = pattern.search(str)
    if m:
        return m.groups()
    return default

def plural(str1,str2,n):
    """ Select one string depending on a numeric value
    
    Args:
        str1 (str) : The string to return if *n* <= 1
        str2 (str) : The string to return if *n* > 1
        n (int) : the numeric value to test 
        
    Returns:
        str : str1 if *n* is 1 or less, str2 otherwise.
        
    Examples:
        >>> n=1
        >>> print "found %d %s" % (n,plural("item","items",n))
        found 1 item
        >>> n=4
        >>> print "found %d %s" % (n,plural("item","items",n))
        found 4 items
    
    """
    if n>1:
        return str2
    return str1

def if_val(val,str1,str2):
    """ Select one string depending on a value
    
    This function return str1 if *val* True, str2 if False.
    
    | str1 or str2 can be a string that may include '%(val)s' : it will replaced by *val* value.
    | str1 or str2 can be a callable : it will be called with *val* as argument
    
    Args:
        val (any type) : value to test
        str1 (str or callable) : The string to return if *val*
        str2 (str or callable) : The string to return if not *val*
        
    Returns:
        str : str1 or str2 or str1(val) or str2(val)
        
    Examples:
        >>> print if_val(3,"Item(s) found : %(val)s","No item found")
        Item(s) found : 3
        >>> print if_val(0,"Item(s) found : %(val)s","No item found")
        No item found    
    """
    if val:
        if callable(str1):
            return str1(val)
        else:
            return str1 % {'val' : val}
    else:
        if callable(str2):
            return str2(val)
        else:
            return str2 % {'val' : val}

def no_one_many(n,str0,str1,str2):
    """ Select one string depending on a n equal to 0,1 or many
    
    This function will return : 
    
    * str0 if n <= 0
    * str1 if n == 1
    * str2 if n >= 2
    
    | str0, str1 or str2 can be a string that may include '%(n)s' : it will replaced by *n* value.
    | str0, str1 or str2 can be a callable : it will be called with *n* as argument
    
    Args:
        n (int) : value to test
        str0 (str or callable) : The string to return if n <= 0
        str1 (str or callable) : The string to return if n == 1
        str2 (str or callable) : The string to return if n >= 2
        
    Returns:
        str : str0 or str1 or str2
        
    Examples:
        >>> print no_one_many(0,"No item","One item","%(n)s items")
        No item
        >>> print no_one_many(1,"No item","One item","%(n)s items")
        One item
        >>> print no_one_many(36,"No item","One item","%(n)s items")
        36 items
    """
    if n <= 0:
        if callable(str0):
            return str0(n)
        else:
            return str0 % {'n' : n}
    elif n == 1:
        if callable(str1):
            return str1(n)
        else:
            return str1 % {'n' : n}
    else:
        if callable(str2):
            return str2(n)
        else:
            return str2 % {'n' : n}

def truncate(str,maxsize,max_end_str='...',end_str_inside=True):
    """ Truncate a string to a specified length and add a suffix (if truncated only)
        
    Args:
        str (str) : The string to truncate
        maxsize (int) : string maximum size before truncating and adding a suffix
        max_end_str (str) : suffix to add when string has been truncated ('...' by default)
        end_str_inside (bool) : Tells whether the suffix 
            is inside the truncated string so the final string length is no more than maxsize or 
            is outside the truncated string so the final string length is no more than maxsize + suffix's length
        
    Returns:
        str : The truncated string
        
    Examples:
        >>> truncate('hello world !',80)
        >>> 'hello world !'        
        >>> truncate('hello world !',5)
        >>> 'he...'        
        >>> truncate('hello world !',5,end_str_inside=False)
        >>> 'hello...'        
        >>> truncate('hello world !',5,' <a href="?more">more...</a>',False)
        >>> 'hello <a href="?more">more...</a>'
        >>> truncate('hello world !',80,' <a href="?more">more...</a>',False)
        >>> 'hello world !'
    
    """
    if len(str) > maxsize:
        if end_str_inside:
            return str[:max(0,maxsize-len(max_end_str))] + max_end_str
        else:
            return str[:maxsize] + max_end_str
    return str

def MB_GB(str,MB="MB",GB="GB"):
    """ Transforms a string representing a memory MegaByte value into GigaBytes if value > 1024
    
    One can specify his own unit
    
    Args:
        str (str) : string representing a value to be devided by 1024 if > 1024
        MB (str) : string for the lowest unit
        GB (str) : string for the highest unit
        
    Returns:
        str : The converted string
        
    Examples:
        >>> MB_GB('512')
        >>> '512 MB'        
        >>> MB_GB('2048')
        >>> '2 GB'        
        >>> MB_GB('2048','MBytes','GBytes')
        >>> '2 GBytes'    
    """
    if str:
        size = int(str)
        if size >= 1024:
            return "%d %s" % (int(size / 1024),GB)
        else:
            return "%d %s" % (size,MB)
    return str

def MHz_GHz(str):
    """ Transforms a string representing a frequency from Mhz to Ghz if value > 1024
        
    Args:
        str (str) : string representing the frequency (Mhz)
        
    Returns:
        str : The converted string
        
    Examples:
        >>> MHz_GHz('377')
        >>> '377 MHz'
        >>> MHz_GHz('2048')
        >>> '2.048 GHz'
    """
    if str:
        size = float(str)
        if size >= 1000:
            return "%.3f GHz" % (size / 1000)
        else:
            return "%s MHz" % str
    return str

def version_lt(v1,v2):
    """ Compare 2 strings representing dotted version number
    
    The goal is to test whether a version string is older than another one. 
    A version string looks like this : "1.45.2.1"
    It can have as many dot you want, but the strings between dots cannot be more than 10 chars long.
    Strings comparaison are done "dot by dot" from left to right and stops as soon as the comparaison is not equal.

    Args:
        v1 (str) : version1 string
        v2 (str) : version2 string
        
    Returns:
        bool : True is v1 older than v2
        
    Examples:
        >>> version_lt('1.2.0','1.12.0')
        >>> True
        >>> version_lt('1.2.0','1.1.9')
        >>> False
        >>> version_lt('1.43c','1.43f')
        >>> True
        >>> version_lt('1.2.5.6.7.8','1.2.5.6.7.9')
        >>> True
    """
    l1 = v1.split('.')
    l2 = v2.split('.')
    for i in range (max(len(l1),len(l2))):
        try:
            sv1 = l1[i]
        except IndexError:
            sv1 = '0'
        sv1 = sv1.rjust(10)
        try:
            sv2 = l2[i]
        except IndexError:
            sv2 = '0'
        sv2 = sv2.rjust(10)
        if sv1 < sv2:
            return True
        elif sv1 > sv2:
            return False
    return False

def vjust(str,level=5,delim='.',bitsize=6,fillchar=' '):
    """ Justify a string representing dotted version number
    
    The goal is to justify/format a version string in a way it can be filtered by a SQL engine : 
    Each substrings will get a fixed length so SQL string comparaison can be used.
    
    Args:
        str (str) : dotted version number
        level (int) : number max of version substrings
        delim (str) : separator (a dot by default)
        bitsize (int) : substrings max length
        fillchar (str) : the char used to fill the blanks
        
    Returns:
        str : the justified string
        
    Examples:
        >>> vjust('1.2')
        >>> '     1.     2.      .      .      .      '
        >>> vjust('1.12')
        >>> '     1.    12.      .      .      .      '
        >>> vjust('1.12',fillchar='0')
        >>> '000001.000012.000000.000000.000000.000000'
    
    """
    nb = str.count(delim)
    # on force le nombre de points à level
    if nb < level:
        str += (level-nb) * delim
    return delim.join([ v.rjust(bitsize,fillchar) for v in str.split(delim)[:level+1] ])

def file_unicode(f):
    """ Convert a filename (unicode, utf-8 or iso-8859-1) into unicode
        
    Args:
        f (str) : a filename
        
    Returns:
        unicode : converted filename        
    """
    if isinstance(f,unicode):
        return f
    try:
        return unicode(f,encoding='iso-8859-1')
    except UnicodeDecodeError:
        return unicode(f,encoding='utf-8',errors='replace')

def file_unicode_list(l):
    """ Convert filenames into unicode strings inside a list
        
    Args:
        l (list) : a filename list
        
    Returns:
        list : converted filename list       
    """
    return [file_unicode(i) for i in l]

def slugify(value):
    """ Convert string to a slug
        
    Args:
        value (str) : the string to convert
        
    Returns:
        str : the slug       

    Examples:
        >>> slugify("he'l'lO  Wörld !")
        >>> 'hello-world'
    """
    value = re.sub('[^\w\s-]', '', remove_accents(value)).strip().lower()
    return re.sub('[-\s]+', '-', value)

base62_map = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
def base62_encode(i):
    """ encode an integer into base62
    
    This can be usefull when encoding an item id to build a short url : see url shorteners like http://pack.li
        
    Args:
        i (int) : the number to convert
        
    Returns:
        str : base62 encoded string       

    Examples:
        >>> base62_encode(1024)
        >>> 'GW'        
    """
    out = ''
    while i > 0:
        r = i % 62
        i /= 62
        out = base62_map[r] + out
    return out

def base62_decode(str):
    """ decode a base62 encoded number
        
    Args:
        str (str) : base62 string
        
    Returns:
        int : decoded integer       

    Examples:
        >>> base62_decode('GW')
        >>> 1024    
    """
    if str is None:
        return None
    i=0
    for c in str:
        i = i*62 + base62_map.index(c)
    return i

def random_password(length=8):
    """ Generate an "easy to memorize" random password
        
    Args:
        length (int) : Password length (default : 8)
        
    Returns:
        str : The random password       

    Examples:
        >>> random_password()
        >>> 'rixerutu'
    """
    vowel='aeiou'
    consonant='bcdfghjklmnpqrstvwxyz'
    pw=''
    for i in range(length):
        if i % 2:
            pw += random.choice(vowel)
        else:
            pw += random.choice(consonant)
    return pw

def is_ip_valid(address):
    """ Check string is a correct IP address (ipv4)
    
    It just checks IP string syntax. Useful for form checking.
        
    Args:
        address (str) : IP address string to check
        
    Returns:
        bool : True if IP string syntax is correct.       

    Examples:
        >>> is_ip_valid('12.23.34.45')
        >>> True
        >>> is_ip_valid('12.23.34.345')
        >>> False
        >>> is_ip_valid('12.23.34')
        >>> False
        >>> is_ip_valid('12.23.34a.45')
        >>> False
        >>> is_ip_valid('12.23.34.45.56')
        >>> False
    """
    if " " in address:
        return False
    parts = address.split(".")
    if len(parts) != 4:
        return False
    for item in parts:
        try:
            if not 0 <= int(item) <= 255:
                return False
        except ValueError:
            return False
    return True

def is_email_valid(email):
    """ Check string is a correct email address
    
    It just checks string syntax. Useful for form checking.
        
    Args:
        address (str) : email address string to check
        
    Returns:
        bool : True if email string syntax is correct.       

    Examples:
        >>> is_email_valid('hello@world.com')
        >>> True
        >>> is_email_valid('hello@world')
        >>> False
        >>> is_email_valid('hello world')
        >>> False
    """
    return bool(re.match(r'[^@]+@[^@]+\.[^@]+', email))


def remove_accents(s):
    """ Remove accents
    
    Args:
        s (str) : string to convert
        
    Returns:
        str : same string without any accent       

    Examples:
        >>> remove_accents('Et voilà !')
        >>> 'Et voila !'
    """
    if isinstance(s,str):
         s = unicode(s,"utf8","replace")
    if isinstance(s,unicode):
         s=unicodedata.normalize('NFD',s)
         return s.encode('ascii','ignore')
    return s