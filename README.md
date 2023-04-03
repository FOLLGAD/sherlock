# Sherlock - Your AI Home Assistant Chatbot 🕵🏻‍♂️⚡️

Sherlock is an open-source AI chatbot designed to automate tasks in your home using the power of GPT-3.5 by OpenAI. By interacting with Home Assistant through the Home Assistant REST API, Sherlock can control various smart home devices, execute bash commands, and even transcribe voice commands. The chatbot is accessible through Telegram and can perform online searches using the Google Search Serper API.

<img width="514" alt="Sherlock" src="https://user-images.githubusercontent.com/1856197/229633885-aae585a9-1e5b-4225-83a8-c31a09d57b2a.png">

It can control specific devices without any hardcoding of `entity_ids` etc. It will match the user's query with the available entities on the network, and decide for itself which entity it thinks you mean. For example "turn of the living room lights" might turn off an entity called "light.big_living_room"

## Table of Contents

1. Features
2. Installation
3. Configuration
4. Usage
5. Contributing
6. License

## Features

- Control smart home devices using Home Assistant REST API
- Play/queue songs using media players connected to Home Assistant
- Execute bash commands
- Transcribe voice commands using OpenAI Whisper
- Interact with Sherlock through Telegram
- Perform Google searches using the Google Search Serper API

## Installation

1. Clone the repository:

```bash
$ git clone https://github.com/your_username/sherlock.git
```

2. Change to the cloned directory:

```bash
$ cd sherlock
```

3. Install the required dependencies:

```bash
$ pip install -r requirements.txt
```

## Configuration

1. Rename example.env to .env and fill in details:

2. Fill in the required details in .env, including your OpenAI API key, Home Assistant URL and API key, Telegram bot token, and Google Search Serper API key.

## Usage

### CLI Usage

If you want to try it out without Telegram, you can use the command-line interface.

1. Start the Sherlock chatbot as a command-line application:

```bash
$ python sherlock.py
```

2. Start interacting with Sherlock by sending text.

### Telegram bot usage

1. Create a bot using the Telegram BotFather and get relevant keys etc.

2. Start Sherlock as a Telegram bot:

```bash
$ python telegram-bot.py
```

3. Open your Telegram app and search for your bot using the bot's username.

4. Start interacting with Sherlock by sending text or voice commands.

Examples:

- Turn on the living room light.
- Set the thermostat to 72°F.
- Search for the best smart home security systems.
- Play Bladee on spotify.

## Contributing

We welcome contributions to help improve Sherlock and make it more accessible to everyone. To contribute, please follow these steps:

- Fork the repository.
- Create a new branch with a descriptive name.
- Make your changes and commit them.
- Open a pull request with a detailed description of your changes.

## License

Sherlock is released under the MIT License.
