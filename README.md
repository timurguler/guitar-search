# guitar-search

#### I sent myself automated alerts to find the guitar of my dreams on Craiglist.

I've been looking to upgrade my guitar recently to a [Seagull](https://seagullguitars.com/) or [Eastman](https://www.eastmanguitars.com/acoustic) and figured Craiglist would be a great place to look.

This seemed like a great opportunity for an automation project, and I've uploaded the repo so that anyone else can use the pipeline for their own Craiglist scavenges.

#### Here's how I did it:
1. I checked for an API (there wasn't one).
2. I used the  ``requests`` package to find and scrape pages that matched key search terms (in compliance with Craiglist policy).
3. I compared current results with previously seen results to check for new postings or updates to existing ones.
4. I email myself details and links for new/updated posts using the ``smtplib`` and ``email`` packages, and keep track of the results for future comparisons.
![image](https://user-images.githubusercontent.com/90712577/153920215-fcc28838-50fb-45eb-b56a-5efcfaa5684e.png)

5. I schedule this script daily with Task Scheduler to automate the process.
![image](https://user-images.githubusercontent.com/90712577/153920540-c3c433c6-e9a2-4ead-b486-188327a97b0d.png)

#### Implementation Details (and how to use it yourself):
* There are two main files used to run this procedure, both located in the ``code`` folder: a module of helper functions called ``seagull_functions.py`` and a main script called ``run_search.py`` The ``run_search.py`` is the one which actually executes the procedure. If you run that on a schedule with the right parameters, you'll get results.
* To use it yourself, you'll need to edit the parameters in the .env file to reflect your email(s), passwords, home Craiglist page, and search terms. I'm using the musical instruments search with terms ``seagull`` and ``eastman`` but these can easily be changed to look for any type of item on the site.
![image](https://user-images.githubusercontent.com/90712577/153922038-43a4fa75-3e29-4792-98eb-ff0cbe2c3b4e.png)
* If you want to change the email message format (probably a good idea if you're no longer looking for guitars) you can edit this in the "SEND EMAIL" section of the``run_search.py`` file

#### Potential Future Enhancements (that probably aren't worth the effort):
1. Implementing a more sophisticated filtering of results - this could be done by adding filter terms for the body of the Craiglist message, or by using NLP to extract insights in a more automated way. This didn't make sense for my use case since there were so few results to begin with, but could be useful for more common items.
2. Location detection - my current implementation uses a manually-inputted variable for the Craigslist site location. If I wanted to, I could implement a procedure which could identify my computer's current location and find Craiglist sites within an $x$ mile radius. This would be a non-trivial undertaking for a trivial payoff, so I opted out.
3. Automated outreach to posters - this might make things a bit more convenient but definitely crosses an ethical boundary, so I'll be writing my outreach messages myself.
