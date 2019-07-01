library(rvest)
library(magrittr)

xpath_selector = '/html/body/center[2]/table/tbody/tr/td/table'

cycles = read_html("http://www.speedcubing.com/chris/bhcorners.html", encoding = "UTF-8") %>%
  html_nodes(xpath = xpath_selector) %>%
  html_table(header = TRUE)

algs_stripped = gsub("\\(.+\\)$", "", gsub("\r\n", "", gsub(" ", "", cycles[[1]]$Algorithm)))

write(algs_stripped, "bh.txt")