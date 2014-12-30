# -*- coding: utf-8 -*-
"""
Python String Extension

With pystrext module, you will be able to manipulate strings.

Created on 2 févr. 2010
@author: elapouya
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

def test_val(val,test_func,str1,str2):
    if test_func(val):
        if callable(str1):
            return str1(val)
        else:
            return str1 % {'val' : val}
    else:
        if callable(str2):
            return str2(val)
        else:
            return str2 % {'val' : val}

def truncate(str,maxsize,max_end_str='...'):
    if len(str) > maxsize:
        return str[:max(0,maxsize-len(max_end_str))] + max_end_str
    return str

def MB_GB(str):
    if str:
        size = int(str)
        if size >= 1024:
            return "%d GB" % int(size / 1024)
        else:
            return "%d MB" % size
    return str

def MHz_GHz(str):
    if str:
        size = float(str)
        if size >= 1000:
            return "%.3f GHz" % (size / 1000)
        else:
            return "%s MHz" % str
    return str

def version_lt(v1,v2):
    """
    Compare deux strings indiquant un n° de version du style 5.2.46 et 5.3
    Retourne True si v1 < v2.
    Marche avec des caractères alphanumérique : on peut tester 12.K.44 avec 12.L
    Ne marche qu'avec des N° de sous-version pas plus grand que 10 caractères ex : 0123456789.9876543210.AZERTYUIOP marche
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
    """
    Fonction qui justifie chaque sous version pour permettre un trie des version dans un ordre numerique :
    1.12 devient : 1.    12
    1.1  devient : 1.     1
    """
    nb = str.count(delim)
    # on force le nombre de points à level
    if nb < level:
        str += (level-nb) * delim
    return delim.join([ v.rjust(bitsize,fillchar) for v in str.split(delim)[:level+1] ])

def file_unicode(f):
    if isinstance(f,unicode):
        return f
    try:
        return unicode(f,encoding='iso-8859-1')
    except UnicodeDecodeError:
        return unicode(f,encoding='utf-8',errors='replace')

def file_unicode_list(l):
    return [file_unicode(i) for i in l]

def slugify(value):
    value = re.sub('[^\w\s-]', '', value).strip().lower()
    return re.sub('[-\s]+', '-', value)

base62_map = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
def base62_encode(i):
    out = ''
    while i > 0:
        r = i % 62
        i /= 62
        out = base62_map[r] + out
    return out

def base62_decode(str):
    if str is None:
        return None
    i=0
    for c in str:
        i = i*62 + base62_map.index(c)
    return i

def random_password(length=8):
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
    return re.match(r'[^@]+@[^@]+\.[^@]+', email)


def remove_accents(s):
   """Removes all accents from the string"""
   if isinstance(s,str):
       s = unicode(s,"utf8","replace")
   if isinstance(s,unicode):
       s=unicodedata.normalize('NFD',s)
       return s.encode('ascii','ignore')
   return s