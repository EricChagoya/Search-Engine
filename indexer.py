'''
@author: Luke Sumaquial
'''
import subprocess
import sys,re


# def install(package):
#     subprocess.check_call([sys.executable, "-m", "pip", "install", package])
# 
# install("nltk")

from nltk.stem import WordNetLemmatizer, PorterStemmer

def tokenizer(token:str) -> str: 
    '''takes in a token(key) from token/freq dict
        returns a modified token
        will include stemming, removing apostrophes, 
        dealing with hyphens, IP addresses, websites, emails, phrases, special characters
    '''
    
    email_pat = re.compile(r'^(?:(\w{0,64})(@)(\w{1,251}).(com))$')
    ip_pat = re.compile(r'^(?:(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3}))$')
    url_pat = re.compile(r'(?:(https|http)?(://)?(www.)?(\w{1,63})(\.\w*)*(\.(?:com|edu|gov|org|net|mil|int|\w{2,3}))(\\w+)?)')
    if email_pat.match(token) != None:
        return token
    elif ip_pat.match(token) != None:
        return token
    elif url_pat.match(token) != None:
        return token
#     print(url_pat.match(token))
    mod_token = ''
    
    refined_token = token.encode().decode('ascii','replace').replace(u'\ufffd','-')
    
    stemmer = PorterStemmer()
    lemmatizer =  WordNetLemmatizer()
    
    stemmed_token = stemmer.stem(refined_token)
    lem_token = lemmatizer.lemmatize(refined_token) 
    if lem_token.endswith('e'):
        itemized_token = re.split('\W', lem_token.rstrip()) 
    else:
        itemized_token = re.split('\W', stemmed_token.rstrip())
    #https://stackoverflow.com/questions/24517722/how-to-stop-nltk-stemmer-from-removing-the-trailing-e
#     print(itemized_token)
    for i in itemized_token:
        mod_token += i
        
    if len(mod_token) >= 1:
        return mod_token.lower()
    else:
        return None


print(tokenizer("Software"))

# if __name__ == '__main__':
#     tokenizer(sys.argv[1])





