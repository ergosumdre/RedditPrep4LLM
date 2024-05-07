# Reddit Data Cleaner for Language Model Fine-Tuning

This repository contains a script for cleaning Reddit data to prepare it for fine-tuning language models (LLMs). It's adapted from the work of [Sentdex](https://github.com/Sentdex/LLM-Finetuning) and tailored specifically for processing Reddit text data.

## Description

Prepare a JSON file tailored for language model fine-tuning, emphasizing conversational threads sourced from a given subreddit post. This script refines Reddit text data, optimizing it for language model adaptation. Drawing inspiration from Sentdex's methodology, it adeptly manages HTML tags, URLs, emojis, and special characters, while also spotlighting conversational threads for nuanced context. By standardizing text formatting and eliminating extraneous noise, it ensures top-tier data quality for refining language models. Its adaptability enables seamless integration with diverse training requirements.

## Key Features

- Preprocessing script tailored specifically for Reddit data.
- Handles HTML tags, URLs, emojis, and special characters.
- Standardizes text formatting and removes noise.
- Optimizes data quality for fine-tuning language models.
- Easily adaptable and customizable for different LLM training requirements.

## Usage

1. Clone or download the repository.
2. Place your raw Reddit data file (e.g., `subreddit_comments.zst`) into the data/zst_file directory.
3. Open a terminal and navigate to the repository directory.
4. Run the cleaning script by executing the following command:
    ```bash
    sh fineTuneDataset.sh data/zst_file/subreddit_comments.zst
    ```
## Contributions

Contributions and feedback are welcome! If you encounter any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the [License Name] License. See the LICENSE file for details.

## Disclaimer

Please note that while this script aims to improve the quality of Reddit data for language model fine-tuning, it may not cover all possible preprocessing requirements. Users are encouraged to review and adapt the script as needed for their specific datasets and use cases.

## Acknowledgements

- This project is inspired by the work of [Sentdex](https://github.com/Sentdex/LLM-Finetuning).

Happy cleaning and fine-tuning!
