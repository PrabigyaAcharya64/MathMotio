# MathMotio 🧮✨

**AI-Powered Mathematical Animation Generator**

Transform mathematical concepts into stunning visual animations using natural language descriptions and the power of Google's Gemini AI combined with Manim.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Manim](https://img.shields.io/badge/Manim-0.19.0-green.svg)](https://manim.community/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](CONTRIBUTING.md)

## 📖 Description

MathMotio is an innovative command-line tool that bridges the gap between mathematical concepts and visual learning. By leveraging Google's Gemini AI and the Manim animation library, it allows users to generate high-quality mathematical animations simply by describing what they want to see in natural language.

### Key Features

- 🤖 **AI-Powered Code Generation**: Uses Google Gemini AI to understand natural language descriptions and generate Manim code
- 🔍 **Intelligent Code Verification**: Automatically verifies and optimizes generated code for best practices
- 🎬 **High-Quality Animations**: Produces professional mathematical animations with consistent styling
- ⚡ **Command-Line Interface**: Fast and efficient workflow for power users and automation

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

### Step-by-Step Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/MathMotio.git
   cd MathMotio
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   GEMINI_API_KEY=your_google_gemini_api_key_here
   ```

5. **Verify installation**
   ```bash
   python -c "import manim; print('Manim installed successfully!')"
   ```

## 🎯 Usage

### Quick Start

1. **Interactive Mode**
   ```bash
   python mathmotio.py
   ```

2. **Direct Command**
   ```bash
   python mathmotio.py "Create a sine wave animation with amplitude 2"
   ```

### Advanced Usage

You can also use individual components for more control:

```bash
# Generate code only
python geminipostfetch.py "your description here"

# Verify and improve code
python geminiverify.py "your description here"

# Render animation
python render.py verified_manim_code.py
```

### Example Queries

- `"Create a parabola animation showing the vertex and focus"`
- `"Show a sine wave with amplitude 2 and period π"`
- `"Generate a cosine function with phase shift"`
- `"Animate a point moving along a circle"`
- `"Show the derivative of a cubic function"`
- `"Create a 3D surface plot of z = sin(x) * cos(y)"`
- `"Animate the construction of a golden spiral"`

## 🏗️ Project Structure

```
MathMotio/
├── mathmotio.py               # Main command-line interface
├── geminipostfetch.py         # AI code generation
├── geminiverify.py            # Code verification and improvement
├── render.py                  # Manim rendering script
├── queryfetch.py              # User input handling
├── requirements.txt           # Python dependencies
├── media/                     # Generated videos and assets
│   ├── videos/
│   ├── images/
│   └── Tex/
├── LICENSE                    # MIT License
├── CONTRIBUTING.md            # Contributing guidelines
├── CODE_OF_CONDUCT.md         # Code of conduct
├── CHANGELOG.md               # Version history
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini API key | Yes |

### API Key Setup

1. **Get your API key** from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **Create a `.env` file** in the project root:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

### Customization

You can customize the animation generation by modifying the prompts in:
- `geminipostfetch.py` - Initial code generation
- `geminiverify.py` - Code verification and improvement

### Output Settings

- **Video Format**: MP4 (H.264)
- **Resolution**: 1920x1080 (1080p)
- **Frame Rate**: 30 FPS
- **Duration**: Minimum 20 seconds
- **Y-axis Range**: [-3.5, 3.5] for optimal mathematical visualization

## 🤝 Contributing

We welcome contributions from the community! Please see our [Contributing Guidelines](CONTRIBUTING.md) for detailed information on how to contribute.

### Code of Conduct

This project is intended to be a safe, welcoming space for collaboration. All contributors are expected to adhere to our [Code of Conduct](CODE_OF_CONDUCT.md).

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Add tests if applicable
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

### Code Style

- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add comments for complex logic
- Include docstrings for functions and classes

### Testing

Before submitting a pull request, please:
- Test your changes locally
- Ensure all existing functionality works
- Add tests for new features if applicable

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📋 Changelog

See [CHANGELOG.md](CHANGELOG.md) for a list of changes and version history.

## 🐛 Known Issues

- Large video files may take time to process
- Some complex mathematical expressions may require multiple attempts
- API rate limits may affect processing speed during high usage


## 🙏 Acknowledgments

- [Manim Community](https://manim.community/) for the amazing animation library
- [Google Gemini AI](https://ai.google.dev/) for powerful natural language processing




*Transform your mathematical ideas into visual reality!*

---

**⭐ If you find this project helpful, please give it a star!** 
