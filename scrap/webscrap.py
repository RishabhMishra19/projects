from bs4 import BeautifulSoup as BS
import requests
import lxml
import pandas as pd

def get_flipkart_prod_links(search_string):
        links=[] 
        try:
            page=requests.get('https://www.flipkart.com/search?q='+search_string).text
            soup=BS(page,'lxml')
            part1=soup.body.div.div.contents[2]#getting product section
            part2=part1.contents[1].contents[0].contents[1].contents#getting all prod section
            l=part2[0].text.split(' ')
            for i in range(len(l)):
                if l[i]=='of':
                    items=40
                    break
            
            base_url="https://www.flipkart.com"
            if items==24: 
                for prod in part2[1:-2]:
                    prod_link=prod.find('a').get('href')
                    full_link=base_url+prod_link
                    links.append(full_link)
            elif items==40:
                for prod in part2[1:-2]:
                    for pr in prod.div.contents:
                        prod_link=pr.find('a').get('href')
                        full_link=base_url+prod_link
                        links.append(full_link)
            else:
                pass
            return links
        except:
            return links

def prod_details(prod_link):
        page=requests.get(prod_link).text
        soup=BS(page,'lxml')
        part1=soup.body.div.div.contents[2]
        part2=part1.contents[1].find('div').contents[1].contents
        
        detail_part=part2[1]
        comment_part=part2[-1]
        
        name=detail_part.div.contents[0].text
        for content in detail_part.div.contents:
            try:
                if content.contents[0].get('class')[0]=='_2i1QSc':
                    price=content.text.split('₹')[1]
                    break
            except:
                pass
            
        
        for content in detail_part.div.contents:
            try:
                if content.contents[0].get('class')[0]=='_3ors59':
                    overall_rating=content.span.text
                    num_ratings=content.text.split(' ')[0][len(overall_rating):]
                    num_reviews=content.text.split(" ")[-2].replace(",","")
                    if not num_reviews.isdigit():
                        num_reviews=num_reviews.split('&')[1]
                    break
            except:
                pass
            
        base_url="https://www.flipkart.com"
        details=[]
        try:
            for content in comment_part.contents[::-1]:
                if content.div.contents[-1].name=='a':
                    all_reviews_link=content.div.contents[-1].get('href')
                    all_reviews_full_link=base_url+all_reviews_link
                    details=[name,price,overall_rating,num_ratings,num_reviews,all_reviews_full_link]
                    break
        except:
            pass

        return details

def review_details(review_link):
        page_p=requests.get(review_link).text
        soup_p=BS(page_p,'lxml')
        part1_p=soup_p.body.div.div.contents[2]
        part2_p=part1_p.find('div').div.contents[1].contents
        pages=int(part2_p[-1].find('span').text.split(' ')[-1].replace(",",""))
        
        if pages>5:
            pages=5
        Reviews=[]
        
        for i in range(pages):
            link=review_link+f'&page={i+1}'
            page=requests.get(link).text
            soup=BS(page,'lxml')
            part1=soup.body.div.div.contents[2]
            part2=part1.div.div.contents[1].contents
            reviews_part=part2[2:-1]
            
            for Review in reviews_part:
                review_head=Review.div.div.div.contents[0]
                review_heading=review_head.p.text
                review_rating=review_head.div.text
                review=Review.div.div.div.contents[1].text[:-9]
                Reviews.append([review_rating,review_heading,review])
        return Reviews

def all_details(search_string):
        k=0
        df=pd.DataFrame(columns=['prod_name','prod_price','overall_rating','num_ratings','num_reviews','user_rating','user_review_heading','user_review_content'])
        
        search_item_links=get_flipkart_prod_links(search_string)

        if len(search_item_links)==0: 
            links=search_item_links
        else:
            links=search_item_links[:10]
        for item_link in links:
            
            item_details=prod_details(item_link)
            
            try:
                reviews_list=review_details(item_details[-1])
                for item_review in reviews_list:
                    k=k+1
                    df.loc[k]=[item_details[0],item_details[1],item_details[2],item_details[3],item_details[4],item_review[0],item_review[1],item_review[2]]
                    if k>=100:
                        return df
            except:
                pass
        return df

