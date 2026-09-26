# Railway Deployment Guide for OwO Bot

## Step 1: Create Discord Bot
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application"
3. Give it a name (e.g., "OwO Auto Bot")
4. Go to "Bot" section → Click "Add Bot"
5. Under TOKEN, click "Copy" (this is your DISCORD_TOKEN)
6. Keep this token safe!

## Step 2: Enable Required Intents
1. In Bot section, scroll down to "INTENTS"
2. Enable:
   - Message Content Intent
   - Server Members Intent (optional)
3. Save changes

## Step 3: Add Bot to Server
1. Go to "OAuth2" → "URL Generator"
2. Select scopes: `bot`
3. Select permissions: `Send Messages`, `Read Messages`
4. Copy the generated URL
5. Open it in browser and select your Discord server

## Step 4: Get Channel ID
1. In Discord, enable Developer Mode (User Settings → Advanced → Developer Mode)
2. Right-click on the channel where OwO commands should go
3. Click "Copy Channel ID"

## Step 5: Deploy on Railway
1. Go to [Railway.app](https://railway.app)
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select `sharmasunil38065-commits/auto-owo`
5. In "Variables" section, add:
   - `DISCORD_TOKEN` = (paste your token from Step 1)
   - `CHANNEL_ID` = (paste your channel ID from Step 4)
   - `OWO_PREFIX` = `owo ` (default, adjust if needed)
   - `COMMAND_INTERVAL_SECONDS` = `30` (adjust as needed)
   - `ENABLE_PRAY` = `true`
   - `ENABLE_RANDOM_COMMANDS` = `true`
6. Click "Deploy"

## Step 6: Verify Bot is Running
1. Check Railway logs - you should see "Logged in as ..."
2. In Discord, the bot should start sending commands automatically

## Commands
- `!owo hunt` - Send hunt command manually
- `!owo battle` - Send battle command manually
- `!status` - Check bot status and configuration

## Troubleshooting
- **Bot not sending commands?** Check if bot has permission to send messages in the channel
- **Token error?** Make sure DISCORD_TOKEN is correct
- **Channel ID error?** Make sure CHANNEL_ID is numeric and correct
- **Check logs** in Railway dashboard for detailed error messages

## Customization
- Edit `COMMAND_INTERVAL_SECONDS` to change how often commands are sent
- Set `ENABLE_PRAY=false` to disable pray command
- Set `ENABLE_RANDOM_COMMANDS=false` to only use hunt/battle
