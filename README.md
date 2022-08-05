<div id="top"></div>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/github_username/repo_name">
    <img src="data/logo.png" alt="Logo" width="192" height="70">
  </a>

<h3 align="center">Jable.tv Python Scraper</h3>

  <p align="center">
    An awesome web scraper powered by CloudScraper to collect video data from jable.tv
    <br />
    <a href="https://github.com/github_username/repo_name"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/github_username/repo_name">View Demo</a>
    ·
    <a href="https://github.com/github_username/repo_name/issues">Report Bug</a>
    ·
    <a href="https://github.com/github_username/repo_name/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
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
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

<!-- [![Product Name Screen Shot][product-screenshot]](https://example.com) -->

Here's a blank template to get started: To avoid retyping too much info. Do a search and replace with your text editor for the following: `github_username`, `repo_name`, `twitter_handle`, `linkedin_username`, `email`, `email_client`, `project_title`, `project_description`

<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

* [Python3](https://python.org/)
* [TinyDB](https://tinydb.readthedocs.io/en/latest/)
* [CloudScraper](https://github.com/VeNoMouS/cloudscraper)
* [Docker](https://docker.com/)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

Docker is required.

### Setup

1. Make sure `Docker` is installed in your machine.
2. Clone the repo.
   ```sh
   git clone https://github.com/noodleslove/jable_py.git
   ```
3. Setup personal `credentials` for gmail account, and `recipients` for email 
   notification.
   Create `secrets.py` in app directory.
   ```sh
   touch jable_py/app/secrets.py
   ```
   Setup following variables to make the application work.
   ```python
   email = {sender-email}
   app_pw = {gmail-app-password}
   recipients = {list-of-recipients}
   ```
4. Open up a terminal and run the following command start up your application.
   ```sh
   docker compose up
   ```
5. If you want to run your services in the background, you can run the
   following command instead.
   ```sh
   docker compose up -d
   ```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [x] Jable.tv webscraping
- [x] Email automation
- [x] Database storage
- [x] Model list personalization
  - [x] Add model to database
  - [x] Remove model from database
- [x] Command line arugements
  - [x] Fetch
  - [x] Send email
  - [x] Add model
  - [x] Remove model
  - [x] List all models
- [x] Dockerize the repository
  - [x] Dockerfile
  - [x] docker compose file
  - [x] docker ignore file
- [ ] Personalized email time
  - [ ] Nested Feature

See the [open issues](https://github.com/noodleslove/jable-py/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Eddie Ho - [@doublemay33](https://twitter.com/doublemay33) - edwin.ho.bj@gmail.com

Project Link: [https://github.com/noodleslove/jable-py](https://github.com/noodleslove/jable-py)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Video source website](https://jable.tv)
* []()
* []()

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/noodleslove/jable_py.svg?style=for-the-badge
[contributors-url]: https://github.com/noodleslove/jable_py/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/noodleslove/jable_py.svg?style=for-the-badge
[forks-url]: https://github.com/noodleslove/jable_py/network/members
[stars-shield]: https://img.shields.io/github/stars/noodleslove/jable_py.svg?style=for-the-badge
[stars-url]: https://github.com/noodleslove/jable_py/stargazers
[issues-shield]: https://img.shields.io/github/issues/noodleslove/jable_py.svg?style=for-the-badge
[issues-url]: https://github.com/noodleslove/jable_py/issues
[license-shield]: https://img.shields.io/github/license/noodleslove/jable_py.svg?style=for-the-badge
[license-url]: https://github.com/noodleslove/jable_py/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png
