"""
Rock-Paper-Scissors-Plus Game Referee
A simple AI chatbot referee using Google ADK
"""

import google.generativeai as genai
import random
import json
from typing import Dict, Any

# Game state storage
game_state = {
    "round_number": 0,
    "user_score": 0,
    "bot_score": 0,
    "user_bomb_used": False,
    "bot_bomb_used": False,
    "game_over": False
}


# Tool 1: Update Game State
def update_game_state(round_number: int = None, user_score: int = None, 
                      bot_score: int = None, user_bomb_used: bool = None,
                      bot_bomb_used: bool = None, game_over: bool = None) -> Dict[str, Any]:
    """Updates the game state with new values"""
    if round_number is not None:
        game_state["round_number"] = round_number
    if user_score is not None:
        game_state["user_score"] = user_score
    if bot_score is not None:
        game_state["bot_score"] = bot_score
    if user_bomb_used is not None:
        game_state["user_bomb_used"] = user_bomb_used
    if bot_bomb_used is not None:
        game_state["bot_bomb_used"] = bot_bomb_used
    if game_over is not None:
        game_state["game_over"] = game_over
    
    return {"status": "updated", "current_state": game_state.copy()}


# Tool 2: Validate Move
def validate_move(move: str) -> Dict[str, Any]:
    """Validates if the user's move is legal"""
    move = move.lower().strip()
    valid_moves = ["rock", "paper", "scissors", "bomb"]
    
    if move not in valid_moves:
        return {"valid": False, "message": "Invalid move. Use: rock, paper, scissors, or bomb"}
    
    if move == "bomb" and game_state["user_bomb_used"]:
        return {"valid": False, "message": "You already used your bomb!"}
    
    return {"valid": True, "move": move}


# Tool 3: Resolve Round
def resolve_round(user_move: str, bot_move: str) -> Dict[str, Any]:
    """Determines the winner of a round"""
    
    # Update bomb usage
    if user_move == "bomb":
        game_state["user_bomb_used"] = True
    if bot_move == "bomb":
        game_state["bot_bomb_used"] = True
    
    # Determine winner
    if user_move == bot_move:
        winner = "draw"
    elif user_move == "bomb":
        winner = "user" if bot_move != "bomb" else "draw"
    elif bot_move == "bomb":
        winner = "bot"
    elif (user_move == "rock" and bot_move == "scissors") or \
         (user_move == "paper" and bot_move == "rock") or \
         (user_move == "scissors" and bot_move == "paper"):
        winner = "user"
    else:
        winner = "bot"
    
    # Update scores
    if winner == "user":
        game_state["user_score"] += 1
    elif winner == "bot":
        game_state["bot_score"] += 1
    
    # Update round number
    game_state["round_number"] += 1
    
    # Check if game is over
    if game_state["round_number"] >= 3:
        game_state["game_over"] = True
    
    return {
        "winner": winner,
        "user_move": user_move,
        "bot_move": bot_move,
        "round": game_state["round_number"],
        "user_score": game_state["user_score"],
        "bot_score": game_state["bot_score"],
        "game_over": game_state["game_over"]
    }


# Bot move selection
def get_bot_move() -> str:
    """Bot decides its move"""
    valid_moves = ["rock", "paper", "scissors"]
    
    # Bot can use bomb if not used yet and randomly decides to
    if not game_state["bot_bomb_used"] and random.random() < 0.15:
        return "bomb"
    
    return random.choice(valid_moves)


# Define tools for ADK
tools = [update_game_state, validate_move, resolve_round]


def play_game():
    """Main game loop"""
    
    # Configure API key (user should set their own)
    # genai.configure(api_key="YOUR_API_KEY_HERE")
    
    print("=" * 50)
    print("ROCK-PAPER-SCISSORS-PLUS GAME REFEREE")
    print("=" * 50)
    
    # Game rules explanation (≤ 5 lines)
    rules = """
Rules: Best of 3 rounds. Valid moves: rock, paper, scissors, bomb.
Rock beats scissors, paper beats rock, scissors beats paper.
Bomb beats everything but can only be used ONCE per game.
Bomb vs bomb = draw. Invalid input wastes your round.
Game ends after 3 rounds automatically.
"""
    print(rules)
    
    # Initialize model with tools
    model = genai.GenerativeModel(
        model_name='gemini-2.0-flash-exp',
        tools=tools
    )
    
    # Start game loop
    while not game_state["game_over"]:
        print(f"\n--- ROUND {game_state['round_number'] + 1} ---")
        print(f"Score - You: {game_state['user_score']} | Bot: {game_state['bot_score']}")
        
        if game_state["user_bomb_used"]:
            print("(Your bomb is used)")
        else:
            print("(You still have your bomb available)")
        
        # Get user input
        user_input = input("\nYour move (rock/paper/scissors/bomb): ").strip().lower()
        
        # Validate move
        validation = validate_move(user_input)
        
        if not validation["valid"]:
            print(f"\n❌ {validation['message']}")
            print("This round is wasted!")
            game_state["round_number"] += 1
            if game_state["round_number"] >= 3:
                game_state["game_over"] = True
            continue
        
        user_move = validation["move"]
        bot_move = get_bot_move()
        
        # Resolve round
        result = resolve_round(user_move, bot_move)
        
        # Display result
        print(f"\n🎮 You played: {result['user_move']}")
        print(f"🤖 Bot played: {result['bot_move']}")
        
        if result["winner"] == "user":
            print("✅ You win this round!")
        elif result["winner"] == "bot":
            print("❌ Bot wins this round!")
        else:
            print("🤝 It's a draw!")
        
        print(f"\nScore after Round {result['round']}: You {result['user_score']} - {result['bot_score']} Bot")
    
    # Game over - final result
    print("\n" + "=" * 50)
    print("GAME OVER!")
    print("=" * 50)
    print(f"Final Score: You {game_state['user_score']} - {game_state['bot_score']} Bot")
    
    if game_state["user_score"] > game_state["bot_score"]:
        print("🎉 YOU WIN THE GAME! 🎉")
    elif game_state["bot_score"] > game_state["user_score"]:
        print("😔 BOT WINS THE GAME!")
    else:
        print("🤝 IT'S A DRAW!")
    print("=" * 50)


if __name__ == "__main__":
    play_game()