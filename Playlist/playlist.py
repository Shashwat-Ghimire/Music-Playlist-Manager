import random  # for playlist shuffling
from collections import deque  # for playlist queue

class Song:
    def __init__(self, title, artist, duration):
        self.title = title  # song title
        self.artist = artist  # artist name
        self.duration = duration  # duration in seconds
        self.next = None  # for next song in linked list
        self.prev = None  # for previous song in linked list
        self.votes = 0  # for priority queue party mode

class Playlist:
    def __init__(self):
        self.head = None  # 1st song in linked list
        self.current = None  # current song in linked list
        self.tail = None  # last song in linked list
        
    def add_song(self, title, artist, duration):
        new_song = Song(title, artist, duration)
        if not self.head:  # if playlist is empty, set new song as head
            self.head = new_song 
            self.tail = new_song
            self.current = new_song
        else:
            current = self.head  # traverse to end of linked list
            while current.next: 
                current = current.next  # move to next song
            current.next = new_song 
            new_song.prev = current 
            self.tail = new_song  # update tail
    
    def next_song(self):
        if self.current and self.current.next:
            self.current = self.current.next
            return self.current
        elif self.current:  # loop back to start if at end
            self.current = self.head
            return self.current
        return None  # no songs in playlist
            
    def previous_song(self):
        if self.current and self.current.prev:
            self.current = self.current.prev
            return self.current
        elif self.current:  # loop back to tail if at start
            self.current = self.tail
            return self.current
        return None  # no songs in playlist
    
    def get_current_song(self): 
        return self.current  # return current song

# For priority queue party mode voting
class PartyPlaylist:
    def __init__(self):
        self.queue = []  # empty priority queue
    
    # add song to priority queue
    def add_song(self, song):
        self.queue.append(song)
        # sorting songs by votes
        self.queue.sort(key=lambda x: x.votes, reverse=True)  # descending order sorting
        
    def get_next(self):
        if self.queue:
            return self.queue.pop(0)  # remove and return the 1st song having most votes
        return None

class PlaylistPlayer:
    def __init__(self):
        # initialize components
        self.library = []  # song library
        self.playlists = {}  # playlists dictionary to store via names
        self.history = deque(maxlen=100)  # recently played songs history
        self.queue = deque()  # next songs queue
        self.party_mode = PartyPlaylist()  # party mode playlist
        self.is_party_mode = False  # for toggling party mode
        self.current_playlist = None  # track the currently playing playlist
        
        # some random songs
        random_songs = [
            ("Chalk Outlines", "Ren", 210),
            ("Blinding Lights", "The Weeknd", 200),
            ("Levitating", "Dua Lipa", 203),
            ("Peaches", "Justin Bieber", 198),
            ("Save Your Tears", "The Weeknd", 215),
            ("Watermelon Sugar", "Harry Styles", 174),
            ("Good 4 U", "Olivia Rodrigo", 178),
            ("dying lately", "iamjakehill", 160),
            ("Gasoline", "Connor Price", 240),
            ("Lucid Dreams", "Juice WRLD", 239),
        ]
        
        for title, artist, duration in random_songs:
            self.library.append(Song(title, artist, duration))
            
    # for adding a new song in library
    def add_to_library(self, title, artist, duration):
        self.library.append(Song(title, artist, duration))
        
    # create new empty playlist
    def create_new_playlist(self, name):
        self.playlists[name] = Playlist()
        
    # for adding a specific song from library to a playlist
    def add_song_to_playlist(self, playlist_name, song_index):
        if playlist_name in self.playlists and 0 <= song_index < len(self.library):
            song = self.library[song_index]  # get song from library by index
            self.playlists[playlist_name].add_song(song.title, song.artist, song.duration)  # instantiate new song in playlist
            
    # for filtering songs by artist
    def filter_songs_by_artist(self, artist):
        return [song for song in self.library if song.artist.lower() == artist.lower()]
    
    # recursive shuffling of song's list
    def shuffle(self, songs, n, result=None):
        if result is None:
            result = []  # base case
        if n == 0 or not songs:
            return result
        song = random.choice(songs)  # randomly pick a song
        result.append(song)
        songs.remove(song)  # remove picked song from original list
        return self.shuffle(songs, n-1, result)
    
    # shuffle a playlist
    def playlist_shuffle(self, playlist_name):
        if playlist_name in self.playlists:  # check if playlist exists
            # collect songs from the playlist
            songs = [] 
            current = self.playlists[playlist_name].head
            while current:
                songs.append(current)
                current = current.next  # move to next song
                
            # shuffle and recreate playlist
            shuffled_songs = self.shuffle(songs, len(songs))
            new_playlist = Playlist()
            for song in shuffled_songs:
                new_playlist.add_song(song.title, song.artist, song.duration)
            self.playlists[playlist_name] = new_playlist     
            
    # display recently played songs    
    def song_history(self):
        return list(self.history)        
            
    # create a queue for next songs to be played
    def create_queue(self, song_index):
        if 0 <= song_index < len(self.library):
            self.queue.append(self.library[song_index])  # add song to queue by index
            
    def voting(self, song_index):
        if 0 <= song_index < len(self.library):
            self.library[song_index].votes += 1  # increment vote count
            if self.is_party_mode:
                self.party_mode.add_song(self.library[song_index])  # add to party mode queue if enabled
            
    def play_next_song(self):
        if self.is_party_mode and self.party_mode.queue:
            song = self.party_mode.get_next()
        elif self.queue:
            song = self.queue.popleft()  # get next song from queue
        elif self.current_playlist and self.playlists[self.current_playlist].get_current_song():
            song = self.playlists[self.current_playlist].next_song()
        else:
            return None  # no song to play
        if song:
            self.history.append(song)  # add to history
        return song 
            
    # toggle party mode   
    def toggle_party_mode(self):
        self.is_party_mode = not self.is_party_mode  # toggle state
        if self.is_party_mode:
            print("Party mode enabled!")
            # recreate party playlist from library
            self.party_mode = PartyPlaylist()
            for song in self.library:
                if song.votes > 0:
                    self.party_mode.add_song(song)
        else:
            print("Party mode disabled!")
            
    # set the current playlist for playing
    def set_current_playlist(self, playlist_name):
        if playlist_name in self.playlists:
            self.current_playlist = playlist_name
            return True
        return False

# main menu for different operations
def main_menu():
    print("1. Add song to library")
    print("2. Create new playlist")
    print("3. Add song to playlist")
    print("4. Filter songs by artist")
    print("5. Shuffle a playlist")
    print("6. View recently played songs")
    print("7. Create next songs queue")
    print("8. Vote for a song (Party Mode)")
    print("9. Play next song")
    print("10. View current song")
    print("11. Play previous song")
    print("12. Toggle Party Mode")
    print("13. View song library")
    print("14. View playlists")
    print("15. Play Songs")
    print("16. Exit")

# Program Loop for Playlist manager
def main():
    play = PlaylistPlayer()  # instantiate playlist player
    while True:
        main_menu()
        command = input("Enter a command (1-16) to proceed: ")
        
        if command == "1":
            # add a new song to library
            title = input("Enter song title: ")
            artist = input("Enter artist name: ")
            duration = int(input("Enter duration in seconds: "))
            play.add_to_library(title, artist, duration)
            print("Successfully added the song to library!")
            
        elif command == "2":
            # create a new playlist
            name = input("Enter a name for the new playlist: ")
            play.create_new_playlist(name)
            print(f"New playlist '{name}' created successfully!")
            
        elif command == "3":
            # add a song to a specific playlist
            name = input("Enter the playlist name: ")
            if name in play.playlists:
                print("Songs available in library:")
                for i, song in enumerate(play.library):  # display library songs with index
                    print(f"{i}. {song.title} by {song.artist}")
                index = int(input("Enter the index of the song to add: "))
                play.add_song_to_playlist(name, index)
                print("Song added to playlist successfully!")
            else:
                print("Playlist not found!")
                
        elif command == "4":
            # filter songs by artists
            artist = input("Enter artist name to filter songs: ")
            filtered_songs = play.filter_songs_by_artist(artist)
            if filtered_songs:
                print(f"Songs by {artist} in the library:")
                for song in filtered_songs:
                    print(f"- {song.title} ({song.duration} sec)")
            else:
                print(f"No songs found by {artist}.")
                
        elif command == "5":
            # shuffle a playlist
            name = input("Enter the playlist name to shuffle: ")
            if name in play.playlists:
                play.playlist_shuffle(name)
                print(f"Playlist {name} shuffled successfully!")
            else:
                print("Playlist not found!")
                
        elif command == "6":
            # view history of recently played songs
            history = play.song_history()
            if history:
                print("Recently played songs:")
                for song in history:
                    print(f"- {song.title} by {song.artist}")
            else:
                print("No songs played recently.")
                
        elif command == "7":
            # create a queue for next songs to be played
            print("Songs available in library:")
            for i, song in enumerate(play.library):  # display library songs with index
                print(f"{i}. {song.title} by {song.artist}")
            index = int(input("Enter the index of the song to add to queue: "))
            play.create_queue(index)
            print("Song added to queue successfully!")
            
        elif command == "8":
            # vote for a song in party mode
            print("Songs available in library:")
            for i, song in enumerate(play.library):  # display library songs with index
                print(f"{i}. {song.title} by {song.artist} (Votes: {song.votes})")
            index = int(input("Enter the index of the song to vote for: "))
            play.voting(index)
            print("Vote registered successfully!")
            
        elif command == "9":
            # play the next song
            song = play.play_next_song()
            if song:
                print(f"Now playing: {song.title} by {song.artist}")
            else:
                print("No song to play.")
                
        elif command == "10":
            # view current song
            playlist_name = input("Enter the playlist name to view current song: ")
            if playlist_name in play.playlists:
                current_song = play.playlists[playlist_name].get_current_song()
                if current_song:
                    print(f"Current song: {current_song.title} by {current_song.artist}")
                else:
                    print("No song is currently playing in this playlist.")
            else:
                print("Playlist not found!")
                
        elif command == "11":
            # play previous song
            playlist_name = input("Enter the playlist name to play previous song: ")
            if playlist_name in play.playlists:
                previous_song = play.playlists[playlist_name].previous_song()
                if previous_song:
                    play.history.append(previous_song)  # add to history
                    print(f"Now playing: {previous_song.title} by {previous_song.artist}")
                else:
                    print("No previous song available in this playlist.")
            else:
                print("Playlist not found!")
                
        elif command == "12":
            # toggle party mode
            play.toggle_party_mode()
            
        elif command == "13":
            # view song library
            print("Songs in library:")
            for song in play.library:
                print(f"- {song.title} by {song.artist} ({song.duration} sec)")
        
        elif command == "14":
            # view playlists
            if play.playlists:
                print("Available playlists:")
                for name, playlist in play.playlists.items():
                    print(f"Playlist: {name}")
                    current = playlist.head
                    while current:
                        print(f"  - {current.title} by {current.artist} ({current.duration} sec)")
                        current = current.next
            else:
                print("No playlists available.")
                
        elif command == "15":
            # play songs from a playlist
            playlist_name = input("Enter the playlist name to play: ")
            if playlist_name in play.playlists:
                if play.set_current_playlist(playlist_name):
                    song = play.playlists[playlist_name].get_current_song()
                    if song:
                        print(f"Now playing: {song.title} by {song.artist}")
                        play.history.append(song)  # add to history
                    else:
                        print("No songs in this playlist.")
                else:
                    print("Failed to set playlist.")
            else:
                print("Playlist not found!")
            
        elif command == "16":
            print("Exiting the playlist manager. Goodbye!")
            break
        
        else:
            print("Invalid command. Please enter a number between 1-16.")
            
if __name__ == "__main__":
    main()