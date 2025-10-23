# Cipher-V1-RBot 🤖
**Advanced AI-Powered Roblox Bot**

This is a sophisticated Roblox bot that demonstrates advanced automation and AI capabilities. The bot can intelligently navigate game worlds, avoid obstacles, and interact with other players through chat.

## 🌟 Features

- **🚶 Intelligent Movement**: Walks around game worlds with realistic movement patterns
- **🧱 Wall Avoidance**: Uses computer vision to detect and avoid walls/obstacles
- **🧠 Smart Pathfinding**: Adaptive navigation that explores efficiently
- **💬 Fact Sharing**: Automatically shares interesting facts in game chat
- **🎮 Hotkey Controls**: F1 to start, F2 to stop - control the bot anytime!
- **⚙️ Configurable**: Easy-to-modify settings for different games and preferences
- **📊 Logging**: Detailed logging for monitoring bot behavior
- **🔒 Safety Features**: Built-in failsafes and emergency stops

## 🎯 How It Works

1. **Computer Vision**: Takes screenshots of the Roblox window and analyzes them
2. **Edge Detection**: Uses OpenCV to identify walls and obstacles
3. **Movement Control**: Simulates keyboard inputs (WASD) for character movement
4. **Chat Interaction**: Automatically sends interesting facts to chat
5. **Adaptive Behavior**: Learns from the environment and adjusts movement patterns

## 📋 Requirements

- **Windows 10/11** (Required for window detection)
- **Python 3.8+** 
- **Roblox** (Desktop application, not browser)
- **Administrative privileges** (for keyboard/mouse automation)

## 🚀 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/aauuzyy/Cipher-V1-RBot.git
   cd Cipher-V1-RBot
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the bot** (optional):
   - Edit `config.json` to customize behavior
   - Modify movement speed, fact intervals, detection sensitivity

## 🚀 Usage

1. **Launch Roblox** and join any game
2. **Position your character** in an open area
3. **Run the bot**:
   ```bash
   python cipher_bot.py
   ```
4. **Follow the prompts** and press Enter to initialize
5. **Use hotkeys to control the bot**:
   - **F1** = Start the bot (begin walking and chatting)
   - **F2** = Stop the bot (pause all activity)
   - **Ctrl+C** = Exit the program completely

### 🎮 Hotkey Controls

The bot now features convenient hotkey controls that work even when Roblox is the active window:

- **F1 Key**: Starts the bot behavior (walking, wall avoidance, fact sharing)
- **F2 Key**: Stops the bot behavior (bot becomes idle but system stays running)
- **Ctrl+C**: Completely exits the bot program

This means you can:
- Start the bot system once
- Use F1/F2 to activate/deactivate as needed
- No need to restart the program each time!

## ⚙️ Configuration

Edit `config.json` to customize the bot's behavior:

```json
{
    "movement": {
        "speed": 0.1,                    // Movement speed multiplier
        "movement_duration": 2.0,        // How long to move forward
        "wall_detection_threshold": 50   // Sensitivity for wall detection
    },
    "chat": {
        "fact_interval": 30,             // Seconds between facts
        "enable_facts": true             // Enable/disable fact sharing
    },
    "hotkeys": {
        "start_key": "f1",               // Key to start the bot
        "stop_key": "f2",                // Key to stop the bot
        "enable_hotkeys": true           // Enable/disable hotkey controls
    }
}
```

## 🎲 Facts Database

The bot comes with 15+ interesting facts including:
- Science facts
- Animal facts  
- Historical facts
- Space facts
- And more!

You can add custom facts by editing the `get_random_fact()` function in `cipher_bot.py`.

## 🛡️ Safety & Ethics

**Important Guidelines:**
- ✅ Use only in games where automation is allowed
- ✅ Respect other players and game rules
- ✅ Use for educational purposes and demonstrations
- ❌ Don't use for unfair advantages or griefing
- ❌ Don't spam chat or disrupt gameplay

## 🔧 Troubleshooting

**Bot can't find Roblox window:**
- Make sure Roblox is running (not Roblox Studio)
- Ensure Roblox window is visible (not minimized)
- Try running as administrator

**Movement not working:**
- Check that Roblox window is focused
- Verify your character is spawned and controllable
- Make sure no other programs are capturing keyboard input

**Wall detection issues:**
- Adjust `wall_detection_threshold` in config.json
- Try different lighting conditions in the game
- Some games may require different detection settings

## 📁 Project Structure

```
Cipher-V1-RBot/
├── cipher_bot.py      # Main bot logic
├── config.json        # Configuration settings
├── requirements.txt   # Python dependencies
├── README.md          # This file
└── cipher_bot.log     # Bot activity logs (created on first run)
```

## 🧪 Technical Details

**Computer Vision:**
- Uses OpenCV for real-time image processing
- Canny edge detection for obstacle identification
- Screenshot-based window capture
- Adaptive threshold detection

**Movement AI:**
- WASD key simulation via PyAutoGUI
- Random exploration patterns
- Obstacle avoidance algorithms
- Adaptive pathfinding

**Chat System:**
- Automatic chat opening with '/' key
- Timed fact sharing
- Safe message handling

## 🔮 Future Enhancements

- 🎯 Object recognition for specific game elements
- 🗺️ Memory mapping of explored areas
- 🤝 Multi-bot coordination
- 📱 Mobile device support
- 🎨 GUI interface for easier configuration
- 🔊 Voice interaction capabilities

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is for educational purposes. Please use responsibly and in accordance with Roblox's Terms of Service.

## ⚠️ Disclaimer

This bot is created for educational and demonstration purposes to showcase automation and AI capabilities. Users are responsible for ensuring their usage complies with Roblox's Terms of Service and game-specific rules. The developers are not responsible for any account penalties that may result from using this bot.

---

**Made with ❤️ by the Cipher Team**

*Demonstrating the power of AI and automation in gaming!*
