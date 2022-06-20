[![Build and test](https://github.com/i-gulyaev/receipt-bot/actions/workflows/ci-tests.yml/badge.svg?branch=main&event=push)](https://github.com/i-gulyaev/receipt-bot/actions/workflows/ci-tests.yml)


# Receipt Telegram Bot

The `receipt-bot` is a Telegram bot that is capable to receive receipts as JSON files and to respond
with the list of categorized items in given receipt to the client.

## Usage

1. Register bot in Telegram.
2. Place API token to `.secrets` file.
   ```sh
   echo "API_TOKEN=<telegram bot token>" >> .secrets
    ```
3. Run bot with docker-compose:
   ```sh
   docker-compose build
   docker-compose up -d
   ```

## DB migration

```sh
docker-compose exec -T db sh -c 'mongodump --archive' > db.dump

docker-compose exec -T db sh -c 'mongorestore --archive' < db.dump
```
