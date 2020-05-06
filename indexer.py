'''
@author: Luke Sumaquial
'''
import subprocess
import sys,re


# def install(package):
#     subprocess.check_call([sys.executable, "-m", "pip", "install", package])
# 
# install("nltk")

from nltk.stem import PorterStemmer

def tokenizer(token:str) -> str: 
    '''takes in a token(key) from token/freq dict
        returns a modified token
        will include stemming, removing apostrophes, 
        dealing with hyphens, IP addresses, websites, emails, phrases, special characters
    '''
    
    email_pat = re.compile(r'^(?:(\w{0,64})(@)(\w{1,251}).(com))$')
    ip_pat = re.compile(r'^(?:(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3}))$')
    url_pat = re.compile(r'(?:(https|http)?(://)?(www.)?(\w{1,63})(\.\w*)?(\.(?:com|edu|gov|org|net|mil|int|\w{2,3})))')
    if email_pat.match(token) != None:
        return token
    elif ip_pat.match(token) != None:
        return token
    elif url_pat.match(token) != None:
        return token
    print(url_pat.match(token))
    mod_token = ''
    
    refined_token = token.encode().decode('ascii','replace').replace(u'\ufffd','-')
    stemmer = PorterStemmer()
    stemmed_token = stemmer.stem(refined_token)
    itemized_token = re.split('\W', stemmed_token.rstrip())
#     print(itemized_token)
    for i in itemized_token:
        mod_token += i
        
    if len(mod_token) >= 1:
        return mod_token
    else:
        return None


print(tokenizer("https://europa.eu/european-union/index_en"))

# if __name__ == '__main__':
#     tokenizer(sys.argv[1])





