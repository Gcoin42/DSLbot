# DSLbot

## Introduction
DSLbot is an information query system that allows users to fetch movie rankings from Douban and property information from Lianjia based on user-defined criteria.

## Installation
Follow these steps to install the project:

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/DSLbot.git
    ```
2. Navigate to the project directory:
    ```bash
    cd DSLbot
    ```
3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration
Update the `config.yaml` file with the necessary configurations for Douban and Lianjia:

```yaml
# config.yaml
douban:
  url: "https://movie.douban.com/top250"
  headers:
    User-Agent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0"

lianjia:
  url: "https://bj.fang.lianjia.com/loupan/"
  headers:
    User-Agent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0"
  num_records: 160
