from zimply import ZIMServer

# initialize zim server
zim_path = "./wikipedia_en_all_maxi_2024-01.zim"  # replace with your zim server.
server = ZIMServer(zim_path)

# find relevant pages
title = "Test 1"
article = server.search_article(title)

if article:
    print(article['content'])
else:
    print(f"Page '{title}' not found.")
