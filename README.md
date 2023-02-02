# Candidate Assessment Bot

Following bot evaluates candidates hard skills by sending custom assessment files using Telegram API and Google Services (Drive, Sheets, Gmail).
<!-- ТУТ НУЖНА KILLER ГИФКА, КАК ЭТО РАБОТАЕТ-->

## Overview

Test assessment is divided into two parts:

* **Task preparation** → managers fill a google doc with custom tasks (in a shared drive);
* **Assessment** → bot sends prepared docs and saves answered-files in a separate google folder per candidate with all corresponding data (answers, time spent etc);

One of the challenges was to limit candidates freedom in the bot, so candidates shouldn't be able to:

* re-enter and start the test again (if time runs out, for instance);
* reload answers after finishing the test;
* get access to other questions and so on.

Which raised another issue: how to design the process of task choosing? In the original approach bot had a menu-like architecture, where candidate could choose a section, then fall down deeper (inner modules) and finally get to assigned tasks. Given a department of multiple teams and managers with their custom tasks, menu-like model was promising.

But in this case candidates could (accidentally or purposefully) click (and access) wrong tasks. To address mentioned above frivolities, the "password" approach was chosen: managers prepare the tasks and _assign_ to candidates specific tests (so there is no possibility of misclicks and wrong access from users). After task preparation, a temporary token is generated, giving the candidate a one-time access to take the test, which automatically limits re-entries and any other forms of cheating :)

Long story short general workflow looks like this:

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

<!-- ## Install -->
<!-- excel и прочее в setup + про пароль в  пассворд и весь credentials-->