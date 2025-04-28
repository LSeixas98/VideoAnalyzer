[![English](https://img.shields.io/badge/Language-English-blue.svg)](README.md)
[![Portuguese](https://img.shields.io/badge/Idioma-Português-green.svg)](README.pt-br.md)

# Music Tutorial Video Analyzer
A web application that uses AI to analyze YouTube music tutorial videos, providing insights about teaching quality and musical content through transcription.

![GitHub](https://img.shields.io/badge/-GitHub-181717?style=flat&logo=github&logoColor=white)
![Python](https://img.shields.io/badge/-Python-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/-Flask-000000?style=flat&logo=flask&logoColor=white)

## 📋 Description
This application allows music teachers, students, and content creators to analyze the pedagogical quality and musical structure of YouTube video tutorials. The system:

- Automatically extracts video transcription
- Uses Google Gemini 1.5 Flash for advanced analysis
- Evaluates teaching methods, language, and level appropriateness
- Identifies instruments, chords, and musical structure
- Provides detailed scores and feedback

## 🚀 Features
- **Customized analysis**: Select which aspects you want to analyze (chords, instruments, musical structure, tablature)
- **Multilingual support**: Transcriptions in Portuguese, English, and other languages
- **Intuitive interface**: Responsive design for use on any device
- **Table visualization**: View results in a structured tabular format
- **JSON visualization**: More technical alternative with expandable/collapsible data
- **Detailed analysis**: Structured output for easy interpretation and integration with other systems

## 📦 Prerequisites
- Python 3.8 or higher
- Google Gemini API key (see setup instructions)
- Internet connection

## ⚙️ Installation and Setup
Clone the repository:
```
git clone https://github.com/LSeixas98/VideoAnalyzer.git
cd VideoAnalyzer
```

Install dependencies:
```
# Recommended method: use virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
# On Windows CMD:
venv\Scripts\activate.bat
# On Linux/macOS:
source venv/bin/activate

# Install dependencies in the virtual environment
pip install -r requirements.txt
```

Configure environment variables: Create a `.env` file in the project root with the following content:
```
# Gemini API Configuration
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-1.5-flash-latest

# Server Configuration
API_HOST=127.0.0.1
API_PORT=5000
```

For local network use, update the API_HOST with your machine's IP:
```
API_HOST=192.168.1.100  # Replace with your local network IP
```

## 🔧 Usage
Start the server:
```
python app.py
```

Access the application: Open a browser and go to:
```
http://localhost:5000  # For local access
# OR
http://192.168.1.100:5000  # For local network access (replace with your IP)
```

Use the application:
1. Paste the YouTube URL in the input field
2. Select the desired analysis options
3. Click "Analyze"
4. Wait for processing (may take a few moments)
5. Toggle between table and JSON views to see the results

## 🔧 Troubleshooting
### pip Permission Issues on Windows
If you encounter permission errors like `[WinError 5] Access denied` when installing packages with pip, try these solutions:

Use virtual environments (recommended):
```
# Navigate to the project directory
cd path/to/VideoAnalyzer

# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On PowerShell:
.\.venv\Scripts\Activate.ps1
# On CMD:
.\.venv\Scripts\activate.bat

# Install dependencies in the virtual environment
python -m pip install -r requirements.txt
```

Run as administrator: If you prefer to install globally, run Command Prompt or PowerShell as administrator.

Install for current user only:
```
pip install -r requirements.txt --user
```

### Modules Not Found
If you receive the error `ModuleNotFoundError: No module named 'google'` or similar:

- Check if you're using the correct virtual environment (if you created one)
- Confirm all dependencies were installed:
```
pip list
```
- Reinstall specific dependencies:
```
pip install google-generativeai youtube-transcript-api
```

## 📂 Project Structure
```
analisador-video-musical/
│
├── app.py                # Main application
├── requirements.txt      # Project dependencies
├── .env                  # Configuration file (not included in the repository)
├── README.md             # This file
├── LICENSE               # Project license
│
├── static/               # Static files
│   ├── css/
│   │   └── styles.css    # Application styles
│   │
│   └── js/
│       └── script.js     # Application JavaScript
│
└── templates/            # HTML Templates
    └── index.html        # Main interface
```

## 🧩 Technologies Used
- Backend: Flask (Python)
- Frontend: HTML, CSS, JavaScript
- Caption API: YouTube Transcript API
- AI: Google Gemini 1.5 Flash
- Data Formatting: JSON
- Configuration: python-dotenv

## ✅ Response Example
The API returns a structured JSON with detailed video analysis, for example:

```json
{
  "videoEvaluation": "Video ID xyzABC123",
  "videoUrl": "https://www.youtube.com/watch?v=xyzABC123",
  "evaluationDate": "2025-04-16",
  "evaluator": "Gemini API (gemini-1.5-flash-latest)",
  "evaluationPoints": {
    "teachingMethod": {
      "score": 4,
      "observations": "Clear and well-structured explanation..."
    },
    "languageUsed": {
      "score": 5,
      "observations": "Accessible language appropriate for the audience..."
    },
    "levelAdequacy": {
      "estimatedVideoLevel": "Intermediate",
      "chordComplexity": {
        "types": "Natural, Barred, Suspended",
        "approximateCount": "Moderate (5-10)"
      },
      "technicalComplexity": "Fingerpicking, Alternate picking",
      "score": 4,
      "observations": "Well-balanced content for the proposed level..."
    }
  },
  "overallScore": 4,
  "generalComments": "Excellent tutorial with good teaching methods...",
  "identifiedChords": ["C", "Am", "F", "G7"],
  "identifiedInstruments": ["Acoustic Guitar", "Electric Guitar"],
  "musicalStructure": {
    "parts": ["Intro", "Verse", "Chorus"],
    "progression": "I-vi-IV-V in C Major",
    "key": "C Major"
  },
  "tablature": {
    "present": true,
    "observations": "Tablature for introduction shown at 2:45"
  }
}
```

## 👨‍💻 Development
### Environment Configuration
#### .env File
The .env file allows configuring the application for different environments:

- Local development: Use `API_HOST=127.0.0.1`
- Local network: Use `API_HOST=` with your machine's IP on the network
- Production: Use `API_HOST=0.0.0.0` to listen on all interfaces

Finding your local network IP:
- Windows: Use the `ipconfig` command in Command Prompt
- Linux: Use `ip addr show` or `ifconfig` in Terminal
- macOS: Use `ifconfig | grep inet` in Terminal

### Adding New Features
To add new analysis criteria:

1. Add new checkboxes in index.html
2. Update the optionsAnalise object in JavaScript
3. Modify the analyze_video_with_gemini function in app.py to include new parameters in the Gemini prompt
4. Update the JSON output schema

## 🛣️ Roadmap
Planned features for future versions:

- [ ] Analysis of complex harmonic progressions
- [ ] Support for videos without captions (audio analysis)
- [ ] PDF report export
- [ ] Comparison between multiple videos
- [ ] Enhanced user interface
- [ ] Public API for integration with other applications

## 📝 Known Limitations
- Depends on the availability of captions/transcriptions in the YouTube video
- Analysis quality depends on the clarity of the transcription
- The Gemini API has token limits that may affect very long videos
- Some automatic captions may contain errors that affect the analysis

## 🔒 Security
- Keep your Gemini API key secure in the .env file
- Add .env to your .gitignore file to avoid sharing your credentials
- In production environments, restrict CORS to specific domains
- For increased security, consider using system environment variables instead of the .env file

## 🧪 Tests
To run automated tests:
```
# Not yet implemented
# pytest tests/
```

## 📚 How to Cite
If you use this project in research or academic work, please cite as:

```
Seixas, L. (2025). VideoAnalyzer: A tool for analyzing music tutorial videos. 
GitHub: https://github.com/LSeixas98/VideoAnalyzer
```

## 👏 Credits
This project uses the following technologies and libraries:

- Flask
- YouTube Transcript API
- Google Gemini API
- Python-dotenv

## 📜 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributions
Contributions are welcome! Feel free to open issues or submit pull requests.

---

Developed with ❤️ for the music community
