# RiderProjectUnloader

... is a Python script designed to speed up JetBrains Rider launch times by unloading all projects within your Visual Studio solutions. It mimics Rider behavior in creating its `.DotSettings.user` file. It does it however in milliseconds instead of you and Rider spending minutes on the same task. The script ensures that Rider ignores all projects on startup, allowing it to start almost instantly whereas on very large solutions it can take many long minutes. Once Rider starts you select which projects to load, typically via its `Load project With Dependencies` feature; and you enable the "Solution Wide Analysis" at the moment of your choice.

## Features

- Extracts project GUIDs from a Visual Studio solution file (`<solution-file>.sln`).
- Encodes these keys to the format expected by Rider.
- Disables "Solution Wide Analysis" in Rider, further improving startup performance.
- Generates a `.DotSettings.user` file that Rider uses to determine which projects to unload on startup.

## How to Use

### Prerequisites

- Python 3.x installed on your system.

### Setup

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/JanZeman/RiderProjectUnloader.git
   git clone git@github.com:JanZeman/RiderProjectUnloader.git
   ```
   Or create the both scripts manually and copy & paste their content.

2. Copy both scripts to your project folder, next to your `<solution-file>.sln`.

3. Ensure that the `unload_rider.sh` script is executable:
   ```bash
   chmod +x unload_rider.sh
   ```
4. Modify content of `unload_rider.sh` by replacing `<solution-file>.sln` with the name of your solution file.

### Execution

1. Run the script with the following command:
   ```bash
   ./unload_rider.sh
   ```
   or
   ```bash
   python unload_rider.py <solution-file>.sln
   ```

   This will generate a `.DotSettings.user` file for the specified solution, which Rider will use to determine which projects to unload on startup.

2. After running the script, restart JetBrains Rider to see the changes. It should start very quickly with all projects in an unloaded state.
3. Decide which projects to load, typically by right-clicking on one of your application projects and selecting "Load Project with Dependencies" option.
4. Optionally re-enable the "Solution Wide Analysis".

### Notes

- This script only needs to be run once, or whenever the solution file changes (e.g., projects are added or removed).
- It's recommended to close Rider before running the script to avoid any conflicts.
- You can manually load any unloaded projects in Rider as needed after the script has run.

## Compatibility

This script has been tested with the following configurations:

- JetBrains Rider versions: [Specify versions, e.g., 2023.1 and later]

If you encounter issues with other configurations, please feel free to report them via GitHub Issues.


## Contributing

Contributions are welcome! Please fork this repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License.

## Author

[@JanZeman](https://github.com/JanZeman)
