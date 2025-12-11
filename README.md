# Housing

## What is this?
A scraper helping poor people looking for accomodation in The Netherlands. If you never lived there, you can't understand. Checks common housing websites and automatically replies to new listings. Based on [Playwright](https://playwright.dev/)

## Note
This tool doesn't do miracles. Don't expect to find an accomodation quickly just because you use this: you still have to go to viewings, make a good impression to landlords, be able to provide the guarantees they ask for and so on. 

## Disclamer
The code provided in this repository is only meant as an example of what can be accomplished with Playwright. It is your sole responsibility to make sure that you comply with the terms of service of the websites you scrape and with any applicable laws. I decline any responsibility for the use of this tool.

## Deploy
First of all, put your personalized messages inside the files under the `Resources` directory.   
Then, create a `.env` file based on `.env.example`.  
With some websites, filling in username and password with Playwright will not work. In that case, you can use `playwritght codegen` to interactively login and then [save the storage](https://playwright.dev/python/docs/codegen#preserve-authenticated-state) containing the authentication cookie. You can then load it from code, thus creating an authenticated session.  
Would you like to run this tool at specific time intervals, but you don't know where to host it? Have a look at [Oracle Cloud Free Tier](https://www.oracle.com/cloud/free/).

### Using Docker
`$ docker build -t housing -f Install/Dockerfile .`  
Create and start the container  
`$ docker run -d --name housing housing`  
To run it at specific time intervals, Review the files `housing-docker.service`and `housing-docker.timer` inside the `Install` directory, and modify them based on your needs.
Copy (or create links) the unit and timer to `/etc/systemd/system/`. Then enable and start the timer  
`$ sudo systemctl enable housing-docker.timer && sudo systemctl start housing-docker.timer`  
Check with  
`$ systemctl list-timers`


### Bare metal
Create a Python virtual enviroment and install the requirements from `requirements.txt`. Then, activate it and run `playwright install`. See ![Playwright's installation instructions](https://playwright.dev/python/docs/intro) for more information.  
Review the files `housing.service`and `housing.timer` inside the `Install` directory, and modify them based on your needs.
Copy (or create links) the unit and timer to `/etc/systemd/system/`. Then enable and start the timer  
`$ sudo systemctl enable housing.timer && sudo systemctl start housing.timer`  
Check with  
`$ systemctl list-timers`

### Note
Websites change frequently, therefore be ready to have to modify the code to make it work. If you do so, consider opening a pull request to help others.

## License
This code is released under the GPLv2 license.