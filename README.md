# Secret Santa

## Table of Contents

- [Project Overview](#project-overview)
- [Core Functionality](#core-functionality)
- [Gmail](#gmail)
- [SMTP Relay](#smtp-relay)
- [Getting Started](#getting-started)
- [Pre-Requisites](#prerequisites)
- [Installation](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Project Overview

Every year my friends and I do a secret santa. For the past couple of years I've written a janky python script that handles it using gmail's SMTP offering.

This year I decided to spruce it up a bit and get a custom domain & use an SMTP relay service. 

Both scripts have been included here, and I'll walk through how both work. 

## Core Functionality

The way the core functionality works for both scripts is:
1. Read in JSON data of each participant's name & email
- I also include an 'exclude' list, so that if descired people in relationships won't get each other (since they're probably already getting each other gifts)

2. Make a list of potential pairings

3. Check if that pairing is valid
- if not, try again
- there's definitely a more clever way to do this, but the problem space is small enough we can just brute force a valid pairing

4. Iterate through each pairing an email the 'gifter' who their 'giftee' is

![script main function](/images/core.png)


## Gmail
Gmail lets you use their SMTP server to send emails from your own email for free.
- all you have to do is supply your creds
- there may be some account permissions you need to allow

Fair warning if you want to customize the message further: SMTP formatting is pretty gross, but I wrangled it to send the following

![Gmail Message](/images/gmail.png)

If you want to see how that part works, check out [SMTP python stuff](santa_gmail.py#55)

Pretty bare bones, but again, it's **free**

There's a few different ways to set up your account to allow SMTP authentication. I used something called an app password, which you can use as the SMTP password (the username being your gmail address). There's some other API based options I saw but haven't looke dinto

![app password](/images/app_password.png)

## SMTP Relay
Ok so now onto the prettier one.

SMTP relays are a service that will forward your message along via their SMTP servers for a free.
- [Mailgun](https://www.mailgun.com/) is a great SMTP relay service that supports custom domains
    - they also have a killer 30 day free trial for 5,000 emails 
    - (**WARNING** does require cred card details)

If you want to go this route you'll probably also want to grab a cheap domain
- I bought the-north-pole.lol for $1.98
- You can also use the built in domains, but they're not nearly as fun sounding

You'll need to add some SPF and DKIM records inside of your domain's settings
- you'll do this from your domain registrar's domain management page

Mailgun has some fantastic documentation for [sending via API](https://documentation.mailgun.com/en/latest/user_manual.html#sending-via-api) with support for multiple languages

- They also support base SMTP if you want to do it that way too

## Getting Started
To use, just clone. 

If you're going the gmail route, it'll ask for your credentials on running

If you're going the smtp relay route, you can set environment variables for your domain and API token:
```
export API_TOKEN=<API TOKEN>
export DOMAIN=DOMAIN` ex. `the-north-pole.lol
```
If not set, you'll be prompted for them as well

### Prerequisites
You'll need to have gmail SMTP or Mailgun/a domain set up

### Installation

1. Clone this repo with: `git clone git@github.com:rob0tster/secret-santa.git`
2. Run the respective python script `python santa_gmail.py` or `python santa_mailgun.py`

## Contributing

I'm all for contributions, but as of now at least these are some little scripts I use for some holiday fun :-)


## License 
This project is licensed under the [MIT License](LICENSE.md) - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgements
- Credit to [Mailgun](https://mailgun.com), really great service and product
- Credit to [gmail](gmail.com) for supporting SMTP



