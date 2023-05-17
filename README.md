# TeamsAutonote
Auto-generate a note or a slideshow from any presentation on MS Teams. 
Useful for classes where the slides aren't posted and only shown live OR where it's too hard to keepup with writing notes.

# Processes
Have a class that takes in a series of images (ensures uniqueness) into either a chat-gpt generated note reading each slide with EasyOCR or simply a slideshow.

# GUI
Host the Teams meet on an alternate browser created with Selenium (requires chromedriver in file) and scrapes the images off the presenter inside the slide.
The record function only records when inside the teams meet and feeds the class which consumes images.
Allows the user to save the file to a user-selected destination as one of the two options mentioned above.

1. User types in address or defaults to Google.ca <br />
![image](https://github.com/M4TTH3/TeamsAutonote/assets/61128748/3e5dbc60-d25d-48d3-a69c-cedc10035273)

2. Hit record and/or stop whenever. <br />
![image](https://github.com/M4TTH3/TeamsAutonote/assets/61128748/c35bf16e-8709-4f26-a5e3-c283ee91b97e)

3. Save the file (Prompts file explorer) <br />
![image](https://github.com/M4TTH3/TeamsAutonote/assets/61128748/8b44857e-1262-4238-9bca-43417094a55c)



# Example
A given slideshow (Shows one slide):
![image](https://github.com/M4TTH3/TeamsAutonote/assets/61128748/aa99e1c2-cb78-4c2f-98da-41ad5fe0a3d4)

A following output:
![image](https://github.com/M4TTH3/TeamsAutonote/assets/61128748/905f6f5a-baf1-4a57-bb73-686901bbd533)
