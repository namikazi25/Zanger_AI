import { createRouteHandlerClient } from "@supabase/auth-helpers-nextjs"
import { cookies } from "next/headers"
import { NextResponse } from "next/server"

export async function POST(request: Request) {
  try {
    const { userId, email, fullName } = await request.json()

    const cookieStore = cookies()
    const supabase = createRouteHandlerClient({ cookies: () => cookieStore })

    // Use the service role to bypass RLS
    const { error } = await supabase.from("profiles").insert({
      id: userId,
      email: email,
      full_name: fullName || null,
    })

    if (error) {
      console.error("Error creating profile:", error)
      return NextResponse.json({ error: error.message }, { status: 500 })
    }

    return NextResponse.json({ success: true })
  } catch (error) {
    console.error("Error in profile creation:", error)
    return NextResponse.json({ error: "Internal Server Error" }, { status: 500 })
  }
}
