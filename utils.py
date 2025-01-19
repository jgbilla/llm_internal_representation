import re
import random

def parse_expression(expression):
    if expression[0] == "(":
        #remove the parentheses
        expression = expression[1:-1]
    parts = expression.split()
    predicate = parts[0]
    args = parts[1:] if len(parts) > 1 else []
    return predicate, args

def parse_state(state):
    pattern = r"\((.*?)\)"
    matches = re.findall(pattern, state)
    expressions = []
    for match in matches:
        predicate, args = parse_expression(match)
        expressions.append((predicate, args))
    return expressions



# Possible actions
# - (pick-up b1): Pick up block b1. --> For this, a block needs to be clear and the arm needs to be empty 
# - (put-down b1): Put down block b1. --> For this, a block needs to be in the arm 
# - (stack b1 b2): Stack block b1 on top of block b2. --> For this, a block needs to be in the arm and the arm needs to be empty
# - (unstack b1 b2): Unstack block b1 from block b2. --> For this, a block needs to be clear and the arm needs to be empty

def is_block_clear(state, block):
    clear = False
    for expression in state:
        predicate, args = expression
        if predicate == "clear" and block in args:
            # the block has been marked as clear, so return true
            return True 
        elif predicate == "on" and block == args[0]:
            clear = True
        elif predicate == "on" and block == args[1]:
            #Another block is currently on top of this block, immediately return false
            return False
    return clear

def is_arm_empty(state):
    for expression in state:
        predicate, args = expression
        if predicate == "arm-empty":
            return True
    return False

def is_block_on_other(state, block, other_block):
    for expression in state:
        predicate, args = expression
        if predicate == "on" and block == args[0] and other_block == args[1]:
            return True
    return False

def is_block_in_arm(state, block):
    for expression in state:
        predicate, args = expression
        if predicate == "holding" and block in args:
            return True
    return False

def is_action_legal(state, action):
    """Given a state and an action, return whether the action is legal or not."""
    
    state = parse_state(state)
    #Get the blocks in the action
    action_predicate, action_blocks = parse_expression(action)
    if action_predicate == "pick-up":
        block = action_blocks[0]
        #check that the arm is empty and the block is clear
        arm_empty = is_arm_empty(state)
        block_clear = is_block_clear(state, block)
        if arm_empty and block_clear:
            return True
        else:
            return False
    elif action_predicate == "put-down":
        block = action_blocks[0]
        #check that the arm is empty and the block is in the arm
        block_in_arm = is_block_in_arm(state, block)
        if block_in_arm:
            return True
        else:
            return False
    elif action_predicate == "stack":
        block = action_blocks[0]
        other_block = action_blocks[1]
        block_in_arm = is_block_in_arm(state, block)
        other_block_clear = is_block_clear(state, other_block)
        if block_in_arm and other_block_clear:
            return True
        else:
            return False 
    elif action_predicate == "unstack":
        block = action_blocks[0]
        other_block = action_blocks[1]
        block_clear = is_block_clear(state, block)
        block_on_other = is_block_on_other(state, block, other_block)
        arm_empty = is_arm_empty(state)
        if block_clear and block_on_other and arm_empty:
            return True
        else:
            return False

def generate_illegal_action(state):
    """Returns a legal action given a state"""
    parsed_state = parse_state(state)
    #Get the blocks in the state
    blocks = []
    for expression in parsed_state:
        predicate, args = expression
        blocks.extend(args)
    blocks = set(blocks)
    #Randomly select an action
    action = random.choice(["pick-up", "put-down", "stack", "unstack"])
    if action == "pick-up" or action == "put-down":
        block = random.choice(list(blocks))
        action = f"({action} {block})"
        if not is_action_legal(state, action):
            return state
        else:
            return generate_illegal_action(state)
    elif action == "stack" or action == "unstack":
        block = random.choice(list(blocks))
        other_block = random.choice(list(blocks - {block}))
        action = f"({action} {block} {other_block})"
        if not is_action_legal(state, action):
            return state
        else:
            return generate_illegal_action(state)

if __name__ == "__main__":
    state = "(on b4 b2) (on-table b1) (holding b3) (on-table b2) (clear b4) (clear b1)"
    action = "(stack b3 b1)"
    print(is_action_legal(state, action))

    


