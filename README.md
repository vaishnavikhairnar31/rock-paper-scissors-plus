# Rock-Paper-Scissors-Plus — AI Game Referee

This project implements a minimal conversational AI referee for a Rock–Paper–Scissors–Plus game using Google ADK.

## Overview
The referee manages a best-of-three game between a user and a bot, enforcing rules, validating moves, tracking state, and explaining outcomes in natural language.

## Game Rules
- Best of 3 rounds
- Valid moves: rock, paper, scissors, bomb
- Bomb can be used once per player
- Bomb beats all moves
- Bomb vs bomb results in a draw
- Invalid input wastes the round

## Architecture
- **Game State**: Stored in a global dictionary to persist across turns
- **Tools**:
  - `validate_move`: Validates user intent
  - `resolve_round`: Applies game logic and updates state
- **Agent**:
  - Uses Gemini via Google ADK to explain round outcomes
- **Interface**: Simple CLI conversational loop

## Tradeoffs
- Bot strategy is intentionally simple to keep focus on agent design
- State is kept in memory (no database) as required

## Possible Improvements
- Smarter bot strategy
- Structured outputs from the agent
- Better prompt control for explanations

## Running the Game
```bash
pip install google-generativeai
python game_referee.py
