# iDotDisplay

iDotDisplay is a simple application for controlling a dot matrix display, similar to what iDotMatrix offers. It allows users to display custom images on their dot matrix display, making it more versatile than what the original application from the manufacturer provides.

![iDot Display](https://ae-pic-a1.aliexpress-media.com/kf/S3eb404ac2c0b42b1b49ad7415829fbf9P.jpg_960x960q75.jpg)

## Features

- [x] Display custom images on your dot matrix display
- [ ] Display custom text messages
- [x] Turn on/off the display
- [ ] Adjust brightness levels

## Architecture

The RESTFul API server application is built using Python and Flask, while the client application is developed using React. The server handles the Bluetooth communication with the dot matrix display, while the client provides a user-friendly interface for controlling the display. The server exposes endpoints for uploading images and controlling the display, which the client interacts with to send commands and display images.

## Installation

### Server

#### As a Docker container

1. Clone the repository:
   ```bash
   git clone https://github.com/ayltai/idotdisplay.git
   cd idotdisplay
   ```
2. Build the Docker image:
   ```bash
   make deploy
   ```
3. Run the Docker container

#### As a standalone application

1. Clone the repository:
   ```bash
   git clone https://github.com/ayltai/idotdisplay.git
   cd idotdisplay/backend
   ```
2. Create a virtual environment and activate it:
   ```bash
   make venv
   source venv/bin/activate
   ```
3. Install the required dependencies:
   ```bash
   make upgrade
   ```
4. Run the server:
   ```bash
   make
   ```

### Client

1. Clone the repository:
   ```bash
   git clone https://github.com/ayltai/idotdisplay.git
   cd idotdisplay/frontend
   ```
2. Install the required dependencies:
   ```bash
   pnpm i
   ```
3. Run the client application:
   ```bash
   pnpm start
   ```

## Usage

1. Open the client application in your web browser (usually at `http://localhost:5173`).
2. Use the interface control the dot matrix display or display custom images.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
