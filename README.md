# Cocogoat Assistant 🥥 🌴
Hi! You can just call me Cocogoat. I'm an assistant with tools and scripts to assist in the Genshin Impact grind. As per our contract.˚ ༘♡ ⋆｡˚

## Current Abilities:
- I can automatically check-in to the Hoyolab website and collect rewards for you at a random time each day. This can either be ran in the background locally or by using a GitHub workflow.

## Setup:
**Option 1** (more complex, challenging, but more automated):<br>
    1. Fork the repo.<br>
    2. You will need to see the data of the post request and save the cookies that are sent when you click check-in on the sign in page: https://act.hoyolab.com/ys/event/signin-sea-v3/index.html?act_id=e202102251931481<br>
    <br>
        - How can I do that?<br>
        In Firefox, go to the checkin page linked above. Make sure you are logged in. Do not click the check-in button yet!<br>
        Hit Ctrl + Shift + E to open the Network tab.<br>
        Watch the tab, you should be able to see some requests already. Click the check-in button and watch for a POST request to appear. There's multiple, so you might have to try different POST ones to get your cookies :) Find the cookies tab. This will have all of the values you need.<br>
        Chrome: same as Firefox but use Ctrl + Shift + I and select the Network tab.<br>
        <br>
    3. Save these values:<br>
        LTUID<br>
        LTOKEN<br>
        ACCOUNTID<br>
        ACCOUNT_ID_V2<br>
        ACCOUNT_MID_V2<br>
        COOKIE_TOKEN_V2<br>
        <br>
    4. Add these as stored secrets to the newly forked repo. Make sure to follow the secret names **exactly** (all caps) and for the value, post the plain text without any quotations.
    <br>
    <br>
    5. Set the GitHub workflow to run randomly every 24 hours.
    <br>


**Option 2** (easier):<br>
Clone or download the repo locally and run main.py manually. Before you do this, update config.json with the browser
that you normally use to login to Hoyolab and set "use_workflow" to "false". The current browsers supported are: Chrome, Firefox, Opera, Edge, Chromium, Brave, and Vivaldi. If you use something other than that, I would recommend using Option 1.

## What I Want to Learn:
- Fishing in Teyvat
- Cooking delicious food to keep up team morale ( ˘▽˘)っ🍜
- Calculate resin regeneration
- Tracking weapon and character ascension materials
- Keep track of wishes and calculate your current pity

## Feedback:
Please feel free to open an issue if you think there is an area I can improve upon. I remember reading in an ancient text that "Only when days be darker than the darkest night, may a qilin be compelled to fight." That's a massive exaggeration... But should the time come for battle, and should you need me, then I will give it every ounce of my strength. 💪(=⌒‿‿⌒=)
