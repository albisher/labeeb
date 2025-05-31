Here’s a comprehensive list of all the commands shown or mentioned in the NetworkChuck video “Top 41 Linux Commands You Should Know” ([YouTube link](https://www.youtube.com/watch?v=6P-vjgPx9ww)), along with notes on their availability and equivalents for **Linux**, **macOS**, and **Windows**.  
**Note:** Many of these commands are Linux/Unix-specific. For macOS, most will work natively or via Homebrew. For Windows, some are available through WSL (Windows Subsystem for Linux), Cygwin, or have PowerShell/Windows equivalents.

---

## Command List from the Video

### 1. `ncdu`
- **Description:** Visual disk usage analyzer.
- **Linux:** `sudo apt install ncdu`  
- **macOS:** `brew install ncdu`
- **Windows:** WSL or use WinDirStat (GUI alternative)

### 2. `duf`
- **Description:** Prettier, modern disk usage/free utility.
- **Linux:** `sudo snap install duf` or `brew install duf`
- **macOS:** `brew install duf`
- **Windows:** WSL or [duf releases](https://github.com/muesli/duf/releases)

### 3. `ripgrep` (`rg`)
- **Description:** Fast search tool (like grep).
- **Linux:** `sudo apt install ripgrep`
- **macOS:** `brew install ripgrep`
- **Windows:** [ripgrep releases](https://github.com/BurntSushi/ripgrep/releases)

### 4. `mosh`
- **Description:** Mobile shell, robust SSH alternative.
- **Linux:** `sudo apt install mosh`
- **macOS:** `brew install mosh`
- **Windows:** WSL or [Mosh for Windows](https://github.com/mobile-shell/mosh/issues/866)

### 5. `lshw`
- **Description:** List hardware details.
- **Linux:** `sudo apt install lshw`
- **macOS:** Not available; use `system_profiler`
- **Windows:** Use `wmic` or `systeminfo`

### 6. `mtr`
- **Description:** Combines ping and traceroute.
- **Linux:** `sudo apt install mtr`
- **macOS:** `brew install mtr`
- **Windows:** WSL or [WinMTR](https://github.com/White-Tiger/WinMTR)

### 7. `fd`
- **Description:** Modern alternative to `find`.
- **Linux:** `sudo apt install fd-find`
- **macOS:** `brew install fd`
- **Windows:** [fd releases](https://github.com/sharkdp/fd/releases)

### 8. `fzf`
- **Description:** Fuzzy finder for interactive filtering.
- **Linux:** `sudo apt install fzf`
- **macOS:** `brew install fzf`
- **Windows:** [fzf releases](https://github.com/junegunn/fzf/releases)

### 9. `ranger`
- **Description:** Terminal file manager.
- **Linux:** `sudo apt install ranger`
- **macOS:** `brew install ranger`
- **Windows:** WSL

### 10. `zoxide` (`z`)
- **Description:** Smarter `cd` command.
- **Linux:** `sudo apt install zoxide`
- **macOS:** `brew install zoxide`
- **Windows:** [zoxide releases](https://github.com/ajeetdsouza/zoxide/releases)

### 11. `exa`
- **Description:** Modern replacement for `ls`.
- **Linux:** `sudo apt install exa`
- **macOS:** `brew install exa`
- **Windows:** [exa releases](https://github.com/ogham/exa/releases)

### 12. `glances`
- **Description:** System monitoring tool.
- **Linux:** `sudo apt install glances`
- **macOS:** `brew install glances`
- **Windows:** `pip install glances`

### 13. `iotop`
- **Description:** Disk I/O usage monitor.
- **Linux:** `sudo apt install iotop`
- **macOS:** Not available natively
- **Windows:** Use Resource Monitor

### 14. `stat`
- **Description:** Detailed file information.
- **Linux:** Built-in
- **macOS:** Built-in (slightly different output)
- **Windows:** Use `Get-Item` in PowerShell

### 15. `dstat`
- **Description:** Resource statistics.
- **Linux:** `sudo apt install dstat`
- **macOS:** `brew install dstat`
- **Windows:** WSL

### 16. `watch`
- **Description:** Run command repeatedly.
- **Linux:** Built-in
- **macOS:** `brew install watch`
- **Windows:** WSL or use PowerShell loops

### 17. `progress`
- **Description:** Show progress of coreutils commands.
- **Linux:** `sudo apt install progress`
- **macOS:** `brew install progress`
- **Windows:** WSL

### 18. `dog`
- **Description:** Modern replacement for `dig`.
- **Linux:** `sudo snap install dog`
- **macOS:** `brew install dog`
- **Windows:** [dog releases](https://github.com/ogham/dog/releases)

### 19. `termshark`
- **Description:** Terminal UI for `tshark` (packet capture).
- **Linux:** `sudo apt install termshark`
- **macOS:** `brew install termshark`
- **Windows:** [termshark releases](https://github.com/gcla/termshark/releases)

### 20. `lsof -i :`
- **Description:** List open files/sockets for a port.
- **Linux:** Built-in
- **macOS:** Built-in
- **Windows:** Use `netstat -ano` or `Get-Process`

### 21. `ipcalc`
- **Description:** Subnet calculator.
- **Linux:** `sudo apt install ipcalc`
- **macOS:** `brew install ipcalc`
- **Windows:** WSL or online tools

### 22. `wormhole`
- **Description:** Secure file transfer.
- **Linux:** `pip install magic-wormhole`
- **macOS:** `pip install magic-wormhole`
- **Windows:** `pip install magic-wormhole`

### 23. `systemd-analyze blame`
- **Description:** Show slowest systemd services.
- **Linux:** Built-in (systemd systems)
- **macOS:** Not available
- **Windows:** Not available

### 24. `procs`
- **Description:** Modern replacement for `ps`.
- **Linux:** `sudo snap install procs` or `brew install procs`
- **macOS:** `brew install procs`
- **Windows:** [procs releases](https://github.com/dalance/procs/releases)

### 25. `lazydocker`
- **Description:** Terminal UI for Docker.
- **Linux:** `brew install lazydocker`
- **macOS:** `brew install lazydocker`
- **Windows:** [lazydocker releases](https://github.com/jesseduffield/lazydocker/releases)

### 26. `rsync`
- **Description:** File sync and transfer.
- **Linux:** Built-in
- **macOS:** Built-in
- **Windows:** WSL or [cwRsync](https://www.itefix.net/cwrsync)

### 27. `shred`
- **Description:** Secure file deletion.
- **Linux:** Built-in
- **macOS:** `brew install coreutils` (then use `gshred`)
- **Windows:** Use `cipher /w` or third-party tools

### 28. `moreutils` (includes `ts`, `errno`, `ifdata`, `vidir`, `vipe`, etc.)
- **Description:** Collection of useful utilities.
- **Linux:** `sudo apt install moreutils`
- **macOS:** `brew install moreutils`
- **Windows:** WSL

#### - `ts`: Add timestamps to output.
#### - `errno`: Lookup error codes.
#### - `ifdata`: Show network interface info.
#### - `vidir`: Edit directory names in text editor.
#### - `vipe`: Edit piped data in text editor.

### 29. `unp`
- **Description:** Unpack any archive.
- **Linux:** `sudo apt install unp`
- **macOS:** Not available natively
- **Windows:** Use 7-Zip or WSL

### 30. `jq`
- **Description:** JSON processor.
- **Linux:** `sudo apt install jq`
- **macOS:** `brew install jq`
- **Windows:** [jq releases](https://github.com/stedolan/jq/releases)

### 31. `taskwarrior`
- **Description:** CLI task manager.
- **Linux:** `sudo apt install taskwarrior`
- **macOS:** `brew install task`
- **Windows:** [taskwarrior releases](https://taskwarrior.org/download/)

### 32. `asciinema`
- **Description:** Record/share terminal sessions.
- **Linux:** `sudo apt install asciinema`
- **macOS:** `brew install asciinema`
- **Windows:** WSL

### 33. `asciinema-agg`
- **Description:** Convert asciinema recordings to GIFs.
- **Linux:** `pip install asciinema-agg`
- **macOS:** `pip install asciinema-agg`
- **Windows:** `pip install asciinema-agg`

### 34. `fabric`
- **Description:** Python CLI tool for SSH automation.
- **Linux:** `pip install fabric`
- **macOS:** `pip install fabric`
- **Windows:** `pip install fabric`

### 35. `ollama`
- **Description:** Local LLM/AI CLI.
- **Linux:** [ollama.com](https://ollama.com/)
- **macOS:** [ollama.com](https://ollama.com/)
- **Windows:** [ollama.com](https://ollama.com/) (Windows support in beta)

---

## Platform Summary

### Linux
- All commands are available natively or via package managers (`apt`, `snap`, `brew`, `pip`).

### macOS
- Most commands available via [Homebrew](https://brew.sh/) or `pip`.
- Some commands (e.g., `lshw`, `iotop`, `systemd-analyze`) are not available or have different equivalents.

### Windows
- Many commands available via [WSL](https://docs.microsoft.com/en-us/windows/wsl/), some as native ports, or via [Chocolatey](https://chocolatey.org/).
- GUI alternatives exist for some (e.g., WinDirStat, WinMTR).
- PowerShell can sometimes provide similar functionality.

---

## Tips

- For **macOS** and **Windows**, install [Homebrew](https://brew.sh/) (macOS) or [WSL](https://docs.microsoft.com/en-us/windows/wsl/) (Windows) to get access to most of these tools.
- Some tools require Python (`pip install ...`).
- Always check the official documentation for the latest installation instructions.

---

**Let me know if you want a table format, installation commands, or more details for a specific platform!**

Citations:
[1] https://www.youtube.com/watch?v=6P-vjgPx9ww

---
Answer from Perplexity: pplx.ai/share