# FDS External Server

A Python-based external server designed to work with the Rusty DCS gRPC Server. This server handles unit tracking and event management for DCS World missions.

## Features

- Real-time unit tracking
- Event processing
- Redis integration for state management
- MIST library integration
- Multi-threaded operation
- Configurable parameters via YAML

## Prerequisites

- Python 3.8+
- Redis server
- DCS World with Rusty DCS gRPC Server
- MIST library installed in DCS

## Installation

1. Clone this repository
2. Install required packages:
```bash
pip install grpc redis pyyaml schedule
```

## Configuration

Edit `server_config.yml` to configure:
- gRPC server connection parameters
- Redis connection settings
- Mission unit configurations
- Capturable regions settings

## Running the Server

Start the server by running:
```bash
python main.py
```

The server will:
1. Initialize connections to gRPC and Redis servers
2. Verify MIST library presence
3. Start unit and event tracking threads
4. Begin processing mission events

## Architecture

- `main.py`: Server entry point and core logic
- `modules/`:
  - `unitFetcher.py`: Handles unit tracking
  - `commonDictionaries.py`: Shared constants and mappings
  - Other supporting modules

## Error Handling

The server includes comprehensive error handling for:
- gRPC connection issues
- Redis connection problems
- MIST library verification
- Stream processing errors

## License

This project is proprietary software. All rights reserved.
