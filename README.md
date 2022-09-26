![demopic](https://user-images.githubusercontent.com/38849824/160300853-ef6fe753-36d6-41a9-9bd2-8a06f7add71d.png)

![](https://img.shields.io/github/license/robswc/tradingview-webhooks-bot?style=for-the-badge)
![](https://img.shields.io/github/repo-size/robswc/tradingview-webhooks-bot?style=for-the-badge)
![](https://img.shields.io/github/commit-activity/y/robswc/tradingview-webhooks-bot?style=for-the-badge)
![](https://img.shields.io/twitter/follow/robswc?style=for-the-badge)




# The What

Tradingview-webhooks-bot (TVWB) is a small, Python-based framework that allows you to extend or implement your own logic
using data from [Tradingview's webhooks](https://www.tradingview.com/support/solutions/43000529348-about-webhooks/).

# The How

TVWB is fundamentally a set of components with a webapp serving as the GUI. TVWB was built with event-driven architecture in mind that provides you with the building blocks to extend or implement your own custom logic.
TVWB uses [Flask](https://flask.palletsprojects.com/en/2.2.x/) to handle the webhooks and provides you with a simple API to interact with the data.

# Quickstart

* Installation
* Serving the App

**Ensure you're in the `src` directory.**

### Creating an action

```bash
python3 tvwb.py action:create NewAction --register
```

This creates an action and automatically registers it with the app.  [Learn more on registering here](https://github.com/robswc/tradingview-webhooks-bot/wiki/Registering).

_Note, action and event names should **_always_** be in PascalCase._

### Linking an action to an event

```bash
python3 tvwb.py action:link NewAction WebhookReceived
```

This links an action to the `WebhookReceived` event.  The `WebhookReceived` event is fired when a webhook is received by the app and is currently the only default event.

### Editing an action

Navigate to `src/components/actions/NewAction.py` and edit the `run` method.  You will see something similar to the following code.
Feel free to delete the "Custom run method" comment and replace it with your own logic.  Below is an example of how you can access
the webhook data.

```python
class NewAction(Action):
    def __init__(self):
        super().__init__()

    def run(self, *args, **kwargs):
        super().run(*args, **kwargs)  # this is required
        """
        Custom run method. Add your custom logic here.
        """
        data = self.validate_data()  # always get data from webhook by calling this method!
        print('Data from webhook:', data)
```

### Running the app

```bash
python3 tvwb.py start
```