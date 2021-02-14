## Touch Portal - YouTube Music Desktop Plugin
This is an integration for [TouchPortal](https://www.touch-portal.com/) that enables control of the [Youtube Music Desktop app](https://ytmdesktop.app) such as
- Toggle Play button
- Skip a current song
- Go to the Previous song
- Seek forward & backward
- Show lyrics
- Like & Dislike the current song
- Add to library
- Add to Playlist
- Volume up and down
and a lot more! Below is an example of what it can do! Image & Page credit goes to [Arbi_ph](arbibarbarona@gmail.com)  on [TouchPortal Discord](https://discord.gg/MgxQb8r).

![Tab-YTMD](https://user-images.githubusercontent.com/55416314/107865596-001dec00-6e1d-11eb-8896-07fd6ee6ad9a.png)

## How to Install
1. Download the .tpp file in release page.
2. Make sure that you have the YTMDesktop app installed or else this plugin will not work.
3. Open TouchPortal and click import Plugins then pick the file that you downloaded it should tell you Plugin has successfully installed.
4. Next, fully close TouchPortal, and on Windows Start Panel, type run or press `Windows+R` and enter `%appdata%\TouchPortal\plugins\TouchPortalYTMusic`<br>
  On mac it should be in Documents folder > TouchPortal > plugins > TouchPortalYTMusic.
5. Open the **Login.json** with any text editor you have.
6. Go to the YTMDesktop app and click Settings > Integrations and enable Remote control and you can have either Protect remote control with password enable or disable.
    If it is disabled you can skip step 7.
7. If Protect remote control with a password is enabled you should able to see something like "XXXXX" in the **Login.json** file that you have opened, replace XXXXX with yours, or else Action will NOT WORK.
8. Save the file that you've edited it should look something like this `{"Password": "MWA5Q"}`<br>
  **AND DO NOT CHANGE ANYTHING ELSE OR ELSE IT WILL NOT WORK.**<br>
  Just save it with "XXXXX" replaced with your own code found in your YTMDesktop app under Settings/Integration.
9. Now you have everything set up, you should be able to reopen TouchPortal and you can click any button and should see a new Category that says "YouTube Music".<br>
  If you don't that means you did something wrong. If you did right you should be good to go.

# Q&A
## I can't follow the guide, What should I do?
You can go to [TouchPortal Discord](https://discord.gg/MgxQb8r) and contact [! xXKiller_BOSSXx#5232](https://discord.com/users/526656592481878026) in the `#ytmd` channel

## When will you update this again?
I will be updating this Plugin only if there's an issue or a new action or State that users suggested, or YTMDesktop app has updated its functions

## Where can I join YTM Desktop Discord or TouchPortal Discord?
[YTM Desktop Discord](https://discord.gg/jEdRHKg7bG) and [TouchPortal Discord](https://discord.gg/MgxQb8r)
