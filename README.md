# Case Study

This repository is a case study project primarily developed using JavaScript, CSS, and HTML. The project combines both Node.js and Python components to deliver its full functionality.

## Project Structure

```
case-study/
├── agents_old/
│   └── part_specialist/
│       └── webscraper.py
├── public/
│   └── index.html
├── src/
│   ├── index.js
│   ├── reportWebVitals.js
│   └── backend/
│       ├── README.md
│       └── customer_service_agent/
│           └── sub_agents/
│               ├── appliance_agent/
│               │   └── agent.py
│               ├── help_agent/
│               │   └── tools.py
│               └── product_specialist/
│                   └── agent.py
├── Original_README.md
```

## Getting Started

### Prerequisites

- [Node.js](https://nodejs.org/) (for JavaScript/React)
- [Python 3](https://www.python.org/) (for backend scripts)

### Installation & Running

1. Install Node.js dependencies:
   ```bash
   npm install
   ```

2. (Optional) Install Python dependencies if a `requirements.txt` file exists:
   ```bash
   pip install -r requirements.txt
   ```

3. Open two terminals and run the following in the project directory:

   **Terminal 1:**
   ```bash
   npm test
   ```

   **Terminal 2:**
   ```bash
   python app.py
   ```

**Both processes should be running for the project to function properly.**

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.