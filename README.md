# Matrix_BestBuy_Stock_Bot
Matrix bot that notifies users when bestbuy items become in-stock.

# Dependencies

- python-matrixbot (https://pypi.org/project/python-matrixbot/)
- BeautifulSoup (https://pypi.org/project/beautifulsoup4/)

# Installation
- Create a bot user on your matrix server and get its access_token
- Edit MATRIX SETTINGS to match your matrix server
- Create file "watchlist.txt" in directory of the bot and modify watchfile_location appropriately 

# Usage
- Add a link to the bot's watchlist (will refresh every 30 seconds and notify it's instock every 60 seconds until OOS again):

  !add [link]
  
- View active watchlist (just prints the list object, cba to make this look nice):

  !list
