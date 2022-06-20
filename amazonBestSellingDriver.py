from scanItems import scanItemFiles
from amazonHTMLScraper import getProductHTML
from amazonscrape import createURLExport
createURLExport(homeURL = "https://www.amazon.com/Best-Sellers-Video-Games-Nintendo-Switch-Games/zgbs/videogames/16227133011/ref=zg_bs_nav_videogames_2_16227128011")
getProductHTML()
scanItemFiles()