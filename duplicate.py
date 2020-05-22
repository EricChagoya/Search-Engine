



def check_similar_url(link_dict: {str:{str:int}}, url:str) -> {'urls'}:
    #parameter: dictionary = {link: {token/link: int}}
    #variable "url" will be used to compare every link
    similar_urls = set()
    for link in link_dict:
        if (compare_two_urls(link, url)):
            similar_urls.add(link)
                    
    return similar_urls


def compare_two_urls(link1:str, link2:str) -> bool:
    total= abs(len(link1) - len(link2))
    if len(link1) > len(link2):
        link2 += (total * " ")
    else:
        link1 += (total * " ")
            
    threshold = round(len(link1) * 0.8)
    similar_characters = sum([1 for a in range(0, len(link1)) if (link1[a] == link2[a])])
        
    if similar_characters >= threshold:
        return True
    return False



def count_tokens(tokens: {str:int}) -> int:
    """It counts how many tokens are in the dict. The first one counts every tokens
    while the second one excludes websites."""
    return sum([v for k, v in tokens.items() if "http" not in k])



def check_duplicates(traveler: {str:{str:int}}, url: str, url_tokens:{str:int}) -> bool:
    """If duplicate, return True."""
    threshold= 0.95
    similar_urls= check_similar_url(traveler, url)
    
    for similar_url in similar_urls:
        same_word= set()
        similar_word= 0
        different_word= 0
        
        for k, v in traveler[similar_url].items():
            if k in url_tokens:
                value= url_tokens[k]
#                 print("url_tokens:",k,value[0])
#                 print("v:",k,v[0])
                similar_word+= min(v[0], value[0])
#                 print("abs(v[0] - value[0]):",abs(v[0] - value[0]))
                different_word+= abs(v[0] - value[0])
                same_word.add(k)
            else:
                different_word= v[0]
        
        total_words= similar_word + different_word
        if (total_words == 0) or (similar_word/total_words) >= threshold:
            return True
    
    return False
        
