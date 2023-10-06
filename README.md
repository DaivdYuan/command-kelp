<img src="./resources/icon.png" align="right" width="150px"/>

# Command-Kelp: Natural Language Command Line Helper

Command-Kelp is a command-line tool designed to simplify your interaction with the command line by using natural language commands. It provides three main functions to enhance your command-line experience: generating commands from descriptions, correcting previous commands, and offering an interactive menu for executing, explaining, and copying commands.

## Table of Contents

- [Command-Kelp: Natural Language Command Line Helper](#command-kelp-natural-language-command-line-helper)
  - [Table of Contents](#table-of-contents)
  - [Quick Start](#quick-start)
  - [Installation](#installation)
  - [Usage](#usage)
    - [General](#general)
    - [Generating Commands](#generating-commands)
    - [Correcting Commands](#correcting-commands)
    - [Interactive Command Menu](#interactive-command-menu)
  - [Contributing](#contributing)

## Quick Start

To correct the previous command:
```bash
$ kelp 
```

To generate a command from a description:
```bash
$ kelp <your instructions here>
```
More examples in the [Usage](#usage) section.

## Installation

To install Command-Kelp, you need to have Python 3.x and `pip` installed. Run the following command:

```bash
$ git clone git@github.com:DaivdYuan/command-kelp.git
$ cd command-kelp && pip install .
```

Run `kelp` for the first time to auto-configure Command-Kelp.

To use Command-Kelp, you need to set the environment variable `OPENAI_API_KEY` to your OpenAI API key. You can find your API key [here](https://beta.openai.com/account/api-keys). 

To use the automatic api key configuration, just run kelp again:
```bash
$ kelp
```

Alternatively, you can set the environment variable manually, preferably in your `.bashrc` or `.zshrc` file:
```bash
export OPENAI_API_KEY="your_api_key"
```

## Usage

### General

```bash
$ kelp [options] [description]
```

### Generating Commands

You can use the `kelp` command along with a description to generate a corresponding command. Simply provide a brief description of what you want to achieve, and Command-Kelp will suggest the appropriate command.

```bash
$ kelp remove the latest commit in git

> git reset --hard HEAD~1
```


```bash
$ kelp compress ./data into a tar.gz file

> tar -czvf data.tar.gz ./data 
```

### Correcting Commands

Similar to the well-known `thefuck` package, Command-Kelp can correct your previous command if you mistype it or make a syntax error. Just type `kelp` or `kelp fuck`, and Command-Kelp will attempt to correct the previous command.

```bash
# WRONG command
$ df-h
command not found: df-h

# corrected
$ kelp
> df -h

```

```bash
# WRONG command
$  npm create app react --typescript
npm ERR! could not determine executable to run

# corrected
$ kelp
> npx create-react-app my-app --template typescript 
```

### Interactive Command Menu

After generating a command or correcting a previous one, Command-Kelp will present you with an interactive menu for the suggested command. This menu includes options to execute, explain, and copy the command to your clipboard.

## Contributing

Contributions to Command-Kelp are welcome! Feel free to open issues and pull requests in the [GitHub repository](https://github.com/DaivdYuan/command-kelp).

Command-Kelp is released under the [MIT License](https://opensource.org/licenses/MIT).