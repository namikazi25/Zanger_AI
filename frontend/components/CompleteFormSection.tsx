import { FileText, ExternalLink, UserCheck } from "lucide-react";

export default function CompleteFormSection() {
  return (
    <div>
      <div className="bg-accent-50 border border-accent-200 rounded-lg p-4 mb-4">
        <h3 className="font-semibold text-primary-900 mb-2 flex items-center gap-2">
          <FileText className="w-4 h-4 text-accent-600" />
          Form N1 Ready
        </h3>
        <p className="text-sm text-primary-700 mb-3">
          Complete your small claims form with guided assistance
        </p>

        <div className="space-y-2">
          <button className="w-full bg-primary-600 hover:bg-primary-700 text-white text-sm px-4 py-2 rounded-lg transition-colors flex items-center justify-center gap-2">
            <FileText className="w-4 h-4" />
            Complete Form N1
          </button>
          <button className="w-full bg-white hover:bg-primary-50 text-primary-700 border border-primary-300 text-sm px-4 py-2 rounded-lg transition-colors flex items-center justify-center gap-2">
            <UserCheck className="w-4 h-4" />
            Request Assistance
          </button>
        </div>
      </div>

      <div className="text-xs text-primary-600 flex items-center gap-1">
        <ExternalLink className="w-3 h-3" />
        <span>Includes filing instructions & deadlines</span>
      </div>
    </div>
  );
}
