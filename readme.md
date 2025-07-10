# Webcrawler Instructions

## How To Use
1. Create a **.env** file (can copy from .env-template for starters). Modify to your liking.
2. Review **app/settings.py** for any variables you'd like to alter from defaults. Put those variables in an 
   **app/environment.yml** file. Suggestions as follows:
   1. Add/Remove "desired searches" from the SEARCH_TERMS list.
   2. Add/Remove "desired URLs" from the CRAWL_URLS (Note: these need to have full protocol and domain to work.)
   3. Change SEARCH_DEPTH, LINKS_MAX_PER_PAGE, SLEEP_MAX, and SLEEP_MIN values. (Note: Be VERY conservative here. Going too 
      deep, with too many links per page with either too long or too short of a sleep will cause issues. Either your 
      queries will be blocked OR it will take FOREVER to crawl through all the results.)
   4. Add any domains you wish to avoid in the EXCLUDED_DOMAINS list. (Don't quote me but I think this will work as a 
      substring search so `google` will exclude ANY domain with that term in its hostname.)
   5. Add users to USERS.
   6. Set different DEFAULT_PASSWORD (so that the USERS don't need to duplicate the same password over and over.)
3. Run `./runme.sh` to load Docker container and execute the searches.
4. Review the `docker-compose logs -f` output to ensure it is doing what you'd like.

## Alternative Usage
Technically you can run the script natively (if on Linux... I haven't tried this on other OSes).
1. `pip install playwright`
2. `playwright install --with-deps`
3. `cd app`
4. `python3 bootstrap.py`
   >If you'd like to run non-headless add **HEADLESS: False** to the **app/environment.yml** file.

## Starting and Stopping
You can use crontab to start and stop the containers on a schedule to simulate humans working in an office.
 * Call the dc-action.sh script to give docker-compose commands 
 * Configure crontab (and maybe install it too) to call start and stop the containers

### EXAMPLE

> 30 23 \* \* 1-5 /home/ec2-user/sdc-traffic-generator/dc-action.sh stop webcrawler1
>
> 30 15 \* \* 1-5 /home/ec2-user/sdc-traffic-generator/dc-action.sh start webcrawler1

## Build Playwright Image
This repository has 2 *things* in it:

1. The contents of **playwright_build** are for building the base Docker image that will be called in the 
   **./Dockerfile**.
2. The toplevel is the webcrawler build. (Eventually I'll move the playwright_build out onto its own repo.)

## Building a new base image
1. `cd playwright_build`
2. Modify what you need.
3. `docker build --platform linux/amd64 -t playwright .`
4. `docker login`
5. `docker tag playwright:latest dmickels/playwright:latest`
6. `docker tag playwright:latest dmickels/playwright:YYYYMMDD`
7. `docker push dmickels/playwright:YYYYMMDD`
8. `docker push dmickels/playwright:latest`
