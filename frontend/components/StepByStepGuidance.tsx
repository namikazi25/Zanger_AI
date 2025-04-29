import type React from "react"
import { MessageSquare } from "lucide-react"

const StepByStepGuidance: React.FC = () => {
  return (
    <div className="mb-8">
      <div className="flex items-start gap-3 mb-4">
        <MessageSquare className="mt-1 w-6 h-6" />
        <h2 className="text-2xl font-bold">Step-by-step guidance</h2>
      </div>

      <ul className="list-disc pl-12 space-y-3 text-lg">
        <li>Identify the claim type and amount</li>
        <li>Try resolving the issue directly</li>
        <li>Prepare your evidence</li>
        <li>
          Complete online via{" "}
          <a href="#" className="text-blue-600 hover:underline">
            Money Claim Online
          </a>{" "}
          or by post
        </li>
        <li>Pay the court fee</li>
      </ul>
    </div>
  )
}

export default StepByStepGuidance
