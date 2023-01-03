# Candidate Assessment bot

Following bot evaluates candidates hard skills by sending custom assessment files using Telegram API and Google Services (Drive, Sheets, Gmail).

## Overview

Test assessment is divided into two parts:

* **Task preparation** → managers fill a google doc with custom tasks (in a shared drive);
* **Assessment** → bot sends prepared docs and saves answered-files in a separate google folder per candidate with all corresponding data (answers, time spent etc);

One of the challenges was to limit candidates freedom in the bot, so candidates shouldn't be able to:

* re-enter and start the test again (if time runs out, for instance);
* reload answers after finishing the test;
* get access to other questions;
* and so on.

Given a department of multiple teams and managers with their custom tasks in a google folder, choosing a particular test to send should be delegated to either managers (assigning in advance) or candidates.

In the original draft bot was sending sections via InlineKeyboardMarkup (buttons) and candidates were free to choose the "assigned" task. While candidates could (accidentally or purposefully) click the wrong section + to limit mentioned above frivolities, the first approach was chosen: managers prepare the tasks and assign them in a google sheet. There a temporary token is generated, giving the candidate a one-time access to take the test, limiting re-entries and cheating :)

Long story short (workflow):

1. Manager fills a new row for candidate in a google sheet: name, email, testing modes (extra excel tasks) and adds link to the main google doc with tasks.
2. Generates access-token. <!-- TODO добавить гифку -->
3. HR sends token and @\<bot_tag\> to candidate.
4. Candidate can call to bot only with the token. After verification, instructions with a "start" button are sent.
5. Clicking "start", candidate receives the files, where answers should be provided.
6. When ready, candidate sends answered files back.
7. Bot:

    * registers spent time;
    * creates a separate google folder for the candidate;
    * sends email notifications to manager;
    * expires token.
