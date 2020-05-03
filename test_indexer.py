



import json
import unittest

from bs4 import BeautifulSoup
import re




class Indexer_Test(unittest.TestCase):

    def setUp(self):
        # Setup tokens
        # Read File and put contents into the indexer
        # See if the token is in the indexer
        self.indexer= None  # Empty indexer maybe?


    def test_ip_address(self):
        ip= "192.168.0.1"
        #self.indexer add(ip)
        #self.assertIn(ip, self.indexer)


    def test_email_address(self):
        email= "info@uci.edu"
        #self.indexer add(email)
        #self.assertIn(email, self.indexer)



    def test_urls(self):
        url= "https://www.ics.uci.edu/~pattis/ICS-33/lectures/unittest.txt"
        #self.indexer add(url)
        #self.assertIn(url, self.indexer)



    def test_stemming(self):
        fishes= "fishes"
        #self.indexer add(fishes)
        #self.assertIn("fish", self.indexer)


    def test_hyphens(self):
        oneway= "one-way"
        #self.indexer add(oneway)
        #self.assertIn(oneway, self.indexer)


    def test_end_period(self):
        stamp= "stamp."
        #self.indexer add(stamp)
        #self.assertIn("stamp", self.indexer)



    def test_extra_comma(self):
        mouse= "mouse,"
        #self.indexer add(mouse)
        #self.assertIn("mouse", self.indexer)


    def test_random_character(self):
        pass




    def test_apostrophes_s(self):
        tom= "Tom's"
        #self.indexer add(tom)
        #self.assertIn("tom", self.indexer)



    def test_apostrophe(self):
        #Apostrophe O'Connel
        OConnel= "O'Connel"
        #self.indexer add(OConncel)
        #self.assertIn("OConncel", self.indexer)




    def test_contractions(self):
        cant= "can't"
        #self.indexer add(cant)
        self.assertIn("cant", cant)



    def test_small_important_tokens(self):
        #am, pm, el paso, World War II
        pass



    def test_phrases(self):
        pass


    def test_abbreviation(self):
        # U.S.A     USA
        USA= "U.S.A"
        #self.indexer add(USA)
        #self.assertIn("USA", USA)
        



json_file= "0a0056fb9a53ec6f190aa2b5fb1a97c33cd69726c8841f89d24fa5abd84d276c.json"
# This method doesn't tell use which text are headers, bolded
"""
with open(json_file, 'r') as f:
    array = json.load(f)

#print (array)
for k, v in array.items():
    print(k, "->", v)
    print()

print(type(array["content"]))
print(array["content"][-1])
"""


#parsed_json = (json.loads(json_file))
#print(json.dumps(parsed_json, indent=4, sort_keys=True))

with open(json_file, 'r') as f:
    print(f)
    for i in f:
        print(i)
    soup = BeautifulSoup(f, "lxml")
    header = soup.find("b")
    #parts = [p.get_text(strip=True, separator=" ") for p in header.find_all_next("p")]
    #print({header.get_text(strip=True): parts})

    
    print(soup)
    print(header)
    #a= soup.find_all(re.compile('^h[1-6]$'))
    a= soup.find_all(re.compile('^header$'))
    print(a)




if __name__ == "__main__":
    #unittest.main()
    pass












