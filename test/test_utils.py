import pytest
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import is_action_legal, generate_illegal_action

def load_test_cases():
    data = []
    with open("blockworld_dataset.json", "r") as f:
        data = json.load(f)
    test_cases = []
    count = 100
    for item in data:
        for i in range(len(item["actions"])):
            test_cases.append((item["states"][i], item["actions"][i]))
        if len(test_cases) >= count:
            break
    print(test_cases)
    return test_cases

@pytest.mark.parametrize("state, action", load_test_cases())
def test_is_action_legal(state, action):
    assert is_action_legal(state, action), f"\nState: {state}\nAction: {action}\nExpected action to be legal but got illegal"

@pytest.mark.parametrize("state, action", load_test_cases())
def test_generate_illegal_action(state, action):
    illegal_action = generate_illegal_action(state)
    assert not is_action_legal(state, illegal_action), f"\nState: {state}\nAction: {illegal_action}\nExpected action to be illegal but got legal"

