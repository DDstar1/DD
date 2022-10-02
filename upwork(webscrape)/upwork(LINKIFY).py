from bs4 import BeautifulSoup
import requests
import csv
import re




headers = {
        'User-Agent' : 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Mobile Safari/537.36'
         }



#Current webpage
webpage_increment=1



while webpage_increment:
        #the initial link which is automated
        address1 = f'https://classifieds.mcclatchy.com/marketplace/biloxi/search/query?categoryId=5&searchProfile=notices&source=biloxi&page={webpage_increment}&size=50&view=list&showExtended=false&startRange=&keywords=&firstDate=07%2F30%2F2022&lastDate=07%2F30%2F2022&ordering=#'


        #loads the first webpage and gets the links to the detailed page
        html_file_1 = requests.get( address1, headers=headers)
        
         #This makes sure that the automatic webscraping breaks when there aren't more page to be scraped
        if html_file_1.status_code != 200 :
                print('THIS IS THE END')
                print(type(html_file_1.status_code))
                break

        #This parses the html page
        soup1 = BeautifulSoup(html_file_1.text, 'lxml')

        panel_body = soup1.find_all('div', class_= 'panel panel-result')

        list_new_linkify_text = []
        list_panel_link = []

        for body in panel_body:
                #Gets panel link
                panel_link = body.find('a', href=True)['href']
               
                #Appends it to link list
                list_panel_link.append(panel_link)

                panel_time = body.find('time').text
                

                #Loads the detailed webpage from the scraped link
                address2 = panel_link

                html_file_2 = requests.get( address2, headers=headers).text

                soup2 = BeautifulSoup(html_file_2, 'lxml')

                linkify_text = soup2.find('p', class_='linkify').text


                #Removes special characters from the linkify text
                new_linkify_text = re.sub('[^A-Za-z0-9]+', ' ', linkify_text)
                list_new_linkify_text.append(new_linkify_text)


        print(len(list_new_linkify_text))
        
        #Writes the new linkify text to a csv file
        with open('linkify.csv', 'a', encoding='utf-8') as csv_out:
                csv_writer = csv.writer(csv_out)
                
                #Makes sure the Info tag is only written once on the csv file
                if webpage_increment == 1:
                        csv_writer.writerow(['INFO'])
                        
                for value in list_new_linkify_text:
                        csv_writer.writerow([value])
                        #print(linkify)

        
        #increases webpage number by 1
        webpage_increment += 1




        