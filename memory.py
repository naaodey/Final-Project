class MemoryManager:

    def __init__(self, max_history=5):

        self.max_history = max_history
        self.memory = {}


    def save(
        self,
        session_id: str,
        question: str,
        answer: dict
    ):

        if session_id not in self.memory:
            self.memory[session_id] = []

        self.memory[session_id].append(
            {
                "question": question,
                "answer": answer
            }
        )

        # Keep only recent conversations

        self.memory[session_id] = (
            self.memory[session_id][-self.max_history:]
        )



    def get_history(
        self,
        session_id: str
    ):

        return self.memory.get(
            session_id,
            []
        )


    def get_context(
        self,
        session_id: str
    ):

        history = self.get_history(
            session_id
        )

        if not history:
            return ""

        context = []

        for item in history:

            context.append(
                f"Question: {item['question']}"
            )

            context.append(
                f"Answer: {item['answer'].get('final_answer', '')}"
            )

        return "\n".join(context)


    def clear(
        self,
        session_id: str
    ):

        if session_id in self.memory:
            del self.memory[session_id]

    
    def clear_all(self):

        self.memory.clear()

    

    def total_sessions(self):

        return len(self.memory)


    def total_conversations(self):

        total = 0

        for history in self.memory.values():
            total += len(history)

        return total



memory_manager = MemoryManager()