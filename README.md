# receipt-bot

The `receipt-bot` is a Telegram bot that is capable to receive receipts as JSON files and to respond
with the list of items in given receipt to the client.

## Usage

1. Register bot in Telegram.
2. Place API token to `.secrets` file.
3. Run bot with docker-compose:
   ```
   docker-compose build
   docker-compose up -d
   ```
