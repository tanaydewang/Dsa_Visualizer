class StateManager:
    def __init__(self):
        # A stack to hold the application states
        self.state_stack = ["main_menu"]

    def get_current_state(self):
        # The current state is always at the top of the stack
        return self.state_stack[-1] if self.state_stack else None

    def push_state(self, state):
        # Add a new state to the top of the stack
        self.state_stack.append(state)
        print(f"Pushed state: {state}. Stack: {self.state_stack}")


    def pop_state(self):
        # Go back by removing the top state
        if len(self.state_stack) > 1:
            self.state_stack.pop()
        print(f"Popped state. Stack: {self.state_stack}")