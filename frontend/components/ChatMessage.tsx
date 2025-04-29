import type React from "react"

export type Message = {
  id: number
  text: string
  sender: "user" | "assistant"
  timestamp: Date
}

interface ChatMessageProps {
  message: Message
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  return (
    <div className={`flex ${message.sender === "user" ? "justify-end" : "justify-start"}`}>
      <div
        className={`${
          message.sender === "user"
            ? "bg-gray-100 rounded-full py-3 px-6 inline-block"
            : "bg-white border rounded-lg p-4 max-w-[80%]"
        }`}
      >
        <p className="text-lg">{message.text}</p>
      </div>
    </div>
  )
}

export default ChatMessage
