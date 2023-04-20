# greed

A customizable Telegram shop bot that accepts bitcoin payments.
Now With Categories, subcategories and variations.

![](https://img.shields.io/badge/version-beta-blue.svg)

## Requirements, Installation & Usage

Please refer to the [main greed project fork](https://github.com/Steffo99/greed) for requirements, installation guide, and usage instructions before proceeding with the bitcoin setup below

## Integrating Bitcoin

1. Edit the `config/config.toml` file to set the below settings
```[Bitcoin]
# Blockonomics API key
api_key = "BLOCKONOMICS_API_KEY"
secret = "YOUR_SECRET"
```
- *api_key* can be obtained by signing up on [Blockonomics Merchants](https://www.blockonomics.co/merchants#/stores) and navigating to  > [Stores](https://www.blockonomics.co/merchants#/stores), 
- *secret* can be any long phrase of your choice like *GreedBtc9123*

2. Add a new store at [Blockonomics Merchants > Stores](https://www.blockonomics.co/merchants#/stores), and set your Callback URL to `https://www.blockonomics.co/api/test_callback?secret=YOUR_SECRET`, substituting in your chosen secret from step 1 in place of `YOUR_SECRET`

That's it! Restart your bot and start accepting bitcoin payments with your bot!

## Screenshots
![Greed Screenshots](https://user-images.githubusercontent.com/22245433/214773115-59db13a8-93cc-4d12-ab3c-4676e60784a0.png)


## Credits
This project is a fork of [greed project](https://github.com/Steffo99/greed) by @Steffo99. We would like to thank @Steffo99 for putting this in public domain. 
