"""@author : Dharmendra Kumar Verma"""import urllib2import sysimport os, timeimport threadingimport warningsfrom url_parser import URLParserHreffrom utils import url_resolverfrom player import Playeros.system("clear && echo WELCOME ...  ")  # Helps in clearing console and greeting the userclass SongsPK():    VERSION = 1.1    #Default directory path on your Desktop    DIRPATH = os.path.expanduser('~/Desktop/songsPK_Collection')    def __init__(self, play_mode=False):        self.play_mode = play_mode        print "Please select an option to proceed\n"        print "1 - Url based bulk song download\n"        print "2 - Movie name based bulk song download\n"        while True:            try:                option = input('Enter your option {1 or 2}\n')                os.system('clear')            except Exception as e:                    print e.message  # To display the error message in console                    continue            if option == 1:                self.urlbased()                break            elif option == 2:                self.moviehandler()                break            else:                print "Invalid option"                continue        os.system('clear && echo PLEASE WAIT ...')        """        checks the existence of default output directory , If not present it will create.        As default location is set to user Desktop, program is not checking the write permission of directory.        If directory error please check the write permission of user of ~/Desktop .        """        if not os.path.exists(self.DIRPATH):            os.system('mkdir %s' % self.DIRPATH)    def write_mp3(self, mp3, filename=None):        """        Writes the downloaded file and renames the title.        """        name = (mp3.geturl()).split('/')        folder_name = os.path.expanduser(self.DIRPATH+'/'+name[-2]+'/')        if not os.path.exists(folder_name):            os.system('mkdir %s' % folder_name)  # Creates a directory on current users Desktop        #File Opening and writing        fullpath = folder_name+filename        with open(fullpath, 'w') as output:            while True:                buf = mp3.read(65536)  # Fixed the Buffer size                if not buf:                    break                output.write(buf)    def urlbased(self, url_datas=None):        """        Prepares the url and then download the mp3 file. To write the file in Disk it depends on write_mp3 function        """        visited_url = []        if not url_datas:            url_datas = raw_input("Enter comma separated url strings\n")            os.system('clear && echo PLEASE WAIT ...')        url_datas = url_datas.split(',')        for url_data in url_datas:            movie_name = url_data.rstrip('.html').split('/')[-1]            if url_data.startswith('www'):                url_data = url_data.replace('www', 'http://www')            try:                s_data = urllib2.urlopen(url_data).read()                song_urls = URLParserHref.get_songs_url(s_data)                parse_url = 0                for url in song_urls:                    parse_url += 1                    try:                        res, finalurl = url_resolver(url)                        # Now check the function                        if finalurl.endswith('.mp3') and finalurl not in visited_url and not finalurl.startswith('..'):                            with warnings.catch_warnings():                                warnings.simplefilter("ignore")                                if self.play_mode:                                    Player.play()                                else:                                    self.write_mp3(res, filename=finalurl.split('/')[-1])  # call to write mp3 file in Disk                        visited_url.append(finalurl)                    except:                        continue                    sys.stdout.write("\r%d out of %d songs processed for movie ---> %s" %(parse_url, len(song_urls), movie_name))                    sys.stdout.flush()            except:                pass    def moviehandler(self):        """            Get Movie name list and allow user to enter multiple movie number to download songs from all the movies in one hit.            STEPS- Enter starting letter of any indian Movie                   Select your movie number from the displayed list                   Files will be downloaded on your desktop in a folder named songsPK_Collection.Movie Name            os command mainly has been used for clearing the mess        """        movie_letter = raw_input('Enter Indian Movie start letter [A-Z] to get movie name list\n')        os.system('clear && echo PLEASE WAIT ...')        try:            url_data = "http://songspk.name/%s_list.html" % movie_letter            movies = urllib2.urlopen(url_data).read()        except:            url_data = "http://songspk.name/indian_movie/%s_List.html" % movie_letter.upper()            movies = urllib2.urlopen(url_data).read()        url_dict = {}        count = 1        for url in URLParserHref.get_movie_names(movies):            if not url.startswith('..'):                url_dict[str(count)] = url                count += 1        for k, v in url_dict.iteritems():            print k + '-----' + v.rstrip('.html').split('/')[-1]        movie = raw_input('Enter comma separated movie number to download all songs of movies\n')        movie = movie.split(',')        os.system('clear && echo PLEASE WAIT ...')        movie_url = ''        for no in movie:            movie_url = "http://songspk.name/%s" % url_dict[no] + ','            threading.Thread(target=self.urlbased, kwargs = (dict(url_datas=movie_url))).start()            while True:                if threading.active_count() < 10:                    break                else:                    time.sleep(10)if __name__ == "__main__":    play_mode = False    if len(sys.argv) > 1:        if sys.argv[1] == "--play":            play_mode = True    if play_mode:        Player._check_mpg123()    SongsPK(play_mode=play_mode)