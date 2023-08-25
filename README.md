# Command-Kelp: Natural Language Command Line Helper

Command-Kelp is a command-line tool designed to simplify your interaction with the command line by using natural language commands. It provides three main functions to enhance your command-line experience: generating commands from descriptions, correcting previous commands, and offering an interactive menu for executing, explaining, and copying commands.

## Table of Contents

- [Command-Kelp: Natural Language Command Line Helper](#command-kelp-natural-language-command-line-helper)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Generating Commands](#generating-commands)
    - [Correcting Commands](#correcting-commands)
    - [Interactive Command Menu](#interactive-command-menu)
  - [Contributing](#contributing)

## Installation

To install Command-Kelp, you need to have Python 3.x and `pip` installed. Run the following command:

```bash
git clone git@github.com:DaivdYuan/command-kelp.git
cd command-kelp && pip install .
```

## Usage

### Generating Commands

You can use the `kelp` command along with a description to generate a corresponding command. Simply provide a brief description of what you want to achieve, and Command-Kelp will suggest the appropriate command.

```bash
$ kelp tar compress data/

> tar -czvf data.tar.gz data 
```

### Correcting Commands

Similar to the well-known `thefuck` package, Command-Kelp can correct your previous command if you mistype it or make a syntax error. Just type `kelp` or `kelp fuck`, and Command-Kelp will attempt to correct the previous command.

```bash
$ df-h
command not found: df-h

$ kelp
> df -h

```

### Interactive Command Menu

After generating a command or correcting a previous one, Command-Kelp will present you with an interactive menu for the suggested command. This menu includes options to execute, explain, and copy the command to your clipboard.

## Contributing

Contributions to Command-Kelp are welcome! Feel free to open issues and pull requests in the [GitHub repository](https://github.com/DaivdYuan/command-kelp).

To use:
<pre><code>$ kelp [options] [your text here]</pre></code>

Command-Kelp is released under the [MIT License](https://opensource.org/licenses/MIT).