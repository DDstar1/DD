'''name =['fidjdmdjhjbjd']
dd_list=['fidjdmdjhjbjd']


if name==dd_list:
    print(True)
else:
    print(False)'''


import re



file = 'WhatsApp Chat with Scholarship Region Q14.txt'


sorted_file = 'sorted.txt'

with open(file, 'r', encoding='utf-8') as file:
    #read lines into a list where each line is an item
    file=file.readlines()
    linenum = 0
    linenum_search = []
    linenum_date = []
    num_down=[]
    #loops through all the line items in the list
    
    #this removes all the whitespaces
    while '\n' in file:
        file.remove('\n')
            
   
    
    for lines in file:
        #removes all blank lines from the loop
        linenum += 1
        #with the re.compile function, you write your regex and flag
        
        pattern_search = re.compile(r'undergraduate', re.IGNORECASE)
        pattern_date = re.compile(r'\d+[/]\d+[/]\d\d')#6/22/22
        
        # then u attach the compile function to the string body u want to sort
        search_matches = pattern_search.finditer(lines)
        date_matches = pattern_date.finditer(lines)


        # I realised loops inside loops inside loops perform codes relative to them...not just all the codes that came before them
        
        for match in search_matches:
            linenum_search.append(linenum)
            #print(match, linenum)
               
        for match in date_matches:
            linenum_date.append(linenum)
            #print(match, linenum)
            
            
    i=0
    j=0
    dupli_del=[]     
    dupli_date=[]   
    print(f'''\n\n\n {len(linenum_search)}    {len(linenum_date)}\n\n\n''')



    while i < len(linenum_search)-1 :
        checker = linenum_search[i] - linenum_date[j]
        j += 1
        if checker < 0:
            
            j -= 2
            
            for num in range( linenum_search[i]+1 , linenum_date[j+1] ):
                dupli_date.append(num)
                
            for num in dupli_date:
                while num in linenum_search:
                    linenum_search.remove(num)
                    
            i += 1
            
            print (dupli_date,'     ',j)
            dupli_date=[]
            
    print('\n\n',linenum_search)

            

            

    range = []
    i = 0
    j=0

    
    while (i < len(linenum_search)-1) and (j <= len(linenum_date)-1):
        checker = linenum_search[i] - linenum_date[j]
        j += 1
        
        if checker < 0:
            j-=2
            range.append(linenum_date[j])
            i += 1
            j = 0
            
        elif checker == 0:
            i += 1
            j = 0
        pass

        
with open(sorted_file, 'w', encoding='utf-8') as f:
    
     
    i = 0
    
    while i < len(range):  
        end_date_index = linenum_date.index(range[i])+1
        #b = file[range[i]-1 : linenum_date[end_date_index]-1]
        f.writelines(file[range[i]-1 : linenum_date[end_date_index]-1])
        f.write('\n\n\n\n\n\n')
        i += 1
        #print(i,'  ', len(range))


        
       

     
      
        
    
    
    

