# -*- coding: utf-8 -*-
'''
Created on 2 févr. 2010

@author: elapouya
'''

import cStringIO, gzip
import re
import random
import unicodedata

def compress(s):
    zbuf = cStringIO.StringIO()
    zfile = gzip.GzipFile(mode='wb', compresslevel=6, fileobj=zbuf)
    zfile.write(s)
    zfile.close()
    output=zbuf.getvalue()
    zbuf.close()
    return output

def uncompress(s):
    zbuf = cStringIO.StringIO(s)
    zfile = gzip.GzipFile(mode='rb', compresslevel=6, fileobj=zbuf)
    output=zfile.read(s)
    zfile.close()
    zbuf.close()
    return output

def get_col(str,**kwargs):
    """
    Exemple : get_col("/a/b/c/path_to_install",col=-1,sep='/',col2=0,sep2='_') donne : 'path'
    """
    for k,v in sorted(kwargs.items()):
        if k[:3] == 'col':
            sep = kwargs.get('sep%s' % k[3:],' ')
            str = str.split(sep)[v]
    return str

def extract(str,pattern):
    m = pattern.search(str)
    if m:
        return m.group(1)
    return None

def extracts(str,pattern,default):
    m = pattern.search(str)
    if m:
        return m.groups()
    return default

def plural(str1,str2,n):
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