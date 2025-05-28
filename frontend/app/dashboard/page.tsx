import { redirect } from "next/navigation";
import { createServerClient } from "@/lib/supabase-server";
import DashboardLayout from "@/components/layouts/dashboard-layout";
import ChatInterface from "@/components/chat-interface";

export default async function DashboardPage() {
  const supabase = createServerClient();
  const {
    data: { session },
  } = await supabase.auth.getSession();

  // If user is not logged in, redirect to login page
  if (!session) {
    redirect("/auth/login");
  }

  // Fetch user profile
  const { data: profile } = await supabase
    .from("profiles")
    .select("*")
    .eq("id", session.user.id)
    .single();

  return (
    <DashboardLayout>
      <div className="mx-auto">
        <ChatInterface />
      </div>
    </DashboardLayout>
  );
}
