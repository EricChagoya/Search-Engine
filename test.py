



import json
import unittest

from bs4 import BeautifulSoup
import re




class Tokens(unittest.TestCase):

    def setUp(self):
        # Setup tokens
        #Read File and put contents into the indexer
        # See if the token is in the indexer
        pass


    def test_ip_address(self):
        print(5)
        #self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
        ip= "192.168.0.1"


    def test_email_address(self):
        email= "info@uci.edu"
        pass



    def test_urls(self):
        pass



    def test_stemming(self):
        pass


    def test_hyphens(self):
        pass


    def test_end_period(self):
        pass



    def test_extra_comma(self):
        pass


    def test_random_character(self):
        pass



    def test_stemming(self):
        pass


    def test_apostrophes_s(self):
        pass



    def test_apostrophe(self):
        #Apostrophe O'Connel
        pass




    def test_contractions(self):
        pass



    def test_small_important_tokens(self):
        #am, pm, el pase, World War II
        pass



    def test_phrases(self):
        pass


    def test_abbreviation(self):
        # U.S.A     USA
        pass



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












