import immoproxio
import immoweb
import pickle

# Perform a search on the website you'd like to scrape according to your criteria and put the link here
proxio_link = 'https://www.immoproxio.be/nl/panden/?transaction=2&cities=1000542-0,1000540-1000542,1000549-1000542,1000550-1000542,1000544-1000542,1000551-1000542,1000547-1000542,1000548-1000542,1000543-1000542,1000545-1000542,1000552-1000542,1000546-1000542,1000539-1000542,1000541-1000542&types=1,2,3&maxprice=800'
web_link = 'https://www.immoweb.be/nl/zoeken/huis-en-appartement/te-huur/gent/arrondissement?countries=BE&maxPrice=800&minSurface=65&page=1&orderBy=relevance'

# The coordinates to two destinations. The script will calculate the distance from these locations to the apartment and return the average. 
dest_a = (51.056332, 3.700853)
dest_b = (51.056691, 3.740310)

# Name of file
filename = "apartment_data.csv"

# Head of file
head = "link;address;size;energy;rooms;price;common costs;avg_distance;garden;balcony;bathtub;EHW;attic;basement;sauna;bookmarks;views\n"

def main():

    apt_file = open(filename, "w")
    apt_file.write(head)

    web_links = immoweb.get_links(web_link)
    # pickle.dump(web_links, open("web_links.p", "wb"))
    web_apts = immoweb.get_info(web_links, dest_a, dest_b)
    # pickle.dump(web_apts, open("web_apts.p", "wb"))
    # web_apts = pickle.load(open("web_apts.p", "rb"))

    proxio_links = immoproxio.get_links(proxio_link)
    # pickle.dump(proxio_links, open("proxio_links.p", "wb"))
    # proxio_links = pickle.load(open("proxio_links.p", "rb"))
    proxio_apts = immoproxio.get_info(proxio_links, dest_a, dest_b)
    # pickle.dump(proxio_apts, open("proxio_apts.p", "wb"))
    # proxio_apts = pickle.load(open("proxio_apts.p", "rb"))


    for row in web_apts:
        apt_file.write(row)
    for row in proxio_apts:
        apt_file.write(row)

    apt_file.close()


if __name__ == '__main__':
    main()
    