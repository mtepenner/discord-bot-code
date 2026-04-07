# Discord Timekeeping & Payroll Bot 🛠️

A professional Discord bot built with `discord.py` designed to streamline workforce management within a Discord server. It allows employees to track their shifts and managers to monitor activity and export payroll data.

## 📋 Table of Contents

  - [Features](https://www.google.com/search?q=%23features)
  - [Technologies Used](https://www.google.com/search?q=%23technologies-used)
  - [Installation](https://www.google.com/search?q=%23installation)
  - [Usage](https://www.google.com/search?q=%23usage)
  - [Project Structure](https://www.google.com/search?q=%23project-structure)

## 🚀 Features

  - **Automated Timekeeping**: Simple `/clock_in` and `/clock_out` commands for employees.
  - **Management Oversight**: View all currently active staff with `/who_is_working`.
  - **Payroll Export**: Generate and download a complete CSV report of all shift history.
  - **Shift Calculations**: Automatically calculates decimal hours and total durations, accounting for break times.
  - **Personal Stats**: Employees can check their own total logged hours with `/my_hours`.

## 🛠️ Technologies Used

  - **Language**: Python 3.x
  - **Library**: `discord.py` (Slash Commands / App Commands)
  - **Database**: SQLite3 for persistent shift and history storage.
  - **Environment**: `python-dotenv` for secure token management.

## 📦 Installation

1.  **Clone the repository:**

    ```bash
    git clone <your-repository-url>
    cd discord-bot-code
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment Variables:**
    Create a `.env` file in the root directory and add your Discord Bot Token:

    ```env
    DISCORD_TOKEN=your_bot_token_here
    ```

4.  **Initialize the Bot:**
    The bot will automatically create the `/data` directory and initialize the SQLite database on its first run.

    ```bash
    python main.py
    ```

## 🎮 Usage

### For Employees

  - `/clock_in`: Start your shift.
  - `/clock_out`: End your shift and save hours to the database.
  - `/my_hours`: View your total accumulated work hours.
  - `/estimate_pay`: Calculate potential earnings based on hours and rate.

### For Managers (Requires 'Manage Server' Permissions)

  - `/who_is_working`: See a real-time list of all clocked-in staff and their current status.
  - `/export_payroll`: Download a CSV file containing all historical shift data.
  - `/server_info`: View quick statistics about the Discord server.

## 📂 Project Structure

  - `main.py`: Entry point for the bot; handles cog loading and event loops.
  - `cogs/`: Contains modular command categories (Timekeeping, Payroll, Management, Utility).
  - `utils/`: Helper scripts for database connections and string formatting.
  - `data/`: Directory where the SQLite database file resides.
