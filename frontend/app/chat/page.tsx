import DashboardLayout from "@/components/layouts/dashboard-layout";
import ChatInterface from "@/components/chat-interface";

export default function ChatPage() {
  return (
    <DashboardLayout>
      <div className="h-full">
        <ChatInterface />
      </div>
    </DashboardLayout>
  );
}
