from selenium import webdriver
from selenium.webdriver.firefox.options import Options

ELEMENTS_IN_LIST = 7
longest = [0, 0, 0, 0, 0, 0, 0]
url = "https://platinumtokens.com/"

def pretty_print(lizt):
    firstLine = ''
    title = ['Item', 'Buy', 'Sell', 'Margin', 'RoI', 'Quantity']
    lizt.insert(0, title)

    for sub in lizt:
        line = ''
        for i in range(len(sub)):
            word = sub[i]

            if '.' in word:
                for k in range(longest[i] - len(word)):
                    line += ' '
                line += word
                line += '% '
            else:
                line += word
                for k in range(longest[i] - len(word)):
                    line += ' '

            line += '\t'

        if 'RoI' in line:
            firstLine = line
        print line

    print firstLine

options = Options()
options.add_argument("--headless")

print 'Opening headless browser...'
driver = webdriver.Firefox(firefox_options=options)
print 'Getting page \'' + url + '\'...'
driver.get(url)
print 'Page download complete. parsing...'

ele = driver.find_element_by_tag_name('tbody')
text = ele.text

tups = []
splits = text.split('\n')
for i in range(len(splits)):
    tup = [] # list not tuple I know
    if i % 2 != 0:
        continue
    split2 = splits[i].split(' ')
    name = ''
    for j in range(len(split2)):
        token = split2[j]
        if token != '%':
            if ELEMENTS_IN_LIST + j <= len(split2):
                name += token + ' '
            else:
                tup.append(token)

    tup.insert(0, name)
    for z in range(len(tup)):
        f = tup[z]
        if len(f) > longest[z]:
            longest[z] = len(f)
    tups.append(tup)
    #print str(tup)

print 'Sort by: (x to exit)'
print 'Buy (1) \nSell (2) \nMargin (3) \nRoI (4) \nQuanity (5)'
sortBy = raw_input('? ')    
num = int(sortBy)

if num == 0:
    tups = sorted(tups, key=lambda x: x[num])
else:
    tups = sorted(tups, key=lambda x: int(x[num].replace('%', '').replace(',', '')))
        
pretty_print(tups)
driver.quit()
