import webbrowser
import sys
import DBPedia_On_This_Day
import whole_year

# format should be open <name of html file>
# or reload <year, month, day>

def main():
    new = 2
    try:
        if "open" in sys.argv:
            openind = sys.argv.index("open")
            file = sys.argv[openind + 1]
            url = "file://C:/Users/Maxi/Documents/SemanticWebJob/DBpediaOTD/Result Pages/" + file
            #brow = webbrowser.get('firefox')
            webbrowser.open(url)
        elif "reload" in sys.argv:
            reloadind = sys.argv.index("reload")
            if sys.argv[reloadind + 1] == "all":
                whole_year.start()
            year = sys.argv[reloadind + 1]
            month = sys.argv[reloadind + 2]
            day = sys.argv[reloadind + 3]
            date = int(year), int(month), int(day)
            DBPedia_On_This_Day.main(date)
    except IndexError:
        print("no file selected")
    except IOError:
        print("no such file")


if __name__ == "__main__":
    main()
