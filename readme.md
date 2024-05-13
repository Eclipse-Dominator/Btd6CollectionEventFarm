The script is a macro that automatically clicks on the expert map that has bonus collection rewards.

To adjust for future events, you can change your window resolution to 1280x720 and screenshot the bonus reward icon like below:

![image](./asset/bonus_reward.png)

While the script supports multiple window resolutions as long as it is 16:9.
The recorded macro is done in a game window size of 1280x720. No testing was done to see if the coordinates maps accurately to other 16:9 resolutions.

To run the script:
```
python3 ./app.py
```

The keylog_replay file can also function as a custom way to replay macros that one has customly recorded.

You can run a recorded gameplay by running `keylogger.py`. Pressing `L Alt` will begin the recording and `Esc` will terminate the session. 

Afterwards, you should run `utils.py` to get the dimension of your btd6 window and prepend the output to the top of your keylog.