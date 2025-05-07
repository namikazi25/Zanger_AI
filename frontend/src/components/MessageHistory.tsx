import type React from "react"
import ChatMessage, { type Message } from "./ChatMessage"

interface MessageHistoryProps {
  messages: Message[]
}

const MessageHistory: React.FC<MessageHistoryProps> = ({ messages }) => {
  return (
    <div className="mb-8">
      <h3 className="text-xl font-bold mb-3 pl-12">Message History:</h3>
      <div className="space-y-4">
        {messages.map((message) => (
          <ChatMessage key={message.id} message={message} />
        ))}
      </div>
    </div>
  )
}

export default MessageHistory
