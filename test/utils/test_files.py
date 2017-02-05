from tools import open_csv, open_xls

"""
d = open_csv('wrong.csv', headers=None, selected=None)
print "\nd=", d
d = open_csv('movies.csv', headers=None, selected=None)  # correct
print "\nd=", d
d = open_csv('movies.csv', headers=['a'], selected=None)  # too few header
print "\nd=", d
d = open_csv('movies.csv', headers=[None], selected=None)  # wrong header
print "\nd=", d
d = open_csv('movies.csv', headers=['a','b','c','d'], selected=None)  # extra headers
print "\nd=", d
d = open_csv('movies.csv', headers=['a','b','c'], selected=[None])  # wrong select
print "\nd=", d
d = open_csv('movies.csv', headers=['a','b','c'], selected=['a'])  # wrong select
print "\nd=", d
d = open_csv('movies.csv', headers=['a','b','c'], selected=[1,3,10])  # correct?
print "\nd=", d
"""

d = open_xls('wrong.xls', headers=None, selected=None)
print "d01=%s\n" % d
d = open_xls('movies.xls', headers=None, selected=None)  # correct
print "d02=%s\n" % d
d = open_xls('movies.xls', headers=['a'], selected=None)  # too few header
print "d03=%s\n" % d
d = open_xls('movies.xls', headers=[None], selected=None)  # wrong header
print "d04=%s\n" % d
d = open_xls('movies.xls', headers=['a','b','c','d'], selected=None)  # extra headers
print "d05=%s\n" % d
d = open_xls('movies.xls', headers=['a','b','c'], selected=[None])  # wrong select
print "d06=%s\n" % d
d = open_xls('movies.xls', headers=['a','b','c'], selected=['a'])  # wrong select
print "d07=%s\n" % d
d = open_xls('movies.xls', headers=['a','b','c'], selected=[1,3,10])  # correct?
print "d08=%s\n" % d

d = open_xls('movies.xls', headers=['a','b','c'], selected=[1,3,10], sheet=2)  #wrong sheet
print "d09=%s\n" % d

d = open_xls('movies.xls', headers=['a','b','c'], selected=[1,3,10], sheetname='foo')  #wrong sheet
print "d10=%s\n" % d

