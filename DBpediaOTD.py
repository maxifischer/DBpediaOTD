import webbrowser
import sys
import DBPedia_On_This_Day
import whole_year
import datetime

# format should be open <name of html file>
# or reload <year, month, day>

def main():
    new = 2
    try:
        if "-open" in sys.argv:
            openind = sys.argv.index("-open")
            file = sys.argv[openind + 1]
            url = "file://C:/Users/Maxi/Documents/SemanticWebJob/DBpediaOTD/Result_Pages/" + file
            #brow = webbrowser.get('firefox')
            webbrowser.open(url)
        elif "-reload" in sys.argv:
            reloadind = sys.argv.index("-reload")
            if sys.argv[reloadind + 1] == "all":
                try:
                    year = int(sys.argv[reloadind + 2])
                except (TypeError, IndexError) as e:
                    year = datetime.datetime.now().year
                whole_year.start(year)
            else:
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
