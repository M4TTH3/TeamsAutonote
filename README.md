# TeamsAutonote
Auto-generate a note or a slideshow from any presentation on MS Teams. 
Useful for classes where the slides aren't posted and only shown live OR where it's too hard to keepup with writing notes.

# Processes:
Have a class that takes in a series of images (ensures uniqueness) into either a chat-gpt generated note reading each slide with EasyOCR or simply a slideshow.

# GUI
Host the Teams meet on an alternate browser created with Selenium (requires chromedriver in file) and scrapes the images off the presenter inside the slide.
The record function only records when inside the teams meet and feeds the class which consumes images.
Allows the user to save the file to a user-selected destination as one of the two options mentioned above.

