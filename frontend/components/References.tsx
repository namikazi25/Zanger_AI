import { ExternalLink, BookOpen } from "lucide-react";

export default function References() {
  const references = [
    { title: "GOV.UK Small Claims Guidance", url: "#" },
    { title: "Civil Procedure Rules Part 27", url: "#" },
    { title: "Court Fees Information", url: "#" },
  ];

  return (
    <div className="space-y-3">
      {references.map((ref, index) => (
        <a
          key={index}
          href={ref.url}
          className="flex items-center gap-3 p-3 bg-white/60 hover:bg-white/80 border border-primary-200 rounded-lg transition-colors group"
        >
          <div className="p-1.5 bg-primary-100 rounded-lg group-hover:bg-primary-200 transition-colors">
            <BookOpen className="w-3 h-3 text-primary-600" />
          </div>
          <div className="flex-1 min-w-0">
            <div className="text-sm font-medium text-primary-900 truncate">
              {ref.title}
            </div>
          </div>
          <ExternalLink className="w-3 h-3 text-primary-500 group-hover:text-primary-600 transition-colors" />
        </a>
      ))}
    </div>
  );
}
