from urllib2 import urlopen

# Retrieve HTML string from the URL
html = urlopen("http://www.pythonscraping.com/exercises/exercise1.html")
print(html.read())
print "hello, urllib2"
print "hello, GZ!"
