<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/Ti1mmy/CheckinWithme">
    <img src="resource/logo.png" alt="Logo" width="300" height="400">
  </a>

  <h3 align="center">CheckinWithme</h3>

  <h4 align="center"><a href="top.gg" target="_blank">» Invite me!</a></h4>

  <p align="center">
    An AI mood-tracking Discord bot powered by
    <br /> <a href="https://www.datastax.com/products/datastax-astra">DataStax Astra's Apache Cassandra Databases</a> | <a href="https://www.linode.com/">Linode Cloud</a> | <a href="https://cloud.google.com/">Google Cloud</a> | <a href="https://www.domain.com/">Domain.com</a> | <a href="https://www.ibm.com/watson/services/tone-analyzer/">IBM Watson Tone Analyzer</a>
    <br />
    <br />
    <a href="https://github.com/Ti1mmy/CheckinWithme/blob/main/README.md"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/Ti1mmy/CheckinWithme">View Demo</a>
    ·
    <a href="https://github.com/Ti1mmy/CheckinWithme/issues">Report Bug</a>
    ·
    <a href="https://github.com/Ti1mmy/CheckinWithme/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Introduction](resource/introduction.png)](https://checkinwithme.tech)

[![Check-In](resource/check-in-pip.png)](https://checkinwithme.tech)

Here's a blank template to get started:
**To avoid retyping too much info. Do a search and replace with your text editor for the following:**
`github_username`, `repo_name`, `twitter_handle`, `email`, `project_title`, `project_description`


### Built With

* [DataStax Astra Database](https://www.datastax.com/products/datastax-astra)
* Hosted on [Linode](https://www.linode.com/)
* [Google Cloud Translation/Natural Language Apis](https://cloud.google.com/)
* [IBM Watson Tone Analyzer](https://www.ibm.com/watson/services/tone-analyzer/)



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* Python `3.9`, `pip3`

1. Update before installing new packages

   ```sh
   sudo apt-get update
   ```
2. Check Python version

   ```sh
   python3 --version
   ```
3. If Python version < `3.9`

   ```sh
   sudo apt install python3.9
   ```
4. Validate

   ```sh
   python3.9 --version
   ```
5. Install `pip3`

   ```sh
   sudo apt-get -y install python3-pip
   ```
6. Validate

   ```sh
   pip3 --version
   ```


### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/Ti1mmy/CheckinWithme.git
   ```
2. Install Prerequisite Libraries
   ```sh
   pip install -r requirements.txt
   ```
3. Configure [DataStaxAstra Database](https://astra.datastax.com/)
    * Initialize CQL Database with keyspace `my_moods`
    * Click on **Connect** in the initialized database. Download and add `secure-connect-database-name.zip` to main directory.
4. Configure [Google Cloud Services](https://cloud.google.com/)
    * Create Service Account with `owner` role
    * Enable [Cloud Translation API](https://console.cloud.google.com/marketplace/product/google/translate.googleapis.com)
    * Enable [Cloud Natural Language API](https://console.cloud.google.com/marketplace/product/google/language.googleapis.com)
5. Add tokens to `config/config.json`
    * Bot tokens for Discord can be found in the [Discord Developer Portal](https://discord.com/developers/docs/intro). 
    * Copy [tokens](https://astra.datastax.com/settings/tokens) from DataStax Astra Database into `config/config.json`
    * Download Google Cloud [Key JSON](https://console.cloud.google.com/apis/credentials/) to `/config/`
    * Include path to Google Cloud JSON in `config.json`
    
   
   
   ```json
   {
   "_Discord Bot": "Import Bot Tokens below if applicable",
   "token": "",
   "token_test": "",

   "_DataStacks Astra Keys_": "Import your DataStax Astra Keys below",
   "secure_connect_bundle": "<PATH-TO-SECURE-CONNECT-BUNDLE.zip>",
   "CLIENT_ID": "",
   "CLIENT_SECRET":"",

   "G_CLOUD_SERVICE_KEYFILE": "config/your-google-cloud-service-keyfile.json",
   }
   ```
6. Add tokens for Reddit and IBM Watson Tone Analysis to `config/reddit_keys.json`, `config/watson.json`
    * Create an application using a Reddit account [here](https://www.reddit.com/prefs/apps) to find the required tokens
    * Create an IBM Watson Tone Analyzer instance [here](https://cloud.ibm.com/catalog/services/tone-analyzer) and import the API key and url
   

   ```json
   // reddit_keys.json
   {
   "_Reddit": "Import Application Tokens Below:",
   "personal_use": "",
   "secret": ""
   }

   // watson.json
   {
   "Watson Tone Recognition AI": "Import API key and URL below:",
   "API_key": "",
   "url": ""
   }
   ```


<!-- USAGE EXAMPLES -->
## Usage

#### Joining
When Pip joins your server, it will create a read-only channel called `#daily-check-in`. Every 24 hours, Pip will make an announcment reminding you to message it with a quick message on how your day is going so far.
#### Check-In
Whenever you feel like logging how you feel, you can save an entry by messaging Pip using the `>checkin` command! Type out your message after the `>checkin` command for Pip to analyze and log how you feel. 
  * If you feel more comfortable expressing how you feel in your own language, Pip is completely able to understand your language as well as responding back using the **same language**!
  * Pip logs your emotions throughout the day! You can let Pip know how you are feeling at any time, not just once per day!
    * e.g. `>checkin Things have been going my way recently, I am grateful for my luck!`
    * par ex. `>checkin Les choses vont dans mon sens ces derniers temps, je suis reconnaissant pour ma chance!`
   
#### History
Pip logs how you are feeling whenever you check in with it! You can view how you felt over the past seven days by viewing your `>history`!

![History](resource/history_example.png)

#### Miscellaneous
  Rate: 
  * You can also let Pip know how you are feeling with the '`>rate`' command! Please include one of the following: `| Anger | Fear | Joy | Sadness |` with the command. This provides a more direct and accurate method for our systems to track your mood.
    * For instance, you could type `>rate Sadness` to let Pip know you're feeling down at the moment.
 
  Motivation:
  * Sends motivational messages to cheer you on to bigger and better.

  Resource
  * Generates a random resource to help you develop your mental health!

<!-- ROADMAP -->
## Roadmap

Optimizations:
  * Replace long if-else trees with native switch-statements upon Python `3.10` release.
  * Move embeds from `bot.py` to a seperate file.

Features:
  * Voice Recognition in `>checkin`
    * Analyses .audio files that users record and send to bot
  * Interactive Web UI to explore mood history in more depth
  * Streak-detection
    * Identifies streaks in good moods and compliments users
  * Thoughts/Graditude Journal Support
    * Stores & Analyzes Journals, easily accessible on future Web UI
  * Chatbot feature
    * Allows users to casually converse with the b



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.


<!-- CONTACT -->
## Contact

Eric Ji - [Linkedin](https://www.linkedin.com/in/eric-ji-0a8793212/) - eric868.ji@gmail.com

Katherine Li [Linkedin](https://www.linkedin.com/in/k-atherine-li/) - katherineli03.kkl@gmail.com

Timothy Zheng - [Linkedin](https://www.linkedin.com/in/timothy-zheng21/) - tim123643@gmail.com

Yang Xu - [Linkedin](https://www.linkedin.com/in/yang-xu-584b0920b/) - boyangfu1991@gmail.com


Devpost Link: [https://github.com/Ti1mmy/CheckinWithme](https://github.com/Ti1mmy/CheckinWithme)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* Pip's avatar from [Canva](https://www.canva.com/), use granted through Pro subscription
* [MLH Mental Health Hacks](https://organize.mlh.io/participants/events/6797-mental-health-hacks)
* [Google Cloud Credits from Google](https://cloud.google.com/)
* [Linode Credits from Linode](https://www.linode.com/)
* [DataStax Astra Credits by DataStax Astra](https://www.datastax.com/products/datastax-astra)

