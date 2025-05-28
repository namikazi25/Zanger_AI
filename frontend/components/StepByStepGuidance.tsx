import Link from "next/link";
import { CheckCircle, Circle } from "lucide-react";

export default function StepByStepGuidance() {
  const steps = [
    { text: "Identify the claim type and amount", completed: true },
    { text: "Try resolving the issue directly", completed: true },
    { text: "Prepare your evidence", completed: false },
    { text: "Complete online filing", completed: false },
    { text: "Pay the court fee", completed: false },
  ];

  return (
    <div className="space-y-3">
      {steps.map((step, index) => (
        <div key={index} className="flex items-start gap-3">
          {step.completed ? (
            <CheckCircle className="w-5 h-5 text-success-600 mt-0.5 flex-shrink-0" />
          ) : (
            <Circle className="w-5 h-5 text-primary-300 mt-0.5 flex-shrink-0" />
          )}
          <span
            className={`text-sm ${
              step.completed
                ? "text-primary-900 font-medium"
                : "text-primary-700"
            }`}
          >
            {step.text}
          </span>
        </div>
      ))}

      <div className="mt-4 pt-3 border-t border-primary-200">
        <Link
          href="#"
          className="text-sm text-primary-600 hover:text-primary-700 font-medium"
        >
          View detailed guide →
        </Link>
      </div>
    </div>
  );
}
